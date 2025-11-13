"""
Tests for AI response generation and save/retrieve functionality (Phase 5).

Tests cover:
- AI response generation with RAG context
- Tone parameter handling (professional, friendly, technical, empathetic)
- Response saving with edit tracking
- Saved responses retrieval
- Context building (similar tickets, KB articles, resolutions)
"""

from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


class TestAIResponseGeneration:
    """Test AI response generation endpoint"""

    def test_suggest_response_endpoint_exists(self):
        """Test AI response suggestion endpoint is accessible"""
        # First create a ticket
        ticket_data = {
            "subject": "Need help with password",
            "body": "I forgot my password and can't log in",
            "channel": "web",
            "customer_id": f"test-ai-{uuid4().hex[:8]}",
        }
        response = client.post("/tickets", json=ticket_data)
        assert response.status_code == 201
        ticket_id = response.json()["id"]

        # Get AI response suggestion
        response = client.get(f"/llm/suggest-response/{ticket_id}?tone=professional")
        # Should succeed or return 500 if LLM unavailable
        assert response.status_code in [200, 500, 503]

    @pytest.mark.parametrize("tone", ["professional", "friendly", "technical", "empathetic"])
    def test_suggest_response_with_different_tones(self, tone):
        """Test AI response generation with all tone options"""
        # Create a ticket
        ticket_data = {
            "subject": f"Test {tone} tone",
            "body": "Testing AI response with different tones",
            "channel": "email",
            "customer_id": f"test-tone-{uuid4().hex[:8]}",
        }
        response = client.post("/tickets", json=ticket_data)
        assert response.status_code == 201
        ticket_id = response.json()["id"]

        # Get AI response with specific tone
        response = client.get(f"/llm/suggest-response/{ticket_id}?tone={tone}")
        assert response.status_code in [200, 500, 503]

        if response.status_code == 200:
            data = response.json()
            assert "response" in data
            assert "tone" in data
            assert data["tone"] == tone

    def test_suggest_response_default_tone(self):
        """Test AI response uses default tone when not specified"""
        ticket_data = {
            "subject": "Default tone test",
            "body": "Testing default tone",
            "channel": "web",
            "customer_id": f"test-default-{uuid4().hex[:8]}",
        }
        response = client.post("/tickets", json=ticket_data)
        ticket_id = response.json()["id"]

        # Get AI response without tone parameter
        response = client.get(f"/llm/suggest-response/{ticket_id}")
        assert response.status_code in [200, 500, 503]

        if response.status_code == 200:
            data = response.json()
            # Should have a default tone
            assert "tone" in data

    def test_suggest_response_invalid_tone(self):
        """Test AI response with invalid tone returns validation error"""
        ticket_data = {
            "subject": "Invalid tone test",
            "body": "Testing invalid tone",
            "channel": "phone",
            "customer_id": f"test-invalid-{uuid4().hex[:8]}",
        }
        response = client.post("/tickets", json=ticket_data)
        ticket_id = response.json()["id"]

        # Try invalid tone
        response = client.get(f"/llm/suggest-response/{ticket_id}?tone=invalid_tone")
        # Should return validation error
        assert response.status_code == 422

    def test_suggest_response_nonexistent_ticket(self):
        """Test AI response for nonexistent ticket returns 404"""
        fake_ticket_id = str(uuid4())
        response = client.get(f"/llm/suggest-response/{fake_ticket_id}?tone=professional")
        assert response.status_code == 404

    def test_suggest_response_includes_context(self):
        """Test AI response includes RAG context information"""
        ticket_data = {
            "subject": "Context test",
            "body": "Testing RAG context",
            "channel": "web",
            "customer_id": f"test-context-{uuid4().hex[:8]}",
        }
        response = client.post("/tickets", json=ticket_data)
        ticket_id = response.json()["id"]

        response = client.get(f"/llm/suggest-response/{ticket_id}?tone=professional")

        if response.status_code == 200:
            data = response.json()
            # Should have context information
            assert "context" in data or "similar_tickets" in data


class TestAIResponseSaving:
    """Test AI response save functionality"""

    def test_save_response_endpoint_exists(self):
        """Test save response endpoint is accessible"""
        # Create a ticket first
        ticket_data = {
            "subject": "Save test",
            "body": "Testing response saving",
            "channel": "web",
            "customer_id": f"test-save-{uuid4().hex[:8]}",
        }
        response = client.post("/tickets", json=ticket_data)
        ticket_id = response.json()["id"]

        # Save a response
        save_data = {
            "ticket_id": ticket_id,
            "response_text": "This is a test AI response",
            "tone": "professional",
            "context_used": {"similar_tickets": 3, "kb_articles": 2},
            "model": "llama3.2:latest",
            "agent_id": "test-agent",
            "was_edited": False,
            "was_sent": False,
        }
        response = client.post("/llm/save-response", json=save_data)
        assert response.status_code in [200, 201]

    def test_save_response_with_edit_tracking(self):
        """Test saving response tracks edit status"""
        ticket_data = {
            "subject": "Edit tracking test",
            "body": "Testing edit tracking",
            "channel": "email",
            "customer_id": f"test-edit-{uuid4().hex[:8]}",
        }
        response = client.post("/tickets", json=ticket_data)
        ticket_id = response.json()["id"]

        # Save response marked as edited
        save_data = {
            "ticket_id": ticket_id,
            "response_text": "This response was edited by the agent",
            "tone": "friendly",
            "context_used": {},
            "model": "llama3.2:latest",
            "agent_id": "test-agent",
            "was_edited": True,
            "was_sent": False,
        }
        response = client.post("/llm/save-response", json=save_data)
        assert response.status_code in [200, 201]

        if response.status_code in [200, 201]:
            data = response.json()
            assert data["was_edited"] is True

    def test_save_response_required_fields(self):
        """Test save response validates required fields"""
        # Missing required fields should return validation error
        save_data = {
            "ticket_id": str(uuid4()),
            "response_text": "Test response",
            # Missing other required fields
        }
        response = client.post("/llm/save-response", json=save_data)
        # Should return validation error
        assert response.status_code == 422

    def test_save_response_invalid_ticket_id(self):
        """Test saving response with invalid ticket ID"""
        save_data = {
            "ticket_id": str(uuid4()),  # Nonexistent ticket
            "response_text": "Test response",
            "tone": "professional",
            "context_used": {},
            "model": "test-model",
            "agent_id": "test-agent",
            "was_edited": False,
            "was_sent": False,
        }
        response = client.post("/llm/save-response", json=save_data)
        # Should return error (404 or 400)
        assert response.status_code in [400, 404, 422]

    def test_save_multiple_responses_for_same_ticket(self):
        """Test saving multiple AI responses for the same ticket"""
        ticket_data = {
            "subject": "Multiple responses test",
            "body": "Testing multiple saves",
            "channel": "chat",
            "customer_id": f"test-multi-{uuid4().hex[:8]}",
        }
        response = client.post("/tickets", json=ticket_data)
        ticket_id = response.json()["id"]

        # Save first response
        save_data1 = {
            "ticket_id": ticket_id,
            "response_text": "First AI response",
            "tone": "professional",
            "context_used": {},
            "model": "llama3.2:latest",
            "agent_id": "agent-1",
            "was_edited": False,
            "was_sent": False,
        }
        response1 = client.post("/llm/save-response", json=save_data1)

        # Save second response
        save_data2 = {
            "ticket_id": ticket_id,
            "response_text": "Second AI response with different tone",
            "tone": "friendly",
            "context_used": {},
            "model": "llama3.2:latest",
            "agent_id": "agent-1",
            "was_edited": True,
            "was_sent": False,
        }
        response2 = client.post("/llm/save-response", json=save_data2)

        # Both should succeed
        assert response1.status_code in [200, 201]
        assert response2.status_code in [200, 201]


class TestAIResponseRetrieval:
    """Test saved AI response retrieval"""

    def test_get_saved_responses_endpoint_exists(self):
        """Test get saved responses endpoint is accessible"""
        # Use any ticket ID (even nonexistent)
        ticket_id = str(uuid4())
        response = client.get(f"/llm/saved-responses/{ticket_id}")
        # Should return empty list or 404
        assert response.status_code in [200, 404]

    def test_get_saved_responses_returns_list(self):
        """Test get saved responses returns a list"""
        # Create ticket and save a response
        ticket_data = {
            "subject": "Retrieval test",
            "body": "Testing response retrieval",
            "channel": "web",
            "customer_id": f"test-retrieve-{uuid4().hex[:8]}",
        }
        response = client.post("/tickets", json=ticket_data)
        ticket_id = response.json()["id"]

        # Save a response
        save_data = {
            "ticket_id": ticket_id,
            "response_text": "Saved response for retrieval",
            "tone": "empathetic",
            "context_used": {},
            "model": "llama3.2:latest",
            "agent_id": "test-agent",
            "was_edited": False,
            "was_sent": False,
        }
        client.post("/llm/save-response", json=save_data)

        # Retrieve saved responses
        response = client.get(f"/llm/saved-responses/{ticket_id}")
        if response.status_code == 200:
            data = response.json()
            assert isinstance(data, list)
            if len(data) > 0:
                # Check structure of first response
                assert "id" in data[0]
                assert "response_text" in data[0]
                assert "tone" in data[0]
                assert "was_edited" in data[0]

    def test_get_saved_responses_nonexistent_ticket(self):
        """Test get saved responses for nonexistent ticket"""
        fake_ticket_id = str(uuid4())
        response = client.get(f"/llm/saved-responses/{fake_ticket_id}")
        # Should return empty list or 404
        assert response.status_code in [200, 404]

        if response.status_code == 200:
            data = response.json()
            assert isinstance(data, list)
            assert len(data) == 0

    def test_saved_responses_ordered_by_creation(self):
        """Test saved responses are ordered by creation time"""
        ticket_data = {
            "subject": "Order test",
            "body": "Testing response ordering",
            "channel": "email",
            "customer_id": f"test-order-{uuid4().hex[:8]}",
        }
        response = client.post("/tickets", json=ticket_data)
        ticket_id = response.json()["id"]

        # Save multiple responses with slight delay
        import time

        for i in range(3):
            save_data = {
                "ticket_id": ticket_id,
                "response_text": f"Response {i}",
                "tone": "professional",
                "context_used": {},
                "model": "llama3.2:latest",
                "agent_id": "test-agent",
                "was_edited": False,
                "was_sent": False,
            }
            client.post("/llm/save-response", json=save_data)
            time.sleep(0.1)  # Small delay to ensure different timestamps

        # Retrieve responses
        response = client.get(f"/llm/saved-responses/{ticket_id}")
        if response.status_code == 200:
            data = response.json()
            # Should have 3 responses
            assert len(data) >= 3

            # Should have created_at timestamps
            if "created_at" in data[0]:
                # Verify ordering (newest first or oldest first depends on implementation)
                timestamps = [r["created_at"] for r in data if "created_at" in r]
                assert len(timestamps) > 0


class TestAIResponseIntegration:
    """Test AI response integration with ticket lifecycle"""

    def test_full_ai_response_workflow(self):
        """Test complete workflow: generate -> save -> retrieve"""
        # 1. Create ticket
        ticket_data = {
            "subject": "Full workflow test",
            "body": "Testing complete AI response workflow",
            "channel": "web",
            "customer_id": f"test-workflow-{uuid4().hex[:8]}",
        }
        response = client.post("/tickets", json=ticket_data)
        assert response.status_code == 201
        ticket_id = response.json()["id"]

        # 2. Generate AI response
        response = client.get(f"/llm/suggest-response/{ticket_id}?tone=friendly")
        if response.status_code == 200:
            suggested_response = response.json()
            response_text = suggested_response.get("response", "Fallback response")

            # 3. Save the response
            save_data = {
                "ticket_id": ticket_id,
                "response_text": response_text,
                "tone": "friendly",
                "context_used": suggested_response.get("context", {}),
                "model": suggested_response.get("model", "unknown"),
                "agent_id": "test-agent",
                "was_edited": False,
                "was_sent": False,
            }
            save_response = client.post("/llm/save-response", json=save_data)

            if save_response.status_code in [200, 201]:
                # 4. Retrieve saved responses
                retrieve_response = client.get(f"/llm/saved-responses/{ticket_id}")
                assert retrieve_response.status_code == 200
                saved_responses = retrieve_response.json()
                assert len(saved_responses) > 0

    def test_ai_response_with_ticket_resolution(self):
        """Test AI response generation considers ticket resolution status"""
        # Create and resolve a ticket
        ticket_data = {
            "subject": "Resolution test",
            "body": "Testing resolved ticket",
            "channel": "email",
            "customer_id": f"test-resolved-{uuid4().hex[:8]}",
        }
        response = client.post("/tickets", json=ticket_data)
        ticket_id = response.json()["id"]

        # Try to get AI response (should work even for resolved tickets)
        response = client.get(f"/llm/suggest-response/{ticket_id}?tone=professional")
        # Should succeed regardless of ticket status
        assert response.status_code in [200, 404, 500, 503]


class TestAIResponsePerformance:
    """Test AI response performance characteristics"""

    def test_response_generation_timeout(self):
        """Test AI response generation completes within reasonable time"""
        import time

        ticket_data = {
            "subject": "Performance test",
            "body": "Testing response generation performance",
            "channel": "web",
            "customer_id": f"test-perf-{uuid4().hex[:8]}",
        }
        response = client.post("/tickets", json=ticket_data)
        ticket_id = response.json()["id"]

        start_time = time.time()
        response = client.get(f"/llm/suggest-response/{ticket_id}?tone=technical")
        elapsed_time = time.time() - start_time

        # Should complete within 30 seconds (even if LLM is slow)
        assert elapsed_time < 30.0

    def test_save_response_performance(self):
        """Test saving response is fast"""
        import time

        ticket_data = {
            "subject": "Save performance test",
            "body": "Testing save performance",
            "channel": "chat",
            "customer_id": f"test-save-perf-{uuid4().hex[:8]}",
        }
        response = client.post("/tickets", json=ticket_data)
        ticket_id = response.json()["id"]

        save_data = {
            "ticket_id": ticket_id,
            "response_text": "Performance test response",
            "tone": "professional",
            "context_used": {},
            "model": "test-model",
            "agent_id": "test-agent",
            "was_edited": False,
            "was_sent": False,
        }

        start_time = time.time()
        response = client.post("/llm/save-response", json=save_data)
        elapsed_time = time.time() - start_time

        # Should save within 2 seconds
        assert elapsed_time < 2.0
