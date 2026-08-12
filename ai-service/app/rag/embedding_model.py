"""
Embedding Model for LearnPath AI RAG.

Loads the sentence-transformers embedding model and converts
text into dense vector embeddings for semantic search.
"""

from __future__ import annotations

from sentence_transformers import SentenceTransformer


class EmbeddingModel:
    """
    Singleton wrapper around the sentence-transformers model.
    """

    MODEL_NAME = "all-MiniLM-L6-v2"

    def __init__(self):
        self.model = SentenceTransformer(self.MODEL_NAME)

    def embed_text(self, text: str) -> list[float]:
        """
        Generate an embedding for a single piece of text.
        """
        embedding = self.model.encode(
            text,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )

        return embedding.tolist()

    def embed_documents(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        """
        Generate embeddings for multiple documents.
        """
        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )

        return embeddings.tolist()


_embedding_model: EmbeddingModel | None = None


def get_embedding_model() -> EmbeddingModel:
    """
    Returns a singleton EmbeddingModel instance.
    """

    global _embedding_model

    if _embedding_model is None:
        _embedding_model = EmbeddingModel()

    return _embedding_model