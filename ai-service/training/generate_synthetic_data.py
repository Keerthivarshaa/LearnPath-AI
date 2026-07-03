"""
Synthetic training data generator for the readiness ensemble model.

No real, outcome-labeled learner history exists yet - LearnPath AI has no
users with a known "did they actually end up ready / pass" ground truth.
This generator produces a domain-informed synthetic dataset so the
ensemble defined in app.ml.readiness_model.build_ensemble() can be
genuinely fitted now (not hand-coded), and retrained later on real data
through the exact same pipeline (train.py) once it exists - only
train.load_training_data() would need to change.

Design notes:
- Each synthetic learner is generated from a single latent "ability"
  value so that topic scores, study engagement, and roadmap progress are
  correlated the way a real learner's data would be, rather than
  independently random.
- The synthetic target label is deliberately generated from a DIFFERENT
  formula than ReadinessModel._predict_fallback()'s heuristic (different
  weights, an added interaction term, and observation noise), so the
  ensemble has something genuinely non-trivial to learn rather than just
  re-deriving the existing heuristic.
- ~15% of samples simulate brand-new onboarding users with no assessment
  data at all, so the trained model also learns that case directly
  (the fallback heuristic short-circuits this case explicitly; a trained
  model has no such special-casing, so it must see these examples during
  training or its behavior for real onboarding users would be
  unpredictable).
"""

import random
from typing import Dict, List, Tuple

from app.ml.feature_engineering import engineer_features, features_to_vector

# Mirrors topic names actually seeded in AssessmentSeeder.java, purely so
# synthetic topic_scores dicts look realistic (not used for any logic).
SAMPLE_TOPICS = [
    "EC2 Instance Models", "IAM Security", "RDS Scalability", "VPC Networking",
    "Garbage Collection", "Pattern Matching", "JDBC Pools",
    "Cryptography", "Network Security",
]

ONBOARDING_SAMPLE_RATE = 0.15


def _sample_onboarding_profile() -> dict:
    """A brand-new user: no assessment, no study history yet."""
    return {
        "topic_scores": None,
        "study_hours_per_week": 0.0,
        "total_study_hours": 0.0,
        "current_streak": 0,
        "longest_streak": 0,
        "completed_milestones_count": 0,
        "total_milestones_count": 0,
        "completion_percentage": 0.0,
    }


def _sample_active_profile(rng: random.Random, ability: float) -> dict:
    """An active learner with some assessment/study/progress history,
    generated around a single latent ability value for realistic
    correlation between fields."""
    num_topics = rng.randint(1, len(SAMPLE_TOPICS))
    topics = rng.sample(SAMPLE_TOPICS, num_topics)
    topic_scores = {t: max(0.0, min(1.0, rng.gauss(ability, 0.15))) for t in topics}

    weekly_hours = max(0.0, rng.gauss(3 + ability * 12, 3))
    total_hours = max(0.0, weekly_hours * rng.uniform(2, 20))

    longest_streak = max(0, int(rng.gauss(5 + ability * 20, 8)))
    current_streak = max(0, min(longest_streak, int(rng.gauss(longest_streak * ability, 5))))

    total_milestones = rng.randint(2, 4)
    completed_milestones = max(
        0, min(total_milestones, int(round(ability * total_milestones + rng.gauss(0, 0.5))))
    )
    completion_percentage = max(
        0.0, min(100.0, (completed_milestones / total_milestones) * 100 + rng.gauss(0, 5))
    )

    return {
        "topic_scores": topic_scores,
        "study_hours_per_week": weekly_hours,
        "total_study_hours": total_hours,
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "completed_milestones_count": completed_milestones,
        "total_milestones_count": total_milestones,
        "completion_percentage": completion_percentage,
    }


def _sample_learner_profile(rng: random.Random) -> Tuple[dict, float]:
    """Samples one plausible raw learner payload (same shape
    feature_engineering.engineer_features() expects), plus the latent
    ability value used to also generate its synthetic target label."""
    ability = rng.betavariate(2, 2)  # 0-1, centered ~0.5, plausible spread

    if rng.random() < ONBOARDING_SAMPLE_RATE:
        return _sample_onboarding_profile(), ability

    return _sample_active_profile(rng, ability), ability


def _synthetic_target(features: Dict[str, float], ability: float, rng: random.Random) -> float:
    """
    Generates the synthetic "ground truth" readiness label (0-1) for one
    profile. Deliberately NOT the same formula as
    ReadinessModel._predict_fallback - the trained model has a genuinely
    different (if related) function to approximate, including a
    nonlinear interaction term and observation noise, both properties a
    real-world label would have.
    """
    if features["has_assessment_data"] == 0.0:
        return max(0.0, min(1.0, 0.3 + rng.gauss(0, 0.05)))

    base = 0.5 * ability + 0.3 * features["avg_topic_score"]
    # Consistency (streak_ratio) matters more when mastery is borderline,
    # and matters less once mastery is already very high.
    interaction = 0.2 * features["streak_ratio"] * (1.0 - features["avg_topic_score"])
    engagement_bonus = 0.1 * min(1.0, features["weekly_study_hours"] / 15.0)
    noise = rng.gauss(0, 0.06)

    target = base + interaction + engagement_bonus + noise
    return max(0.0, min(1.0, target))


def generate_dataset(n_samples: int = 800, seed: int = 42) -> Tuple[List[List[float]], List[float]]:
    """
    Generates a synthetic (X, y) training set.

    Returns:
        X: feature vectors, ordered per feature_engineering.FEATURE_NAMES
           (via features_to_vector, reused as-is from Part 2)
        y: target readiness scores in [0, 1]
    """
    rng = random.Random(seed)
    X: List[List[float]] = []
    y: List[float] = []

    for _ in range(n_samples):
        raw_payload, ability = _sample_learner_profile(rng)
        features = engineer_features(raw_payload)
        target = _synthetic_target(features, ability, rng)

        X.append(features_to_vector(features))
        y.append(target)

    return X, y
