"""
Intent Classification - LearnPath AI

Uses a fine-tuned DistilBERT model when available.
Falls back to a lightweight rule-based classifier if the
trained model has not yet been generated.

This guarantees that the NLP pipeline never crashes while
still allowing the project to demonstrate a genuine Deep
Learning model once training has been completed.
"""

from pathlib import Path

import tensorflow as tf
from transformers import (
    AutoTokenizer,
    TFAutoModelForSequenceClassification,
)

from app.nlp.synthetic_intent_data import INTENTS

MODEL_DIR = (
    Path(__file__).parent /
    "models" /
    "intent_classifier"
)


class IntentClassifier:

    def __init__(self):

        self.model = None
        self.tokenizer = None
        self.model_source = "rule_based"

        if MODEL_DIR.exists():
            try:
                self.tokenizer = AutoTokenizer.from_pretrained(
                    str(MODEL_DIR)
                )

                self.model = (
                    TFAutoModelForSequenceClassification
                    .from_pretrained(str(MODEL_DIR))
                )

                self.model_source = "distilbert"

            except Exception:
                self.model = None
                self.tokenizer = None

    def classify(self, text: str):

        text = (text or "").strip()

        if not text:
            return {
                "intent": "GENERAL_CHAT",
                "confidence": 1.0,
                "modelSource": self.model_source,
            }

        if self.model is not None:

            encoded = self.tokenizer(
                text,
                truncation=True,
                padding=True,
                max_length=64,
                return_tensors="tf",
            )

            logits = self.model(encoded).logits

            probabilities = tf.nn.softmax(
                logits,
                axis=1,
            ).numpy()[0]

            prediction = int(tf.argmax(probabilities, axis=0))

            return {
                "intent": INTENTS[prediction],
                "confidence": float(probabilities[prediction]),
                "modelSource": self.model_source,
            }

        return self._fallback(text)

    def _fallback(self, text: str):

        lower = text.lower()

        if any(
            phrase in lower
            for phrase in [
                "progress",
                "score",
                "completed",
                "my marks",
                "my performance",
            ]
        ):
            intent = "CHECK_PROGRESS"

        elif any(
            phrase in lower
            for phrase in [
                "roadmap",
                "plan",
                "study plan",
                "schedule",
                "learning path",
            ]
        ):
            intent = "REQUEST_ROADMAP"

        elif any(
            phrase in lower
            for phrase in [
                "quiz",
                "question",
                "test me",
                "practice",
                "mcq",
            ]
        ):
            intent = "REQUEST_QUIZ"

        elif any(
            phrase in lower
            for phrase in [
                "difference",
                "compare",
                "versus",
                "vs",
            ]
        ):
            intent = "COMPARE_TOPICS"

        elif any(
            phrase in lower
            for phrase in [
                "what is",
                "explain",
                "define",
                "how does",
                "teach",
            ]
        ):
            intent = "EXPLAIN_CONCEPT"

        elif any(
            phrase in lower
            for phrase in [
                "hello",
                "hi",
                "thanks",
                "thank you",
                "good morning",
                "good evening",
            ]
        ):
            intent = "GENERAL_CHAT"

        else:
            intent = "GENERAL_CHAT"

        return {
            "intent": intent,
            "confidence": 0.60,
            "modelSource": "rule_based",
        }


_classifier = IntentClassifier()


def classify_intent(text: str):
    """
    Public API used by the rest of LearnPath AI.
    """
    return _classifier.classify(text)