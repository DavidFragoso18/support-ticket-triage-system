import numpy as np
from typing import List, Tuple, Union
from sqlmodel import Session, select
from app.db.models.kb import KBArticle
from app.db.models.resolutions import Resolution
from app.db.models.ticket import Ticket
from app.services.serialize import from_bytes
from app.nlp.embeddings import emb

def cosine(a: np.ndarray, b: np.ndarray) -> float:
    # embeddings are normalized, but keep generic
    denom = (np.linalg.norm(a) * np.linalg.norm(b))
    if denom == 0:
        return 0.0
    return float(np.dot(a, b) / denom)

def suggest_for_text(session: Session, text: str, top_k: int = 5) -> List[Tuple[Union[KBArticle, Tuple[Ticket, Resolution]], float]]:
    """
    Find relevant KB articles and past resolutions for a ticket.
    Returns a combined list of suggestions sorted by relevance.
    """
    # Encode ticket text
    q_vec = emb.encode_text(text)

    # Load all KB articles
    kb_articles = session.exec(select(KBArticle)).all()
    scored_kb = []
    for art in kb_articles:
        if art.embedding is None:
            continue
        vec = from_bytes(art.embedding)
        score = cosine(q_vec, vec)
        scored_kb.append((art, score))

    # For Phase 2: Also check resolved tickets (simplified - no embeddings yet)
    # We'll match on keywords for now, full semantic search in Phase 4
    resolutions = session.exec(
        select(Resolution, Ticket)
        .join(Ticket, Resolution.ticket_id == Ticket.id)
        .limit(20)  # Limit to recent resolutions
    ).all()
    
    scored_resolutions = []
    for resolution, ticket in resolutions:
        # Simple keyword matching score (0-1)
        text_lower = text.lower()
        ticket_text = f"{ticket.subject} {ticket.body}".lower()
        
        # Count common words as a simple relevance metric
        text_words = set(text_lower.split())
        ticket_words = set(ticket_text.split())
        if len(text_words) > 0:
            common = len(text_words & ticket_words)
            score = min(common / len(text_words), 1.0) * 0.7  # Cap at 0.7 for keyword matches
            if score > 0.1:  # Only include if somewhat relevant
                scored_resolutions.append(((ticket, resolution), score))

    # Combine and sort by score
    all_suggestions = scored_kb + scored_resolutions
    all_suggestions.sort(key=lambda x: x[1], reverse=True)
    
    return all_suggestions[:top_k]
