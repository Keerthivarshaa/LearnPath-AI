"""
Prompt Builder - LearnPath AI

This module combines outputs from different AI modules into a
single structured prompt that can be sent to an LLM or SLM.

The Prompt Builder does NOT call any AI model itself.
Its only responsibility is to organize learner context.
"""

from typing import Optional


class PromptBuilder:
    @staticmethod
    def build_prompt(
        learner_question: str,
        intent: str,
        readiness_score: float,
        knowledge_gaps: list[str],
        ocr_text: str = "",
        image_prediction: str = "",
        retrieved_context: list[str] | None = None,
    ) -> str:
        """
        Builds a structured prompt for the language model.
        """

        prompt = []

        prompt.append("### LearnPath AI Context ###")

        prompt.append(f"\nLearner Question:\n{learner_question}")

        prompt.append(f"\nDetected Intent:\n{intent}")

        if readiness_score is not None:
            prompt.append(
                f"\nReadiness Score:\n{readiness_score:.2f}%"
            )

        if knowledge_gaps:
            prompt.append(
                "\nKnowledge Gaps:\n"
                + "\n".join(f"- {gap}" for gap in knowledge_gaps)
            )

        if image_prediction:
            prompt.append(
                f"\nDetected Image Topic:\n{image_prediction}"
            )

        if ocr_text:
            prompt.append(
                f"\nOCR Extracted Text:\n{ocr_text}"
            )

        # -----------------------------
        # RAG Retrieved Context
        # -----------------------------
        if retrieved_context:
            prompt.append("\n### Retrieved Study Material ###")

            for chunk in retrieved_context:
                prompt.append(f"\n- {chunk}")

        prompt.append(
            "\n### Instructions ###"
        )

        prompt.append(
            "Generate a personalized response suitable for the learner's "
            "current understanding. "
            "Use the retrieved study material whenever it is relevant and "
            "prioritize it over general knowledge. "
            "Explain concepts clearly, focus on knowledge gaps, and provide "
            "practical guidance when appropriate."
        )

        return "\n".join(prompt)