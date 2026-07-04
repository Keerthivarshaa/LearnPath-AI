"""
Deep learning routes (CNN + transfer learning study-image classifier).

Kept in its own file, separate from app/api/routes/ml.py, so the
readiness-prediction and image-classification code paths stay fully
independent even though both happen to mount under the same /ml URL
prefix (the exact endpoint path required for this feature).
"""

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.dl.model import get_study_image_classifier
from app.schemas.study_image import StudyImageClassificationResponse

router = APIRouter(prefix="/ml", tags=["deep-learning"])


@router.post("/classify-study-image", response_model=StudyImageClassificationResponse)
async def classify_study_image(file: UploadFile = File(...)) -> StudyImageClassificationResponse:
    """
    Classifies an uploaded study-material image (diagram, notes,
    screenshot) into a coarse subject category. Currently backed by an
    untrained MobileNetV2 placeholder head until real training data
    exists (see app/dl/train.py) - a prediction is still returned,
    clearly labeled via modelSource, so this endpoint never crashes.
    """
    image_bytes = await file.read()

    classifier = get_study_image_classifier()
    try:
        result = classifier.predict(image_bytes)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    return StudyImageClassificationResponse(**result)
