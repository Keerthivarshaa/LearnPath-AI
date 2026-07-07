# app/nlp/tokenizer.py

"""
Tokenization - Module 4 (NLP Pipeline).

Thin wrapper around the shared spaCy pipeline (spacy_loader.py). Kept
deliberately minimal - returns plain token strings, nothing more.
Tokenization is treated as a standalone, demonstrable capability here
(matching the specialization requirement), not as a required
intermediate step other functions in this package must route through -
entity_recognizer.py computes its own spaCy Doc directly, since it
needs more than token strings (see that file's docstring).

Independent of app/dl/, app/ml/, app/llm/, app/ocr/ - no shared imports.
"""

from typing import List

from app.nlp.spacy_loader import get_nlp


def tokenize(text: str) -> List[str]:
    """
    Splits text into tokens using spaCy's tokenizer.

    Returns a plain list of strings (JSON-serializable) - never spaCy
    Token objects. Pure-whitespace tokens are dropped since they carry
    no information; punctuation is kept as separate tokens, since that
    is what accurate tokenization means.

    Works identically whether or not en_core_web_sm is downloaded -
    tokenization itself does not depend on the statistical model, only
    NER does (see spacy_loader.py).
    """
    if not text or not text.strip():
        return []

    doc = get_nlp()(text)
    return [token.text for token in doc if not token.is_space]