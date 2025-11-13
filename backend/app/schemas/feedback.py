from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class FeedbackCreate(BaseModel):
    classification_id: UUID
    action: str  # accepted, rejected, corrected
    corrected_intent: Optional[str] = None
    corrected_sentiment: Optional[str] = None
    corrected_priority: Optional[str] = None
    agent_id: Optional[str] = None
    notes: Optional[str] = None


class FeedbackOut(BaseModel):
    id: UUID
    classification_id: UUID
    action: str
    corrected_intent: Optional[str] = None
    corrected_sentiment: Optional[str] = None
    corrected_priority: Optional[str] = None
    agent_id: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime
