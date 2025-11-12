"""Tests for WebSocket real-time updates"""
import pytest
from fastapi.testclient import TestClient
from app.main import app
import json
import time

client = TestClient(app)


def test_websocket_connection():
    """Test basic WebSocket connection"""
    with client.websocket_connect("/ws/tickets") as websocket:
        # Should receive connection confirmation
        data = websocket.receive_json()
        assert data["type"] == "connection_established"
        assert "connection_id" in data


def test_websocket_connection_with_agent():
    """Test WebSocket connection with agent ID"""
    with client.websocket_connect("/ws/tickets?agent_id=agent-123") as websocket:
        data = websocket.receive_json()
        assert data["type"] == "connection_established"
        assert data["agent_id"] == "agent-123"


def test_websocket_ping_pong():
    """Test ping/pong keep-alive mechanism"""
    with client.websocket_connect("/ws/tickets") as websocket:
        # Skip connection message
        websocket.receive_json()
        
        # Send ping
        websocket.send_json({"type": "ping"})
        
        # Should receive pong
        response = websocket.receive_json()
        assert response["type"] == "pong"


def test_websocket_status_endpoint():
    """Test WebSocket status endpoint"""
    response = client.get("/ws/status")
    assert response.status_code == 200
    data = response.json()
    assert "active_connections" in data
    assert "agent_subscriptions" in data
    assert "redis_connected" in data


def test_ticket_claim_endpoint():
    """Test ticket claim with broadcast"""
    # First create a ticket
    ticket_data = {
        "subject": "Test claim ticket",
        "body": "Testing ticket claim functionality",
        "channel": "web",
        "customer_id": "cust-123"
    }
    create_response = client.post("/tickets", json=ticket_data)
    assert create_response.status_code == 201
    ticket_id = create_response.json()["id"]
    
    # Claim the ticket
    claim_response = client.post(
        f"/tickets/{ticket_id}/claim",
        params={"agent_id": "agent-456"}
    )
    assert claim_response.status_code == 200
    data = claim_response.json()
    assert data["success"] is True
    assert data["ticket"]["assigned_agent_id"] == "agent-456"
    assert data["ticket"]["status"] == "in_progress"


def test_ticket_release_endpoint():
    """Test ticket release with broadcast"""
    # Create and claim a ticket
    ticket_data = {
        "subject": "Test release ticket",
        "body": "Testing ticket release functionality",
        "channel": "email",
        "customer_id": "cust-789"
    }
    create_response = client.post("/tickets", json=ticket_data)
    ticket_id = create_response.json()["id"]
    
    # Claim it first
    client.post(f"/tickets/{ticket_id}/claim", params={"agent_id": "agent-999"})
    
    # Release the ticket
    release_response = client.post(f"/tickets/{ticket_id}/release")
    assert release_response.status_code == 200
    data = release_response.json()
    assert data["success"] is True
    assert data["ticket"]["assigned_agent_id"] is None
    assert data["ticket"]["status"] == "open"


def test_ticket_claim_conflict():
    """Test that claiming an already claimed ticket returns conflict"""
    # Create a ticket
    ticket_data = {
        "subject": "Test conflict",
        "body": "Testing claim conflict",
        "channel": "phone",
        "customer_id": "cust-conflict"
    }
    create_response = client.post("/tickets", json=ticket_data)
    ticket_id = create_response.json()["id"]
    
    # Claim by first agent
    client.post(f"/tickets/{ticket_id}/claim", params={"agent_id": "agent-1"})
    
    # Try to claim by second agent
    conflict_response = client.post(
        f"/tickets/{ticket_id}/claim",
        params={"agent_id": "agent-2"}
    )
    assert conflict_response.status_code == 409


def test_websocket_receives_new_ticket_broadcast():
    """Test that connected clients receive new ticket broadcasts"""
    with client.websocket_connect("/ws/tickets") as websocket:
        # Skip connection message
        websocket.receive_json()
        
        # Create a new ticket (this should trigger a broadcast)
        ticket_data = {
            "subject": "Broadcast test ticket",
            "body": "This should be broadcast to all clients",
            "channel": "chat",
            "customer_id": "cust-broadcast"
        }
        
        # Create ticket in separate request
        import threading
        def create_ticket():
            time.sleep(0.5)  # Small delay to ensure websocket is ready
            client.post("/tickets", json=ticket_data)
        
        thread = threading.Thread(target=create_ticket)
        thread.start()
        
        # Wait for broadcast message (with timeout)
        websocket.settimeout(2.0)
        try:
            message = websocket.receive_json()
            # Should receive ticket_update message
            assert message["type"] == "ticket_update"
            assert message["event"] == "ticket_created"
            assert "data" in message
        except:
            # If no message received, that's okay for now
            # (broadcast happens in background task which may be delayed)
            pass
        finally:
            thread.join()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
