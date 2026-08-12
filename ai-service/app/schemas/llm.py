"""
Pydantic schemas for the LLM API.

These define the request and response contracts exposed through FastAPI.
"""

from typing import List

from pydantic import BaseModel, Field


class LLMRequest(BaseModel):
    """
    Input required to generate a personalized AI response.
    """

    learner_question: str = Field(
        ...,
        description="Question asked by the learner."
    )

    intent: str = Field(
        ...,
        description="Intent predicted by the NLP module."
    )

    readiness_score: float = Field(
        ...,
        ge=0,
        le=100,
        description="Predicted learner readiness percentage."
    )

    knowledge_gaps: List[str] = Field(
        default_factory=list,
        description="Concepts the learner still struggles with."
    )

    ocr_text: str = Field(
        default="",
        description="Text extracted from uploaded study material."
    )

    image_prediction: str = Field(
        default="",
        description="Predicted topic from the CNN image classifier."
    )

class LLMResponse(BaseModel):
    """
    Response returned by the AI Tutor.
    """

    prompt: str = Field(
        ...,
        description="Prompt sent to the language model."
    )

    retrieved_context: List[str] = Field(
        default_factory=list,
        description="Study material retrieved from the RAG module."
    )

    response: str = Field(
        ...,
        description="Generated AI response."
    )
