from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlmodel import Session

from app.core.errors import internal_error, logger, not_found
from app.db.base import get_session
from app.db.models.kb import KBArticle
from app.db.models.resolutions import Resolution
from app.db.models.ticket import Ticket
from app.services.suggestions import suggest_for_text

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
                preview = item.body[:200] + ("..." if len(item.body) > 200 else "")
                out.append(SuggestionOut(
                    id=item.id,
                    type="kb_article",
                    title=item.title,
                    preview=preview,
                    score=round(score, 4)
                ))
            elif isinstance(item, Resolution):
                # Resolution template suggestion
                preview = item.body[:200] + ("..." if len(item.body) > 200 else "")
                out.append(SuggestionOut(
                    id=item.id,
                    type="resolution_template",
                    title=item.title,
                    preview=preview,
                    score=round(score, 4),
                    ticket_id=None  # Resolution templates aren't linked to specific tickets
                ))
        
        return out
    except Exception:
        logger.exception("GET_SUGGESTIONS_FAILED")
        raise internal_error("GET_SUGGESTIONS_FAILED", "Could not compute suggestions.")
