"""
Chat Service with streaming RAG responses.

Implements personalized RAG pipeline with OpenRouter (Claude Haiku) streaming.
"""

import asyncio
import json
from typing import AsyncGenerator, Dict, List
import httpx
from sqlalchemy.orm import Session
from loguru import logger

from app.core.config import settings
from app.services.personalized_retrieval_service import personalized_retrieval_service
from app.services.embedding_service import embedding_service
from app.services.vector_service import vector_service


class ChatService:
    """
    Streaming chat service with personalized RAG retrieval.

    Pipeline:
    1. Generate query embedding
    2. FAISS search for top-50 candidates
    3. Re-rank using PersonalizedRetrievalService (hybrid scoring)
    4. Format context with circle information
    5. Stream Claude Haiku response via OpenRouter
    """

    def __init__(self):
        self.openrouter_base_url = "https://openrouter.ai/api/v1"
        self.model = "anthropic/claude-3-haiku"
        self.max_tokens = 500
        self.temperature = 0.7

    async def stream_chat(
        self,
        query: str,
        user_id: str,
        db: Session,
        top_k: int = 10
    ) -> AsyncGenerator[Dict, None]:
        """
        Stream chat response with personalized RAG context.

        Args:
            query: User's question
            user_id: User UUID for filtering
            db: Database session
            top_k: Number of somethings to include in context

        Yields:
            Dict events:
            - {"token": str} for each token
            - {"done": true, "circles_used": [str]} when complete
            - {"error": str} if failure
        """
        circles_used = []

        try:
            # Step 1: Generate query embedding
            query_embedding = embedding_service.generate_embedding(query)

            # Step 2: FAISS search for top-50 candidates
            faiss_results = await vector_service.search_similar(
                query_embedding,
                top_k=50
            )

            if not faiss_results:
                # No somethings found - inform user
                yield {"token": "I don't have any saved somethings to reference yet. "}
                yield {"token": "Try capturing some thoughts first!"}
                yield {"done": True, "circles_used": []}
                return

            # Step 3: Re-rank using hybrid scoring
            reranked_results = personalized_retrieval_service.retrieve_and_rerank(
                query_embedding=query_embedding,
                user_id=user_id,
                faiss_results=faiss_results,
                db=db,
                top_k=top_k
            )

            # Extract something IDs
            something_ids = [r["something_id"] for r in reranked_results]

            # Step 4: Format RAG context
            context = personalized_retrieval_service.format_rag_context(
                something_ids,
                db
            )

            # Extract circles used from context (parse circle names)
            # Simple extraction: find all [Circle: Name] patterns
            import re
            circle_matches = re.findall(r'\[Circle: ([^\]]+)\]', context)
            circles_used = list(set([c for c in circle_matches if c != "Uncategorized"]))

            # Step 5: Build system prompt with circle context
            system_prompt = self._build_system_prompt(context)

            # Step 6: Stream from OpenRouter
            async for event in self._stream_from_openrouter(query, system_prompt):
                yield event

            # Final event with circles used
            yield {"done": True, "circles_used": circles_used}

        except Exception as e:
            logger.error(f"Chat stream error: {e}")
            yield {"error": f"Failed to generate response: {str(e)}"}

    def _build_system_prompt(self, context: str) -> str:
        """Build system prompt with RAG context."""
        return f"""You are Pookie, a helpful assistant that answers questions based on the user's personal knowledge base.

{context}

Instructions:
- Answer the question using ONLY the information from the user's saved somethings above
- Reference specific circles when relevant (e.g., "Based on your Fitness circle...")
- If the answer isn't in the provided context, say so honestly
- Keep responses concise (2-4 sentences)
- Be conversational and friendly"""

    async def _stream_from_openrouter(
        self,
        query: str,
        system_prompt: str,
        max_retries: int = 2
    ) -> AsyncGenerator[Dict, None]:
        """
        Stream response from OpenRouter API with retry logic.

        Yields:
            Dict with {"token": str} for each token
        """
        if not settings.OPENROUTER_API_KEY:
            yield {"error": "Chat feature not configured. Please add OpenRouter API key."}
            return

        headers = {
            "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://pookie.app",
            "X-Title": "Pookie"
        }

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query}
            ],
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "stream": True
        }

        url = f"{self.openrouter_base_url}/chat/completions"

        for attempt in range(max_retries + 1):
            try:
                async with httpx.AsyncClient(timeout=30.0) as client:
                    async with client.stream("POST", url, json=payload, headers=headers) as response:
                        if response.status_code == 429:
                            # Rate limit - retry with backoff
                            if attempt < max_retries:
                                await asyncio.sleep(2 ** attempt)  # Exponential backoff
                                continue
                            yield {"error": "Service is busy. Please try again in a moment."}
                            return

                        if response.status_code == 401:
                            yield {"error": "Authentication failed. Please check API key configuration."}
                            return

                        if response.status_code == 402:
                            yield {"error": "API quota exceeded. Please add credits to your OpenRouter account."}
                            return

                        if response.status_code != 200:
                            error_text = await response.aread()
                            logger.error(f"OpenRouter error {response.status_code}: {error_text}")

                            # Retry on server errors
                            if response.status_code >= 500 and attempt < max_retries:
                                await asyncio.sleep(1)
                                continue

                            yield {"error": f"Service temporarily unavailable (error {response.status_code})"}
                            return

                        # Stream tokens
                        async for line in response.aiter_lines():
                            if not line.strip():
                                continue

                            if line.startswith("data: "):
                                line = line[6:]  # Remove "data: " prefix

                            if line == "[DONE]":
                                break

                            try:
                                data = json.loads(line)
                                if "choices" in data and len(data["choices"]) > 0:
                                    delta = data["choices"][0].get("delta", {})
                                    if "content" in delta:
                                        token = delta["content"]
                                        yield {"token": token}
                            except json.JSONDecodeError:
                                continue

                        # Success - break retry loop
                        break

            except httpx.TimeoutException:
                if attempt < max_retries:
                    logger.warning(f"OpenRouter timeout, retrying... (attempt {attempt + 1})")
                    await asyncio.sleep(1)
                    continue
                logger.error("OpenRouter request timeout after retries")
                yield {"error": "Request timed out. Please try again."}
                return

            except httpx.ConnectError:
                if attempt < max_retries:
                    logger.warning(f"OpenRouter connection error, retrying... (attempt {attempt + 1})")
                    await asyncio.sleep(2)
                    continue
                logger.error("OpenRouter connection failed after retries")
                yield {"error": "Unable to connect to chat service. Please check your internet connection."}
                return

            except Exception as e:
                logger.error(f"OpenRouter streaming error: {e}")
                yield {"error": "An unexpected error occurred. Please try again."}
                return


# Singleton instance
chat_service = ChatService()
