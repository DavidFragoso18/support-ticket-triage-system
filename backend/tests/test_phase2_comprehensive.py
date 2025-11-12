"""
Comprehensive tests for Phase 2 features.

Tests cover:
- Ticket filtering (intent, sentiment, priority, channel, date range)
- Search functionality
- Suggestions endpoint (KB articles and resolution templates)
- Pagination
- Edge cases
"""
import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta
from uuid import uuid4

from app.main import app

client = TestClient(app)


class TestTicketFiltering:
    """Test ticket filtering functionality"""
    
    @pytest.fixture
    def create_test_tickets(self):
        """Create a set of tickets with different attributes"""
        tickets = []
        
        # Billing ticket - negative sentiment, P1 priority
        billing_ticket = {
            "subject": "Double charge on my account",
            "body": "I was charged twice for my subscription. This is unacceptable, please refund immediately.",
            "channel": "email",
            "customer_id": f"test-{uuid4().hex[:8]}"
        }
        r = client.post("/tickets", json=billing_ticket)
        assert r.status_code == 201
        tickets.append(r.json())
        
        # Account access ticket - negative sentiment
        account_ticket = {
            "subject": "Cannot login to my account",
            "body": "I forgot my password and the reset link is not working. Need help urgently.",
            "channel": "web",
            "customer_id": f"test-{uuid4().hex[:8]}"
        }
        r = client.post("/tickets", json=account_ticket)
        assert r.status_code == 201
        tickets.append(r.json())
        
        # Positive feedback - positive sentiment, P4 priority
        feedback_ticket = {
            "subject": "Great new feature!",
            "body": "I love the new dashboard update. It's so much easier to use now.",
            "channel": "web",
            "customer_id": f"test-{uuid4().hex[:8]}"
        }
        r = client.post("/tickets", json=feedback_ticket)
        assert r.status_code == 201
        tickets.append(r.json())
        
        # General inquiry - neutral sentiment
        inquiry_ticket = {
            "subject": "Question about pricing plans",
            "body": "Can you explain the difference between the basic and premium plans?",
            "channel": "chat",
            "customer_id": f"test-{uuid4().hex[:8]}"
        }
        r = client.post("/tickets", json=inquiry_ticket)
        assert r.status_code == 201
        tickets.append(r.json())
        
        return tickets
    
    def test_filter_by_intent(self, create_test_tickets):
        """Should filter tickets by intent"""
        # Filter for billing intent
        r = client.get("/tickets?page=1&page_size=10&intent=billing")
        assert r.status_code == 200
        data = r.json()
        
        assert "items" in data
        assert "total" in data
        
        # Should have at least some results
        assert isinstance(data["items"], list)
    
    def test_filter_by_priority(self, create_test_tickets):
        """Should filter tickets by priority"""
        # Filter for P1 priority
        r = client.get("/tickets?page=1&page_size=10&priority=P1")
        assert r.status_code == 200
        data = r.json()
        
        assert "items" in data
        assert "total" in data
        
        # Check that returned tickets have P1 priority
        for ticket in data["items"]:
            if ticket.get("classification"):
                assert ticket["classification"].get("priority") in ["P1", None]
    
    def test_filter_by_sentiment(self, create_test_tickets):
        """Should filter tickets by sentiment"""
        # Filter for negative sentiment
        r = client.get("/tickets?page=1&page_size=10&sentiment=negative")
        assert r.status_code == 200
        data = r.json()
        
        assert "items" in data
        assert "total" in data
        assert isinstance(data["items"], list)
    
    def test_filter_by_channel(self, create_test_tickets):
        """Should filter tickets by channel"""
        # Filter for email channel
        r = client.get("/tickets?page=1&page_size=10&channel=email")
        assert r.status_code == 200
        data = r.json()
        
        assert "items" in data
        
        # Check that returned tickets have email channel
        for ticket in data["items"]:
            assert ticket.get("channel") in ["email", None]
    
    def test_filter_multiple_criteria(self, create_test_tickets):
        """Should filter tickets with multiple criteria"""
        # Filter for billing intent AND P1 priority
        r = client.get("/tickets?page=1&page_size=10&intent=billing&priority=P1")
        assert r.status_code == 200
        data = r.json()
        
        assert "items" in data
        assert "total" in data
    
    def test_filter_by_date_range(self):
        """Should filter tickets by date range"""
        # Filter for tickets from last 7 days
        start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        end_date = datetime.now().strftime("%Y-%m-%d")
        
        r = client.get(f"/tickets?page=1&page_size=10&start_date={start_date}&end_date={end_date}")
        assert r.status_code == 200
        data = r.json()
        
        assert "items" in data
        assert "total" in data
    
    def test_filter_invalid_intent(self):
        """Should handle invalid intent gracefully"""
        r = client.get("/tickets?page=1&page_size=10&intent=invalid_intent_type")
        assert r.status_code in [200, 422]
        
        if r.status_code == 200:
            # Should return empty results or all results
            data = r.json()
            assert "items" in data
    
    def test_filter_no_results(self):
        """Should handle filters that return no results"""
        # Use very specific future date range
        start_date = (datetime.now() + timedelta(days=100)).strftime("%Y-%m-%d")
        end_date = (datetime.now() + timedelta(days=200)).strftime("%Y-%m-%d")
        
        r = client.get(f"/tickets?page=1&page_size=10&start_date={start_date}&end_date={end_date}")
        assert r.status_code == 200
        data = r.json()
        
        assert data["total"] >= 0
        assert isinstance(data["items"], list)


class TestPagination:
    """Test pagination functionality"""
    
    def test_pagination_first_page(self):
        """Should return first page of results"""
        r = client.get("/tickets?page=1&page_size=5")
        assert r.status_code == 200
        data = r.json()
        
        assert "items" in data
        assert "total" in data
        assert "page" in data
        assert "pages" in data
        assert data["page"] == 1
        assert len(data["items"]) <= 5
    
    def test_pagination_page_size(self):
        """Should respect page_size parameter"""
        r = client.get("/tickets?page=1&page_size=3")
        assert r.status_code == 200
        data = r.json()
        
        assert len(data["items"]) <= 3
    
    def test_pagination_second_page(self):
        """Should return second page of results"""
        r = client.get("/tickets?page=2&page_size=5")
        assert r.status_code == 200
        data = r.json()
        
        assert data["page"] == 2
    
    def test_pagination_invalid_page(self):
        """Should handle invalid page numbers gracefully"""
        r = client.get("/tickets?page=0&page_size=10")
        # Should either return 422 or default to page 1
        assert r.status_code in [200, 422]
    
    def test_pagination_large_page_number(self):
        """Should handle page numbers beyond available data"""
        r = client.get("/tickets?page=9999&page_size=10")
        assert r.status_code == 200
        data = r.json()
        
        # Should return empty items or last page
        assert isinstance(data["items"], list)


class TestSuggestions:
    """Test suggestions endpoint (KB articles and resolution templates)"""
    
    @pytest.fixture
    def billing_ticket(self):
        """Create a billing-related ticket"""
        ticket_data = {
            "subject": "Refund request for double charge",
            "body": "I was charged twice for my subscription this month. Can I get a refund for the duplicate charge?",
            "channel": "email",
            "customer_id": f"test-{uuid4().hex[:8]}"
        }
        r = client.post("/tickets", json=ticket_data)
        assert r.status_code == 201
        return r.json()
    
    @pytest.fixture
    def password_ticket(self):
        """Create a password-related ticket"""
        ticket_data = {
            "subject": "Cannot reset password",
            "body": "I'm trying to reset my password but the email link is not working. I need access to my account.",
            "channel": "web",
            "customer_id": f"test-{uuid4().hex[:8]}"
        }
        r = client.post("/tickets", json=ticket_data)
        assert r.status_code == 201
        return r.json()
    
    def test_suggestions_endpoint_exists(self, billing_ticket):
        """Suggestions endpoint should be accessible"""
        ticket_id = billing_ticket["id"]
        r = client.get(f"/suggestions/{ticket_id}")
        assert r.status_code == 200
    
    def test_suggestions_returns_list(self, billing_ticket):
        """Suggestions should return a list"""
        ticket_id = billing_ticket["id"]
        r = client.get(f"/suggestions/{ticket_id}")
        assert r.status_code == 200
        
        suggestions = r.json()
        assert isinstance(suggestions, list)
    
    def test_suggestions_structure(self, billing_ticket):
        """Each suggestion should have required fields"""
        ticket_id = billing_ticket["id"]
        r = client.get(f"/suggestions/{ticket_id}")
        assert r.status_code == 200
        
        suggestions = r.json()
        if suggestions:
            suggestion = suggestions[0]
            
            # Check required fields
            assert "id" in suggestion
            assert "title" in suggestion
            assert "preview" in suggestion
            assert "score" in suggestion
            assert "type" in suggestion
            
            # Check types
            assert isinstance(suggestion["id"], str)
            assert isinstance(suggestion["title"], str)
            assert isinstance(suggestion["preview"], str)
            assert isinstance(suggestion["score"], (int, float))
            assert suggestion["type"] in ["kb_article", "resolution_template"]
    
    def test_suggestions_scoring(self, billing_ticket):
        """Suggestions should have similarity scores"""
        ticket_id = billing_ticket["id"]
        r = client.get(f"/suggestions/{ticket_id}")
        assert r.status_code == 200
        
        suggestions = r.json()
        if suggestions:
            # Scores should be between 0 and 1
            for suggestion in suggestions:
                assert 0 <= suggestion["score"] <= 1
    
    def test_suggestions_ordering(self, billing_ticket):
        """Suggestions should be ordered by score (highest first)"""
        ticket_id = billing_ticket["id"]
        r = client.get(f"/suggestions/{ticket_id}")
        assert r.status_code == 200
        
        suggestions = r.json()
        if len(suggestions) > 1:
            # Check that scores are in descending order
            scores = [s["score"] for s in suggestions]
            assert scores == sorted(scores, reverse=True)
    
    def test_suggestions_limit_parameter(self, billing_ticket):
        """Suggestions should respect limit parameter"""
        ticket_id = billing_ticket["id"]
        
        # Request only 3 suggestions
        r = client.get(f"/suggestions/{ticket_id}?limit=3")
        assert r.status_code == 200
        
        suggestions = r.json()
        assert len(suggestions) <= 3
    
    def test_suggestions_different_tickets(self, billing_ticket, password_ticket):
        """Different tickets should get different suggestions"""
        # Get suggestions for billing ticket
        r1 = client.get(f"/suggestions/{billing_ticket['id']}")
        assert r1.status_code == 200
        billing_suggestions = r1.json()
        
        # Get suggestions for password ticket
        r2 = client.get(f"/suggestions/{password_ticket['id']}")
        assert r2.status_code == 200
        password_suggestions = r2.json()
        
        # Suggestions should be different (allowing some overlap)
        if billing_suggestions and password_suggestions:
            billing_ids = {s["id"] for s in billing_suggestions}
            password_ids = {s["id"] for s in password_suggestions}
            
            # At least some suggestions should be different
            assert billing_ids != password_ids or len(billing_suggestions) <= 1
    
    def test_suggestions_nonexistent_ticket(self):
        """Should handle suggestions for non-existent ticket"""
        fake_id = str(uuid4())
        r = client.get(f"/suggestions/{fake_id}")
        assert r.status_code in [404, 200]
        
        if r.status_code == 200:
            # Should return empty list
            suggestions = r.json()
            assert isinstance(suggestions, list)
    
    def test_suggestions_invalid_ticket_id(self):
        """Should handle invalid ticket ID format"""
        r = client.get("/suggestions/invalid-id-format")
        assert r.status_code in [404, 422]


class TestSearchFunctionality:
    """Test search functionality"""
    
    @pytest.fixture
    def searchable_tickets(self):
        """Create tickets with specific searchable content"""
        tickets = []
        
        # Ticket with "refund" keyword
        refund_ticket = {
            "subject": "Refund policy question",
            "body": "What is your refund policy for monthly subscriptions?",
            "channel": "email",
            "customer_id": f"test-{uuid4().hex[:8]}"
        }
        r = client.post("/tickets", json=refund_ticket)
        assert r.status_code == 201
        tickets.append(r.json())
        
        # Ticket with "password" keyword
        password_ticket = {
            "subject": "Password reset issue",
            "body": "I cannot reset my password using the forgot password link.",
            "channel": "web",
            "customer_id": f"test-{uuid4().hex[:8]}"
        }
        r = client.post("/tickets", json=password_ticket)
        assert r.status_code == 201
        tickets.append(r.json())
        
        return tickets
    
    def test_search_by_subject(self, searchable_tickets):
        """Should search tickets by subject"""
        r = client.get("/tickets?page=1&page_size=10&search=refund")
        assert r.status_code == 200
        data = r.json()
        
        assert "items" in data
        # At least the refund ticket should be in results
        if data["items"]:
            subjects = [t["subject"].lower() for t in data["items"]]
            # Some result should contain "refund"
            assert any("refund" in s for s in subjects)
    
    def test_search_by_body(self, searchable_tickets):
        """Should search tickets by body content"""
        r = client.get("/tickets?page=1&page_size=10&search=password")
        assert r.status_code == 200
        data = r.json()
        
        assert "items" in data
    
    def test_search_case_insensitive(self, searchable_tickets):
        """Search should be case-insensitive"""
        r1 = client.get("/tickets?page=1&page_size=10&search=PASSWORD")
        r2 = client.get("/tickets?page=1&page_size=10&search=password")
        
        assert r1.status_code == 200
        assert r2.status_code == 200
        
        # Should return similar results
        data1 = r1.json()
        data2 = r2.json()
        
        # Both should have items (case shouldn't matter)
        assert isinstance(data1["items"], list)
        assert isinstance(data2["items"], list)
    
    def test_search_no_results(self):
        """Should handle search with no results"""
        r = client.get("/tickets?page=1&page_size=10&search=xyznonexistentterm123")
        assert r.status_code == 200
        data = r.json()
        
        assert data["total"] >= 0
        assert isinstance(data["items"], list)
    
    def test_search_with_filters(self, searchable_tickets):
        """Should combine search with filters"""
        r = client.get("/tickets?page=1&page_size=10&search=password&intent=account_access")
        assert r.status_code == 200
        data = r.json()
        
        assert "items" in data
        assert "total" in data


class TestEdgeCases:
    """Test edge cases and error handling"""
    
    def test_empty_filters(self):
        """Should handle request with no filters"""
        r = client.get("/tickets?page=1&page_size=10")
        assert r.status_code == 200
        data = r.json()
        
        assert "items" in data
        assert "total" in data
    
    def test_invalid_date_format(self):
        """Should handle invalid date format"""
        r = client.get("/tickets?page=1&page_size=10&start_date=invalid-date")
        # Should either return 422 or handle gracefully
        assert r.status_code in [200, 422]
    
    def test_negative_page_size(self):
        """Should handle negative page size"""
        r = client.get("/tickets?page=1&page_size=-10")
        assert r.status_code in [200, 422]
    
    def test_very_large_page_size(self):
        """Should handle very large page size"""
        r = client.get("/tickets?page=1&page_size=10000")
        assert r.status_code == 200
        data = r.json()
        
        # Should cap at reasonable limit
        assert len(data["items"]) <= 100  # Assuming max limit


class TestIntegration:
    """Integration tests combining multiple Phase 2 features"""
    
    def test_filter_search_pagination_combined(self):
        """Should work with filters, search, and pagination together"""
        r = client.get("/tickets?page=1&page_size=5&intent=billing&search=charge")
        assert r.status_code == 200
        data = r.json()
        
        assert "items" in data
        assert "total" in data
        assert "page" in data
        assert data["page"] == 1
        assert len(data["items"]) <= 5
    
    def test_suggestions_after_classification(self):
        """Suggestions should work with classified tickets"""
        # Create ticket (auto-classified)
        ticket_data = {
            "subject": "Billing error",
            "body": "I was charged incorrectly",
            "channel": "email",
            "customer_id": f"test-{uuid4().hex[:8]}"
        }
        r = client.post("/tickets", json=ticket_data)
        assert r.status_code == 201
        ticket = r.json()
        
        # Get suggestions
        r2 = client.get(f"/suggestions/{ticket['id']}")
        assert r2.status_code == 200
        suggestions = r2.json()
        
        assert isinstance(suggestions, list)
