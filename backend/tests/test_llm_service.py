"""
Tests for LLM service and AI response generation.
"""

from unittest.mock import AsyncMock, Mock, patch

import pytest

from app.services.llm import LLMService


class TestLLMService:
    """Test suite for LLM service"""

    @pytest.fixture
    def llm_service(self):
        """Create LLM service instance"""
        return LLMService()

    @pytest.fixture
    def sample_context(self):
        """Sample RAG context"""
        return [
            {
                "type": "ticket",
                "similarity": 0.92,
                "data": {
                    "id": "123",
                    "subject": "Password reset issue",
                    "body": "I can't reset my password",
                },
            },
            {
                "type": "kb",
                "data": {
                    "id": "456",
                    "title": "Password Reset Guide",
                    "body": "To reset your password, click the forgot password link...",
                },
            },
        ]

    def test_llm_service_initialization(self, llm_service):
        """Test LLM service initializes with correct defaults"""
        assert llm_service.ollama_url in ("http://ollama:11434", "http://localhost:11434")
        assert llm_service.use_ollama

    def test_build_context_string_with_tickets(self, llm_service, sample_context):
        """Test context string building with ticket data"""
        context_str = llm_service._build_context_string(sample_context)

        assert "Similar Ticket:" in context_str
        assert "Password reset issue" in context_str
        assert "I can't reset my password" in context_str

    def test_build_context_string_with_kb_articles(self, llm_service, sample_context):
        """Test context string building with KB articles"""
        context_str = llm_service._build_context_string(sample_context)

        assert "Knowledge Base Article:" in context_str
        assert "Password Reset Guide" in context_str
        assert "To reset your password" in context_str

    def test_build_context_string_empty(self, llm_service):
        """Test context string building with empty context"""
        context_str = llm_service._build_context_string([])
        assert context_str == "No relevant context available."

    @pytest.mark.parametrize(
        "tone,expected_instruction",
        [
            ("professional", "formal"),
            ("friendly", "friendly"),
            ("technical", "technical"),
            ("empathetic", "empathetic"),
        ],
    )
    def test_build_prompt_with_different_tones(
        self, llm_service, sample_context, tone, expected_instruction
    ):
        """Test prompt building with different tones"""
        prompt = llm_service._build_prompt(
            "Password reset issue",
            "I can't reset my password",
            llm_service._build_context_string(sample_context),
            tone,
        )

        assert expected_instruction in prompt.lower()
        assert "Password reset issue" in prompt
        assert "I can't reset my password" in prompt

    @pytest.mark.asyncio
    async def test_generate_with_ollama_success(self, llm_service):
        """Test successful response generation with Ollama"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"response": "Thank you for contacting support..."}

        with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
            mock_post.return_value = mock_response

            response = await llm_service._generate_with_ollama("Test prompt")

            assert response == "Thank you for contacting support..."

    @pytest.mark.asyncio
    async def test_generate_with_ollama_connection_error(self, llm_service):
        """Test Ollama connection error handling"""
        with patch("httpx.AsyncClient.post", side_effect=Exception("Connection refused")):
            response = await llm_service._generate_with_ollama("Test prompt")
            assert response is None

    @pytest.mark.asyncio
    async def test_generate_with_openai_success(self, llm_service):
        """Test successful response generation with OpenAI"""
        llm_service.openai_api_key = "test-key"

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "Here is a helpful response..."}}]
        }

        with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
            mock_post.return_value = mock_response

            response = await llm_service._generate_with_openai("Test prompt")

            assert response == "Here is a helpful response..."
            mock_post.assert_called_once()

    @pytest.mark.asyncio
    async def test_generate_with_openai_no_api_key(self, llm_service):
        """Test OpenAI generation without API key"""
        llm_service.openai_api_key = ""

        response = await llm_service._generate_with_openai("Test prompt")
        assert response is None

    @pytest.mark.asyncio
    async def test_generate_response_uses_ollama_when_enabled(self, llm_service, sample_context):
        """Test that Ollama is used when enabled"""
        llm_service.use_ollama = True

        with patch.object(
            llm_service, "_generate_with_ollama", new_callable=AsyncMock
        ) as mock_ollama:
            mock_ollama.return_value = "Ollama response"

            response = await llm_service.generate_response(
                "Test subject", "Test body", sample_context, "professional"
            )

            assert response == "Ollama response"
            mock_ollama.assert_called_once()

    @pytest.mark.asyncio
    async def test_generate_response_falls_back_to_openai(self, llm_service, sample_context):
        """Test fallback to OpenAI when Ollama is disabled"""
        llm_service.use_ollama = False
        llm_service.openai_api_key = "test-key"

        with patch.object(
            llm_service, "_generate_with_openai", new_callable=AsyncMock
        ) as mock_openai:
            mock_openai.return_value = "OpenAI response"

            response = await llm_service.generate_response(
                "Test subject", "Test body", sample_context, "friendly"
            )

            assert response == "OpenAI response"
            mock_openai.assert_called_once()

    def test_context_string_with_resolutions(self, llm_service):
        """Test context string building with resolution templates"""
        context = [
            {
                "type": "resolution",
                "data": {
                    "id": "789",
                    "title": "Password Reset Template",
                    "body": "Follow these steps to reset...",
                },
            }
        ]

        context_str = llm_service._build_context_string(context)

        assert "Resolution Template:" in context_str
        assert "Password Reset Template" in context_str
        assert "Follow these steps to reset..." in context_str

    def test_context_string_with_mixed_types(self, llm_service):
        """Test context string with all context types"""
        context = [
            {"type": "ticket", "similarity": 0.9, "data": {"subject": "Test 1", "body": "Body 1"}},
            {"type": "kb", "data": {"title": "KB 1", "body": "Content 1"}},
            {"type": "resolution", "data": {"title": "Resolution 1", "body": "Steps 1"}},
        ]

        context_str = llm_service._build_context_string(context)

        assert "Similar Ticket:" in context_str
        assert "Knowledge Base Article:" in context_str
        assert "Resolution Template:" in context_str
