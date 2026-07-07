# app/nlp/entity_recognizer.py

"""
Named Entity Recognition - Module 4 (NLP Pipeline).

Combines two entity sources:
  1. spaCy's built-in statistical NER (general entities: people, orgs,
     products, etc.) - satisfies the NER requirement with a standard,
     recognized technique. Skipped when the loaded pipeline has no NER
     component (spacy_loader.has_statistical_ner() is False - e.g.
     running on the blank-pipeline fallback because en_core_web_sm
     hasn't been downloaded).
  2. A custom PhraseMatcher seeded from domain_vocabulary.py - what
     actually matters for this product: recognizing "IAM", "EC2",
     "G1GC", etc., which general-purpose statistical NER does not
     meaningfully recognize. Always available, independent of whether
     the downloaded spaCy model exists, since it only needs a
     tokenizer + vocab, not the statistical model.

Every entity returned is a plain, JSON-serializable dict - no spaCy
Doc/Span/Token objects ever leave this module.

Confidence: PhraseMatcher matches are exact string matches, so their
confidence is genuinely 1.0, not an estimate. spaCy's default
en_core_web_sm NER component does not expose a per-entity confidence
score through the standard API (that requires enabling beam-search NER,
a heavier, non-default configuration not used here) - rather than
fabricate a number spaCy doesn't actually provide, statistical entities
report confidence: None. Callers should treat None as "confidence not
available from this source", not as zero confidence.

Independent of app/dl/, app/ml/, app/llm/, app/ocr/ - no shared imports
or state with those packages.
"""

import logging
from typing import Dict, List, Optional

from spacy.matcher import PhraseMatcher

from app.nlp.domain_vocabulary import DOMAIN_TOPICS
from app.nlp.spacy_loader import get_nlp, has_statistical_ner

logger = logging.getLogger(__name__)

_domain_matcher: Optional[PhraseMatcher] = None


def _build_domain_matcher() -> PhraseMatcher:
    """
    Builds the PhraseMatcher over DOMAIN_TOPICS's surface forms.

    attr="LOWER" makes matching case-insensitive by comparing each
    token's lowercased form, so domain_vocabulary.py's all-lowercase
    phrases correctly match "IAM", "Iam", "iam", etc. in real user text
    without needing to lowercase the input ourselves.
    """
    nlp = get_nlp()
    matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
    for canonical_topic, surface_forms in DOMAIN_TOPICS.items():
        patterns = [nlp.make_doc(phrase) for phrase in surface_forms]
        matcher.add(canonical_topic, patterns)
    logger.info(
        "Built domain PhraseMatcher: %d canonical topics, %d surface forms.",
        len(DOMAIN_TOPICS), sum(len(v) for v in DOMAIN_TOPICS.values()),
    )
    return matcher


def _get_domain_matcher() -> PhraseMatcher:
    """
    Cached at module level, same justification as spacy_loader.py
    caching the pipeline itself: DOMAIN_TOPICS never changes at
    runtime, so rebuilding this per call would be pure waste.
    """
    global _domain_matcher
    if _domain_matcher is None:
        _domain_matcher = _build_domain_matcher()
    return _domain_matcher


def extract_entities(text: str) -> List[Dict]:
    """
    Extracts entities from text, combining spaCy's statistical NER
    (when available) with domain-vocabulary phrase matching (always
    available).

    Returns a list of plain dicts, each shaped:
        {
            "text": "<exact surface text matched>",
            "topic": "<canonical topic name, or None>",
            "label": "<spaCy entity label (e.g. 'ORG') or 'DOMAIN_TOPIC'>",
            "source": "statistical" | "domain",
            "confidence": 1.0 | None,
        }

    "topic" is the field the future Prompt Builder should key off for
    weak-topic/knowledge-gap linkage - it is the normalized canonical
    name (e.g. "IAM Security") regardless of which surface form
    ("iam", "iam role", "IAM Security") triggered the match, and is
    None for general statistical entities that have no corresponding
    certification topic (e.g. a mentioned company name).

    Overlapping statistical and domain matches over the same text span
    are deliberately both returned rather than merged/deduplicated -
    they represent genuinely different signals (a generic NER label vs.
    a domain-specific canonical topic), and the future Prompt Builder is
    better positioned to decide how to weigh them than this function is.

    Returns an empty list for empty/whitespace-only input - never raises
    for ordinary text input.
    """
    if not text or not text.strip():
        return []

    doc = get_nlp()(text)
    entities: List[Dict] = []

    if has_statistical_ner():
        for ent in doc.ents:
            entities.append({
                "text": ent.text,
                "topic": None,
                "label": ent.label_,
                "source": "statistical",
                "confidence": None,
            })

    matcher = _get_domain_matcher()
    nlp = get_nlp()
    for match_id, start, end in matcher(doc):
        span = doc[start:end]
        canonical_topic = nlp.vocab.strings[match_id]
        entities.append({
            "text": span.text,
            "topic": canonical_topic,
            "label": "DOMAIN_TOPIC",
            "source": "domain",
            "confidence": 1.0,
        })

    logger.debug(
        "extract_entities: %d statistical, %d domain entities found in %d-char input.",
        sum(1 for e in entities if e["source"] == "statistical"),
        sum(1 for e in entities if e["source"] == "domain"),
        len(text),
    )
    return entities