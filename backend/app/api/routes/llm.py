"""
LLM-powered response generation routes using RAG.
"""
from uuid import UUID

from fastapi import APIRouter, Body, Depends, Query
from pydantic import BaseModel
from sqlmodel import Session, select, text

from app.core.errors import internal_error, logger
from app.db.base import get_session
from app.db.models.ai_responses import AIResponse
from app.db.models.ticket import Ticket
from app.nlp.embeddings import emb
from app.services.llm import llm_service

router = APIRouter(prefix="/llm", tags=["llm"])


class ResponseSuggestion(BaseModel):
    """LLM-generated response suggestion"""
    response: str
    tone: str
    context_used: int
    model: str


class SaveResponseRequest(BaseModel):
    """Request to save an AI-generated response"""
    ticket_id: str
    response_text: str
    tone: str
    context_used: int
    model: str
    agent_id: str
    was_edited: bool = False


class SavedResponseInfo(BaseModel):
    """Saved response information"""
    id: str
    ticket_id: str
    created_at: str
    message: str


@router.get("/suggest-response/{ticket_id}", response_model=ResponseSuggestion)
async def suggest_response(
    ticket_id: str,
    tone: str = Query(default="professional", regex="^(professional|friendly|technical|empathetic)$"),
    session: Session = Depends(get_session),
):
    """
    Generate an AI-powered response suggestion for a ticket using RAG.
    
    This endpoint:
    1. Retrieves the ticket details
    2. Finds similar resolved tickets
    3. Finds relevant KB articles
    4. Finds relevant resolution templates
    5. Uses LLM to generate a contextual response
    
    Tones:
    - professional: Formal and business-like
    - friendly: Warm and approachable
    - technical: Detailed with technical explanations
    - empathetic: Understanding and supportive
    """
    try:
        # Get the ticket
        ticket = session.get(Ticket, ticket_id)
        if not ticket:
            raise internal_error("TICKET_NOT_FOUND", "Ticket not found")
        
        # Build context using RAG
        context = await _build_rag_context(
            ticket.subject,
            ticket.body,
            session
        )
        
        # Generate response using LLM
        response_text = await llm_service.generate_response(
            ticket_subject=ticket.subject,
            ticket_body=ticket.body,
            context=context,
            tone=tone
        )
        
        if not response_text:
            # Fallback to template-based response
            response_text = _generate_fallback_response(ticket, context)
        
        return ResponseSuggestion(
            response=response_text,
            tone=tone,
            context_used=len(context),
            model=llm_service.model if llm_service.use_ollama else "gpt-3.5-turbo"
        )
        
    except Exception:
        logger.exception("SUGGEST_RESPONSE_FAILED")
        raise internal_error("SUGGEST_RESPONSE_FAILED", "Could not generate response suggestion.")


async def _build_rag_context(
    subject: str,
    body: str,
    session: Session,
    max_items: int = 5
) -> list:
    """
    Build RAG context by retrieving similar tickets, KB articles, and resolutions.
    """
    context = []
    query_text = f"{subject} {body}"
    query_embedding = emb.encode_to_list(query_text)
    
    try:
        # 1. Find similar resolved tickets
        ticket_query = text("""
            SELECT id, subject, body, status
            FROM tickets
            WHERE embedding IS NOT NULL 
              AND status IN ('resolved', 'closed')
            ORDER BY embedding <=> CAST(:embedding AS vector)
            LIMIT :limit
        """)
        
        ticket_results = session.execute(
            ticket_query,
            {"embedding": str(query_embedding), "limit": 3}
        ).fetchall()
        
        for row in ticket_results:
            similarity = 1.0 - float(row[3]) if len(row) > 3 else 0.0
            if similarity > 0.6:  # Only include highly relevant tickets
                context.append({
                    "type": "ticket",
                    "similarity": similarity,
                    "data": {
                        "id": str(row[0]),
                        "subject": row[1],
                        "body": row[2]
                    }
                })
        
        # 2. Find relevant KB articles
        kb_query = text("""
            SELECT id, title, body
            FROM kb_articles
            WHERE embedding IS NOT NULL
            ORDER BY embedding <=> CAST(:embedding AS vector)
            LIMIT :limit
        """)
        
        kb_results = session.execute(
            kb_query,
            {"embedding": str(query_embedding), "limit": 2}
        ).fetchall()
        
        for row in kb_results:
            context.append({
                "type": "kb",
                "data": {
                    "id": str(row[0]),
                    "title": row[1],
                    "body": row[2]
                }
            })
        
        # 3. Find relevant resolution templates
        res_query = text("""
            SELECT id, title, body
            FROM resolutions
            WHERE embedding IS NOT NULL
            ORDER BY embedding <=> CAST(:embedding AS vector)
            LIMIT :limit
        """)
        
        res_results = session.execute(
            res_query,
            {"embedding": str(query_embedding), "limit": 2}
        ).fetchall()
        
        for row in res_results:
            context.append({
                "type": "resolution",
                "data": {
                    "id": str(row[0]),
                    "title": row[1],
                    "body": row[2]
                }
            })
        
    except Exception as e:
        logger.error(f"Error building RAG context: {e}")
    
    return context[:max_items]


def _generate_fallback_response(ticket: Ticket, context: list) -> str:
    """
    Generate a fallback template-based response when LLM is unavailable.
    """
    response_parts = [
        "Thank you for contacting support regarding your issue.",
        "",
        f"We've received your inquiry about: {ticket.subject}",
        ""
    ]
    
    if context:
        response_parts.append("Based on similar cases, here are some steps that may help:")
        response_parts.append("")
        
        for i, item in enumerate(context[:2], 1):
            if item["type"] == "kb":
                kb_data = item["data"]
                response_parts.append(f"{i}. Reference: {kb_data.get('title', 'N/A')}")
            elif item["type"] == "resolution":
                res_data = item["data"]
                response_parts.append(f"{i}. Solution: {res_data.get('title', 'N/A')}")
    else:
        response_parts.append("Our team will review your case and provide a detailed response shortly.")
    
    response_parts.extend([
        "",
        "If you have any additional questions or concerns, please don't hesitate to reach out.",
        "",
        "Best regards,",
        "Support Team"
    ])
    
    return "\n".join(response_parts)


@router.post("/save-response", response_model=SavedResponseInfo)
async def save_response(
    request: SaveResponseRequest = Body(...),
    session: Session = Depends(get_session),
):
    """
    Save an AI-generated response for future reference.
    
    This allows agents to save AI-generated responses that they've reviewed
    and potentially edited. Saved responses can be tracked for quality analysis.
    """
    try:
        # Verify ticket exists
        ticket = session.get(Ticket, request.ticket_id)
        if not ticket:
            raise internal_error("TICKET_NOT_FOUND", "Ticket not found")
        
        # Create AI response record
        ai_response = AIResponse(
            ticket_id=UUID(request.ticket_id),
            response_text=request.response_text,
            tone=request.tone,
            context_used=request.context_used,
            model=request.model,
            agent_id=request.agent_id,
            was_edited=request.was_edited,
            was_sent=False,  # Will be updated when actually sent
        )
        
        session.add(ai_response)
        session.commit()
        session.refresh(ai_response)
        
        return SavedResponseInfo(
            id=str(ai_response.id),
            ticket_id=str(ai_response.ticket_id),
            created_at=ai_response.created_at.isoformat(),
            message="Response saved successfully"
        )
        
    except Exception:
        logger.exception("SAVE_RESPONSE_FAILED")
        raise internal_error("SAVE_RESPONSE_FAILED", "Could not save response.")


@router.get("/saved-responses/{ticket_id}")
async def get_saved_responses(
    ticket_id: str,
    session: Session = Depends(get_session),
):
    """
    Get all saved AI responses for a specific ticket.
    """
    try:
        statement = select(AIResponse).where(AIResponse.ticket_id == UUID(ticket_id)).order_by(AIResponse.created_at.desc())
        responses = session.exec(statement).all()
        
        return [{
            "id": str(r.id),
            "response_text": r.response_text,
            "tone": r.tone,
            "context_used": r.context_used,
            "model": r.model,
            "agent_id": r.agent_id,
            "was_edited": r.was_edited,
            "was_sent": r.was_sent,
            "created_at": r.created_at.isoformat()
        } for r in responses]
        
    except Exception:
        logger.exception("GET_SAVED_RESPONSES_FAILED")
        raise internal_error("GET_SAVED_RESPONSES_FAILED", "Could not retrieve saved responses.")

