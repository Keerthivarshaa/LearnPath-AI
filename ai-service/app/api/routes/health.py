"""
Health and root status endpoints.

These endpoints exist to verify the service is running and reachable
before any ML/NLP functionality is added in later milestones.
"""

from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/")
def root():
    """Basic service identity check."""
    return {
        "service": "learnpath-ai-service",
        "status": "running",
        "version": "0.1.0",
    }


@router.get("/health")
def health_check():
    """Liveness check for the AI service."""
    return {"status": "ok"}
