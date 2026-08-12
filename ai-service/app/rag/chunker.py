"""
Document Chunker for LearnPath AI RAG.

Splits extracted document text into overlapping chunks while
preserving sentence boundaries as much as possible.
"""

from __future__ import annotations

import re
import uuid

from app.rag.models import DocumentChunk


class DocumentChunker:
    """
    Splits document text into overlapping chunks.
    """

    def __init__(
        self,
        chunk_size: int = 500,
        chunk_overlap: int = 100,
    ):
        if chunk_overlap >= chunk_size:
            raise ValueError(
                "chunk_overlap must be smaller than chunk_size."
            )

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk_document(
        self,
        document_name: str,
        text: str,
    ) -> list[DocumentChunk]:
        """
        Converts a document into chunks.
        """

        document_id = str(uuid.uuid4())

        sentences = self._split_sentences(text)

        chunks: list[DocumentChunk] = []

        current_text = ""
        chunk_id = 0

        for sentence in sentences:

            if len(current_text) + len(sentence) <= self.chunk_size:

                current_text += sentence + " "

            else:

                chunks.append(
                    DocumentChunk(
                        document_id=document_id,
                        document_name=document_name,
                        chunk_id=chunk_id,
                        text=current_text.strip(),
                    )
                )

                chunk_id += 1

                overlap = current_text[
                    max(
                        0,
                        len(current_text) - self.chunk_overlap,
                    ):
                ]

                current_text = overlap + sentence + " "

        if current_text.strip():

            chunks.append(
                DocumentChunk(
                    document_id=document_id,
                    document_name=document_name,
                    chunk_id=chunk_id,
                    text=current_text.strip(),
                )
            )

        return chunks

    @staticmethod
    def _split_sentences(text: str) -> list[str]:
        """
        Basic sentence splitter.
        """

        sentences = re.split(
            r"(?<=[.!?])\s+",
            text.strip(),
        )

        return [
            sentence.strip()
            for sentence in sentences
            if sentence.strip()
        ]