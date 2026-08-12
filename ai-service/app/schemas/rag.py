"""
Pydantic schemas for the RAG module.
"""

from pydantic import BaseModel


class RAGUploadResponse(BaseModel):
    """
    Response after indexing a document.
    """

    document_name: str
    chunks: int
    status: str


class RAGQueryRequest(BaseModel):
    """
    Query request.
    """

    query: str
    top_k: int = 5


class RetrievedChunk(BaseModel):
    """
    Retrieved chunk.
    """

    document_name: str
    chunk_id: int
    score: float
    text: str


class RAGQueryResponse(BaseModel):
    """
    Query response.
    """

    results: list[RetrievedChunk]


class RAGStatusResponse(BaseModel):
    """
    Status response.
    """

    documents: int
    index_loaded: bool