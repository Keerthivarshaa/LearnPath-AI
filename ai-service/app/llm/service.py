"""
LLM Service - LearnPath AI

Coordinates Prompt Builder and the LLM Client.

This layer contains the business logic for AI tutoring.
It builds the final prompt, sends it to the language model,
and returns the generated response.
"""

from app.llm.client import get_llm_client
from app.prompt_builder import PromptBuilder


class LLMService:
    """
    High-level AI tutoring service.
    """

    def __init__(self):
        self.client = get_llm_client()

    def generate_response(
        self,
        learner_question: str,
        intent: str,
        readiness_score: float,
        knowledge_gaps: list[str],
        ocr_text: str = "",
        image_prediction: str = "",
    ) -> dict:
        """
        Generates a personalized AI response.
        """

        prompt = PromptBuilder.build_prompt(
            learner_question=learner_question,
            intent=intent,
            readiness_score=readiness_score,
            knowledge_gaps=knowledge_gaps,
            ocr_text=ocr_text,
            image_prediction=image_prediction,
        )

        answer = self.client.generate(prompt)

        return {
            "prompt": prompt,
            "response": answer,
        }


_service = None


def get_llm_service() -> LLMService:
    """
    Singleton accessor.
    """

    global _service

    if _service is None:
        _service = LLMService()

    return _service