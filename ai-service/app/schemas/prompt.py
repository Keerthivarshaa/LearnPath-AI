"""
Pydantic schemas for the Prompt Builder.
"""

from typing import List, Optional

from pydantic import BaseModel


class PromptRequest(BaseModel):
    learner_question: str
    intent: str = "GENERAL_CHAT"
    readiness_score: Optional[float] = None
    knowledge_gaps: Optional[List[str]] = None
    ocr_text: Optional[str] = None
    image_prediction: Optional[str] = None


class PromptResponse(BaseModel):
    prompt: str