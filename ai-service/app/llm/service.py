"""
LLM Service - LearnPath AI

Coordinates the Agentic AI layer, RAG, Prompt Builder,
and the LLM Client.

The Agent Planner decides which AI capabilities are
required for the learner's request.

The LLM Service then executes the required workflow
and generates the final personalized response.
"""

from app.agent.service import get_agent_service
from app.llm.client import get_llm_client
from app.prompt_builder import PromptBuilder
from app.rag.service import get_rag_service


class LLMService:
    """
    High-level AI Tutor service.

    This service acts as the entry point for the
    Agentic AI tutoring workflow.
    """

    def __init__(self):
        self.client = get_llm_client()
        self.agent_service = get_agent_service()
        self.rag_service = get_rag_service()

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
        Generates a personalized AI response
        using the Agentic AI workflow.
        """

        # ----------------------------------------
        # STEP 1: Agent creates an execution plan
        # ----------------------------------------

        agent_plan = self.agent_service.create_plan(
            learner_question=learner_question,
            intent=intent,
            ocr_text=ocr_text,
            image_prediction=image_prediction,
        )

        print("=" * 60)
        print("AGENT DECISION")
        print(agent_plan)
        print("=" * 60)

        # ----------------------------------------
        # STEP 2: Retrieve study material using RAG
        # ----------------------------------------

        retrieved_context = []

        if agent_plan.use_rag:

            retrieved_chunks = self.rag_service.retrieve(
                query=learner_question,
                top_k=3,
            )

            retrieved_context = [
                result.chunk.text
                for result in retrieved_chunks
            ]

        print("=" * 60)
        print("RETRIEVED CONTEXT")
        print(retrieved_context)
        print("=" * 60)

        # ----------------------------------------
        # STEP 3: Build final prompt
        # ----------------------------------------

        prompt = PromptBuilder.build_prompt(
            learner_question=learner_question,
            intent=intent,
            readiness_score=readiness_score,
            knowledge_gaps=knowledge_gaps,
            ocr_text=ocr_text,
            image_prediction=image_prediction,
            retrieved_context=retrieved_context,
        )

        # ----------------------------------------
        # STEP 4: Generate response using LLM
        # ----------------------------------------

        answer = self.client.generate(prompt)

        # ----------------------------------------
        # STEP 5: Return complete result
        # ----------------------------------------

        return {
            "prompt": prompt,
            "retrieved_context": retrieved_context,
            "response": answer,
        }


_service: LLMService | None = None


def get_llm_service() -> LLMService:
    """
    Singleton accessor.
    """

    global _service

    if _service is None:
        _service = LLMService()

    return _service