from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, select

from app.core.errors import not_found
from app.db.base import get_session
from app.db.models.kb import KBArticle
from app.db.models.resolutions import Resolution
from app.db.models.ticket_resolution import TicketResolution

router = APIRouter(prefix="/resolutions", tags=["resolutions"])


class TicketResolutionOut(BaseModel):
    id: UUID
    ticket_id: UUID
    summary: str
    details: str
    created_at: str


class ApplySuggestionRequest(BaseModel):
    ticket_id: UUID
    suggestion_id: UUID
    suggestion_type: str  # "kb_article" or "resolution_template"
    agent_id: Optional[str] = None


@router.get("", response_model=list[TicketResolutionOut])
def list_ticket_resolutions(
    ticket_id: Optional[UUID] = None, session: Session = Depends(get_session)
):
    """
    List actual resolutions applied to tickets. Optionally filter by ticket_id.
    """
    q = select(TicketResolution).order_by(TicketResolution.created_at.desc())
    if ticket_id:
        q = q.where(TicketResolution.ticket_id == ticket_id)
    rows = session.exec(q).all()
    return [
        TicketResolutionOut(
            id=r.id,
            ticket_id=r.ticket_id,
            summary=r.summary,
            details=r.details,
            created_at=r.created_at.isoformat(),
        )
        for r in rows
    ]


@router.post("/apply", response_model=TicketResolutionOut, status_code=201)
def apply_suggestion(req: ApplySuggestionRequest, session: Session = Depends(get_session)):
    """
    Apply a suggestion (KB article or resolution template) as a resolution for a ticket.
    """
    # Fetch the suggestion content
    if req.suggestion_type == "kb_article":
        article = session.get(KBArticle, req.suggestion_id)
        if not article:
            raise not_found("KB_ARTICLE_NOT_FOUND", "KB article not found")
        summary = article.title
        details = article.body
        template_id = None
    elif req.suggestion_type == "resolution_template":
        template = session.get(Resolution, req.suggestion_id)
        if not template:
            raise not_found("TEMPLATE_NOT_FOUND", "Resolution template not found")
        summary = template.title
        details = template.body
        template_id = template.id
    else:
        raise HTTPException(status_code=400, detail="Invalid suggestion_type")

    # Create the ticket resolution
    ticket_resolution = TicketResolution(
        ticket_id=req.ticket_id,
        summary=summary,
        details=details,
        template_id=template_id,
        agent_id=req.agent_id,
    )

    session.add(ticket_resolution)
    session.commit()
    session.refresh(ticket_resolution)

    return TicketResolutionOut(
        id=ticket_resolution.id,
        ticket_id=ticket_resolution.ticket_id,
        summary=ticket_resolution.summary,
        details=ticket_resolution.details,
        created_at=ticket_resolution.created_at.isoformat(),
    )
