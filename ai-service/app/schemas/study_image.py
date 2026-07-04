"""
Response schema for the study-image classification API.
"""

from typing import List

from pydantic import BaseModel, ConfigDict, Field


class TopPrediction(BaseModel):
    category: str
    confidence: float = Field(..., ge=0, le=1)


class StudyImageClassificationResponse(BaseModel):
    """
    Response contract for POST /ml/classify-study-image.

    predictedCategory / confidence / topPredictions match the required
    contract exactly. modelSource is an additive field (mirrors
    ReadinessResponse.modelSource from readiness.py) so callers can tell
    a real trained prediction apart from the untrained placeholder
    without this contract ever needing to change once train.py produces
    a real model - the same pattern already used for the readiness
    endpoint.
    """

    model_config = ConfigDict(populate_by_name=True)

    predicted_category: str = Field(..., alias="predictedCategory")
    confidence: float = Field(..., alias="confidence", ge=0, le=1)
    top_predictions: List[TopPrediction] = Field(..., alias="topPredictions")
    model_source: str = Field(..., alias="modelSource")
