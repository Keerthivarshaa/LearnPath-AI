"""
ML prediction routes.
"""

from fastapi import APIRouter, HTTPException

from app.ml.feature_engineering import FeatureValidationError
from app.ml.readiness_model import get_readiness_model
from app.schemas.readiness import ReadinessRequest, ReadinessResponse

router = APIRouter(prefix="/ml", tags=["ml"])


@router.post("/predict-readiness", response_model=ReadinessResponse)
def predict_readiness(request: ReadinessRequest) -> ReadinessResponse:
    """
    Predicts a learner's certification readiness score from their
    assessment/progress data. Currently backed by a documented fallback
    heuristic (see ReadinessModel) until a trained model exists.
    """
    model = get_readiness_model()
    try:
        result = model.predict(request.model_dump())
    except FeatureValidationError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    return ReadinessResponse(**result)
