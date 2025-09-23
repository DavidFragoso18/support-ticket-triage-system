from fastapi import APIRouter, Depends
from pydantic import BaseModel
from uuid import UUID
from sqlmodel import Session, select
from app.db.base import get_session
from app.db.models.ticket import Ticket, TicketClassification
from app.db.models.kb import KBArticle
from app.services.suggestions import suggest_for_text
from app.core.errors import internal_error, not_found, logger

router = APIRouter(prefix="/suggestions", tags=["suggestions"])

class SuggestionOut(BaseModel):
    id: UUID
    title: str
    preview: str
    score: float

@router.get("/{ticket_id}", response_model=list[SuggestionOut])
def get_suggestions(ticket_id: UUID, session: Session = Depends(get_session)) -> list[SuggestionOut]:
    try:
        t = session.get(Ticket, ticket_id)
        if not t:
            raise not_found("TICKET_NOT_FOUND", "Ticket not found.")
        pairs = suggest_for_text(session, t.body, top_k=2)
        out = []
        for art, score in pairs:
            preview = art.content[:200] + ("..." if len(art.content) > 200 else "")
            out.append(SuggestionOut(id=art.id, title=art.title, preview=preview, score=round(score, 4)))
        return out
    except Exception:
        logger.exception("GET_SUGGESTIONS_FAILED")
        raise internal_error("GET_SUGGESTIONS_FAILED", "Could not compute suggestions.")
