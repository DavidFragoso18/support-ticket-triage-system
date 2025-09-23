from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from app.db.base import get_session
from app.db.models.resolutions import Resolution

router = APIRouter(prefix="/resolutions", tags=["resolutions"])

class ResolutionOut(BaseModel):
    id: UUID
    ticket_id: UUID
    summary: str
    details: str
    created_at: str

@router.get("", response_model=list[ResolutionOut])
def list_resolutions(ticket_id: Optional[UUID] = None, session: Session = Depends(get_session)):
    q = select(Resolution).order_by(Resolution.created_at.desc())
    if ticket_id:
        q = q.where(Resolution.ticket_id == ticket_id)
    rows = session.exec(q).all()
    return [
        ResolutionOut(
            id=r.id,
            ticket_id=r.ticket_id,
            summary=r.summary,
            details=r.details,
            created_at=r.created_at.isoformat(),
        )
        for r in rows
    ]
