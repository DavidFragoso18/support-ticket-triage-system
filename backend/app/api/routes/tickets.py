from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from typing import Optional, List
from uuid import UUID
from sqlmodel import select, func, Session
from sqlalchemy import and_
from app.db.base import get_session
from app.db.models.ticket import Ticket, TicketClassification
from app.schemas.ticket import TicketCreate, TicketOut, TicketListOut, ClassificationOut
from app.nlp.pipeline import nlp
from app.nlp.embeddings import emb
from app.services.priority_rules import choose_priority
from app.services.websocket_manager import manager
from app.core.errors import internal_error, not_found, logger

router = APIRouter(prefix="/tickets", tags=["tickets"])

@router.post("", status_code=201, response_model=TicketOut)
async def create_ticket(
    ticket_data: TicketCreate,
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_session),
) -> TicketOut:
    try:
        # Run NLP classification
        text = ticket_data.subject + " " + ticket_data.body
        intent, intent_score, sentiment, sentiment_score, low = nlp.classify_text(text)
        
        # Create the ticket without embedding first
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
        
        # Generate and update embedding using raw SQL (pgvector requires casting)
        embedding_vector = emb.encode_to_list(text)
        embedding_str = str(embedding_vector)
        
        from sqlalchemy import text as sql_text
        update_query = sql_text("""
            UPDATE tickets 
            SET embedding = CAST(:embedding AS vector)
            WHERE id = CAST(:ticket_id AS uuid)
        """)
        session.execute(update_query, {"embedding": embedding_str, "ticket_id": str(ticket.id)})
        session.commit()
        priority = choose_priority(intent, sentiment, text)

        
        # Save classification
        classification = TicketClassification(
        ticket_id=ticket.id,
        intent=intent,
        sentiment=sentiment,
        priority=priority,
        confidence=intent_score,  # or min(intent_score, sentiment_score)
        low_confidence=low
        )
        
        session.add(classification)
        session.commit()
        session.refresh(classification)
        
        ticket_out = TicketOut(
            id=ticket.id,
            subject=ticket.subject,
            body=ticket.body,
            channel=ticket.channel,
            customer_id=ticket.customer_id,
            language=ticket.language,
            created_at=ticket.created_at,
            updated_at=ticket.updated_at,
            classification=ClassificationOut(
                id=classification.id,
                intent=classification.intent,
                sentiment=classification.sentiment,
                priority=classification.priority,
                confidence=classification.confidence,
                low_confidence=classification.low_confidence,
            )
        )
        
        # Broadcast new ticket to all connected clients
        background_tasks.add_task(
            manager.broadcast_ticket_update,
            "ticket_created",
            ticket_out.model_dump()
        )
        
        # Send high-priority alert if urgent
        if priority in ["urgent", "high"]:
            background_tasks.add_task(
                manager.broadcast_high_priority_alert,
                ticket_out.model_dump()
            )
        
        return ticket_out
        
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
                    id=classification.id,
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
                            id=cl.id,
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


@router.get("/{ticket_id}/similar")
def get_similar_tickets(
    ticket_id: UUID,
    limit: int = Query(default=5, ge=1, le=20),
    session: Session = Depends(get_session),
):
    """
    Find similar tickets using vector similarity search.
    Returns top N most similar tickets (excluding the current ticket).
    """
    try:
        from sqlalchemy import text
        
        # First check if ticket exists and has an embedding using raw SQL
        check_query = text("""
            SELECT embedding FROM tickets WHERE id = CAST(:ticket_id AS uuid)
        """)
        
        result = session.execute(check_query, {"ticket_id": str(ticket_id)})
        row = result.first()
        
        if not row:
            raise not_found("TICKET_NOT_FOUND", f"Ticket {ticket_id} not found")
        
        if not row.embedding:
            return {"similar_tickets": []}
        
        # Get the embedding as string representation
        query_embedding = str(row.embedding)
        
        # Build vector similarity query
        # Using raw SQL for pgvector cosine similarity operator
        query = text("""
            SELECT 
                id,
                subject,
                body,
                created_at,
                (1 - (embedding <=> CAST(:query_embedding AS vector))) as similarity
            FROM tickets
            WHERE id != CAST(:ticket_id AS uuid)
                AND embedding IS NOT NULL
                AND (1 - (embedding <=> CAST(:query_embedding AS vector))) > 0.5
            ORDER BY embedding <=> CAST(:query_embedding AS vector)
            LIMIT :limit
        """)
        
        result = session.execute(
            query,
            {
                "query_embedding": query_embedding,
                "ticket_id": str(ticket_id),
                "limit": limit
            }
        )
        
        similar_tickets = []
        for row in result:
            similar_tickets.append({
                "id": str(row.id),
                "subject": row.subject,
                "preview": row.body[:150] + "..." if len(row.body) > 150 else row.body,
                "created_at": row.created_at.isoformat(),
                "similarity": round(float(row.similarity), 4)
            })
        
        return {"similar_tickets": similar_tickets}
        
    except HTTPException:
        raise
    except Exception:
        logger.exception("GET_SIMILAR_TICKETS_FAILED")
        raise internal_error("GET_SIMILAR_TICKETS_FAILED", "Could not retrieve similar tickets.")
