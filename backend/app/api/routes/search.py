"""
Semantic search routes using vector embeddings.

Provides similarity search across KB articles, resolutions, and tickets.
"""

from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, select, text
from typing import List
from app.db.base import get_session
from app.db.models.kb import KBArticle
from app.db.models.resolutions import Resolution
from app.nlp.embeddings import emb
from app.core.errors import internal_error, logger
from pydantic import BaseModel


router = APIRouter(prefix="/search", tags=["search"])


class SearchResult(BaseModel):
    """Similarity search result."""
    id: str
    title: str
    preview: str
    similarity: float
    type: str  # "kb" or "resolution"


@router.get("/similar", response_model=List[SearchResult])
def search_similar(
    query: str = Query(..., min_length=3, description="Search query text"),
    limit: int = Query(5, ge=1, le=20, description="Number of results"),
    session: Session = Depends(get_session),
) -> List[SearchResult]:
    """
    Semantic search for similar KB articles and resolutions.
    
    Uses pgvector cosine similarity with sentence-transformers embeddings.
    """
    try:
        # Generate query embedding
        query_embedding = emb.encode_to_list(query)
        
        results: List[SearchResult] = []
        
        # Search KB articles
        kb_stmt = text("""
            SELECT id, title, body, (embedding <=> CAST(:embedding AS vector)) AS distance
            FROM kb_articles
            WHERE embedding IS NOT NULL
            ORDER BY embedding <=> CAST(:embedding AS vector)
            LIMIT :limit
        """)
        
        kb_results = session.execute(
            kb_stmt,
            {"embedding": str(query_embedding), "limit": limit}
        ).fetchall()
        
        for row in kb_results:
            # Convert distance to similarity (1 - cosine distance)
            similarity = 1.0 - row[3]
            if similarity > 0.5:  # Filter low similarity results
                results.append(SearchResult(
                    id=str(row[0]),
                    title=row[1],
                    preview=row[2][:150] + "..." if len(row[2]) > 150 else row[2],
                    similarity=round(similarity, 4),
                    type="kb"
                ))
        
        # Search Resolutions
        res_stmt = text("""
            SELECT id, title, body, (embedding <=> CAST(:embedding AS vector)) AS distance
            FROM resolutions
            WHERE embedding IS NOT NULL
            ORDER BY embedding <=> CAST(:embedding AS vector)
            LIMIT :limit
        """)
        
        res_results = session.execute(
            res_stmt,
            {"embedding": str(query_embedding), "limit": limit}
        ).fetchall()
        
        for row in res_results:
            similarity = 1.0 - row[3]
            if similarity > 0.5:
                results.append(SearchResult(
                    id=str(row[0]),
                    title=row[1],
                    preview=row[2][:150] + "..." if len(row[2]) > 150 else row[2],
                    similarity=round(similarity, 4),
                    type="resolution"
                ))
        
        # Sort all results by similarity and limit
        results.sort(key=lambda x: x.similarity, reverse=True)
        return results[:limit]
        
    except Exception:
        logger.exception("SEARCH_SIMILAR_FAILED")
        raise internal_error("SEARCH_SIMILAR_FAILED", "Could not perform similarity search.")
