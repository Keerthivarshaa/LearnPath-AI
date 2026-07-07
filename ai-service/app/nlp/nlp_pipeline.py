"""
NLP Pipeline - Module 4 (NLP Pipeline).

Single orchestration entry point for the NLP package.

This module combines:
    • Tokenization
    • Named Entity Recognition
    • Sentiment Analysis
    • Knowledge Gap Detection
    • Intent Classification

Future modules (Prompt Builder, AI Tutor, /chat) should call ONLY
analyze_message() instead of calling the individual NLP modules
themselves.

Independent of OCR, CNN, ML, Spring Boot and React.
"""

from typing import Dict

from app.nlp.tokenizer import tokenize
from app.nlp.entity_recognizer import extract_entities
from app.nlp.sentiment_analyzer import analyze_sentiment
from app.nlp.knowledge_gap import extract_knowledge_gaps
from app.nlp.intent_classifier import classify_intent


def analyze_message(text: str) -> Dict:
    """
    Runs the complete NLP pipeline.

    Returns:

    {
        "tokens": [...],
        "entities": [...],
        "sentiment": {...},
        "knowledge_gaps": [...],
        "intent": {...}
    }

    This function intentionally performs no Prompt Engineering,
    no LLM interaction, and no database access. It simply analyzes
    the learner's message and returns structured information for
    future modules.
    """

    if not text or not text.strip():
        return {
            "tokens": [],
            "entities": [],
            "sentiment": {
                "label": "NEUTRAL",
                "compound": 0.0,
                "positive": 0.0,
                "neutral": 1.0,
                "negative": 0.0,
            },
            "knowledge_gaps": [],
            "intent": {
                "intent": "GENERAL_CHAT",
                "confidence": 1.0,
                "model_source": "rule_based",
            },
        }

    return {
        "tokens": tokenize(text),
        "entities": extract_entities(text),
        "sentiment": analyze_sentiment(text),
        "knowledge_gaps": extract_knowledge_gaps(text),
        "intent": classify_intent(text),
    }