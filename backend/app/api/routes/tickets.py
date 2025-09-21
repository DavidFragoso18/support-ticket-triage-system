from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional, List
from uuid import UUID
from sqlmodel import select, func, Session
from app.db.base import get_session
from app.db.models.ticket import Ticket, TicketClassification
from app.schemas.ticket import TicketCreate, TicketOut, TicketListOut, ClassificationOut
from app.nlp.pipeline import nlp
from app.services.priority_rules import choose_priority
from app.core.errors import internal_error, not_found, logger

router = APIRouter(prefix="/tickets", tags=["tickets"])

@router.post("", response_model=TicketOut, status_code=201)
def create_ticket(payload: TicketCreate, session: Session = Depends(get_session)) -> TicketOut:
    try:
        # Use a transaction so we don’t leave half-written rows
        with session.begin():
            ticket = Ticket(
                subject=payload.subject,
                body=payload.body,
                channel=payload.channel,
                customer_id=payload.customer_id,
                language=payload.language,
            )
            session.add(ticket)
            session.flush()  # ensure ticket.id is available

            # NLP can fail; we catch and turn into clean 500
            try:
                intent, intent_conf, sentiment, sentiment_conf, low_conf = nlp.classify_text(ticket.body)
                priority = choose_priority(intent, sentiment, low_conf, ticket.body)
            except Exception:
                logger.exception("CLASSIFY_ON_CREATE_FAILED")
                # Re-raise as clean 500; transaction will rollback
                raise internal_error("CLASSIFY_ON_CREATE_FAILED", "Could not classify ticket.")

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

        # Build response outside the transaction
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
    except HTTPException:
        # We already built the proper error payload
        raise
    except Exception:
        logger.exception("CREATE_TICKET_FAILED")
        raise internal_error("CREATE_TICKET_FAILED", "Could not create ticket.")

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
        q = select(Ticket).order_by(Ticket.created_at.desc())
        total = session.exec(select(func.count()).select_from(Ticket)).one()
        items = session.exec(q.offset((page - 1) * page_size).limit(page_size)).all()

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
    except Exception:
        logger.exception("LIST_TICKETS_FAILED")
        raise internal_error("LIST_TICKETS_FAILED", "Could not list tickets.")

@router.get("/{ticket_id}", response_model=TicketOut)
def get_ticket(ticket_id: UUID, session: Session = Depends(get_session)) -> TicketOut:
    try:
        t = session.get(Ticket, ticket_id)
        if not t:
            raise not_found("TICKET_NOT_FOUND", "Ticket not found.")
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
    except HTTPException:
        raise
    except Exception:
        logger.exception("GET_TICKET_FAILED")
        raise internal_error("GET_TICKET_FAILED", "Could not fetch ticket.")
