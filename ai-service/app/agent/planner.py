"""
Agent Planner - LearnPath AI

The planner decides which AI capabilities should be used
for a learner's request.
"""

from __future__ import annotations

from app.agent.models import AgentDecision


class AgentPlanner:
    """
    Decides which AI modules are required for a learner request.
    """

    def create_plan(
        self,
        learner_question: str,
        intent: str,
        ocr_text: str = "",
        image_prediction: str = "",
    ) -> AgentDecision:

        question = learner_question.lower().strip()
        detected_intent = intent.upper().strip()

        # NLP is always used to understand the learner's question.
        use_nlp = True

        # RAG is used to retrieve relevant study material.
        use_rag = True

        # OCR is used when OCR text is available.
        use_ocr = bool(ocr_text.strip())

        # CNN is used when an image topic is available.
        use_cnn = bool(image_prediction.strip())

        # Check whether ML readiness prediction is needed.
        readiness_keywords = [
            "ready",
            "readiness",
            "prepared",
            "preparation",
            "can i start",
            "should i learn",
            "am i ready",
            "my level",
            "my progress",
            "how much do i know",
            "how well do i know",
            "assess me",
            "evaluate my knowledge",
            "check my knowledge",
        ]

        use_readiness = (
            any(keyword in question for keyword in readiness_keywords)
            or "READINESS" in detected_intent
            or "ASSESSMENT" in detected_intent
        )

        # LLM generates the final personalized response.
        use_llm = True

        return AgentDecision(
            use_nlp=use_nlp,
            use_rag=use_rag,
            use_ocr=use_ocr,
            use_cnn=use_cnn,
            use_readiness=use_readiness,
            use_llm=use_llm,
        )