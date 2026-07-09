"""
LLM API Routes - LearnPath AI

Exposes the AI Tutor endpoint.

This route receives learner context from the Spring Boot backend,
passes it to the LLM Service, and returns the generated response.
"""

from fastapi import APIRouter, HTTPException

from app.llm.service import get_llm_service
from app.schemas.llm import LLMRequest, LLMResponse

router = APIRouter(
    prefix="/llm",
    tags=["LLM"],
)


@router.post(
    "/generate",
    response_model=LLMResponse,
)
async def generate_response(request: LLMRequest):
    """
    Generate a personalized AI response.
    """

    service = get_llm_service()

    try:
        result = service.generate_response(
            learner_question=request.learner_question,
            intent=request.intent,
            readiness_score=request.readiness_score,
            knowledge_gaps=request.knowledge_gaps,
            ocr_text=request.ocr_text,
            image_prediction=request.image_prediction,
        )

        return LLMResponse(**result)

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )