"""
LLM service for generating response suggestions using Ollama or OpenAI.
"""

import os
from typing import Dict, List, Optional

import httpx

from app.core.errors import logger


class LLMService:
    """Service for LLM-based response generation"""

    def __init__(self):
        self.ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434")
        self.openai_api_key = os.getenv("OPENAI_API_KEY", "")
        self.model = os.getenv("LLM_MODEL", "phi3:mini")
        self.use_ollama = os.getenv("USE_OLLAMA", "true").lower() == "true"

    async def generate_response(
        self, ticket_subject: str, ticket_body: str, context: List[Dict], tone: str = "professional"
    ) -> Optional[str]:
        """
        Generate a response suggestion using RAG.

        Args:
            ticket_subject: Subject of the ticket
            ticket_body: Body/description of the ticket
            context: List of relevant context (similar tickets, KB articles)
            tone: Response tone (professional, friendly, technical)

        Returns:
            Generated response text or None if generation fails
        """
        try:
            # Build context string from similar tickets and KB articles
            context_str = self._build_context_string(context)

            # Build prompt
            prompt = self._build_prompt(ticket_subject, ticket_body, context_str, tone)

            # Generate response
            if self.use_ollama:
                return await self._generate_with_ollama(prompt)
            else:
                return await self._generate_with_openai(prompt)

        except Exception as e:
            logger.error(f"LLM generation failed: {e}")
            return None

    def _build_context_string(self, context: List[Dict]) -> str:
        """Build context string from similar tickets and KB articles"""
        context_parts = []

        for item in context:
            if item.get("type") == "ticket":
                ticket = item.get("data", {})
                context_parts.append(
                    f"Similar Ticket:\n"
                    f"Subject: {ticket.get('subject', 'N/A')}\n"
                    f"Issue: {ticket.get('body', 'N/A')[:200]}...\n"
                )
            elif item.get("type") == "kb":
                kb = item.get("data", {})
                context_parts.append(
                    f"Knowledge Base Article:\n"
                    f"Title: {kb.get('title', 'N/A')}\n"
                    f"Content: {kb.get('body', 'N/A')[:200]}...\n"
                )
            elif item.get("type") == "resolution":
                res = item.get("data", {})
                context_parts.append(
                    f"Resolution Template:\n"
                    f"Title: {res.get('title', 'N/A')}\n"
                    f"Solution: {res.get('body', 'N/A')[:200]}...\n"
                )

        return "\n---\n".join(context_parts) if context_parts else "No relevant context available."

    def _build_prompt(self, subject: str, body: str, context: str, tone: str) -> str:
        """Build the prompt for LLM"""
        tone_instructions = {
            "professional": "Use a professional and formal tone.",
            "friendly": "Use a friendly and approachable tone.",
            "technical": "Use a technical and detailed tone with specific explanations.",
            "empathetic": "Use an empathetic and understanding tone.",
        }

        tone_instruction = tone_instructions.get(tone, tone_instructions["professional"])

        prompt = f"""You are a helpful customer support assistant. \
Generate a response to the following support ticket.

{tone_instruction}

TICKET:
Subject: {subject}
Description: {body}

RELEVANT CONTEXT:
{context}

Generate a helpful, accurate, and actionable response that addresses the customer's issue. \
If the context includes solutions or KB articles, reference them in your response. \
Keep the response concise (2-3 paragraphs maximum).

RESPONSE:"""

        return prompt

    async def _generate_with_ollama(self, prompt: str) -> Optional[str]:
        """Generate response using Ollama"""
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f"{self.ollama_url}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        "stream": False,
                        "options": {"temperature": 0.7, "top_p": 0.9, "max_tokens": 500},
                    },
                )

                if response.status_code == 200:
                    result = response.json()
                    return result.get("response", "").strip()
                else:
                    logger.error(f"Ollama request failed: {response.status_code}")
                    return None

        except httpx.ConnectError:
            logger.error(f"Could not connect to Ollama at {self.ollama_url}")
            return None
        except Exception as e:
            logger.error(f"Ollama generation error: {e}")
            return None

    async def _generate_with_openai(self, prompt: str) -> Optional[str]:
        """Generate response using OpenAI API"""
        if not self.openai_api_key:
            logger.error("OpenAI API key not configured")
            return None

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.openai_api_key}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": "gpt-3.5-turbo",
                        "messages": [
                            {
                                "role": "system",
                                "content": "You are a helpful customer support assistant.",
                            },
                            {"role": "user", "content": prompt},
                        ],
                        "temperature": 0.7,
                        "max_tokens": 500,
                    },
                )

                if response.status_code == 200:
                    result = response.json()
                    return result["choices"][0]["message"]["content"].strip()
                else:
                    logger.error(f"OpenAI request failed: {response.status_code}")
                    return None

        except Exception as e:
            logger.error(f"OpenAI generation error: {e}")
            return None


# Global LLM service instance
llm_service = LLMService()
