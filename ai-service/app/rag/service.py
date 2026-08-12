"""
RAG Service for LearnPath AI.

Coordinates the complete Retrieval-Augmented Generation pipeline.

Pipeline:

Document
    ↓
Loader
    ↓
Chunker
    ↓
Embedding Model
    ↓
FAISS Vector Store
    ↓
Retriever
"""

from __future__ import annotations

import shutil
import uuid
from pathlib import Path

from app.rag.chunker import DocumentChunker
from app.rag.document_loader import DocumentLoader
from app.rag.embedding_model import get_embedding_model
from app.rag.retriever import get_retriever
from app.rag.vector_store import get_vector_store


class RAGService:
    """
    High-level service coordinating the RAG pipeline.
    """

    STORAGE_DIR = Path("app/rag/storage/documents")

    def __init__(self):
        self.chunker = DocumentChunker()
        self.embedding_model = get_embedding_model()
        self.vector_store = get_vector_store()
        self.retriever = get_retriever()

        self.STORAGE_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )

    def ingest_document(
        self,
        uploaded_file,
    ) -> dict:
        """
        Stores a document and indexes it.
        """

        extension = Path(uploaded_file.filename).suffix

        filename = (
            f"{uuid.uuid4()}{extension}"
        )

        saved_path = self.STORAGE_DIR / filename

        with saved_path.open("wb") as buffer:
            shutil.copyfileobj(
                uploaded_file.file,
                buffer,
            )

        document_name, text = DocumentLoader.load(
            str(saved_path)
        )

        chunks = self.chunker.chunk_document(
            document_name=document_name,
            text=text,
        )

        embeddings = self.embedding_model.embed_documents(
            [chunk.text for chunk in chunks]
        )

        self.vector_store.add_documents(
            chunks,
            embeddings,
        )

        self.vector_store.save()

        return {
            "document_name": document_name,
            "chunks": len(chunks),
            "status": "Indexed successfully",
        }

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
    ):
        """
        Retrieve relevant chunks.
        """

        return self.retriever.retrieve(
            query=query,
            top_k=top_k,
        )

    def status(self) -> dict:
        """
        Returns RAG status.
        """

        return {
            "documents": len(self.vector_store.chunks),
            "index_loaded": self.vector_store.index is not None,
        }


_rag_service: RAGService | None = None


def get_rag_service() -> RAGService:
    """
    Singleton accessor.
    """

    global _rag_service

    if _rag_service is None:
        _rag_service = RAGService()

    return _rag_service