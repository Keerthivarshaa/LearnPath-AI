from fastapi import APIRouter, File, HTTPException, UploadFile

from app.ocr.text_extractor import extract_text

router = APIRouter(
    prefix="/ocr",
    tags=["ocr"],
)


@router.post("/extract-text")
async def extract_text_from_image(file: UploadFile = File(...)):
    """
    Extract text from an uploaded image using Tesseract OCR.
    """

    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="Only image files are supported.",
        )

    image_bytes = await file.read()

    try:
        text = extract_text(image_bytes)

        return {
            "success": True,
            "text": text,
            "length": len(text),
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=422,
            detail=str(exc),
        )