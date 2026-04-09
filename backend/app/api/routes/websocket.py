"""WebSocket routes for real-time ticket updates"""

import logging
import uuid
from typing import Optional

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    WebSocket,
    WebSocketDisconnect,
    status,
)
from sqlmodel import Session

from app.db.base import get_session
from app.db.models.ticket import Ticket
from app.services.websocket_manager import manager

router = APIRouter()
logger = logging.getLogger(__name__)


@router.websocket("/ws/tickets")
async def websocket_tickets_endpoint(websocket: WebSocket, agent_id: Optional[str] = None):
    """
    WebSocket endpoint for real-time ticket updates

    Clients connect to receive live updates about:
    - New tickets created
    - Ticket status changes
    - Priority updates
    - Tickets claimed/released by agents
    - High-priority alerts
    """
    connection_id = str(uuid.uuid4())

    await manager.connect(websocket, connection_id, agent_id)

    try:
        # Send connection confirmation
        await manager.send_personal_message(
            {
                "type": "connection_established",
                "connection_id": connection_id,
                "agent_id": agent_id,
            },
            connection_id,
        )

        # Keep connection alive and handle incoming messages
        while True:
            data = await websocket.receive_json()

            # Handle different message types from client
            message_type = data.get("type")

            if message_type == "ping":
                await manager.send_personal_message({"type": "pong"}, connection_id)
            elif message_type == "presence_update":
                # Update agent presence status
                status_val = data.get("status", "online")
                if agent_id:
                    await manager.send_presence_update(agent_id, status_val)

    except WebSocketDisconnect:
        manager.disconnect(connection_id, agent_id)
        logger.info(f"Client {connection_id} disconnected normally")
    except Exception as e:
        logger.error(f"WebSocket error for {connection_id}: {e}")
        manager.disconnect(connection_id, agent_id)


@router.post("/tickets/{ticket_id}/claim")
async def claim_ticket(ticket_id: str, agent_id: str, session: Session = Depends(get_session)):
    """
    Claim a ticket and broadcast the update

    This endpoint allows an agent to claim a ticket, preventing
    other agents from working on it simultaneously.
    """
    # Get ticket from database
    try:
        ticket_uuid = uuid.UUID(ticket_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid ticket ID format")

    ticket = session.get(Ticket, ticket_uuid)

    if not ticket:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found")

    # Check if already claimed
    if ticket.assigned_agent_id and ticket.assigned_agent_id != agent_id:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Ticket already claimed by agent {ticket.assigned_agent_id}",
        )

    # Claim the ticket
    ticket.assigned_agent_id = agent_id
    ticket.status = "in_progress"
    session.add(ticket)
    session.commit()
    session.refresh(ticket)

    # Track agent activity
    from datetime import datetime

    from app.db.models.analytics import AgentActivity

    activity = AgentActivity(
        agent_id=agent_id, ticket_id=ticket.id, action="claimed", timestamp=datetime.utcnow()
    )
    session.add(activity)
    session.commit()

    # Broadcast the claim to all connected clients
    await manager.notify_ticket_claimed(
        ticket_id=ticket_id, agent_id=agent_id, ticket_data=ticket.model_dump()
    )

    return {
        "success": True,
        "message": f"Ticket {ticket_id} claimed by agent {agent_id}",
        "ticket": ticket,
    }


@router.post("/tickets/{ticket_id}/release")
async def release_ticket(ticket_id: str, session: Session = Depends(get_session)):
    """
    Release a ticket back to the pool

    This endpoint allows an agent to release a claimed ticket,
    making it available for other agents to claim.
    """
    # Get ticket from database
    try:
        ticket_uuid = uuid.UUID(ticket_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid ticket ID format")

    ticket = session.get(Ticket, ticket_uuid)

    if not ticket:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found")

    # Store the previous agent_id before releasing
    previous_agent_id = ticket.assigned_agent_id

    # Release the ticket
    ticket.assigned_agent_id = None
    ticket.status = "open"
    session.add(ticket)
    session.commit()
    session.refresh(ticket)

    # Track agent activity
    if previous_agent_id:
        from datetime import datetime

        from app.db.models.analytics import AgentActivity

        activity = AgentActivity(
            agent_id=previous_agent_id,
            ticket_id=ticket.id,
            action="released",
            timestamp=datetime.utcnow(),
        )
        session.add(activity)
        session.commit()

    # Broadcast the release to all connected clients
    await manager.notify_ticket_released(ticket_id=ticket_id, ticket_data=ticket.model_dump())

    return {"success": True, "message": f"Ticket {ticket_id} released", "ticket": ticket}


@router.get("/ws/status")
async def websocket_status():
    """
    Get WebSocket connection status and statistics
    """
    return {
        "active_connections": len(manager.active_connections),
        "agent_subscriptions": {
            agent_id: len(connections)
            for agent_id, connections in manager.agent_subscriptions.items()
        },
        "redis_connected": manager.redis_client is not None,
    }
