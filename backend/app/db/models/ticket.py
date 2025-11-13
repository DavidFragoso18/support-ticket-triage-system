"""
Ticket database models.

Defines SQLModel tables for support tickets and their classifications.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel


class Ticket(SQLModel, table=True):
    """Support ticket model."""

    __tablename__ = "tickets"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    subject: str = Field(max_length=200, index=True)
    body: str
    channel: str = Field(default="web", max_length=50)
    customer_id: Optional[str] = Field(default=None, max_length=100, index=True)
    language: Optional[str] = Field(default="en", max_length=10)
    status: str = Field(
        default="open", max_length=50, index=True
    )  # open, in_progress, resolved, closed
    assigned_agent_id: Optional[str] = Field(default=None, max_length=100, index=True)
    # Note: embedding column exists in DB but not in model - handled via raw SQL
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to classification
    classification: Optional["TicketClassification"] = Relationship(back_populates="ticket")


class TicketClassification(SQLModel, table=True):
    """Ticket classification model for ML predictions."""

    __tablename__ = "ticket_classifications"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    ticket_id: UUID = Field(foreign_key="tickets.id", unique=True, index=True)
    intent: str = Field(max_length=50)
    sentiment: str = Field(max_length=50)
    priority: str = Field(max_length=50)
    confidence: float
    low_confidence: bool = Field(default=False)
    source: Optional[str] = Field(default="ai", max_length=50)  # "ai" or "human"
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship back to ticket
    ticket: Optional[Ticket] = Relationship(back_populates="classification")
