import numpy as np
from typing import List, Tuple
from sqlmodel import Session, select
from app.db.models.kb import KBArticle
from app.services.serialize import from_bytes
from app.nlp.embeddings import emb

def cosine(a: np.ndarray, b: np.ndarray) -> float:
    # embeddings are normalized, but keep generic
    denom = (np.linalg.norm(a) * np.linalg.norm(b))
    if denom == 0:
        return 0.0
    return float(np.dot(a, b) / denom)

def suggest_for_text(session: Session, text: str, top_k: int = 2) -> List[Tuple[KBArticle, float]]:
    # Encode ticket text
    q_vec = emb.encode_text(text)

    # Load all KB articles (small set in Phase 2)
    rows = session.exec(select(KBArticle)).all()
    scored = []
    for art in rows:
        if art.embedding is None:
            continue
        vec = from_bytes(art.embedding)
        score = cosine(q_vec, vec)
        scored.append((art, score))

    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:top_k]
