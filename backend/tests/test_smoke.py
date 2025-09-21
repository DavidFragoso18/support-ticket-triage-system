import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    """Health endpoint should respond with status ok"""
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_classify_billing():
    """Billing complaint should be negative sentiment and P1 priority"""
    r = client.post(
        "/classify",
        json={"text": "I was charged twice for my subscription, please fix it ASAP."},
    )
    assert r.status_code == 200
    data = r.json()
    assert "intent" in data
    assert "sentiment" in data
    assert "priority" in data
    assert data["priority"] in {"P1", "P2", "P3"}


def test_ticket_roundtrip():
    """Create ticket → auto-classify → fetch by list & id"""
    payload = {
        "subject": "Double charge",
        "body": "I was charged twice",
        "channel": "email",
        "customer_id": "cust123",
    }

    # Create
    r = client.post("/tickets", json=payload)
    assert r.status_code == 201
    t = r.json()
    assert t["subject"] == payload["subject"]
    assert "classification" in t

    # List
    r2 = client.get("/tickets?page=1&page_size=5")
    assert r2.status_code == 200
    data = r2.json()
    assert "items" in data
    assert any(item["id"] == t["id"] for item in data["items"])

    # Fetch by id
    r3 = client.get(f"/tickets/{t['id']}")
    assert r3.status_code == 200
    t2 = r3.json()
    assert t2["id"] == t["id"]
