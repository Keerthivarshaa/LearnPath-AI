"""
Sentiment Analysis - Module 4 (NLP Pipeline).

Uses VADER (Valence Aware Dictionary and sEntiment Reasoner) - a
lexicon/rule-based analyzer purpose-built for short, informal text
(social media, chat messages), which is exactly what tutor chat
messages are. Chosen over a transformer-based sentiment model
deliberately: VADER needs no model download and no GPU, and avoids
introducing a third heavy ML framework (PyTorch) alongside TensorFlow
for no real accuracy benefit on this kind of text. The one place this
project spends transformer weight on NLP is BERT intent classification
(Module 5), where fine-tuning is actually load-bearing.

Independent of app/dl/, app/ml/, app/llm/, app/ocr/, and the rest of
app/nlp/ - no shared imports or state. Deliberately does NOT do any
keyword/phrase matching (e.g. "confused", "don't understand") - that is
knowledge_gap.py's responsibility (Section 5), kept separate so this
module stays a pure, honest reflection of VADER's own numeric output.
"""

import logging
from typing import Dict

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

logger = logging.getLogger(__name__)

_analyzer = None

# VADER's own documented convention for the neutral band around 0.
_NEUTRAL_BAND = 0.05

# Threshold splitting each polarity direction into two learner-friendly
# labels. This is a deliberate, documented approximation, not a claim
# that VADER truly distinguishes the emotion of "confusion" from
# "frustration" - VADER measures valence and intensity, not discrete
# emotion categories. In practice, uncertainty ("I don't understand
# this") tends to read as mildly negative rather than strongly negative
# to a lexicon-based analyzer, so mild negativity is labeled CONFUSED
# and strong negativity FRUSTRATED. Mirrored on the positive side: mild
# positivity is CONFIDENT, strong positivity is POSITIVE.
_STRONG_BAND = 0.5


def _get_analyzer() -> SentimentIntensityAnalyzer:
    """
    VADER's analyzer only holds a static lexicon (no learned weights, no
    meaningful load cost like spaCy's pipeline or the CNN/readiness
    models) - cached at module level purely to avoid rebuilding the
    lexicon dict on every call, not because loading it is expensive.
    """
    global _analyzer
    if _analyzer is None:
        _analyzer = SentimentIntensityAnalyzer()
        logger.info("VADER SentimentIntensityAnalyzer initialized.")
    return _analyzer


def _label_from_compound(compound: float) -> str:
    if compound <= -_STRONG_BAND:
        return "FRUSTRATED"
    if compound <= -_NEUTRAL_BAND:
        return "CONFUSED"
    if compound < _NEUTRAL_BAND:
        return "NEUTRAL"
    if compound < _STRONG_BAND:
        return "CONFIDENT"
    return "POSITIVE"


def analyze_sentiment(text: str) -> Dict:
    """
    Analyzes the sentiment of a piece of text using VADER.

    Returns a JSON-serializable dict:
        {
            "label": "CONFUSED" | "FRUSTRATED" | "NEUTRAL" | "CONFIDENT" | "POSITIVE",
            "compound": float,   # VADER's overall polarity, -1 to 1
            "positive": float,   # proportion of text scored positive, 0-1
            "neutral": float,    # proportion of text scored neutral, 0-1
            "negative": float,   # proportion of text scored negative, 0-1
        }

    Empty or whitespace-only input returns a neutral, zeroed result
    rather than calling VADER on nothing or raising - there is no
    sentiment to measure in empty text, so an explicit NEUTRAL result is
    the honest answer, not an error condition.
    """
    if not text or not text.strip():
        return {
            "label": "NEUTRAL",
            "compound": 0.0,
            "positive": 0.0,
            "neutral": 1.0,
            "negative": 0.0,
        }

    scores = _get_analyzer().polarity_scores(text)
    label = _label_from_compound(scores["compound"])

    result = {
        "label": label,
        "compound": scores["compound"],
        "positive": scores["pos"],
        "neutral": scores["neu"],
        "negative": scores["neg"],
    }

    logger.debug(
        "analyze_sentiment: label=%s compound=%.3f (input length=%d)",
        label, scores["compound"], len(text),
    )
    return result
