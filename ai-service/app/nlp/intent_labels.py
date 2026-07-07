"""
Intent labels used throughout the LearnPath AI NLP pipeline.

This file contains only constants—no business logic.

The intent classifier predicts one of these labels for every
learner message. Downstream modules (Prompt Builder, Chat Engine,
RAG, Agentic AI) use these labels to decide how the assistant
should respond.

Keeping the labels centralized prevents different parts of the
system from using inconsistent strings.

Module:
    BERT Intent Classification (Module 5)

Used by:
    - synthetic_intent_data.py
    - train_intent_classifier.py
    - intent_classifier.py
    - prompt_builder.py (future)
    - chat_engine.py (future)
"""

from typing import List


# ------------------------------------------------------------------
# Intent Labels
# ------------------------------------------------------------------

EXPLAIN_CONCEPT = "EXPLAIN_CONCEPT"

ASK_EXAMPLE = "ASK_EXAMPLE"

QUIZ_ME = "QUIZ_ME"

CHECK_PROGRESS = "CHECK_PROGRESS"

ASK_ROADMAP = "ASK_ROADMAP"

UPLOAD_IMAGE = "UPLOAD_IMAGE"

GENERAL_CHAT = "GENERAL_CHAT"


# ------------------------------------------------------------------
# Ordered list of labels.
#
# The order is important because the training script converts labels
# into numeric IDs using this list.
# ------------------------------------------------------------------

INTENT_LABELS: List[str] = [
    EXPLAIN_CONCEPT,
    ASK_EXAMPLE,
    QUIZ_ME,
    CHECK_PROGRESS,
    ASK_ROADMAP,
    UPLOAD_IMAGE,
    GENERAL_CHAT,
]


# ------------------------------------------------------------------
# Label → ID mapping
# ------------------------------------------------------------------

LABEL_TO_ID = {
    label: index
    for index, label in enumerate(INTENT_LABELS)
}


# ------------------------------------------------------------------
# ID → Label mapping
# ------------------------------------------------------------------

ID_TO_LABEL = {
    index: label
    for index, label in enumerate(INTENT_LABELS)
}