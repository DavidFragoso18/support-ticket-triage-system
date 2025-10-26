from fastapi import APIRouter, Depends
from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from sqlmodel import Session, select
from app.db.base import get_session
from app.db.models.ticket import Ticket, TicketClassification
from app.db.models.kb import KBArticle
from app.db.models.resolutions import Resolution
from app.services.suggestions import suggest_for_text
from app.core.errors import internal_error, not_found, logger

router = APIRouter(prefix="/suggestions", tags=["suggestions"])

class SuggestionOut(BaseModel):
    id: UUID
    type: str  # "kb_article" or "past_resolution"
    title: str
    preview: str
    score: float
    ticket_id: Optional[UUID] = None  # For past resolutions

@router.get("/{ticket_id}", response_model=list[SuggestionOut])
def get_suggestions(ticket_id: UUID, session: Session = Depends(get_session)) -> list[SuggestionOut]:
    try:
        t = session.get(Ticket, ticket_id)
        if not t:
            raise not_found("TICKET_NOT_FOUND", "Ticket not found.")
        
        suggestions = suggest_for_text(session, t.body, top_k=5)
        out = []
        
        for item, score in suggestions:
            if isinstance(item, KBArticle):
                # KB Article suggestion
                preview = item.answer[:200] + ("..." if len(item.answer) > 200 else "")
                out.append(SuggestionOut(
                    id=item.id,
                    type="kb_article",
                    title=item.question,
                    preview=preview,
                    score=round(score, 4)
                ))
            else:
                # Past resolution suggestion (ticket, resolution tuple)
                ticket, resolution = item
                preview = resolution.summary[:200] + ("..." if len(resolution.summary) > 200 else "")
                out.append(SuggestionOut(
                    id=resolution.id,
                    type="past_resolution",
                    title=ticket.subject,
                    preview=preview,
                    score=round(score, 4),
                    ticket_id=ticket.id
                ))
        
        return out
    except Exception:
        logger.exception("GET_SUGGESTIONS_FAILED")
        raise internal_error("GET_SUGGESTIONS_FAILED", "Could not compute suggestions.")
