"""
LLM service for meaning generation.

Story 2.4 AC 8: Stub implementation until OpenRouter integration (Story 3.1).
Returns None (graceful degradation) until LLM library is integrated.
"""
from typing import Optional
from loguru import logger


class LLMService:
    """
    LLM service for generating meaning/interpretation of somethings.

    STUB IMPLEMENTATION: Returns None until OpenRouter is integrated in Epic 3 Story 3.1.

    Future Implementation (Story 3.1):
    - Model: OpenRouter mistralai/mistral-7b-instruct:free
    - Temperature: 0.6
    - Max tokens: 100
    - Output: 1-2 sentence meaning/interpretation
    """

    _instance = None

    def __new__(cls):
        """Singleton pattern to ensure only one LLMService instance."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            logger.info("LLMService initialized (stub mode - returns None)")
        return cls._instance

    def generate_meaning(self, content: str) -> Optional[str]:
        """
        Generate 1-2 sentence meaning/interpretation for content.

        STUB IMPLEMENTATION: Always returns None until OpenRouter integrated (Story 3.1).

        Args:
            content: Text content to generate meaning for

        Returns:
            None (stub implementation - graceful degradation)

        Future Behavior (Story 3.1):
            - Will call OpenRouter API with system prompt
            - Temperature: 0.6, max_tokens: 100
            - Returns 1-2 sentence interpretation
            - Returns None if LLM fails
        """
        if not content or not content.strip():
            logger.debug("generate_meaning called with empty content")
            return None

        logger.debug(
            f"generate_meaning stub called for content (length: {len(content)}) - "
            "returning None (LLM not implemented yet)"
        )

        # STUB: Return None until OpenRouter integration in Story 3.1
        # This satisfies AC 8: "Returns None if LLM fails"
        return None


# Global singleton instance
# Matches pattern from embedding_service.py (Story 2.2)
llm_service = LLMService()
