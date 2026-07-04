"""
Image preprocessing for the study-image classifier.

Converts raw uploaded image bytes into a MobileNetV2-ready input batch:
decode -> RGB -> resize to 224x224 -> MobileNetV2's own preprocess_input
normalization (scales pixels to [-1, 1], matching how the ImageNet
backbone was originally trained). Using any other normalization here
would silently degrade transfer-learning accuracy, since the frozen
backbone's weights expect this exact input distribution.

Fully independent of app/ml/ - no shared code or state with the
readiness pipeline.
"""

import io
from typing import Tuple

import numpy as np
import tensorflow as tf
from PIL import Image, UnidentifiedImageError

# MobileNetV2's standard input resolution.
IMAGE_SIZE: Tuple[int, int] = (224, 224)


def preprocess_image_bytes(image_bytes: bytes) -> np.ndarray:
    """
    Decodes raw image bytes and returns a (1, 224, 224, 3) float32 array
    ready to feed into the study-image classifier.

    Raises ValueError for anything that isn't a decodable image, so the
    API layer can return a clean HTTP 422 instead of a raw stack trace.
    """
    if not image_bytes:
        raise ValueError("Empty image data")

    try:
        image = Image.open(io.BytesIO(image_bytes))
        image = image.convert("RGB")
    except UnidentifiedImageError as exc:
        raise ValueError(f"Could not decode image: {exc}") from exc

    image = image.resize(IMAGE_SIZE)
    array = np.asarray(image, dtype=np.float32)
    array = tf.keras.applications.mobilenet_v2.preprocess_input(array)
    return np.expand_dims(array, axis=0)  # add batch dimension
