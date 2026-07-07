"""
Knowledge Gap Detection - Module 4 (NLP Pipeline).

Combines:
1. Domain entities extracted from entity_recognizer.py
2. Sentiment from sentiment_analyzer.py
3. Confusion phrases written by the learner

The goal is NOT to replace the assessment-based weakTopics already
stored in the database. Instead, this module detects conversational,
real-time knowledge gaps from chat messages.

Returns JSON-serializable dictionaries only.
"""

import re
from typing import Dict, List

from app.nlp.entity_recognizer import extract_entities
from app.nlp.sentiment_analyzer import analyze_sentiment


CONFUSION_PATTERNS = [
    r"don't understand",
    r"do not understand",
    r"didn't understand",
    r"confused",
    r"confusing",
    r"not sure",
    r"struggling",
    r"having trouble",
    r"can't understand",
    r"cannot understand",
    r"need help",
    r"help me",
    r"don't know",
    r"do not know",
    r"stuck",
]


def _contains_confusion_phrase(text: str) -> bool:
    """
    Checks whether the learner explicitly expresses confusion.
    """
    lower = text.lower()

    for pattern in CONFUSION_PATTERNS:
        if re.search(pattern, lower):
            return True

    return False


def extract_knowledge_gaps(text: str) -> List[Dict]:
    """
    Detects possible knowledge gaps from learner conversation.

    Returns:

    [
        {
            "topic": "...",
            "confidence": 0.95,
            "reason": "...",
        }
    ]
    """

    if not text or not text.strip():
        return []

    entities = extract_entities(text)
    sentiment = analyze_sentiment(text)

    confusion = _contains_confusion_phrase(text)

    gaps = []

    for entity in entities:

        if entity["topic"] is None:
            continue

        confidence = 0.60
        reasons = []

        if confusion:
            confidence += 0.20
            reasons.append("confusion phrase")

        if sentiment["label"] == "CONFUSED":
            confidence += 0.10
            reasons.append("confused sentiment")

        elif sentiment["label"] == "FRUSTRATED":
            confidence += 0.20
            reasons.append("frustrated sentiment")

        if entity["source"] == "domain":
            confidence += 0.10
            reasons.append("domain topic detected")

        confidence = min(confidence, 1.0)

        gaps.append(
            {
                "topic": entity["topic"],
                "confidence": round(confidence, 2),
                "reason": ", ".join(reasons) if reasons else "topic mentioned",
            }
        )

    # Remove duplicate topics while keeping highest confidence
    unique = {}

    for gap in gaps:
        topic = gap["topic"]

        if topic not in unique:
            unique[topic] = gap
        elif gap["confidence"] > unique[topic]["confidence"]:
            unique[topic] = gap

    return list(unique.values())