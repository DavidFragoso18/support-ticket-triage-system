"""
Ticket Resolution database model.

Links resolved tickets to their resolution content.
This is different from Resolution (templates) - these are actual resolutions
applied to specific tickets.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class TicketResolution(SQLModel, table=True):
    """Actual resolution applied to a ticket."""

    __tablename__ = "ticket_resolutions"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    ticket_id: UUID = Field(foreign_key="tickets.id", index=True)

    # Resolution content
    summary: str = Field(max_length=500)
    details: str

    # Optional reference to template used
    template_id: Optional[UUID] = Field(default=None, foreign_key="resolutions.id")

    # Agent who applied the resolution
    agent_id: Optional[str] = Field(default=None, max_length=100)

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
