from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID
from sqlmodel import Session, select
from app.db.base import get_session
from app.db.models.feedback import ClassificationFeedback
from app.db.models.ticket import TicketClassification
from app.schemas.feedback import FeedbackCreate, FeedbackOut
from app.core.errors import internal_error, not_found, logger

router = APIRouter(prefix="/feedback", tags=["feedback"])

@router.post("", status_code=201, response_model=FeedbackOut)
def create_feedback(
    feedback_data: FeedbackCreate,
    session: Session = Depends(get_session),
) -> FeedbackOut:
    """
    Submit agent feedback on a classification.
    Agents can accept, reject, or correct AI predictions.
    """
    try:
        # Verify classification exists
        classification = session.get(TicketClassification, feedback_data.classification_id)
        if not classification:
            raise not_found("CLASSIFICATION_NOT_FOUND", "Classification not found.")
        
        # Create feedback record
        feedback = ClassificationFeedback(
            classification_id=feedback_data.classification_id,
            action=feedback_data.action,
            corrected_intent=feedback_data.corrected_intent,
            corrected_sentiment=feedback_data.corrected_sentiment,
            corrected_priority=feedback_data.corrected_priority,
            agent_id=feedback_data.agent_id,
            notes=feedback_data.notes,
        )
        
        session.add(feedback)
        session.commit()
        session.refresh(feedback)
        
        # If corrected, update the existing classification with corrected values
        if feedback_data.action == "corrected":
            # Update the classification with corrected values
            if feedback_data.corrected_intent:
                classification.intent = feedback_data.corrected_intent
            if feedback_data.corrected_sentiment:
                classification.sentiment = feedback_data.corrected_sentiment
            if feedback_data.corrected_priority:
                classification.priority = feedback_data.corrected_priority
            
            # Mark as human-corrected with 100% confidence
            classification.confidence = 1.0
            classification.low_confidence = False
            classification.source = "human"
            
            session.add(classification)
            session.commit()
        
        return FeedbackOut(
            id=feedback.id,
            classification_id=feedback.classification_id,
            action=feedback.action,
            corrected_intent=feedback.corrected_intent,
            corrected_sentiment=feedback.corrected_sentiment,
            corrected_priority=feedback.corrected_priority,
            agent_id=feedback.agent_id,
            notes=feedback.notes,
            created_at=feedback.created_at,
        )
        
    except HTTPException:
        raise
    except Exception:
        logger.exception("CREATE_FEEDBACK_FAILED")
        raise internal_error("CREATE_FEEDBACK_FAILED", "Could not create feedback.")

@router.get("/{classification_id}", response_model=list[FeedbackOut])
def get_feedback(
    classification_id: UUID,
    session: Session = Depends(get_session),
) -> list[FeedbackOut]:
    """
    Get all feedback for a specific classification.
    """
    try:
        feedbacks = session.exec(
            select(ClassificationFeedback)
            .where(ClassificationFeedback.classification_id == classification_id)
            .order_by(ClassificationFeedback.created_at.desc())
        ).all()
        
        return [
            FeedbackOut(
                id=f.id,
                classification_id=f.classification_id,
                action=f.action,
                corrected_intent=f.corrected_intent,
                corrected_sentiment=f.corrected_sentiment,
                corrected_priority=f.corrected_priority,
                agent_id=f.agent_id,
                notes=f.notes,
                created_at=f.created_at,
            )
            for f in feedbacks
        ]
        
    except Exception:
        logger.exception("GET_FEEDBACK_FAILED")
        raise internal_error("GET_FEEDBACK_FAILED", "Could not retrieve feedback.")
