"""
Pydantic schemas for the Agentic AI API.
"""

from typing import List

from pydantic import BaseModel, Field


class AgentRequest(BaseModel):
    """
    Input required by the Agentic AI Tutor.
    """

    learner_question: str = Field(
        ...,
        description="Question asked by the learner.",
    )

    intent: str = Field(
        ...,
        description="Intent detected by the NLP module.",
    )

    readiness_score: float = Field(
        80.0,
        ge=0,
        le=100,
        description="Learner readiness score.",
    )

    knowledge_gaps: List[str] = Field(
        default_factory=list,
        description="Known knowledge gaps of the learner.",
    )

    ocr_text: str = Field(
        default="",
        description="Text extracted using OCR.",
    )

    image_prediction: str = Field(
        default="",
        description="Topic predicted by the CNN image classifier.",
    )


class AgentPlan(BaseModel):
    """
    Represents the decisions made by the Agent Planner.
    """

    use_nlp: bool
    use_rag: bool
    use_ocr: bool
    use_cnn: bool
    use_readiness: bool
    use_llm: bool


class AgentResponse(BaseModel):
    """
    Response returned by the Agentic AI Tutor.
    """

    agent_plan: AgentPlan

    prompt: str

    retrieved_context: List[str] = Field(
        default_factory=list,
    )

    response: str