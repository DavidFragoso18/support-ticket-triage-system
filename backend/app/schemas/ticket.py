from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class ClassificationOut(BaseModel):
    id: UUID
    intent: str
    sentiment: str
    priority: str
    confidence: float
    low_confidence: bool

class TicketCreate(BaseModel):
    subject: str = Field(min_length=5, max_length=200)
    body: str
    channel: str = Field(default="web")
    customer_id: Optional[str] = None
    language: Optional[str] = None

class TicketOut(BaseModel):
    id: UUID
    subject: str
    body: str
    channel: str
    customer_id: Optional[str]
    language: Optional[str]
    created_at: datetime
    updated_at: datetime
    classification: Optional[ClassificationOut] = None

    intent: Optional[str] = None
    sentiment: Optional[str] = None
    priority: Optional[str] = None

class TicketListOut(BaseModel):
    items: List[TicketOut]
    page: int
    page_size: int
    total: int
