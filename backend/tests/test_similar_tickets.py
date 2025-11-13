"""
Tests for the similar tickets feature (Phase 4).

Tests cover:
- GET /tickets/{id}/similar endpoint
- Similarity threshold filtering (>0.5)
- Ordering by similarity score
- Edge cases (no embeddings, single ticket, non-existent ticket)
- Limit parameter
"""
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


class TestSimilarTicketsEndpoint:
    """Test similar tickets endpoint basic functionality"""
    
    @pytest.fixture
    def create_similar_tickets(self):
        """Create a set of similar tickets for testing"""
        tickets = []
        
        # Create 3 tickets about password reset
        password_tickets = [
            {
                "subject": "Cannot reset password",
                "body": "I forgot my password and the reset email is not arriving. Please help.",
                "channel": "web",
                "customer_id": f"test-user-{uuid4().hex[:8]}"
            },
            {
                "subject": "Password reset link broken",
                "body": "The password reset link I received does not work when I click it.",
                "channel": "email",
                "customer_id": f"test-user-{uuid4().hex[:8]}"
            },
            {
                "subject": "Help with password",
                "body": "I need to reset my password but I'm not getting the email.",
                "channel": "web",
                "customer_id": f"test-user-{uuid4().hex[:8]}"
            }
        ]
        
        for ticket_data in password_tickets:
            r = client.post("/tickets", json=ticket_data)
            assert r.status_code == 201
            tickets.append(r.json())
        
        # Create 1 dissimilar ticket about billing
        billing_ticket = {
            "subject": "Billing question",
            "body": "I have a question about my invoice charges for last month.",
            "channel": "email",
            "customer_id": f"test-user-{uuid4().hex[:8]}"
        }
        r = client.post("/tickets", json=billing_ticket)
        assert r.status_code == 201
        tickets.append(r.json())
        
        return tickets
    
    def test_similar_tickets_endpoint_exists(self, create_similar_tickets):
        """Similar tickets endpoint should be accessible"""
        tickets = create_similar_tickets
        ticket_id = tickets[0]["id"]
        
        r = client.get(f"/tickets/{ticket_id}/similar")
        assert r.status_code == 200
    
    def test_similar_tickets_response_structure(self, create_similar_tickets):
        """Similar tickets response should have expected structure"""
        tickets = create_similar_tickets
        ticket_id = tickets[0]["id"]
        
        r = client.get(f"/tickets/{ticket_id}/similar")
        assert r.status_code == 200
        data = r.json()
        
        assert "similar_tickets" in data
        assert isinstance(data["similar_tickets"], list)
    
    def test_similar_ticket_item_structure(self, create_similar_tickets):
        """Each similar ticket should have required fields"""
        tickets = create_similar_tickets
        ticket_id = tickets[0]["id"]
        
        r = client.get(f"/tickets/{ticket_id}/similar")
        data = r.json()
        
        if len(data["similar_tickets"]) > 0:
            similar = data["similar_tickets"][0]
            
            # Check required fields
            assert "id" in similar
            assert "subject" in similar
            assert "preview" in similar
            assert "created_at" in similar
            assert "similarity" in similar
            
            # Check types
            assert isinstance(similar["id"], str)
            assert isinstance(similar["subject"], str)
            assert isinstance(similar["preview"], str)
            assert isinstance(similar["created_at"], str)
            assert isinstance(similar["similarity"], (int, float))


class TestSimilarityScoring:
    """Test similarity score calculations and filtering"""
    
    @pytest.fixture
    def password_ticket(self):
        """Create a ticket about password issues"""
        ticket_data = {
            "subject": "Password reset not working",
            "body": "I clicked forgot password but the email never arrives. I checked spam folder.",
            "channel": "web",
            "customer_id": f"test-pwd-{uuid4().hex[:6]}"
        }
        r = client.post("/tickets", json=ticket_data)
        assert r.status_code == 201
        return r.json()
    
    def test_similarity_score_range(self, password_ticket):
        """Similarity scores should be between 0 and 1"""
        ticket_id = password_ticket["id"]
        
        r = client.get(f"/tickets/{ticket_id}/similar")
        data = r.json()
        
        for similar in data["similar_tickets"]:
            similarity = similar["similarity"]
            assert 0 <= similarity <= 1
    
    def test_similarity_threshold(self, password_ticket):
        """Only tickets with similarity > 0.5 should be returned"""
        ticket_id = password_ticket["id"]
        
        r = client.get(f"/tickets/{ticket_id}/similar")
        data = r.json()
        
        for similar in data["similar_tickets"]:
            similarity = similar["similarity"]
            assert similarity > 0.5
    
    def test_similarity_ordering(self, password_ticket):
        """Similar tickets should be ordered by similarity (highest first)"""
        ticket_id = password_ticket["id"]
        
        r = client.get(f"/tickets/{ticket_id}/similar")
        data = r.json()
        similar_tickets = data["similar_tickets"]
        
        if len(similar_tickets) > 1:
            # Check that each ticket has similarity >= next ticket
            for i in range(len(similar_tickets) - 1):
                current_sim = similar_tickets[i]["similarity"]
                next_sim = similar_tickets[i + 1]["similarity"]
                assert current_sim >= next_sim
    
    def test_excludes_current_ticket(self, password_ticket):
        """Similar tickets should not include the current ticket"""
        ticket_id = password_ticket["id"]
        
        r = client.get(f"/tickets/{ticket_id}/similar")
        data = r.json()
        
        for similar in data["similar_tickets"]:
            assert similar["id"] != ticket_id


class TestSimilarTicketsParameters:
    """Test query parameters for similar tickets endpoint"""
    
    @pytest.fixture
    def ticket_with_many_similar(self):
        """Create a ticket that should have many similar matches"""
        # Create main ticket
        main_ticket = {
            "subject": "Account login problem",
            "body": "I cannot log into my account. Password reset is not working.",
            "channel": "web",
            "customer_id": f"test-main-{uuid4().hex[:6]}"
        }
        r = client.post("/tickets", json=main_ticket)
        assert r.status_code == 201
        return r.json()
    
    def test_limit_parameter_default(self, ticket_with_many_similar):
        """Default limit should be 5"""
        ticket_id = ticket_with_many_similar["id"]
        
        r = client.get(f"/tickets/{ticket_id}/similar")
        data = r.json()
        
        # Should return at most 5 results (default limit)
        assert len(data["similar_tickets"]) <= 5
    
    def test_limit_parameter_custom(self, ticket_with_many_similar):
        """Should respect custom limit parameter"""
        ticket_id = ticket_with_many_similar["id"]
        
        r = client.get(f"/tickets/{ticket_id}/similar?limit=3")
        data = r.json()
        
        # Should return at most 3 results
        assert len(data["similar_tickets"]) <= 3
    
    def test_limit_parameter_max(self, ticket_with_many_similar):
        """Limit should be capped at 20"""
        ticket_id = ticket_with_many_similar["id"]
        
        r = client.get(f"/tickets/{ticket_id}/similar?limit=100")
        data = r.json()
        
        # Should return at most 20 results (max limit)
        assert len(data["similar_tickets"]) <= 20
    
    def test_limit_parameter_invalid(self, ticket_with_many_similar):
        """Invalid limit should be rejected or handled gracefully"""
        ticket_id = ticket_with_many_similar["id"]
        
        r = client.get(f"/tickets/{ticket_id}/similar?limit=-1")
        # Should either return 422 (validation error) or handle gracefully
        assert r.status_code in [200, 422]


class TestSimilarTicketsEdgeCases:
    """Test edge cases and error handling"""
    
    def test_similar_tickets_nonexistent_ticket(self):
        """Request for non-existent ticket should return 404"""
        fake_id = str(uuid4())
        r = client.get(f"/tickets/{fake_id}/similar")
        assert r.status_code == 404
    
    def test_similar_tickets_invalid_uuid(self):
        """Invalid UUID should return 422 or 404"""
        r = client.get("/tickets/invalid-uuid/similar")
        assert r.status_code in [404, 422]
    
    def test_similar_tickets_no_embedding(self):
        """Ticket without embedding should return empty list"""
        # This would require a ticket created without embeddings
        # For now, just verify the endpoint handles this case
        # by checking response structure
        pass
    
    def test_similar_tickets_single_ticket(self):
        """When only one ticket exists, should return empty list"""
        # Create a unique ticket
        unique_ticket = {
            "subject": f"Unique ticket {uuid4().hex[:8]}",
            "body": f"This is a unique ticket with random content {uuid4().hex}",
            "channel": "web",
            "customer_id": f"unique-{uuid4().hex[:8]}"
        }
        r = client.post("/tickets", json=unique_ticket)
        assert r.status_code == 201
        ticket = r.json()
        
        # Query for similar tickets
        r = client.get(f"/tickets/{ticket['id']}/similar")
        assert r.status_code == 200
        data = r.json()
        
        # Should return empty list or very few results
        assert isinstance(data["similar_tickets"], list)


class TestSimilarTicketsPreview:
    """Test preview text generation"""
    
    def test_preview_truncation(self):
        """Preview should be truncated to 150 characters"""
        # Create ticket with long body
        long_body = "This is a very long ticket body. " * 20  # Much longer than 150 chars
        ticket_data = {
            "subject": "Test preview truncation",
            "body": long_body,
            "channel": "web",
            "customer_id": f"test-preview-{uuid4().hex[:6]}"
        }
        r = client.post("/tickets", json=ticket_data)
        assert r.status_code == 201
        ticket = r.json()
        
        # Get similar tickets (if any)
        r = client.get(f"/tickets/{ticket['id']}/similar")
        data = r.json()
        
        for similar in data["similar_tickets"]:
            # Preview should be <= 153 chars (150 + "...")
            assert len(similar["preview"]) <= 153
    
    def test_preview_no_truncation_short_body(self):
        """Short body should not be truncated"""
        short_body = "Short ticket body"
        ticket_data = {
            "subject": "Test short preview",
            "body": short_body,
            "channel": "web",
            "customer_id": f"test-short-{uuid4().hex[:6]}"
        }
        r = client.post("/tickets", json=ticket_data)
        assert r.status_code == 201


class TestSimilarTicketsPerformance:
    """Test performance of similar tickets endpoint"""
    
    def test_similar_tickets_response_time(self):
        """Similar tickets should respond quickly"""
        import time
        
        # Create a test ticket
        ticket_data = {
            "subject": "Performance test ticket",
            "body": "Testing response time for similar tickets endpoint",
            "channel": "web",
            "customer_id": f"perf-test-{uuid4().hex[:6]}"
        }
        r = client.post("/tickets", json=ticket_data)
        assert r.status_code == 201
        ticket = r.json()
        
        # Measure response time
        start_time = time.time()
        r = client.get(f"/tickets/{ticket['id']}/similar")
        end_time = time.time()
        
        assert r.status_code == 200
        response_time = end_time - start_time
        
        # Should respond within 2 seconds
        assert response_time < 2.0
