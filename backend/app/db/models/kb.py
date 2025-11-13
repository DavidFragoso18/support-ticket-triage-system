"""
Knowledge Base database models.

Defines SQLModel tables for knowledge base articles.
"""

from sqlmodel import SQLModel, Field, Column
from typing import Optional
from datetime import datetime
from uuid import UUID, uuid4
from pgvector.sqlalchemy import Vector


class KBArticle(SQLModel, table=True):
    """Knowledge base article model with vector embeddings."""

    __tablename__ = "kb_articles"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    title: str = Field(max_length=200, index=True)
    body: str
    category: str = Field(max_length=100, index=True)
    tags: Optional[str] = Field(default=None)  # Comma-separated tags

    # Vector embedding for semantic search (384 dimensions for all-MiniLM-L6-v2)
    embedding: Optional[list] = Field(default=None, sa_column=Column(Vector(384)))

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
