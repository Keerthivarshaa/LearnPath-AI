"""
Request/response schemas for the readiness prediction API.

ReadinessRequest fields intentionally match the exact keys
feature_engineering.engineer_features() already expects (Part 2's
contract, reused as-is), so the route can call
`engineer_features(request.model_dump())` with no translation layer.

ReadinessResponse fields are exposed to callers in camelCase (matching
the JSON convention every existing Java DTO in this project already
uses via Jackson), while staying snake_case internally in Python.
"""

from typing import Dict, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ReadinessRequest(BaseModel):
    """
    Raw learner data submitted for a readiness prediction. Every field is
    optional, mirroring feature_engineering.LearnerRawData - a brand-new
    user may not yet have assessment or progress history.
    """

    topic_scores: Optional[Dict[str, float]] = Field(
        default=None,
        description="Per-topic correct ratio (0-1), e.g. {'IAM Security': 0.9}",
    )
    study_hours_per_week: Optional[float] = Field(default=None, ge=0)
    total_study_hours: Optional[float] = Field(default=None, ge=0)
    current_streak: Optional[float] = Field(default=None, ge=0)
    longest_streak: Optional[float] = Field(default=None, ge=0)
    completed_milestones_count: Optional[float] = Field(default=None, ge=0)
    total_milestones_count: Optional[float] = Field(default=None, ge=0)
    completion_percentage: Optional[float] = Field(default=None, ge=0, le=100)

    @field_validator("topic_scores")
    @classmethod
    def validate_topic_scores(cls, value):
        if value is None:
            return value
        for topic, score in value.items():
            if not isinstance(score, (int, float)):
                raise ValueError(f"topic score for '{topic}' must be numeric")
        return value


class ReadinessResponse(BaseModel):
    """
    Response contract for a readiness prediction. This shape is intended
    to stay stable across Part 3 (fallback heuristic) and Part 4+
    (trained ensemble) so callers never need to change.
    """

    model_config = ConfigDict(populate_by_name=True)

    readiness_score: float = Field(..., alias="readinessScore", ge=0, le=100)
    readiness_level: str = Field(..., alias="readinessLevel", description="LOW | MODERATE | HIGH")
    explanation: str
    engineered_features: Dict[str, float] = Field(..., alias="engineeredFeatures")
    model_source: str = Field(
        ..., alias="modelSource", description="'fallback_heuristic' or 'trained_ensemble'"
    )
