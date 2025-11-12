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

def suggest_for_text(session: Session, text: str, top_k: int = 5) -> List[Tuple[Union[KBArticle, Resolution], float]]:
    """
    Find relevant KB articles and resolution templates for a ticket.
    Returns a combined list of suggestions sorted by relevance (score is cosine similarity).
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

    # Load all resolution templates
    resolutions = session.exec(select(Resolution)).all()
    scored_resolutions = []
    for res in resolutions:
        if res.embedding is None:
            continue
        vec = from_bytes(res.embedding)
        score = cosine(q_vec, vec)
        scored_resolutions.append((res, score))

    # Combine and sort by score
    all_suggestions = scored_kb + scored_resolutions
    all_suggestions.sort(key=lambda x: x[1], reverse=True)
    
    return all_suggestions[:top_k]
