"""
Image preprocessing for OCR text extraction.

Distinct from app/dl/preprocessing.py (which prepares images for
MobileNetV2 classification: fixed 224x224 shape, normalized to
[-1, 1]). OCR has entirely different requirements - Tesseract works on
arbitrary-size grayscale images and has no fixed input shape - so
nothing from the CNN module's preprocessing applies here. This is a
genuinely separate concern, not a duplication of it.

Deliberately conservative: converts to grayscale and upscales small
images (both well-established, close-to-always-safe accuracy
improvements for Tesseract), but does NOT apply binarization/
thresholding. A naive global threshold is a common OCR preprocessing
step, but it can measurably hurt accuracy on unevenly-lit photos - a
likely scenario for this project's stated use cases (phone photos of
handwritten notes, whiteboards). Tesseract's own internal binarization
generally handles that better than a fixed cutoff would. Left as a
documented, easy addition later if evaluation shows a specific image
type needs it.
"""

import io

from PIL import Image, UnidentifiedImageError

# Tesseract's accuracy drops noticeably on small text; upscaling images
# below this size (on the longer edge) is a well-documented improvement.
# Images already at or above this size are left at their original
# resolution - downscaling is never applied, since that would only lose
# detail.
MIN_LONG_EDGE_PX = 1000


def preprocess_image_for_ocr(image_bytes: bytes) -> Image.Image:
    """
    Decodes raw image bytes and returns a PIL Image ready for Tesseract:
    grayscale, upscaled if small. Returns a PIL Image (not a numpy array)
    since that's exactly what pytesseract's API expects directly - no
    unnecessary conversion.

    Raises ValueError for anything that isn't a decodable image, so
    text_extractor.py can distinguish "bad input" (raise) from "no text
    found" (return "") - two different situations that must not be
    conflated.
    """
    if not image_bytes:
        raise ValueError("Empty image data")

    try:
        image = Image.open(io.BytesIO(image_bytes))
        image = image.convert("L")  # grayscale
    except UnidentifiedImageError as exc:
        raise ValueError(f"Could not decode image: {exc}") from exc

    return _upscale_if_small(image)


def _upscale_if_small(image: Image.Image) -> Image.Image:
    long_edge = max(image.size)
    if long_edge >= MIN_LONG_EDGE_PX:
        return image

    scale = MIN_LONG_EDGE_PX / long_edge
    new_size = (round(image.width * scale), round(image.height * scale))
    return image.resize(new_size, Image.LANCZOS)
