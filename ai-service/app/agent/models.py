"""
Agent Models - LearnPath AI

Defines the internal data structures used by the
Agentic AI orchestration layer.
"""

from dataclasses import dataclass


@dataclass
class AgentDecision:
    """
    Represents the decisions made by the AI Tutor agent.
    """

    use_nlp: bool = True
    use_rag: bool = False
    use_ocr: bool = False
    use_cnn: bool = False
    use_readiness: bool = False
    use_llm: bool = True