from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional, List
from uuid import UUID
from sqlmodel import select, func
from sqlmodel import Session
from app.db.base import get_session
from app.db.models.ticket import Ticket, TicketClassification
from app.schemas.ticket import TicketCreate, TicketOut, TicketListOut, ClassificationOut
from app.nlp.pipeline import nlp
from app.services.priority_rules import choose_priority
from datetime import datetime

router = APIRouter(prefix="/tickets", tags=["tickets"])

@router.post("", response_model=TicketOut, status_code=201)
def create_ticket(payload: TicketCreate, session: Session = Depends(get_session)) -> TicketOut:
    ticket = Ticket(
        subject=payload.subject,
        body=payload.body,
        channel=payload.channel,
        customer_id=payload.customer_id,
        language=payload.language,
    )
    session.add(ticket)
    session.commit()
    session.refresh(ticket)

    # classify-on-create (optional but nice)
    intent, intent_conf, sentiment, sentiment_conf, low_conf = nlp.classify_text(ticket.body)
    priority = choose_priority(intent, sentiment, low_conf, ticket.body)
    classification = TicketClassification(
        ticket_id=ticket.id,
        intent=intent,
        sentiment=sentiment,
        priority=priority,
        confidence=float(min(intent_conf, sentiment_conf)),
        low_confidence=low_conf,
        source="model",
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
        ),
    )

@router.get("", response_model=TicketListOut)
def list_tickets(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    intent: Optional[List[str]] = Query(default=None),
    sentiment: Optional[List[str]] = Query(default=None),
    priority: Optional[List[str]] = Query(default=None),
    session: Session = Depends(get_session),
) -> TicketListOut:
    q = select(Ticket)
    # minimal filter demo: join last classification via subquery or skip for Phase 1
    total = session.exec(select(func.count()).select_from(Ticket)).one()

    items = session.exec(q.offset((page - 1) * page_size).limit(page_size)).all()
    # For Phase 1, fetch latest classification per ticket if exists
    result = []
    for t in items:
        cl = session.exec(
            select(TicketClassification)
            .where(TicketClassification.ticket_id == t.id)
            .order_by(TicketClassification.created_at.desc())
            .limit(1)
        ).first()
        result.append(
            TicketOut(
                id=t.id, subject=t.subject, body=t.body, channel=t.channel,
                customer_id=t.customer_id, language=t.language,
                created_at=t.created_at, updated_at=t.updated_at,
                classification=ClassificationOut(
                    intent=cl.intent, sentiment=cl.sentiment,
                    priority=cl.priority, confidence=cl.confidence,
                    low_confidence=cl.low_confidence,
                ) if cl else None
            )
        )
    return TicketListOut(items=result, page=page, page_size=page_size, total=total)

@router.get("/{ticket_id}", response_model=TicketOut)
def get_ticket(ticket_id: UUID, session: Session = Depends(get_session)) -> TicketOut:
    t = session.get(Ticket, ticket_id)
    if not t:
        raise HTTPException(status_code=404, detail="Ticket not found")
    cl = session.exec(
        select(TicketClassification)
        .where(TicketClassification.ticket_id == t.id)
        .order_by(TicketClassification.created_at.desc())
        .limit(1)
    ).first()
    return TicketOut(
        id=t.id, subject=t.subject, body=t.body, channel=t.channel,
        customer_id=t.customer_id, language=t.language,
        created_at=t.created_at, updated_at=t.updated_at,
        classification=ClassificationOut(
            intent=cl.intent, sentiment=cl.sentiment,
            priority=cl.priority, confidence=cl.confidence,
            low_confidence=cl.low_confidence,
        ) if cl else None
    )
