"""
Analytics database models for tracking agent activities and feedback.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class AgentActivity(SQLModel, table=True):
    """Track agent actions for performance analytics"""

    __tablename__ = "agent_activities"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    agent_id: str = Field(max_length=100, index=True)
    ticket_id: UUID = Field(foreign_key="tickets.id", index=True)
    action: str = Field(max_length=50, index=True)  # claimed, released, resolved, escalated
    timestamp: datetime = Field(default_factory=datetime.utcnow, index=True)
    duration_seconds: Optional[int] = None  # Time spent on ticket
    extra_data: Optional[str] = None  # JSON string for additional data


class SuggestionFeedback(SQLModel, table=True):
    """Track feedback on AI suggestions for model improvement"""

    __tablename__ = "suggestion_feedback"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    ticket_id: UUID = Field(foreign_key="tickets.id", index=True)
    suggestion_type: str = Field(max_length=50, index=True)  # resolution, response, priority
    suggestion_id: Optional[UUID] = None  # Link to specific suggestion if applicable
    agent_id: str = Field(max_length=100, index=True)
    rating: int = Field(ge=1, le=5)  # 1-5 star rating
    was_used: bool = Field(default=False)
    feedback_text: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow, index=True)
