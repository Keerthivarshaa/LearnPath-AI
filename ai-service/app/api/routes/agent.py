from fastapi import APIRouter, HTTPException

from app.agent.service import get_agent_service
from app.schemas.llm import LLMRequest


router = APIRouter(
    prefix="/agent",
    tags=["Agentic AI"],
)


@router.post("/plan")
async def create_agent_plan(request: LLMRequest):
    """
    Create an execution plan for the Agentic AI Tutor.
    """

    try:
        agent_service = get_agent_service()

        decision = agent_service.create_plan(
            learner_question=request.learner_question,
            intent=request.intent,
            ocr_text=request.ocr_text,
            image_prediction=request.image_prediction,
        )

        return {
            "learner_question": request.learner_question,
            "intent": request.intent,
            "plan": {
                "use_nlp": decision.use_nlp,
                "use_rag": decision.use_rag,
                "use_ocr": decision.use_ocr,
                "use_cnn": decision.use_cnn,
                "use_readiness": decision.use_readiness,
                "use_llm": decision.use_llm,
            },
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )


@router.post("/execute")
async def execute_agent_plan(request: LLMRequest):
    """
    Execute the Agentic AI Tutor plan.
    """

    try:
        agent_service = get_agent_service()

        result = agent_service.execute_plan(
            learner_question=request.learner_question,
            intent=request.intent,
            readiness_score=request.readiness_score,
            knowledge_gaps=request.knowledge_gaps,
            ocr_text=request.ocr_text,
            image_prediction=request.image_prediction,
        )

        return result

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )