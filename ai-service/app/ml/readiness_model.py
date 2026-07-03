"""
Ensemble readiness prediction model.

Predicts a 0-100 certification "readiness" score from the engineered
features produced by feature_engineering.py.

Current status: no trained model exists yet (the training pipeline is
Part 4), so ReadinessModel falls back to a transparent, documented
heuristic scorer. The class is structured so that once a trained
ensemble (Random Forest + Gradient Boosting, combined via a
VotingRegressor) is fitted and persisted to MODEL_PATH, it will be
loaded and used automatically - callers (the /ml/predict-readiness
endpoint, and later Spring Boot's MLRoadmapGenerator) never need to
change.

Implemented in Level 1a - Part 3. No training pipeline yet.
"""

import logging
from pathlib import Path
from typing import Dict, Optional

from sklearn.ensemble import (
    GradientBoostingRegressor,
    RandomForestRegressor,
    VotingRegressor,
)

from app.ml.feature_engineering import engineer_features, features_to_vector

logger = logging.getLogger(__name__)

# Where a trained model will be persisted once Part 4's training pipeline
# exists. Loading is attempted lazily and any failure is non-fatal - the
# fallback heuristic keeps the service working either way.
MODEL_PATH = Path(__file__).parent / "models" / "readiness_ensemble.joblib"

READINESS_THRESHOLDS = {
    "HIGH": 70.0,
    "MODERATE": 40.0,
}


def build_ensemble() -> VotingRegressor:
    """
    Defines the ensemble architecture that the training pipeline (Part 4)
    will fit on real feature/outcome data and persist to MODEL_PATH.

    Kept here, next to the model that will eventually consume it, so the
    two stay in sync. Not fitted or invoked anywhere in Part 3 - this is
    a blueprint, not a trained model.
    """
    return VotingRegressor(
        estimators=[
            ("random_forest", RandomForestRegressor(n_estimators=100, max_depth=8, random_state=42)),
            ("gradient_boosting", GradientBoostingRegressor(n_estimators=100, max_depth=3, random_state=42)),
        ]
    )


class ReadinessModel:
    """
    Predicts certification readiness from raw learner data.

    predict() is the only method callers should use. Internally:
      1. Engineers features via feature_engineering.engineer_features()
         (reused exactly as implemented in Part 2 - no changes there).
      2. Uses a trained ensemble if one has been persisted to
         MODEL_PATH, otherwise falls back to a documented heuristic.
      3. Returns a response dict with a stable shape regardless of which
         path was used, so Part 4 can introduce real training without
         any caller needing to change.
    """

    def __init__(self, model_path: Path = MODEL_PATH):
        self._model_path = model_path
        self._model = self._try_load_model()

    def _try_load_model(self):
        if not self._model_path.exists():
            logger.info(
                "No trained readiness model found at %s - using fallback heuristic.",
                self._model_path,
            )
            return None
        try:
            import joblib  # only imported if a persisted model actually exists

            model = joblib.load(self._model_path)
            logger.info("Loaded trained readiness model from %s", self._model_path)
            return model
        except Exception as exc:  # a corrupt/incompatible model file must never break predictions
            logger.warning(
                "Failed to load trained model at %s (%s) - using fallback heuristic instead.",
                self._model_path,
                exc,
            )
            return None

    @property
    def is_using_trained_model(self) -> bool:
        return self._model is not None

    def predict(self, payload: dict) -> Dict:
        """
        Runs a full prediction from a raw payload (same shape
        feature_engineering.engineer_features() expects).

        Raises FeatureValidationError (propagated from feature_engineering)
        if the payload is malformed; the caller (the FastAPI route) is
        expected to translate that into an HTTP 422.
        """
        features = engineer_features(payload)

        if self._model is not None:
            score = self._predict_with_model(features)
            source = "trained_ensemble"
        else:
            score = self._predict_fallback(features)
            source = "fallback_heuristic"

        score = max(0.0, min(100.0, score))
        level = self._score_to_level(score)
        explanation = self._build_explanation(features, score, level, source)

        return {
            "readiness_score": round(score, 2),
            "readiness_level": level,
            "explanation": explanation,
            "engineered_features": features,
            "model_source": source,
        }

    def _predict_with_model(self, features: Dict[str, float]) -> float:
        vector = [features_to_vector(features)]
        raw_prediction = self._model.predict(vector)[0]
        return float(raw_prediction) * 100.0  # trained model outputs 0-1

    def _predict_fallback(self, features: Dict[str, float]) -> float:
        """
        Transparent, hand-specified heuristic used only until a trained
        model exists (Part 4). Deliberately simple and documented rather
        than dressed up as a real model. Weighting reflects a rough,
        stated judgment of what should matter most for exam readiness:

          - assessment mastery matters most (60%): how well the user is
            actually scoring, penalized for breadth of weak topics.
          - study engagement matters next (25%): weekly hours and recent
            streak consistency relative to personal best.
          - roadmap progress matters least (15%): partly a downstream
            consequence of the other two rather than an independent
            readiness signal.

        A user with no assessment data yet is deliberately capped at a
        fixed moderate-low score rather than run through the formula,
        since "unknown" should never be indistinguishable from "ready".
        """
        if features["has_assessment_data"] == 0.0:
            return 35.0

        mastery = features["avg_topic_score"] * (1.0 - 0.3 * features["weak_topic_ratio"])
        engagement = (
            0.5 * min(1.0, features["weekly_study_hours"] / 10.0)
            + 0.5 * features["streak_ratio"]
        )
        progress = (
            0.5 * features["milestone_completion_ratio"]
            + 0.5 * features["completion_percentage_normalized"]
        )

        composite = 0.60 * mastery + 0.25 * engagement + 0.15 * progress
        return composite * 100.0

    @staticmethod
    def _score_to_level(score: float) -> str:
        if score >= READINESS_THRESHOLDS["HIGH"]:
            return "HIGH"
        if score >= READINESS_THRESHOLDS["MODERATE"]:
            return "MODERATE"
        return "LOW"

    @staticmethod
    def _build_explanation(
        features: Dict[str, float], score: float, level: str, source: str
    ) -> str:
        if features["has_assessment_data"] == 0.0:
            return (
                "No assessment data yet, so this is a placeholder estimate. "
                "Complete the diagnostic assessment for an accurate readiness score."
            )

        weak_pct = round(features["weak_topic_ratio"] * 100)
        parts = [f"Readiness is {level.lower()} at {round(score)}/100."]
        if weak_pct > 0:
            parts.append(f"{weak_pct}% of assessed topics are still below the mastery threshold.")
        if features["streak_ratio"] < 0.5:
            parts.append("Recent study consistency is below your own best streak.")
        if source == "fallback_heuristic":
            parts.append(
                "(Estimated using a heuristic scorer; a trained model will replace "
                "this in a later phase.)"
            )
        return " ".join(parts)


# Module-level singleton so model loading (currently trivial, later
# potentially expensive) happens once per process, not once per request.
_readiness_model: Optional[ReadinessModel] = None


def get_readiness_model() -> ReadinessModel:
    global _readiness_model
    if _readiness_model is None:
        _readiness_model = ReadinessModel()
    return _readiness_model
