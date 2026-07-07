from fastapi import APIRouter
from pydantic import BaseModel

from app.nlp.entity_recognizer import extract_entities
from app.nlp.knowledge_gap import extract_knowledge_gaps
from app.nlp.nlp_pipeline import analyze_message
from app.nlp.sentiment_analyzer import analyze_sentiment
from app.nlp.tokenizer import tokenize

router = APIRouter(
    prefix="/nlp",
    tags=["nlp"],
)


class TextRequest(BaseModel):
    text: str


@router.post("/tokenize")
def tokenize_text(request: TextRequest):
    return {
        "tokens": tokenize(request.text)
    }


@router.post("/entities")
def entities(request: TextRequest):
    return {
        "entities": extract_entities(request.text)
    }


@router.post("/sentiment")
def sentiment(request: TextRequest):
    return analyze_sentiment(request.text)


@router.post("/knowledge-gap")
def knowledge_gap(request: TextRequest):
    return {
        "knowledge_gaps": extract_knowledge_gaps(request.text)
    }


@router.post("/analyze")
def analyze(request: TextRequest):
    return analyze_message(request.text)