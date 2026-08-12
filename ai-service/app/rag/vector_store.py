"""
FAISS Vector Store for LearnPath AI RAG.

Stores document embeddings and performs similarity search.
"""

from __future__ import annotations

from pathlib import Path
import pickle

import faiss
import numpy as np

from app.rag.models import DocumentChunk, RetrievalResult


class VectorStore:
    """
    Manages the FAISS vector index.
    """

    INDEX_FILE = "app/rag/storage/faiss.index"
    CHUNKS_FILE = "app/rag/storage/chunks.pkl"

    def __init__(self):
        self.index: faiss.Index | None = None
        self.chunks: list[DocumentChunk] = []

        # Automatically restore previous index
        self.load()

    def add_documents(
        self,
        chunks: list[DocumentChunk],
        embeddings: list[list[float]],
    ) -> None:
        """
        Add document chunks and their embeddings.
        """

        vectors = np.array(embeddings, dtype=np.float32)

        if self.index is None:
            dimension = vectors.shape[1]
            self.index = faiss.IndexFlatIP(dimension)

        self.index.add(vectors)
        self.chunks.extend(chunks)

    def similarity_search(
        self,
        query_embedding: list[float],
        top_k: int = 5,
    ) -> list[RetrievalResult]:
        """
        Retrieve similar chunks.
        """

        if self.index is None:
            return []

        if not self.chunks:
            return []

        query = np.array([query_embedding], dtype=np.float32)

        scores, indices = self.index.search(query, top_k)

        results: list[RetrievalResult] = []

        for score, idx in zip(scores[0], indices[0]):

            if idx == -1:
                continue

            if idx >= len(self.chunks):
                continue

            results.append(
                RetrievalResult(
                    chunk=self.chunks[idx],
                    score=float(score),
                )
            )

        return results

    def save(self) -> None:
        """
        Save FAISS index and chunk metadata.
        """

        if self.index is None:
            return

        storage = Path(self.INDEX_FILE).parent
        storage.mkdir(parents=True, exist_ok=True)

        faiss.write_index(
            self.index,
            self.INDEX_FILE,
        )

        with open(self.CHUNKS_FILE, "wb") as f:
            pickle.dump(self.chunks, f)

    def load(self) -> None:
        """
        Restore FAISS index and chunks.
        """

        if Path(self.INDEX_FILE).exists():
            self.index = faiss.read_index(
                self.INDEX_FILE
            )

        if Path(self.CHUNKS_FILE).exists():
            with open(self.CHUNKS_FILE, "rb") as f:
                self.chunks = pickle.load(f)


_vector_store: VectorStore | None = None


def get_vector_store() -> VectorStore:
    """
    Singleton accessor.
    """

    global _vector_store

    if _vector_store is None:
        _vector_store = VectorStore()

    return _vector_store