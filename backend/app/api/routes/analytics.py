from fastapi import APIRouter, Depends, Query
from typing import Optional
from datetime import datetime, timedelta
from sqlmodel import Session, select, func
from app.db.base import get_session
from app.db.models.ticket import Ticket, TicketClassification
from app.db.models.feedback import ClassificationFeedback
from app.schemas.analytics import (
    AnalyticsOverview,
    IntentDistribution,
    SentimentDistribution,
    PriorityDistribution,
    TimeSeriesData,
    ClassificationAccuracy,
)
from app.core.errors import internal_error, logger

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/overview", response_model=AnalyticsOverview)
def get_overview(
    session: Session = Depends(get_session),
) -> AnalyticsOverview:
    """Get overall system metrics"""
    try:
        # Total tickets
        total_tickets = session.exec(select(func.count(Ticket.id))).one()
        
        # Tickets created today
        today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        tickets_today = session.exec(
            select(func.count(Ticket.id))
            .where(Ticket.created_at >= today_start)
        ).one()
        
        # Average confidence
        avg_confidence = session.exec(
            select(func.avg(TicketClassification.confidence))
        ).one() or 0.0
        
        # Low confidence count
        low_confidence_count = session.exec(
            select(func.count(TicketClassification.id))
            .where(TicketClassification.low_confidence == True)
        ).one()
        
        # Feedback count
        feedback_count = session.exec(
            select(func.count(ClassificationFeedback.id))
        ).one()
        
        return AnalyticsOverview(
            total_tickets=total_tickets,
            tickets_today=tickets_today,
            avg_confidence=round(avg_confidence, 4),
            low_confidence_count=low_confidence_count,
            feedback_count=feedback_count,
        )
    except Exception:
        logger.exception("GET_OVERVIEW_FAILED")
        raise internal_error("GET_OVERVIEW_FAILED", "Could not retrieve overview.")

@router.get("/intent-distribution", response_model=list[IntentDistribution])
def get_intent_distribution(
    session: Session = Depends(get_session),
) -> list[IntentDistribution]:
    """Get distribution of intents"""
    try:
        # Get intent counts
        results = session.exec(
            select(
                TicketClassification.intent,
                func.count(TicketClassification.id).label("count")
            )
            .group_by(TicketClassification.intent)
        ).all()
        
        total = sum(r[1] for r in results)
        
        return [
            IntentDistribution(
                intent=intent,
                count=count,
                percentage=round((count / total * 100) if total > 0 else 0, 2)
            )
            for intent, count in results
        ]
    except Exception:
        logger.exception("GET_INTENT_DISTRIBUTION_FAILED")
        raise internal_error("GET_INTENT_DISTRIBUTION_FAILED", "Could not retrieve intent distribution.")

@router.get("/sentiment-distribution", response_model=list[SentimentDistribution])
def get_sentiment_distribution(
    session: Session = Depends(get_session),
) -> list[SentimentDistribution]:
    """Get distribution of sentiments"""
    try:
        results = session.exec(
            select(
                TicketClassification.sentiment,
                func.count(TicketClassification.id).label("count")
            )
            .group_by(TicketClassification.sentiment)
        ).all()
        
        total = sum(r[1] for r in results)
        
        return [
            SentimentDistribution(
                sentiment=sentiment,
                count=count,
                percentage=round((count / total * 100) if total > 0 else 0, 2)
            )
            for sentiment, count in results
        ]
    except Exception:
        logger.exception("GET_SENTIMENT_DISTRIBUTION_FAILED")
        raise internal_error("GET_SENTIMENT_DISTRIBUTION_FAILED", "Could not retrieve sentiment distribution.")

@router.get("/priority-distribution", response_model=list[PriorityDistribution])
def get_priority_distribution(
    session: Session = Depends(get_session),
) -> list[PriorityDistribution]:
    """Get distribution of priorities"""
    try:
        results = session.exec(
            select(
                TicketClassification.priority,
                func.count(TicketClassification.id).label("count")
            )
            .group_by(TicketClassification.priority)
        ).all()
        
        total = sum(r[1] for r in results)
        
        return [
            PriorityDistribution(
                priority=priority,
                count=count,
                percentage=round((count / total * 100) if total > 0 else 0, 2)
            )
            for priority, count in results
        ]
    except Exception:
        logger.exception("GET_PRIORITY_DISTRIBUTION_FAILED")
        raise internal_error("GET_PRIORITY_DISTRIBUTION_FAILED", "Could not retrieve priority distribution.")

@router.get("/tickets-over-time", response_model=list[TimeSeriesData])
def get_tickets_over_time(
    days: int = Query(7, ge=1, le=90),
    session: Session = Depends(get_session),
) -> list[TimeSeriesData]:
    """Get ticket volume over time"""
    try:
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # Get tickets grouped by date within time range
        results = session.exec(
            select(
                func.date(Ticket.created_at).label("date"),
                func.count(Ticket.id).label("count")
            )
            .where(Ticket.created_at >= start_date)
            .group_by(func.date(Ticket.created_at))
            .order_by(func.date(Ticket.created_at))
        ).all()
        
        # If no results in time range, get the most recent tickets available
        if not results:
            logger.info(f"No tickets in last {days} days, fetching most recent data")
            results = session.exec(
                select(
                    func.date(Ticket.created_at).label("date"),
                    func.count(Ticket.id).label("count")
                )
                .group_by(func.date(Ticket.created_at))
                .order_by(func.date(Ticket.created_at).desc())
                .limit(min(days, 30))  # Show up to 30 most recent days
            ).all()
            
            # Reverse to show chronologically
            results = list(reversed(results))
        
        return [
            TimeSeriesData(
                date=str(date),
                count=count
            )
            for date, count in results
        ]
    except Exception:
        logger.exception("GET_TICKETS_OVER_TIME_FAILED")
        raise internal_error("GET_TICKETS_OVER_TIME_FAILED", "Could not retrieve time series data.")

@router.get("/classification-accuracy", response_model=ClassificationAccuracy)
def get_classification_accuracy(
    session: Session = Depends(get_session),
) -> ClassificationAccuracy:
    """
    Get model accuracy metrics based on agent feedback with per-field breakdown
    
    For each field (intent, sentiment, priority):
    - Accepted: feedback action is 'accepted' OR corrected but this field unchanged
    - Corrected: feedback action is 'corrected' AND this field was changed
    - Accuracy: accepted / total_feedback
    """
    try:
        # Get all feedback records
        all_feedback = session.exec(select(ClassificationFeedback)).all()
        total_feedback = len(all_feedback)
        
        if total_feedback == 0:
            return ClassificationAccuracy(
                intent_accuracy=0.0,
                sentiment_accuracy=0.0,
                priority_accuracy=0.0,
                overall_accuracy=0.0,
                intent_accepted=0,
                intent_corrected=0,
                sentiment_accepted=0,
                sentiment_corrected=0,
                priority_accepted=0,
                priority_corrected=0,
                total_feedback=0
            )
        
        # Per-field calculations
        # Intent: accepted if action='accepted' OR (action='corrected' but intent not changed)
        intent_accepted = sum(1 for f in all_feedback if f.action == "accepted" or (f.action == "corrected" and f.corrected_intent is None))
        intent_corrected = sum(1 for f in all_feedback if f.action == "corrected" and f.corrected_intent is not None)
        
        # Sentiment: accepted if action='accepted' OR (action='corrected' but sentiment not changed)
        sentiment_accepted = sum(1 for f in all_feedback if f.action == "accepted" or (f.action == "corrected" and f.corrected_sentiment is None))
        sentiment_corrected = sum(1 for f in all_feedback if f.action == "corrected" and f.corrected_sentiment is not None)
        
        # Priority: accepted if action='accepted' OR (action='corrected' but priority not changed)
        priority_accepted = sum(1 for f in all_feedback if f.action == "accepted" or (f.action == "corrected" and f.corrected_priority is None))
        priority_corrected = sum(1 for f in all_feedback if f.action == "corrected" and f.corrected_priority is not None)
        
        # Calculate per-field accuracy (0.0 to 1.0)
        intent_accuracy = intent_accepted / total_feedback if total_feedback > 0 else 0.0
        sentiment_accuracy = sentiment_accepted / total_feedback if total_feedback > 0 else 0.0
        priority_accuracy = priority_accepted / total_feedback if total_feedback > 0 else 0.0
        
        # Overall accuracy is the average of the three field accuracies
        overall_accuracy = (intent_accuracy + sentiment_accuracy + priority_accuracy) / 3.0
        
        return ClassificationAccuracy(
            intent_accuracy=round(intent_accuracy, 4),
            sentiment_accuracy=round(sentiment_accuracy, 4),
            priority_accuracy=round(priority_accuracy, 4),
            overall_accuracy=round(overall_accuracy, 4),
            intent_accepted=intent_accepted,
            intent_corrected=intent_corrected,
            sentiment_accepted=sentiment_accepted,
            sentiment_corrected=sentiment_corrected,
            priority_accepted=priority_accepted,
            priority_corrected=priority_corrected,
            total_feedback=total_feedback
        )
    except Exception:
        logger.exception("GET_CLASSIFICATION_ACCURACY_FAILED")
        raise internal_error("GET_CLASSIFICATION_ACCURACY_FAILED", "Could not retrieve accuracy metrics.")
