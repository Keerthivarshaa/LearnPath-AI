"""
Feature engineering module.

Transforms raw learner assessment/progress data (the shape that will
eventually be assembled by Spring Boot's future MLRoadmapGenerator from
AssessmentResultDTO / ProgressDTO) into a fixed-order numerical feature
vector consumable by the ensemble readiness model implemented in Part 3.

This module has no FastAPI/HTTP dependency and no Spring Boot integration -
it is a pure, testable transformation layer, built entirely on the
standard library so no new project dependencies are introduced.

Implemented in Level 1a - Part 2.
"""

import math
from dataclasses import dataclass
from typing import Dict, List, Optional

# ---------------------------------------------------------------------------
# Canonical feature schema
# ---------------------------------------------------------------------------
# Fixed, ordered list of engineered feature names. The readiness model
# (Part 3) will use this exact order to build its training/inference
# matrix, so this list must stay stable once a model is trained against it.
FEATURE_NAMES: List[str] = [
    "avg_topic_score",
    "topic_score_std",
    "weak_topic_ratio",
    "num_topics_assessed",
    "has_assessment_data",
    "weekly_study_hours",
    "total_study_hours_log1p",
    "current_streak_days",
    "streak_ratio",
    "milestone_completion_ratio",
    "completion_percentage_normalized",
]

# Kept in sync with AssessmentService.submitAssessment (Java), which already
# classifies a topic as "strong" at a >=0.7 correct ratio. Reusing the same
# threshold means the ML features never disagree with the rest of the app
# about what counts as a weak topic.
STRONG_TOPIC_THRESHOLD = 0.7

# Sane clipping bounds against bad/extreme input, mirroring constraints
# already enforced on the frontend (Register.jsx: study hours 1-60/week).
MAX_WEEKLY_STUDY_HOURS = 60.0
MAX_STREAK_DAYS = 3650.0  # ~10 years - generous ceiling, not a real limit


@dataclass
class LearnerRawData:
    """
    Raw learner data as it will be supplied by the caller (eventually
    Spring Boot). Every field is optional because a brand-new user may
    have no assessment or progress history yet - this dataclass gives
    downstream code one clearly-defined shape to work against instead of
    a loosely-typed dict.
    """
    topic_scores: Optional[Dict[str, float]] = None          # topic -> correct ratio (0-1)
    study_hours_per_week: Optional[float] = None
    total_study_hours: Optional[float] = None
    current_streak: Optional[float] = None
    longest_streak: Optional[float] = None
    completed_milestones_count: Optional[float] = None
    total_milestones_count: Optional[float] = None
    completion_percentage: Optional[float] = None            # 0-100, as produced by ProgressDTO


class FeatureValidationError(ValueError):
    """
    Raised when raw input is fundamentally malformed (wrong type for a
    field that was actually supplied), as opposed to merely missing.
    Missing values are not errors - they are handled with documented
    defaults inside the feature functions below.
    """


def parse_raw_data(payload: dict) -> LearnerRawData:
    """
    Validates and coerces an incoming raw payload (a plain dict, e.g. a
    future JSON request body) into a LearnerRawData instance.

    Missing keys are treated as "unknown" and left as None so that
    engineer_features() can apply feature-specific defaults. A key that
    IS present but has the wrong type raises FeatureValidationError,
    since that indicates a caller bug rather than a legitimately absent
    value.
    """
    if not isinstance(payload, dict):
        raise FeatureValidationError("payload must be a dict")

    topic_scores = payload.get("topic_scores")
    if topic_scores is not None:
        if not isinstance(topic_scores, dict):
            raise FeatureValidationError("topic_scores must be a dict of topic -> score")
        for topic, score in topic_scores.items():
            if not isinstance(score, (int, float)):
                raise FeatureValidationError(f"topic score for '{topic}' must be numeric")

    def _optional_number(key: str):
        value = payload.get(key)
        if value is None:
            return None
        if not isinstance(value, (int, float)):
            raise FeatureValidationError(f"'{key}' must be numeric if provided")
        return float(value)

    return LearnerRawData(
        topic_scores=topic_scores,
        study_hours_per_week=_optional_number("study_hours_per_week"),
        total_study_hours=_optional_number("total_study_hours"),
        current_streak=_optional_number("current_streak"),
        longest_streak=_optional_number("longest_streak"),
        completed_milestones_count=_optional_number("completed_milestones_count"),
        total_milestones_count=_optional_number("total_milestones_count"),
        completion_percentage=_optional_number("completion_percentage"),
    )


# ---------------------------------------------------------------------------
# Individual feature groups
# ---------------------------------------------------------------------------

def _compute_topic_features(topic_scores: Optional[Dict[str, float]]) -> Dict[str, float]:
    """
    Derives mastery-related features from per-topic assessment scores.

    - avg_topic_score: overall competency signal across everything the
      user has been assessed on.
    - topic_score_std: how UNEVEN mastery is. A user strong in 5 topics
      and weak in 1 looks very different from someone uniformly average,
      even if their mean score is similar - this captures that.
    - weak_topic_ratio: proportion of topics below STRONG_TOPIC_THRESHOLD,
      i.e. the same definition of "weak" AssessmentService already uses.
    - num_topics_assessed: breadth signal. A readiness score built from
      one topic is far less reliable than one built from six.
    - has_assessment_data: explicit flag for "no assessment taken yet".
      Without this flag, a brand-new user and a user who scored 0.5 on
      everything would look identical to the model - the flag lets the
      model tell "unknown" apart from "actually average".
    """
    if not topic_scores:
        # No assessment yet - use a neutral midpoint (not 0.0, which would
        # misleadingly imply "answered everything wrong"). has_assessment_data
        # disambiguates this case from a genuine average score of 0.5.
        return {
            "avg_topic_score": 0.5,
            "topic_score_std": 0.0,
            "weak_topic_ratio": 0.0,
            "num_topics_assessed": 0.0,
            "has_assessment_data": 0.0,
        }

    # Clip each raw score into [0, 1] in case of upstream bad data
    # (e.g. a ratio miscomputed as a percentage) rather than letting it
    # silently skew the whole feature set.
    scores = [max(0.0, min(1.0, float(s))) for s in topic_scores.values()]
    n = len(scores)
    mean_score = sum(scores) / n

    variance = sum((s - mean_score) ** 2 for s in scores) / n
    std_score = math.sqrt(variance)

    weak_count = sum(1 for s in scores if s < STRONG_TOPIC_THRESHOLD)

    return {
        "avg_topic_score": mean_score,
        "topic_score_std": std_score,
        "weak_topic_ratio": weak_count / n,
        "num_topics_assessed": float(n),
        "has_assessment_data": 1.0,
    }


def _compute_engagement_features(data: LearnerRawData) -> Dict[str, float]:
    """
    Derives study-habit features.

    - weekly_study_hours: stated weekly commitment, clipped to the same
      [0, 60] range already enforced at registration, so malformed or
      extreme values can't distort the model.
    - total_study_hours_log1p: cumulative hours logged so far, log1p
      scaled. Raw cumulative hours grow unbounded over time and would
      dominate a linear feature space; log-scaling keeps "10 vs 20 hours"
      meaningfully different while "500 vs 510 hours" barely moves it -
      which matches how diminishing an extra hour actually is at that
      point.
    - current_streak_days: recent day-to-day consistency.
    - streak_ratio: current streak relative to the user's own longest
      streak (safe divide-by-zero handling for new users). Values near
      1.0 mean the user is at their personal best right now; low values
      may mean a recent lapse even if their longest streak was once high.
    """
    weekly_hours = data.study_hours_per_week or 0.0
    weekly_hours = max(0.0, min(MAX_WEEKLY_STUDY_HOURS, weekly_hours))

    total_hours = max(0.0, data.total_study_hours or 0.0)
    total_hours_log = math.log1p(total_hours)

    current_streak = max(0.0, min(MAX_STREAK_DAYS, data.current_streak or 0.0))
    longest_streak = max(0.0, data.longest_streak or 0.0)
    streak_ratio = (current_streak / longest_streak) if longest_streak > 0 else 0.0
    streak_ratio = max(0.0, min(1.0, streak_ratio))

    return {
        "weekly_study_hours": weekly_hours,
        "total_study_hours_log1p": total_hours_log,
        "current_streak_days": current_streak,
        "streak_ratio": streak_ratio,
    }


def _compute_progress_features(data: LearnerRawData) -> Dict[str, float]:
    """
    Derives roadmap-progress features.

    - milestone_completion_ratio: completed vs total milestones for the
      user's certification track, safely handling total=0 (e.g. an
      onboarding user with no roadmap generated yet).
    - completion_percentage_normalized: reuses the completion percentage
      Spring Boot's ProgressService already computes and stores, scaled
      to 0-1. Deliberately reused rather than recomputed here, so the ML
      feature can never disagree with the number the user already sees
      in the UI.
    """
    completed = data.completed_milestones_count or 0.0
    total = data.total_milestones_count or 0.0
    milestone_ratio = (completed / total) if total > 0 else 0.0
    milestone_ratio = max(0.0, min(1.0, milestone_ratio))

    completion_pct = max(0.0, min(100.0, data.completion_percentage or 0.0))

    return {
        "milestone_completion_ratio": milestone_ratio,
        "completion_percentage_normalized": completion_pct / 100.0,
    }


# ---------------------------------------------------------------------------
# Public entry points (used by readiness_model.py in Part 3)
# ---------------------------------------------------------------------------

def engineer_features(payload: dict) -> Dict[str, float]:
    """
    Main entry point. Validates a raw payload and returns a fully
    engineered, named feature dict covering every key in FEATURE_NAMES.

    This is what the readiness model (Part 3) will call before running
    inference, and what a future training script will call for each
    historical record when building a training dataset.
    """
    raw = parse_raw_data(payload)

    features: Dict[str, float] = {}
    features.update(_compute_topic_features(raw.topic_scores))
    features.update(_compute_engagement_features(raw))
    features.update(_compute_progress_features(raw))

    # Defensive check: guarantees every column the model expects is always
    # present, even if a future feature group is added and someone forgets
    # to wire it into the block above.
    missing = [name for name in FEATURE_NAMES if name not in features]
    if missing:
        raise FeatureValidationError(f"engineer_features() did not produce: {missing}")

    return features


def features_to_vector(features: Dict[str, float]) -> List[float]:
    """
    Converts a named feature dict into the fixed-order numeric vector the
    scikit-learn ensemble model will expect in Part 3. Kept separate from
    engineer_features() so callers that only need the interpretable dict
    (e.g. logging, or the Streamlit inspector from the Master Plan) aren't
    forced to deal with vector/column ordering.
    """
    return [float(features[name]) for name in FEATURE_NAMES]
