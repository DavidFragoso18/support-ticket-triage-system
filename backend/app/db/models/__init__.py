"""
Database models package.

This package contains SQLModel table definitions for the application.
"""

from .ai_responses import AIResponse
from .analytics import AgentActivity, SuggestionFeedback
from .feedback import ClassificationFeedback
from .kb import KBArticle
from .resolutions import Resolution
from .ticket import Ticket, TicketClassification
from .ticket_resolution import TicketResolution

__all__ = [
    "Ticket",
    "TicketClassification",
    "KBArticle",
    "Resolution",
    "ClassificationFeedback",
    "TicketResolution",
    "AIResponse",
    "AgentActivity",
    "SuggestionFeedback",
]
