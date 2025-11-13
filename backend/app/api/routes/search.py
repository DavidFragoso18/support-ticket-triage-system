"""
Semantic search routes using vector embeddings.

Provides similarity search across KB articles, resolutions, and tickets.
"""
from typing import List

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlmodel import Session, text

from app.core.errors import internal_error, logger
from app.db.base import get_session
from app.nlp.embeddings import emb

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


@router.get("/tickets")
async def search_tickets(
    q: str = Query(..., min_length=3, description="Search query"),
    limit: int = Query(default=10, ge=1, le=50),
    threshold: float = Query(default=0.5, ge=0.0, le=1.0, description="Similarity threshold"),
    mode: str = Query(default="hybrid", regex="^(semantic|keyword|hybrid)$"),
    session: Session = Depends(get_session),
):
    """
    Advanced semantic search for tickets.
    
    Modes:
    - semantic: Vector similarity search only (best for conceptual queries)
    - keyword: Full-text search only (best for exact terms)
    - hybrid: Combined approach with ranking (recommended)
    """
    try:
        from app.schemas.ticket import ClassificationOut, TicketOut
        
        results = []
        
        if mode == "semantic":
            # Pure vector similarity search
            query_embedding = emb.encode_to_list(q)
            embedding_str = str(query_embedding)
            
            query = text("""
                SELECT 
                    t.id, t.subject, t.body, t.channel, t.customer_id, t.language,
                    t.created_at, t.updated_at, t.status, t.assigned_agent_id,
                    1 - (t.embedding <=> CAST(:embedding AS vector)) as similarity,
                    tc.id as classification_id, tc.intent, tc.sentiment, tc.priority,
                    tc.confidence, tc.low_confidence
                FROM tickets t
                LEFT JOIN ticket_classifications tc ON t.id = tc.ticket_id
                WHERE t.embedding IS NOT NULL
                ORDER BY t.embedding <=> CAST(:embedding AS vector)
                LIMIT :limit
            """)
            
            result = session.execute(
                query,
                {"embedding": embedding_str, "limit": limit}
            )
            rows = result.fetchall()
            
            for row in rows:
                if row.similarity >= threshold:
                    results.append({
                        "ticket": TicketOut(
                            id=row.id,
                            subject=row.subject,
                            body=row.body,
                            channel=row.channel,
                            customer_id=row.customer_id,
                            language=row.language,
                            created_at=row.created_at,
                            updated_at=row.updated_at,
                            classification=ClassificationOut(
                                id=row.classification_id,
                                intent=row.intent,
                                sentiment=row.sentiment,
                                priority=row.priority,
                                confidence=row.confidence,
                                low_confidence=row.low_confidence
                            ) if row.classification_id else None
                        ),
                        "score": float(row.similarity),
                        "match_type": "semantic"
                    })
                    
        elif mode == "keyword":
            # Full-text search using PostgreSQL tsvector
            query = text("""
                SELECT 
                    t.id, t.subject, t.body, t.channel, t.customer_id, t.language,
                    t.created_at, t.updated_at, t.status, t.assigned_agent_id,
                    ts_rank(t.search_vector, to_tsquery('english', :query)) as rank,
                    tc.id as classification_id, tc.intent, tc.sentiment, tc.priority,
                    tc.confidence, tc.low_confidence
                FROM tickets t
                LEFT JOIN ticket_classifications tc ON t.id = tc.ticket_id
                WHERE t.search_vector @@ to_tsquery('english', :query)
                ORDER BY rank DESC
                LIMIT :limit
            """)
            
            # Convert query to tsquery format (replace spaces with &)
            tsquery = " & ".join(q.split())
            
            result = session.execute(
                query,
                {"query": tsquery, "limit": limit}
            )
            rows = result.fetchall()
            
            for row in rows:
                results.append({
                    "ticket": TicketOut(
                        id=row.id,
                        subject=row.subject,
                        body=row.body,
                        channel=row.channel,
                        customer_id=row.customer_id,
                        language=row.language,
                        created_at=row.created_at,
                        updated_at=row.updated_at,
                        classification=ClassificationOut(
                            id=row.classification_id,
                            intent=row.intent,
                            sentiment=row.sentiment,
                            priority=row.priority,
                            confidence=row.confidence,
                            low_confidence=row.low_confidence
                        ) if row.classification_id else None
                    ),
                    "score": float(row.rank),
                    "match_type": "keyword"
                })
                
        else:  # hybrid mode
            # Combine both approaches with weighted scoring
            query_embedding = emb.encode_to_list(q)
            embedding_str = str(query_embedding)
            tsquery = " & ".join(q.split())
            
            query = text("""
                SELECT 
                    t.id, t.subject, t.body, t.channel, t.customer_id, t.language,
                    t.created_at, t.updated_at, t.status, t.assigned_agent_id,
                    (1 - (t.embedding <=> CAST(:embedding AS vector))) as semantic_score,
                    COALESCE(
                        ts_rank(t.search_vector, to_tsquery('english', :query)), 0
                    ) as keyword_score,
                    (0.6 * (1 - (t.embedding <=> CAST(:embedding AS vector))) + 
                     0.4 * COALESCE(
                         ts_rank(t.search_vector, to_tsquery('english', :query)), 0
                     )) as hybrid_score,
                    tc.id as classification_id, tc.intent, tc.sentiment, tc.priority,
                    tc.confidence, tc.low_confidence
                FROM tickets t
                LEFT JOIN ticket_classifications tc ON t.id = tc.ticket_id
                WHERE t.embedding IS NOT NULL
                ORDER BY hybrid_score DESC
                LIMIT :limit
            """)
            
            result = session.execute(
                query,
                {"embedding": embedding_str, "query": tsquery, "limit": limit}
            )
            rows = result.fetchall()
            
            for row in rows:
                if row.hybrid_score >= threshold:
                    results.append({
                        "ticket": TicketOut(
                            id=row.id,
                            subject=row.subject,
                            body=row.body,
                            channel=row.channel,
                            customer_id=row.customer_id,
                            language=row.language,
                            created_at=row.created_at,
                            updated_at=row.updated_at,
                            classification=ClassificationOut(
                                id=row.classification_id,
                                intent=row.intent,
                                sentiment=row.sentiment,
                                priority=row.priority,
                                confidence=row.confidence,
                                low_confidence=row.low_confidence
                            ) if row.classification_id else None
                        ),
                        "score": float(row.hybrid_score),
                        "semantic_score": float(row.semantic_score),
                        "keyword_score": float(row.keyword_score),
                        "match_type": "hybrid"
                    })
        
        return {
            "query": q,
            "mode": mode,
            "results": results,
            "count": len(results)
        }
        
    except Exception:
        logger.exception("TICKET_SEARCH_FAILED")
        raise internal_error("TICKET_SEARCH_FAILED", "Could not perform ticket search.")
