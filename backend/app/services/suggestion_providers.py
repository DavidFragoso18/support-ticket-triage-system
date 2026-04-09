"""
Suggestion providers with inheritance and generator-based ranking.
Demonstrates OOP patterns for extensible suggestion systems.
"""
from abc import ABC, abstractmethod
from typing import Generator, List, Tuple

import numpy as np
from sqlmodel import Session, select

from app.db.models.kb import KBArticle
from app.db.models.resolutions import Resolution
from app.nlp.embeddings import emb
from app.services.serialize import from_bytes


class SuggestionProvider(ABC):
    """Abstract base class for suggestion providers."""

    def __init__(self, session: Session, query_vector: np.ndarray):
        self.session = session
        self.query_vector = query_vector

    @abstractmethod
    def get_candidates(self) -> List:
        """Fetch all candidate items from database."""
        pass

    @abstractmethod
    def extract_embedding(self, item) -> np.ndarray:
        """Extract embedding vector from item."""
        pass

    def cosine_similarity(self, vec: np.ndarray) -> float:
        """Calculate cosine similarity between query and candidate."""
        denom = np.linalg.norm(self.query_vector) * np.linalg.norm(vec)
        return float(np.dot(self.query_vector, vec) / denom) if denom != 0 else 0.0

    def ranked_suggestions(self, min_score: float = 0.0) -> Generator[Tuple, None, None]:
        """Generator yielding (item, score) pairs above threshold, sorted by score."""
        candidates = self.get_candidates()
        scored = []
        for item in candidates:
            vec = self.extract_embedding(item)
            if vec is not None:
                score = self.cosine_similarity(vec)
                if score >= min_score:
                    scored.append((item, score))
        scored.sort(key=lambda x: x[1], reverse=True)
        yield from scored


class KBArticleProvider(SuggestionProvider):
    """Provider for knowledge base article suggestions."""

    def get_candidates(self) -> List[KBArticle]:
        return list(self.session.exec(select(KBArticle)).all())

    def extract_embedding(self, item: KBArticle) -> np.ndarray:
        return from_bytes(item.embedding) if item.embedding else None
