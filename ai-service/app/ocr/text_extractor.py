"""
OCR text extraction - Module 3.

Exposes one function, extract_text(), for future in-process use by the
Prompt Builder (not wired in yet - out of scope for this module).

Deliberately a plain function, not a class/singleton like
StudyImageClassifier: Tesseract has no model to load into memory and no
meaningful warm-up cost, so there is nothing worth caching. Copying the
CNN module's singleton pattern here would be unjustified complexity.

Independent of app/dl/ and app/ml/ - no shared imports or state.
"""

import logging

import pytesseract

from app.ocr.preprocessing import preprocess_image_for_ocr

logger = logging.getLogger(__name__)


def extract_text(image_bytes: bytes) -> str:
    """
    Extracts text from an image using Tesseract OCR.

    Returns an empty string - never raises - when either:
      - the image is valid but contains no readable text, or
      - the Tesseract binary isn't installed/reachable on this machine.
    Both cases mean the same thing to a future caller (Prompt Builder):
    "no text to contribute" - deliberately not distinguished, per the
    agreed design.

    Raises ValueError only for undecodable image bytes (propagated from
    preprocessing.preprocess_image_for_ocr) - a genuine caller error,
    not an OCR-availability concern.
    """
    image = preprocess_image_for_ocr(image_bytes)  # raises ValueError for bad bytes

    try:
        text = pytesseract.image_to_string(image)
    except pytesseract.TesseractNotFoundError:
        logger.warning(
            "Tesseract binary not found - returning empty OCR text. "
            "Install it (e.g. `apt-get install tesseract-ocr`) to enable OCR."
        )
        return ""
    except Exception as exc:  # any other Tesseract/runtime failure must not crash the caller
        logger.warning("OCR extraction failed (%s) - returning empty text.", exc)
        return ""

    return text.strip()
