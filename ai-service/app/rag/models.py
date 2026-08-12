"""
Internal domain models for the RAG module.

These dataclasses are used throughout the Retrieval-Augmented
Generation pipeline.
"""

from dataclasses import dataclass, field


@dataclass(slots=True)
class DocumentChunk:
    """
    Represents a chunk of text extracted from an uploaded document.
    """

    document_id: str
    document_name: str
    chunk_id: int
    text: str
    metadata: dict[str, str] = field(default_factory=dict)


@dataclass(slots=True)
class RetrievalResult:
    """
    Represents a retrieved document chunk along with
    its similarity score.
    """

    chunk: DocumentChunk
    score: float