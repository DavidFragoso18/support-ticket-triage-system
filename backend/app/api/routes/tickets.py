from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional, List
from uuid import UUID
from sqlmodel import select, func, Session
from sqlalchemy import and_
from app.db.base import get_session
from app.db.models.ticket import Ticket, TicketClassification
from app.schemas.ticket import TicketCreate, TicketOut, TicketListOut, ClassificationOut
from app.nlp.pipeline import nlp
from app.services.priority_rules import choose_priority
from app.core.errors import internal_error, not_found, logger

router = APIRouter(prefix="/tickets", tags=["tickets"])

@router.post("", status_code=201, response_model=TicketOut)
def create_ticket(
    ticket_data: TicketCreate,
    session: Session = Depends(get_session),
) -> TicketOut:
    try:
        # Create the ticket
        ticket = Ticket(
            subject=ticket_data.subject,
            body=ticket_data.body,
            channel=ticket_data.channel,
            customer_id=ticket_data.customer_id,
            language=ticket_data.language or "en"
        )
        
        session.add(ticket)
        session.commit()
        session.refresh(ticket)
        
        # Run NLP classification
        text = ticket_data.subject + " " + ticket_data.body
        intent, intent_score, sentiment, sentiment_score, low_conf = nlp.classify_text(text)
        priority = choose_priority(intent, sentiment, low_conf, text)

        
        # Save classification
        classification = TicketClassification(
        ticket_id=ticket.id,
        intent=intent,
        sentiment=sentiment,
        priority=priority,
        confidence=intent_score,  # or min(intent_score, sentiment_score)
        low_confidence=low_conf
        )
        
        session.add(classification)
        session.commit()
        session.refresh(classification)
        
        return TicketOut(
            id=ticket.id,
            subject=ticket.subject,
            body=ticket.body,
            channel=ticket.channel,
            customer_id=ticket.customer_id,
            language=ticket.language,
            created_at=ticket.created_at,
            updated_at=ticket.updated_at,
            classification=ClassificationOut(
                intent=classification.intent,
                sentiment=classification.sentiment,
                priority=classification.priority,
                confidence=classification.confidence,
                low_confidence=classification.low_confidence,
            )
        )
        
    except Exception:
        logger.exception("CREATE_TICKET_FAILED")
        raise internal_error("CREATE_TICKET_FAILED", "Could not create ticket.")
# ... keep create_ticket and get_ticket as you have them ...
@router.get("/{ticket_id}", response_model=TicketOut)
def get_ticket(
    ticket_id: UUID,
    session: Session = Depends(get_session),
) -> TicketOut:
    try:
        ticket = session.get(Ticket, ticket_id)
        if not ticket:
            raise not_found("TICKET_NOT_FOUND", f"Ticket {ticket_id} not found.")
        
        # Get latest classification
        classification = session.exec(
            select(TicketClassification)
            .where(TicketClassification.ticket_id == ticket_id)
            .order_by(TicketClassification.created_at.desc())
        ).first()
        
        return TicketOut(
            id=ticket.id,
            subject=ticket.subject,
            body=ticket.body,
            channel=ticket.channel,
            customer_id=ticket.customer_id,
            language=ticket.language,
            created_at=ticket.created_at,
            updated_at=ticket.updated_at,
            classification=(
                ClassificationOut(
                    intent=classification.intent,
                    sentiment=classification.sentiment,
                    priority=classification.priority,
                    confidence=classification.confidence,
                    low_confidence=classification.low_confidence,
                ) if classification else None
            )
        )
        
    except HTTPException:
        raise
    except Exception:
        logger.exception("GET_TICKET_FAILED")
        raise internal_error("GET_TICKET_FAILED", "Could not retrieve ticket.")
    
@router.get("", response_model=TicketListOut)
def list_tickets(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    intent: Optional[List[str]] = Query(default=None),
    sentiment: Optional[List[str]] = Query(default=None),
    priority: Optional[List[str]] = Query(default=None),
    session: Session = Depends(get_session),
) -> TicketListOut:
    try:
        # Subquery: latest classification timestamp per ticket
        latest_ts_sq = (
            select(
                TicketClassification.ticket_id,
                func.max(TicketClassification.created_at).label("max_created_at"),
            )
            .group_by(TicketClassification.ticket_id)
            .subquery()
        )

        # Join tickets ↔ latest classification (C alias) via the subquery
        C = TicketClassification
        T = Ticket
        base = (
            select(T, C)
            .join(latest_ts_sq, latest_ts_sq.c.ticket_id == T.id, isouter=True)
            .join(
                C,
                and_(
                    C.ticket_id == latest_ts_sq.c.ticket_id,
                    C.created_at == latest_ts_sq.c.max_created_at,
                ),
                isouter=True,
            )
        )

        # Apply filters at SQL level (on latest classification)
        conditions = []
        if intent:
            conditions.append(C.intent.in_(intent))
        if sentiment:
            conditions.append(C.sentiment.in_(sentiment))
        if priority:
            conditions.append(C.priority.in_(priority))
        if conditions:
            base = base.where(and_(*conditions))

        # Total count AFTER filters
        total = session.exec(
            select(func.count()).select_from(base.subquery())
        ).one()

        # Page slice ordered by newest ticket
        page_q = base.order_by(T.created_at.desc()).offset((page - 1) * page_size).limit(page_size)
        rows = session.exec(page_q).all()

        # Build response
        items: List[TicketOut] = []
        for t, cl in rows:
            items.append(
                TicketOut(
                    id=t.id,
                    subject=t.subject,
                    body=t.body,
                    channel=t.channel,
                    customer_id=t.customer_id,
                    language=t.language,
                    created_at=t.created_at,
                    updated_at=t.updated_at,
                    classification=(
                        ClassificationOut(
                            intent=cl.intent,
                            sentiment=cl.sentiment,
                            priority=cl.priority,
                            confidence=cl.confidence,
                            low_confidence=cl.low_confidence,
                        ) if cl else None
                    ),
                )
            )

        return TicketListOut(items=items, page=page, page_size=page_size, total=total)
    except Exception:
        logger.exception("LIST_TICKETS_SQL_FAILED")
        raise internal_error("LIST_TICKETS_SQL_FAILED", "Could not list tickets.")
