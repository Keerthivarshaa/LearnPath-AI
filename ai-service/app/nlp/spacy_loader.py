"""
Shared spaCy pipeline loader - Module 4 (NLP Pipeline).

spaCy's pipeline load is a genuinely expensive, one-time cost (unlike
Tesseract's per-call subprocess in the OCR module), so it's cached via a
module-level singleton - the same justification already used for
app/ml/readiness_model.py and app/dl/model.py's models.

Internal to app/nlp/ only - get_nlp() returns a raw spaCy Language
object, which is fine here (tokenizer.py and entity_recognizer.py, both
inside this same package, consume it directly). Nothing outside
app/nlp/ should ever import this module; every public function this
package exposes converts to plain, JSON-serializable Python before
returning - see tokenizer.py / entity_recognizer.py.

Falls back to a blank pipeline (tokenizer only, no statistical NER) if
en_core_web_sm hasn't been downloaded, rather than crashing - consistent
with how every other module in this project degrades gracefully
(ReadinessModel, StudyImageClassifier, ChatEngine, extract_text all do
the same). Run `python -m spacy download en_core_web_sm` once to enable
full statistical NER; domain-vocabulary matching (Section 3) still works
either way, since it doesn't depend on the downloaded model.
"""

import logging
from typing import Optional

import spacy
from spacy.language import Language

logger = logging.getLogger(__name__)

MODEL_NAME = "en_core_web_sm"

_nlp: Optional[Language] = None
_has_statistical_ner: bool = False


def _load_pipeline() -> Language:
    global _has_statistical_ner
    try:
        nlp = spacy.load(MODEL_NAME)
        _has_statistical_ner = "ner" in nlp.pipe_names
        logger.info("Loaded spaCy pipeline '%s' (statistical NER available).", MODEL_NAME)
        return nlp
    except OSError as exc:
        logger.warning(
            "spaCy model '%s' not found (%s) - falling back to a blank "
            "tokenizer-only pipeline. Statistical NER will be unavailable "
            "(domain-vocabulary entity matching still works). Run "
            "`python -m spacy download %s` to enable it.",
            MODEL_NAME, exc, MODEL_NAME,
        )
        _has_statistical_ner = False
        return spacy.blank("en")


def get_nlp() -> Language:
    """
    Returns the shared spaCy pipeline, loading it once per process.
    Internal to app/nlp/ - do not import this from outside the package.
    """
    global _nlp
    if _nlp is None:
        _nlp = _load_pipeline()
    return _nlp


def has_statistical_ner() -> bool:
    """
    Whether the loaded pipeline includes spaCy's statistical NER
    component. False when running on the blank-pipeline fallback.
    entity_recognizer.py (Section 3) uses this to skip straight to
    domain-vocabulary matching without attempting doc.ents on a pipeline
    that has no NER component at all.
    """
    get_nlp()  # ensure the pipeline (and _has_statistical_ner) is loaded
    return _has_statistical_ner
