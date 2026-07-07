"""
Prompt Builder API Route
"""

from fastapi import APIRouter

from app.prompt_builder import PromptBuilder
from app.schemas.prompt import (
    PromptRequest,
    PromptResponse,
)

router = APIRouter(
    prefix="/prompt",
    tags=["Prompt Builder"],
)


@router.post(
    "/build",
    response_model=PromptResponse,
)
def build_prompt(request: PromptRequest):

    prompt = PromptBuilder.build_prompt(
        learner_question=request.learner_question,
        intent=request.intent,
        readiness_score=request.readiness_score,
        knowledge_gaps=request.knowledge_gaps,
        ocr_text=request.ocr_text,
        image_prediction=request.image_prediction,
    )

    return PromptResponse(
        prompt=prompt
    )