"""
LearnPath AI - ML/AI Microservice
FastAPI application entrypoint.

This service provides AI/ML capabilities (readiness prediction, NLP, RAG,
agentic tutoring) to the existing LearnPath AI Spring Boot backend. It is
called internally by Spring Boot and does not interact with the React
frontend or the primary PostgreSQL database directly.

Run locally:
    uvicorn main:app --reload --port 8001
"""

from fastapi import FastAPI

from app.api.routes import health

app = FastAPI(
    title="LearnPath AI - ML Service",
    description=(
        "Internal AI/ML microservice powering LearnPath AI's readiness "
        "prediction, NLP, and tutoring capabilities."
    ),
    version="0.1.0",
)

app.include_router(health.router)
