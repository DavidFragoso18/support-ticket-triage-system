from fastapi import APIRouter
from app.schemas.classify import ClassifyIn, ClassifyOut
from app.nlp.pipeline import nlp
from app.services.priority_rules import choose_priority
from app.core.errors import internal_error, logger

router = APIRouter(prefix="/classify", tags=["classify"])

@router.post("", response_model=ClassifyOut)
def classify(body: ClassifyIn) -> ClassifyOut:
    try:
        text = body.text  # Use the single text field, not subject + body
        intent, intent_conf, sentiment, sentiment_conf, low_conf = nlp.classify_text(text)
        
        # Fixed: choose_priority only needs intent, sentiment, and text
        priority = choose_priority(intent, sentiment, text)
        
        return ClassifyOut(
            intent=intent,
            sentiment=sentiment,
            priority=priority,
            confidence=float(min(intent_conf, sentiment_conf)),
            low_confidence=low_conf
        )
    except Exception:
        logger.exception("CLASSIFY_FAILED")
        raise internal_error("CLASSIFY_FAILED", "Classification failed. Please try again.")