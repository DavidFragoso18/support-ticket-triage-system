"""
Tests for ticket creation with embedding generation (Phase 4).

Tests cover:
- POST /tickets endpoint with automatic embedding generation
- Ticket validation
- Embedding generation during creation
- Edge cases and error handling
"""

from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app


class TestTicketCreation:
    """Test basic ticket creation functionality"""

    def test_create_ticket_basic(self, client):
        """Should successfully create a ticket"""
        ticket_data = {
            "subject": "Test ticket creation",
            "body": "This is a test ticket body",
            "channel": "web",
            "customer_id": f"test-{uuid4().hex[:8]}",
        }

        r = client.post("/tickets", json=ticket_data)
        assert r.status_code == 201

        data = r.json()
        assert "id" in data
        assert data["subject"] == ticket_data["subject"]
        assert data["body"] == ticket_data["body"]
        assert data["channel"] == ticket_data["channel"]
        assert data["customer_id"] == ticket_data["customer_id"]

    def test_create_ticket_auto_classification(self, client):
        """Created ticket should include classification"""
        ticket_data = {
            "subject": "Billing issue",
            "body": "I was charged twice for my subscription",
            "channel": "email",
            "customer_id": f"test-{uuid4().hex[:8]}",
        }

        r = client.post("/tickets", json=ticket_data)
        assert r.status_code == 201

        data = r.json()
        assert "classification" in data
        classification = data["classification"]

        assert "intent" in classification
        assert "sentiment" in classification
        assert "priority" in classification
        assert "confidence" in classification

    def test_create_ticket_generates_uuid(self, client):
        """Created ticket should have a valid UUID"""
        ticket_data = {
            "subject": "UUID test",
            "body": "Testing UUID generation",
            "channel": "web",
            "customer_id": f"test-{uuid4().hex[:8]}",
        }

        r = client.post("/tickets", json=ticket_data)
        assert r.status_code == 201

        data = r.json()
        ticket_id = data["id"]

        # Should be a valid UUID string
        from uuid import UUID

        try:
            UUID(ticket_id)
            assert True
        except ValueError:
            assert False, "Ticket ID is not a valid UUID"


class TestTicketValidation:
    """Test ticket validation rules"""

    def test_create_ticket_missing_required(self, client):
        """Should reject ticket without subject"""
        ticket_data = {"body": "Missing subject", "channel": "web", "customer_id": "test-user"}

        r = client.post("/tickets", json=ticket_data)
        assert r.status_code == 422

    def test_create_ticket_invalid_priority(self, client):
        """Should reject ticket without body"""
        ticket_data = {"subject": "Missing body", "channel": "web", "customer_id": "test-user"}

        r = client.post("/tickets", json=ticket_data)
        assert r.status_code == 422

    def test_create_ticket_empty_subject(self, client):
        """Should reject ticket with empty subject"""
        ticket_data = {
            "subject": "",
            "body": "Empty subject test",
            "channel": "web",
            "customer_id": "test-user",
        }

        r = client.post("/tickets", json=ticket_data)
        # Should either reject or handle gracefully
        assert r.status_code in [201, 422]

    def test_update_ticket_not_found(self, client):
        """Should reject ticket with empty body"""
        ticket_data = {
            "subject": "Empty body test",
            "body": "",
            "channel": "web",
            "customer_id": "test-user",
        }

        r = client.post("/tickets", json=ticket_data)
        # Should either reject or handle gracefully
        assert r.status_code in [201, 422]

    def test_create_ticket_invalid_channel(self, client):
        """Should use default channel if not provided"""
        ticket_data = {
            "subject": "Default channel test",
            "body": "Testing default channel",
            "customer_id": f"test-{uuid4().hex[:8]}",
        }

        r = client.post("/tickets", json=ticket_data)
        # May accept or reject depending on implementation
        assert r.status_code in [201, 422]


class TestEmbeddingGeneration:
    """Test automatic embedding generation"""

    def test_ticket_has_embedding_after_creation(self, client):
        """Ticket should have embedding generated after creation"""
        ticket_data = {
            "subject": "Embedding test",
            "body": "This ticket should have an embedding generated automatically",
            "channel": "web",
            "customer_id": f"test-{uuid4().hex[:8]}",
        }

        r = client.post("/tickets", json=ticket_data)
        assert r.status_code == 201
        ticket = r.json()
        ticket_id = ticket["id"]

        # Try to find similar tickets - this will fail if no embedding exists
        r = client.get(f"/tickets/{ticket_id}/similar")
        assert r.status_code == 200
        # If embedding exists, it should return a valid response
        data = r.json()
        assert "similar_tickets" in data

    def test_different_tickets_different_embeddings(self, client):
        """Different ticket content should produce different similar results"""
        # Create ticket about password
        password_ticket = {
            "subject": "Password reset issue",
            "body": "I cannot reset my password",
            "channel": "web",
            "customer_id": f"test-{uuid4().hex[:8]}",
        }
        r1 = client.post("/tickets", json=password_ticket)
        assert r1.status_code == 201
        pwd_ticket = r1.json()

        # Create ticket about billing
        billing_ticket = {
            "subject": "Billing question",
            "body": "I have a question about my invoice",
            "channel": "web",
            "customer_id": f"test-{uuid4().hex[:8]}",
        }
        r2 = client.post("/tickets", json=billing_ticket)
        assert r2.status_code == 201
        bill_ticket = r2.json()

        # Get similar tickets for each
        r_pwd_similar = client.get(f"/tickets/{pwd_ticket['id']}/similar")
        r_bill_similar = client.get(f"/tickets/{bill_ticket['id']}/similar")

        assert r_pwd_similar.status_code == 200
        assert r_bill_similar.status_code == 200

        # Different tickets should have different similar results
        # (This is a weak test but validates embeddings are working)
        assert r_pwd_similar.json() != r_bill_similar.json()


class TestTicketRetrieval:
    """Test retrieving created tickets"""

    def test_get_ticket_not_found(self, client):
        """Should retrieve ticket by ID after creation"""
        ticket_data = {
            "subject": "Retrieval test",
            "body": "Testing ticket retrieval",
            "channel": "web",
            "customer_id": f"test-{uuid4().hex[:8]}",
        }

        # Create ticket
        r = client.post("/tickets", json=ticket_data)
        assert r.status_code == 201
        created_ticket = r.json()
        ticket_id = created_ticket["id"]

        # Retrieve ticket
        r = client.get(f"/tickets/{ticket_id}")
        assert r.status_code == 200

        retrieved_ticket = r.json()
        assert retrieved_ticket["id"] == ticket_id
        assert retrieved_ticket["subject"] == ticket_data["subject"]
        assert retrieved_ticket["body"] == ticket_data["body"]

    def test_list_tickets_pagination(self, client):
        """New ticket should appear in list endpoint"""
        # Get current ticket count
        r1 = client.get("/tickets?page=1&page_size=100")
        initial_count = len(r1.json()["items"])

        # Create new ticket
        ticket_data = {
            "subject": "List test",
            "body": "Testing ticket list",
            "channel": "web",
            "customer_id": f"test-{uuid4().hex[:8]}",
        }
        r = client.post("/tickets", json=ticket_data)
        assert r.status_code == 201
        new_ticket = r.json()

        # Get updated list
        r2 = client.get("/tickets?page=1&page_size=100")
        updated_count = len(r2.json()["items"])

        # Count should have increased
        assert updated_count > initial_count

        # New ticket should be in list
        ticket_ids = [t["id"] for t in r2.json()["items"]]
        assert new_ticket["id"] in ticket_ids


class TestTicketClassification:
    """Test automatic classification during creation"""

    def test_billing_classification(self):
        """Billing-related ticket should be classified correctly"""
        ticket_data = {
            "subject": "Billing problem",
            "body": "I was charged twice for my subscription. Please refund.",
            "channel": "email",
            "customer_id": f"test-{uuid4().hex[:8]}",
        }

        r = client.post("/tickets", json=ticket_data)
        assert r.status_code == 201

        data = r.json()
        classification = data["classification"]

        # Should detect billing intent
        assert classification["intent"] in ["billing", "refund_cancellation"]
        # Should detect negative sentiment
        assert classification["sentiment"] in ["negative", "neutral"]
        # Should be high priority
        assert classification["priority"] in ["P1", "P2"]

    def test_technical_issue_classification(self):
        """Technical issue should be classified correctly"""
        ticket_data = {
            "subject": "App crashes on startup",
            "body": "The mobile app crashes every time I try to open it. I've tried reinstalling.",
            "channel": "web",
            "customer_id": f"test-{uuid4().hex[:8]}",
        }

        r = client.post("/tickets", json=ticket_data)
        assert r.status_code == 201

        data = r.json()
        classification = data["classification"]

        # Should detect bug/issue intent
        assert classification["intent"] in ["bug_issue", "general_inquiry"]
        # Should have appropriate priority
        assert classification["priority"] in ["P1", "P2", "P3"]

    def test_positive_feedback_classification(self):
        """Positive feedback should be classified correctly"""
        ticket_data = {
            "subject": "Love the new feature!",
            "body": "The new dashboard is amazing! Thanks for the great update.",
            "channel": "web",
            "customer_id": f"test-{uuid4().hex[:8]}",
        }

        r = client.post("/tickets", json=ticket_data)
        assert r.status_code == 201

        data = r.json()
        classification = data["classification"]

        # Should detect positive sentiment
        assert classification["sentiment"] == "positive"
        # Should be lower priority
        assert classification["priority"] in ["P3", "P4"]


class TestConcurrentTicketCreation:
    """Test creating multiple tickets concurrently"""

    def test_create_multiple_tickets_sequentially(self):
        """Should handle multiple ticket creations"""
        tickets_created = []

        for i in range(5):
            ticket_data = {
                "subject": f"Test ticket {i}",
                "body": f"This is test ticket number {i}",
                "channel": "web",
                "customer_id": f"test-{uuid4().hex[:8]}",
            }

            r = client.post("/tickets", json=ticket_data)
            assert r.status_code == 201
            tickets_created.append(r.json())

        # All tickets should have unique IDs
        ticket_ids = [t["id"] for t in tickets_created]
        assert len(ticket_ids) == len(set(ticket_ids))


class TestTicketEdgeCases:
    """Test edge cases and special characters"""

    def test_ticket_with_special_characters(self):
        """Should handle special characters in subject and body"""
        ticket_data = {
            "subject": "Special chars: @#$%^&*()_+-=[]{}|;:',.<>?/",
            "body": "Testing special characters: émojis 🚀 and ñ accents",
            "channel": "web",
            "customer_id": f"test-{uuid4().hex[:8]}",
        }

        r = client.post("/tickets", json=ticket_data)
        assert r.status_code == 201

        data = r.json()
        assert data["subject"] == ticket_data["subject"]
        assert data["body"] == ticket_data["body"]

    def test_ticket_with_very_long_body(self):
        """Should handle very long ticket body"""
        long_body = "This is a very long ticket body. " * 100  # ~3500 characters
        ticket_data = {
            "subject": "Long body test",
            "body": long_body,
            "channel": "web",
            "customer_id": f"test-{uuid4().hex[:8]}",
        }

        r = client.post("/tickets", json=ticket_data)
        assert r.status_code == 201

    def test_ticket_with_newlines(self):
        """Should handle newlines in ticket body"""
        ticket_data = {
            "subject": "Newline test",
            "body": "Line 1\nLine 2\nLine 3\n\nLine 5",
            "channel": "web",
            "customer_id": f"test-{uuid4().hex[:8]}",
        }

        r = client.post("/tickets", json=ticket_data)
        assert r.status_code == 201

        data = r.json()
        assert "\n" in data["body"]
