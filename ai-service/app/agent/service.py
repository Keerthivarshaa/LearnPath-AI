from __future__ import annotations

from dataclasses import asdict

from app.agent.executor import AgentExecutor
from app.agent.models import AgentDecision
from app.agent.planner import AgentPlanner


class AgentService:
    """
    High-level Agentic AI orchestration service.
    """

    def __init__(self):
        self.planner = AgentPlanner()
        self.executor = AgentExecutor()

    def create_plan(
        self,
        learner_question: str,
        intent: str,
        ocr_text: str = "",
        image_prediction: str = "",
    ) -> AgentDecision:
        """
        Create an execution plan using the Agent Planner.
        """

        return self.planner.create_plan(
            learner_question=learner_question,
            intent=intent,
            ocr_text=ocr_text,
            image_prediction=image_prediction,
        )

    def execute_plan(
        self,
        learner_question: str,
        intent: str,
        readiness_score: float,
        knowledge_gaps: list[str],
        ocr_text: str = "",
        image_prediction: str = "",
    ) -> dict:
        """
        Create an execution plan and execute the selected modules.
        """

        # Create Agent Plan
        decision = self.create_plan(
            learner_question=learner_question,
            intent=intent,
            ocr_text=ocr_text,
            image_prediction=image_prediction,
        )

        # Execute Agent Plan
        execution_result = self.executor.execute(
            plan=decision,
            learner_question=learner_question,
            intent=intent,
            readiness_score=readiness_score,
            knowledge_gaps=knowledge_gaps,
            ocr_text=ocr_text,
            image_prediction=image_prediction,
        )

        # Return result
        return {
            "plan": asdict(decision),
            "execution": execution_result,
        }


_agent_service: AgentService | None = None


def get_agent_service() -> AgentService:
    """
    Singleton accessor for the Agent Service.
    """

    global _agent_service

    if _agent_service is None:
        _agent_service = AgentService()

    return _agent_service