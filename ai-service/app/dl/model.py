"""
CNN + Transfer Learning model for classifying uploaded study images
(diagrams, notes, screenshots) into a coarse subject category.

Architecture: MobileNetV2 (ImageNet weights, frozen) as a feature
extractor, with a small trainable classification head on top. This
mirrors app/ml/readiness_model.py's design deliberately:
  - build_model() defines the architecture blueprint, same role as
    readiness_model.build_ensemble() - not fitted here, train.py does that.
  - StudyImageClassifier tries to load a persisted trained model from
    MODEL_PATH on startup, exactly like ReadinessModel, and falls back to
    a clearly-labeled placeholder if none exists or loading fails.

Status: no trained head exists yet - see train.py and
app/dl/data/README.md for why, and how to produce one. Predictions from
the untrained placeholder are NOT meaningful (the head's weights are
random); they exist purely so this endpoint can be exercised end-to-end
and never crashes, before real training data is available.

This module is fully independent of app/ml/ (the certification-readiness
pipeline) - no imports between the two, no shared state.
"""

import logging
from pathlib import Path
from typing import Dict, List, Optional

import tensorflow as tf
from tensorflow.keras import layers, models

from app.dl.preprocessing import IMAGE_SIZE, preprocess_image_bytes

logger = logging.getLogger(__name__)

# Ordered, fixed category schema - the classification head's output layer
# has exactly this many units, in this order. Must stay in sync with the
# folder names expected under app/dl/data/ (see train.py / data/README.md).
CATEGORIES: List[str] = ["Java", "Database", "Cloud", "Networking", "Security", "Other"]

# Where a trained/fine-tuned model will be persisted once real training
# data exists. Checked on startup exactly like
# app/ml/readiness_model.MODEL_PATH - loading is attempted lazily and any
# failure is non-fatal.
MODEL_PATH = Path(__file__).parent / "models" / "study_image_classifier.keras"


def build_model() -> tf.keras.Model:
    """
    Builds the MobileNetV2 transfer-learning architecture: frozen
    ImageNet backbone + a small trainable classification head.

    Not fitted here - train.py calls this, fits the head on real data,
    and persists the result to MODEL_PATH. Kept here (like
    app/ml/readiness_model.build_ensemble()) so the architecture and the
    class that serves it can never drift apart.
    """
    base_model = tf.keras.applications.MobileNetV2(
        input_shape=(*IMAGE_SIZE, 3),
        include_top=False,
        weights="imagenet",
    )
    base_model.trainable = False  # freeze the backbone - only the head trains

    inputs = tf.keras.Input(shape=(*IMAGE_SIZE, 3))
    x = base_model(inputs, training=False)
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dense(128, activation="relu")(x)
    x = layers.Dropout(0.3)(x)
    outputs = layers.Dense(len(CATEGORIES), activation="softmax")(x)

    return models.Model(inputs, outputs, name="study_image_classifier")


class StudyImageClassifier:
    """
    Classifies a study-material image into one of CATEGORIES.

    predict() is the only method callers should use. Internally:
      1. Preprocesses the raw image bytes (preprocessing.py, reused as-is)
      2. Uses a trained model if one has been persisted to MODEL_PATH,
         otherwise builds the untrained architecture and uses that,
         clearly flagging the result as a placeholder via model_source.
      3. Returns a response dict with a stable shape regardless of which
         path was used - mirrors ReadinessModel's design so a future
         retrained model requires no API changes.
    """

    def __init__(self, model_path: Path = MODEL_PATH):
        self._model_path = model_path
        self._model, self._is_trained = self._load_or_build()

    def _load_or_build(self):
        if self._model_path.exists():
            try:
                model = tf.keras.models.load_model(self._model_path)
                logger.info("Loaded trained study-image classifier from %s", self._model_path)
                return model, True
            except Exception as exc:  # a corrupt/incompatible model file must never break predictions
                logger.warning(
                    "Failed to load trained CNN at %s (%s) - using untrained placeholder instead.",
                    self._model_path, exc,
                )
        else:
            logger.info(
                "No trained study-image classifier found at %s - serving an untrained "
                "MobileNetV2 placeholder. Predictions will not be meaningful until "
                "train.py has been run on real data.",
                self._model_path,
            )

        return build_model(), False

    @property
    def is_using_trained_model(self) -> bool:
        return self._is_trained

    def predict(self, image_bytes: bytes) -> Dict:
        """
        Classifies one image. Raises ValueError (propagated from
        preprocessing.preprocess_image_bytes) if image_bytes cannot be
        decoded as an image - the caller (the FastAPI route) is expected
        to translate that into an HTTP 422.
        """
        batch = preprocess_image_bytes(image_bytes)  # shape (1, 224, 224, 3)
        probabilities = self._model.predict(batch, verbose=0)[0]  # shape (len(CATEGORIES),)

        ranked = sorted(
            zip(CATEGORIES, probabilities.tolist()),
            key=lambda pair: pair[1],
            reverse=True,
        )

        top_category, top_confidence = ranked[0]
        top_predictions = [
            {"category": category, "confidence": round(float(confidence), 4)}
            for category, confidence in ranked[:3]
        ]

        return {
            "predicted_category": top_category,
            "confidence": round(float(top_confidence), 4),
            "top_predictions": top_predictions,
            "model_source": "trained_cnn" if self._is_trained else "untrained_placeholder",
        }


# Module-level singleton, mirroring app.ml.readiness_model.get_readiness_model -
# loading a multi-megabyte MobileNetV2 backbone is expensive and should
# happen once per process, not once per request.
_classifier: Optional[StudyImageClassifier] = None


def get_study_image_classifier() -> StudyImageClassifier:
    global _classifier
    if _classifier is None:
        _classifier = StudyImageClassifier()
    return _classifier
