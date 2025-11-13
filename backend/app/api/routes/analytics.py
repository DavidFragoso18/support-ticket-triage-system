from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, func, select

from app.core.errors import internal_error, logger
from app.db.base import get_session
from app.db.models.feedback import ClassificationFeedback
from app.db.models.ticket import Ticket, TicketClassification
from app.schemas.analytics import (
    AnalyticsOverview,
    ClassificationAccuracy,
    IntentDistribution,
    PriorityDistribution,
    SentimentDistribution,
    TimeSeriesData,
)

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
            .where(TicketClassification.low_confidence)
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
        raise internal_error(
            "GET_INTENT_DISTRIBUTION_FAILED",
            "Could not retrieve intent distribution."
        )

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
        raise internal_error(
            "GET_SENTIMENT_DISTRIBUTION_FAILED",
            "Could not retrieve sentiment distribution."
        )

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
        raise internal_error(
            "GET_PRIORITY_DISTRIBUTION_FAILED",
            "Could not retrieve priority distribution."
        )

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
        raise internal_error(
            "GET_TICKETS_OVER_TIME_FAILED",
            "Could not retrieve time series data."
        )

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
        # Intent: accepted if action='accepted' OR corrected but intent not changed
        intent_accepted = sum(
            1 for f in all_feedback
            if f.action == "accepted"
            or (f.action == "corrected" and f.corrected_intent is None)
        )
        intent_corrected = sum(
            1 for f in all_feedback
            if f.action == "corrected" and f.corrected_intent is not None
        )
        
        # Sentiment: accepted if action='accepted' OR corrected but sentiment not changed
        sentiment_accepted = sum(
            1 for f in all_feedback
            if f.action == "accepted"
            or (f.action == "corrected" and f.corrected_sentiment is None)
        )
        sentiment_corrected = sum(
            1 for f in all_feedback
            if f.action == "corrected" and f.corrected_sentiment is not None
        )
        
        # Priority: accepted if action='accepted' OR corrected but priority not changed
        priority_accepted = sum(
            1 for f in all_feedback
            if f.action == "accepted"
            or (f.action == "corrected" and f.corrected_priority is None)
        )
        priority_corrected = sum(
            1 for f in all_feedback
            if f.action == "corrected" and f.corrected_priority is not None
        )
        
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
        raise internal_error(
            "GET_CLASSIFICATION_ACCURACY_FAILED",
            "Could not retrieve accuracy metrics."
        )


@router.get("/trends")
def get_trends(
    days: int = Query(default=7, ge=1, le=90),
    session: Session = Depends(get_session),
):
    """Get ticket trends over time"""
    try:
        from app.schemas.analytics import TrendData
        
        trends = []
        end_date = datetime.utcnow().date()
        
        for i in range(days):
            current_date = end_date - timedelta(days=i)
            next_date = current_date + timedelta(days=1)
            
            # Total tickets created on this day
            total_tickets = session.exec(
                select(func.count(Ticket.id))
                .where(Ticket.created_at >= current_date)
                .where(Ticket.created_at < next_date)
            ).one()
            
            # High priority tickets
            high_priority = session.exec(
                select(func.count(TicketClassification.id))
                .join(Ticket, TicketClassification.ticket_id == Ticket.id)
                .where(Ticket.created_at >= current_date)
                .where(Ticket.created_at < next_date)
                .where(TicketClassification.priority.in_(["urgent", "high", "P1", "P2"]))
            ).one()
            
            # Resolved tickets (with status)
            resolved = session.exec(
                select(func.count(Ticket.id))
                .where(Ticket.created_at >= current_date)
                .where(Ticket.created_at < next_date)
                .where(Ticket.status == "resolved")
            ).one()
            
            trends.append(TrendData(
                date=current_date.isoformat(),
                total_tickets=total_tickets,
                high_priority=high_priority,
                resolved=resolved,
                avg_resolution_time=0.0  # TODO: Calculate when we track resolution times
            ))
        
        return {"trends": trends[::-1]}  # Reverse to get chronological order
        
    except Exception:
        logger.exception("GET_TRENDS_FAILED")
        raise internal_error(
            "GET_TRENDS_FAILED",
            "Could not retrieve trend data."
        )


@router.get("/agents/performance")
def get_agent_performance(
    days: int = Query(default=7, ge=1, le=90),
    session: Session = Depends(get_session),
):
    """Get agent performance metrics"""
    try:
        from app.db.models.analytics import AgentActivity, SuggestionFeedback
        from app.schemas.analytics import AgentPerformance
        
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # Get all agents who have been active
        agents = session.exec(
            select(AgentActivity.agent_id)
            .where(AgentActivity.timestamp >= start_date)
            .distinct()
        ).all()
        
        performance_data = []
        
        for agent_id in agents:
            # Tickets claimed
            tickets_claimed = session.exec(
                select(func.count(AgentActivity.id))
                .where(AgentActivity.agent_id == agent_id)
                .where(AgentActivity.action == "claimed")
                .where(AgentActivity.timestamp >= start_date)
            ).one()
            
            # Tickets resolved
            tickets_resolved = session.exec(
                select(func.count(AgentActivity.id))
                .where(AgentActivity.agent_id == agent_id)
                .where(AgentActivity.action == "resolved")
                .where(AgentActivity.timestamp >= start_date)
            ).one()
            
            # Average resolution time
            avg_resolution_time = session.exec(
                select(func.avg(AgentActivity.duration_seconds))
                .where(AgentActivity.agent_id == agent_id)
                .where(AgentActivity.action == "resolved")
                .where(AgentActivity.timestamp >= start_date)
            ).one() or 0.0
            
            # Total active time
            total_active_time = session.exec(
                select(func.sum(AgentActivity.duration_seconds))
                .where(AgentActivity.agent_id == agent_id)
                .where(AgentActivity.timestamp >= start_date)
            ).one() or 0.0
            
            # Feedback given
            feedback_given = session.exec(
                select(func.count(SuggestionFeedback.id))
                .where(SuggestionFeedback.agent_id == agent_id)
                .where(SuggestionFeedback.timestamp >= start_date)
            ).one()
            
            # Average feedback rating
            avg_rating = session.exec(
                select(func.avg(SuggestionFeedback.rating))
                .where(SuggestionFeedback.agent_id == agent_id)
                .where(SuggestionFeedback.timestamp >= start_date)
            ).one() or 0.0
            
            performance_data.append(AgentPerformance(
                agent_id=agent_id,
                tickets_claimed=tickets_claimed,
                tickets_resolved=tickets_resolved,
                avg_resolution_time_seconds=float(avg_resolution_time),
                total_active_time_seconds=float(total_active_time),
                feedback_given=feedback_given,
                avg_feedback_rating=float(avg_rating)
            ))
        
        # Sort by tickets resolved (descending)
        performance_data.sort(key=lambda x: x.tickets_resolved, reverse=True)
        
        return {"agents": performance_data}
        
    except Exception:
        logger.exception("GET_AGENT_PERFORMANCE_FAILED")
        raise internal_error(
            "GET_AGENT_PERFORMANCE_FAILED",
            "Could not retrieve agent performance data."
        )


@router.get("/dashboard")
def get_dashboard(
    days: int = Query(default=7, ge=1, le=90),
    session: Session = Depends(get_session),
):
    """Get complete analytics dashboard data"""
    try:
        from app.schemas.analytics import AnalyticsDashboard
        
        # Get all the data components
        overview = get_overview(session)
        intent_dist = get_intent_distribution(session)
        sentiment_dist = get_sentiment_distribution(session)
        priority_dist = get_priority_distribution(session)
        trends_data = get_trends(days, session)
        agents_data = get_agent_performance(days, session)
        accuracy = get_classification_accuracy(session)
        
        return AnalyticsDashboard(
            overview=overview,
            intent_distribution=intent_dist,
            sentiment_distribution=sentiment_dist,
            priority_distribution=priority_dist,
            trends=trends_data["trends"],
            top_agents=agents_data["agents"][:10],  # Top 10 agents
            model_accuracy=accuracy,
            total_feedback=accuracy.total_feedback
        )
        
    except Exception:
        logger.exception("GET_DASHBOARD_FAILED")
        raise internal_error(
            "GET_DASHBOARD_FAILED",
            "Could not retrieve dashboard data."
        )
