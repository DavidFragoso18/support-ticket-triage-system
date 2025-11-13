"""
AI-generated response database models.

Defines SQLModel tables for storing AI-generated responses.
"""

from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID, uuid4


class AIResponse(SQLModel, table=True):
    """Saved AI-generated response model."""

    __tablename__ = "ai_responses"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    ticket_id: UUID = Field(foreign_key="tickets.id", index=True)
    response_text: str
    tone: str = Field(max_length=50)  # professional, friendly, technical, empathetic
    context_used: int = Field(default=0)  # Number of RAG sources used
    model: str = Field(max_length=100)  # e.g., "llama3.2:latest"
    agent_id: Optional[str] = Field(default=None, max_length=100, index=True)
    was_edited: bool = Field(default=False)  # Track if agent edited the response
    was_sent: bool = Field(default=False)  # Track if response was sent to customer
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
