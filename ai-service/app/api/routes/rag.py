"""
FastAPI routes for RAG.
"""

from fastapi import APIRouter, File, UploadFile

from app.rag.service import get_rag_service
from app.schemas.rag import (
    RAGQueryRequest,
    RAGQueryResponse,
    RAGStatusResponse,
    RAGUploadResponse,
    RetrievedChunk,
)

router = APIRouter(
    prefix="/rag",
    tags=["rag"],
)

service = get_rag_service()


@router.post(
    "/upload",
    response_model=RAGUploadResponse,
)
def upload_document(
    file: UploadFile = File(...),
):
    """
    Upload and index a document.
    """

    result = service.ingest_document(file)

    return RAGUploadResponse(**result)


@router.post(
    "/query",
    response_model=RAGQueryResponse,
)
def query_documents(
    request: RAGQueryRequest,
):
    """
    Query indexed documents.
    """

    retrieved = service.retrieve(
        request.query,
        request.top_k,
    )

    return RAGQueryResponse(
        results=[
            RetrievedChunk(
                document_name=item.chunk.document_name,
                chunk_id=item.chunk.chunk_id,
                score=item.score,
                text=item.chunk.text,
            )
            for item in retrieved
        ]
    )


@router.get(
    "/status",
    response_model=RAGStatusResponse,
)
def status():
    """
    Get RAG status.
    """

    return RAGStatusResponse(
        **service.status()
    )