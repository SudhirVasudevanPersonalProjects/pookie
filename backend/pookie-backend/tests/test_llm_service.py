"""
Tests for LLM service meaning generation.

Story 2.4 AC 8: Stub implementation returns None until OpenRouter integrated (Story 3.1).
"""
import pytest
from app.services.llm_service import LLMService


class TestLLMServiceMeaningGeneration:
    """Test meaning generation functionality."""

    def test_generate_meaning_returns_none_when_not_implemented(self):
        """Test generate_meaning returns None when LLM not available (stub)."""
        llm_service = LLMService()
        result = llm_service.generate_meaning("I want to learn piano")

        # Stub implementation returns None (graceful degradation)
        assert result is None

    def test_generate_meaning_with_empty_content(self):
        """Test generate_meaning handles empty content gracefully."""
        llm_service = LLMService()
        result = llm_service.generate_meaning("")

        assert result is None

    def test_generate_meaning_with_long_content(self):
        """Test generate_meaning handles long content."""
        llm_service = LLMService()
        long_content = "I want to learn piano " * 100
        result = llm_service.generate_meaning(long_content)

        # Should return None (stub implementation)
        assert result is None

    def test_llm_service_is_singleton(self):
        """Test LLMService follows singleton pattern like other services."""
        service1 = LLMService()
        service2 = LLMService()

        # Should be the same instance
        assert service1 is service2
