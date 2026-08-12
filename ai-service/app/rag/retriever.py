"""
Retriever for LearnPath AI RAG.

Retrieves the most relevant document chunks
for a user query using semantic similarity.
"""

from __future__ import annotations

from app.rag.embedding_model import get_embedding_model
from app.rag.models import RetrievalResult
from app.rag.vector_store import get_vector_store


class Retriever:
    """
    Retrieves the most relevant document chunks.
    """

    def __init__(self):
        self.embedding_model = get_embedding_model()
        self.vector_store = get_vector_store()

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[RetrievalResult]:
        """
        Retrieve the most relevant chunks.
        """

        query_embedding = self.embedding_model.embed_text(query)

        return self.vector_store.similarity_search(
            query_embedding=query_embedding,
            top_k=top_k,
        )


_retriever: Retriever | None = None


def get_retriever() -> Retriever:
    """
    Singleton accessor.
    """

    global _retriever

    if _retriever is None:
        _retriever = Retriever()

    return _retriever