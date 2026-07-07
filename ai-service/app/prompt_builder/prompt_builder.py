"""
Prompt Builder - LearnPath AI

This module combines outputs from different AI modules into a
single structured prompt that can be sent to an LLM or SLM.

The Prompt Builder does NOT call any AI model itself.
Its only responsibility is to organize learner context.
"""

from typing import List, Optional


class PromptBuilder:

    @staticmethod
    def build_prompt(
        learner_question: str,
        intent: str = "GENERAL_CHAT",
        readiness_score: Optional[float] = None,
        knowledge_gaps: Optional[List[str]] = None,
        ocr_text: Optional[str] = None,
        image_prediction: Optional[str] = None,
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

        prompt.append(
            "\n### Instructions ###"
        )

        prompt.append(
            "Generate a personalized response suitable for the learner's "
            "current understanding. Explain concepts clearly, focus on "
            "knowledge gaps, and provide practical guidance when appropriate."
        )

        return "\n".join(prompt)
    