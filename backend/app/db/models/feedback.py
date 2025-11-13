"""
Feedback database models.

Defines SQLModel tables for classification feedback (user corrections).
"""

from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID, uuid4


class ClassificationFeedback(SQLModel, table=True):
    """
    Feedback on ticket classifications.

    Stores user corrections/confirmations of ML predictions to improve the model.
    """

    __tablename__ = "classification_feedback"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    classification_id: UUID = Field(foreign_key="ticket_classifications.id", index=True)

    # Action taken: "accepted", "rejected", or "corrected"
    action: str = Field(max_length=50)

    # If action="corrected", store the corrected values
    corrected_intent: Optional[str] = Field(default=None, max_length=50)
    corrected_sentiment: Optional[str] = Field(default=None, max_length=50)
    corrected_priority: Optional[str] = Field(default=None, max_length=50)

    # Optional notes from the agent
    notes: Optional[str] = Field(default=None, max_length=500)

    # Track which agent provided feedback (if available)
    agent_id: Optional[str] = Field(default=None, max_length=100, index=True)

    created_at: datetime = Field(default_factory=datetime.utcnow)
