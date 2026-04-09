"""WebSocket connection manager for real-time updates"""

import json
import logging
from typing import Dict, Optional, Set

import redis.asyncio as redis
from fastapi import WebSocket

from app.core.config import settings

logger = logging.getLogger(__name__)


class ConnectionManager:
    """Manages WebSocket connections and broadcasts messages"""

    def __init__(self):
        # Store active connections by connection ID
        self.active_connections: Dict[str, WebSocket] = {}
        # Store agent subscriptions (agent_id -> set of connection IDs)
        self.agent_subscriptions: Dict[str, Set[str]] = {}
        # Redis connection for pub/sub across multiple backend instances
        self.redis_client: Optional[redis.Redis] = None
        self.pubsub = None

    async def connect_redis(self):
        """Initialize Redis connection for pub/sub"""
        try:
            self.redis_client = redis.from_url(
                settings.redis_url, encoding="utf-8", decode_responses=True
            )
            await self.redis_client.ping()
            logger.info("✅ Redis connected for WebSocket pub/sub")
        except Exception as e:
            logger.error(f"❌ Redis connection failed: {e}")
            self.redis_client = None

    async def disconnect_redis(self):
        """Close Redis connection"""
        if self.redis_client:
            await self.redis_client.close()
            logger.info("Redis connection closed")

    async def connect(
        self, websocket: WebSocket, connection_id: str, agent_id: Optional[str] = None
    ):
        """Accept a new WebSocket connection"""
        await websocket.accept()
        self.active_connections[connection_id] = websocket

        # Subscribe agent to their personal channel
        if agent_id:
            if agent_id not in self.agent_subscriptions:
                self.agent_subscriptions[agent_id] = set()
            self.agent_subscriptions[agent_id].add(connection_id)

        logger.info(f"✅ WebSocket connected: {connection_id} (agent: {agent_id})")
        logger.info(f"📊 Active connections: {len(self.active_connections)}")

    def disconnect(self, connection_id: str, agent_id: Optional[str] = None):
        """Remove a WebSocket connection"""
        if connection_id in self.active_connections:
            del self.active_connections[connection_id]

        # Unsubscribe from agent channel
        if agent_id and agent_id in self.agent_subscriptions:
            self.agent_subscriptions[agent_id].discard(connection_id)
            if not self.agent_subscriptions[agent_id]:
                del self.agent_subscriptions[agent_id]

        logger.info(f"❌ WebSocket disconnected: {connection_id}")
        logger.info(f"📊 Active connections: {len(self.active_connections)}")

    async def send_personal_message(self, message: dict, connection_id: str):
        """Send a message to a specific connection"""
        if connection_id in self.active_connections:
            try:
                await self.active_connections[connection_id].send_json(message)
            except Exception as e:
                logger.error(f"Error sending to {connection_id}: {e}")
                self.disconnect(connection_id)

    async def send_to_agent(self, message: dict, agent_id: str):
        """Send a message to all connections of a specific agent"""
        if agent_id in self.agent_subscriptions:
            for connection_id in list(self.agent_subscriptions[agent_id]):
                await self.send_personal_message(message, connection_id)

    async def broadcast(self, message: dict, exclude: Optional[str] = None):
        """Broadcast a message to all connected clients"""
        disconnected = []
        for connection_id, websocket in self.active_connections.items():
            if connection_id == exclude:
                continue
            try:
                await websocket.send_json(message)
            except Exception as e:
                logger.error(f"Error broadcasting to {connection_id}: {e}")
                disconnected.append(connection_id)

        # Clean up disconnected connections
        for connection_id in disconnected:
            self.disconnect(connection_id)

    async def broadcast_ticket_update(self, event_type: str, ticket_data: dict):
        """Broadcast ticket updates to all clients"""
        logger.info(f"📢 Broadcasting ticket update: {event_type}")
        # Convert non-serializable types (UUID, datetime) to strings
        serializable_data = json.loads(json.dumps(ticket_data, default=str))

        message = {
            "type": "ticket_update",
            "event": event_type,
            "data": serializable_data,
        }
        logger.info(f"📤 Sending to {len(self.active_connections)} connections")
        await self.broadcast(message)

        # Publish to Redis for multi-instance support
        if self.redis_client:
            try:
                await self.redis_client.publish("ticket_updates", json.dumps(message))
            except Exception as e:
                logger.error(f"Error publishing to Redis: {e}")

    async def broadcast_high_priority_alert(self, ticket_data: dict):
        """Send high-priority ticket alert to all agents"""
        logger.info("🚨 Broadcasting high-priority alert")
        # Convert non-serializable types to strings
        serializable_data = json.loads(json.dumps(ticket_data, default=str))

        message = {
            "type": "high_priority_alert",
            "data": serializable_data,
        }
        await self.broadcast(message)

    async def notify_ticket_claimed(self, ticket_id: str, agent_id: str, ticket_data: dict):
        """Notify when a ticket is claimed by an agent"""
        # Convert non-serializable types to strings
        serializable_data = json.loads(json.dumps(ticket_data, default=str))

        message = {
            "type": "ticket_claimed",
            "ticket_id": ticket_id,
            "agent_id": agent_id,
            "data": serializable_data,
        }
        await self.broadcast(message)

    async def notify_ticket_released(self, ticket_id: str, ticket_data: dict):
        """Notify when a ticket is released back to the pool"""
        # Convert non-serializable types to strings
        serializable_data = json.loads(json.dumps(ticket_data, default=str))

        message = {
            "type": "ticket_released",
            "ticket_id": ticket_id,
            "data": serializable_data,
        }
        await self.broadcast(message)

    async def send_presence_update(self, agent_id: str, status: str):
        """Broadcast agent presence status (online/offline/away)"""
        message = {
            "type": "agent_presence",
            "agent_id": agent_id,
            "status": status,
        }
        await self.broadcast(message)


# Global connection manager instance
manager = ConnectionManager()
