"""
Agent Executor - LearnPath AI

The Agent Executor executes the plan created by the Agent Planner.

It coordinates the existing AI modules:
- NLP
- RAG
- OCR
- CNN
- Readiness ML
- LLM

The executor does not decide what to use.
The Agent Planner makes that decision.
The executor follows the plan and calls the required services.
"""

from __future__ import annotations

from app.agent.models import AgentDecision


class AgentExecutor:
    """
    Executes the AI modules selected by the Agent Planner.
    """

    def execute(
        self,
        plan: AgentDecision,
        learner_question: str,
        intent: str,
        readiness_score: float,
        knowledge_gaps: list[str],
        ocr_text: str = "",
        image_prediction: str = "",
    ) -> dict:
        """
        Execute the modules selected in the agent plan.
        """

        execution_results = {
            "modules_executed": [],
            "nlp_result": None,
            "rag_result": None,
            "ocr_result": None,
            "cnn_result": None,
            "readiness_result": None,
            "llm_result": None,
        }

        # --------------------------------------------------
        # 1. NLP
        # --------------------------------------------------

        if plan.use_nlp:
            print("🤖 Agent: Executing NLP module")

            try:
                from app.nlp.nlp_pipeline import analyze_message
                from app.nlp.tokenizer import tokenize
                from app.nlp.entity_recognizer import extract_entities
                from app.nlp.sentiment_analyzer import analyze_sentiment
                from app.nlp.knowledge_gap import extract_knowledge_gaps

                nlp_result = {
                    "tokens": tokenize(learner_question),
                    "entities": extract_entities(learner_question),
                    "sentiment": analyze_sentiment(learner_question),
                    "knowledge_gaps": extract_knowledge_gaps(
                        learner_question
                    ),
                    "intent": analyze_message(learner_question),
                }

                execution_results["nlp_result"] = nlp_result
                execution_results["modules_executed"].append("NLP")

            except Exception as exc:
                print(f"⚠️ NLP execution failed: {exc}")

                execution_results["nlp_result"] = {
                    "status": "NLP execution failed",
                    "error": str(exc),
                }

        # --------------------------------------------------
        # 2. RAG
        # --------------------------------------------------

        if plan.use_rag:
            print("📚 Agent: Executing RAG module")

            try:
                from app.rag.service import get_rag_service

                rag_service = get_rag_service()

                retrieved_chunks = rag_service.retrieve(
                    query=learner_question,
                    top_k=3,
                )

                rag_result = []

                for result in retrieved_chunks:
                    rag_result.append(
                        {
                            "text": result.chunk.text,
                            "score": result.score,
                        }
                    )

                execution_results["rag_result"] = rag_result
                execution_results["modules_executed"].append("RAG")

            except Exception as exc:
                print(f"⚠️ RAG execution failed: {exc}")

                execution_results["rag_result"] = {
                    "status": "RAG execution failed",
                    "error": str(exc),
                }

        # --------------------------------------------------
        # 3. OCR
        # --------------------------------------------------

        if plan.use_ocr:
            print("📄 Agent: Executing OCR module")

            execution_results["ocr_result"] = {
                "status": "OCR data available",
                "ocr_text": ocr_text,
            }

            execution_results["modules_executed"].append("OCR")

        # --------------------------------------------------
        # 4. CNN
        # --------------------------------------------------

        if plan.use_cnn:
            print("🖼️ Agent: Executing CNN module")

            execution_results["cnn_result"] = {
                "status": "CNN prediction available",
                "image_prediction": image_prediction,
            }

            execution_results["modules_executed"].append("CNN")

        # --------------------------------------------------
        # 5. Readiness ML
        # --------------------------------------------------

        if plan.use_readiness:
            print("📊 Agent: Executing Readiness ML module")

            execution_results["readiness_result"] = {
                "readiness_score": readiness_score,
                "knowledge_gaps": knowledge_gaps,
            }

            execution_results["modules_executed"].append(
                "READINESS_ML"
            )

        # --------------------------------------------------
        # 6. LLM
        # --------------------------------------------------

        if plan.use_llm:
            print("🧠 Agent: Executing LLM module")

            try:
                from app.llm.service import get_llm_service

                llm_service = get_llm_service()

                llm_result = llm_service.generate_response(
                    learner_question=learner_question,
                    intent=intent,
                    readiness_score=readiness_score,
                    knowledge_gaps=knowledge_gaps,
                    ocr_text=ocr_text,
                    image_prediction=image_prediction,
                )

                execution_results["llm_result"] = llm_result
                execution_results["modules_executed"].append("LLM")

            except Exception as exc:
                print(f"⚠️ LLM execution failed: {exc}")

                execution_results["llm_result"] = {
                    "status": "LLM execution failed",
                    "error": str(exc),
                }

        return execution_results