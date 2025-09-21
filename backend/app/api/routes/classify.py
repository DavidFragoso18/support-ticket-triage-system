from fastapi import APIRouter
from app.schemas.classify import ClassifyIn, ClassifyOut
from app.nlp.pipeline import nlp
from app.services.priority_rules import choose_priority

router = APIRouter(prefix="/classify", tags=["classify"])

@router.post("", response_model=ClassifyOut)
def classify(body: ClassifyIn) -> ClassifyOut:
    intent, intent_conf, sentiment, sentiment_conf, low_conf = nlp.classify_text(body.text)
    priority = choose_priority(intent, sentiment, low_conf, body.text)
    return ClassifyOut(
        intent=intent,
        sentiment=sentiment,
        priority=priority,
        confidence=float(min(intent_conf, sentiment_conf)),
        low_confidence=low_conf
    )
