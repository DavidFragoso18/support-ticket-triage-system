from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from pydantic import BaseModel
from app.db.base import get_session
from app.db.models.kb import KBArticle

router = APIRouter(prefix="/kb", tags=["kb"])

class KBOut(BaseModel):
    id: str
    title: str
    tags: str | None = None
    created_at: str

@router.get("", response_model=list[KBOut])
def list_kb(session: Session = Depends(get_session)) -> list[KBOut]:
    rows = session.exec(select(KBArticle).order_by(KBArticle.created_at.desc())).all()
    return [
        KBOut(id=str(r.id), title=r.title, tags=r.tags, created_at=r.created_at.isoformat())
        for r in rows
    ]
