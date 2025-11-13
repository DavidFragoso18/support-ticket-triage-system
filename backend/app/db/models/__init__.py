"""
Database models package.

This package contains SQLModel table definitions for the application.
"""

from .ticket import Ticket, TicketClassification
from .kb import KBArticle
from .resolutions import Resolution
from .feedback import ClassificationFeedback
from .ticket_resolution import TicketResolution
from .ai_responses import AIResponse
from .analytics import AgentActivity, SuggestionFeedback

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
