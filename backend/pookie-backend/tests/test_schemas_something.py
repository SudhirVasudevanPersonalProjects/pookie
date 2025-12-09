"""
Tests for Something Pydantic schemas.

Verifies schema validation, field aliases (snake_case <-> camelCase),
and content type enum handling as specified in Story 2.1 acceptance criteria.
"""
import pytest
from pydantic import ValidationError
from app.schemas.something import (
    SomethingCreate,
    SomethingResponse,
    SomethingUpdateMeaning,
    ContentType
)
from datetime import datetime


class TestContentTypeEnum:
    """Test ContentType enum values and validation."""

    def test_content_type_enum_values(self):
        """Test all valid ContentType enum values."""
        assert ContentType.text.value == "text"
        assert ContentType.image.value == "image"
        assert ContentType.video.value == "video"
        assert ContentType.url.value == "url"

    def test_content_type_from_string(self):
        """Test creating ContentType from string."""
        assert ContentType("text") == ContentType.text
        assert ContentType("image") == ContentType.image
        assert ContentType("video") == ContentType.video
        assert ContentType("url") == ContentType.url


class TestSomethingCreateSchema:
    """Test SomethingCreate schema for API input validation."""

    def test_create_with_text_content(self):
        """Test creating something with text content."""
        schema = SomethingCreate(
            content="I want to get jacked",
            contentType=ContentType.text
        )
        assert schema.content == "I want to get jacked"
        assert schema.content_type == ContentType.text
        assert schema.media_url is None

    def test_create_with_image_and_media_url(self):
        """Test creating something with image type and media URL."""
        schema = SomethingCreate(
            content=None,
            contentType=ContentType.image,
            mediaUrl="https://storage.supabase.com/bucket/image.jpg"
        )
        assert schema.content is None
        assert schema.content_type == ContentType.image
        assert schema.media_url == "https://storage.supabase.com/bucket/image.jpg"

    def test_create_with_video(self):
        """Test creating something with video content."""
        schema = SomethingCreate(
            contentType=ContentType.video,
            mediaUrl="https://storage.supabase.com/bucket/video.mp4"
        )
        assert schema.content_type == ContentType.video
        assert schema.media_url == "https://storage.supabase.com/bucket/video.mp4"

    def test_create_with_url_type(self):
        """Test creating something with external URL."""
        schema = SomethingCreate(
            content="Check out this article",
            contentType=ContentType.url,
            mediaUrl="https://example.com/article"
        )
        assert schema.content_type == ContentType.url
        assert schema.media_url == "https://example.com/article"

    def test_create_defaults(self):
        """Test default values for optional fields."""
        schema = SomethingCreate(content="Test")
        assert schema.content_type == ContentType.text  # Default
        assert schema.media_url is None  # Default


class TestSomethingCamelCaseAliases:
    """Test Field aliases convert between snake_case and camelCase."""

    def test_create_accepts_camelcase(self):
        """Test schema accepts camelCase field names (from API)."""
        schema = SomethingCreate(
            content="Test",
            contentType=ContentType.text,
            mediaUrl="https://example.com/file.jpg"
        )
        assert schema.content_type == ContentType.text
        assert schema.media_url == "https://example.com/file.jpg"

    def test_create_accepts_snake_case(self):
        """Test schema accepts snake_case field names (internal)."""
        schema = SomethingCreate(
            content="Test",
            content_type=ContentType.text,
            media_url="https://example.com/file.jpg"
        )
        assert schema.content_type == ContentType.text
        assert schema.media_url == "https://example.com/file.jpg"

    def test_dump_with_aliases_uses_camelcase(self):
        """Test model_dump(by_alias=True) outputs camelCase."""
        schema = SomethingCreate(
            content="Test",
            content_type=ContentType.text,
            media_url="https://example.com/file.jpg"
        )
        dumped = schema.model_dump(by_alias=True)

        # Should have camelCase keys
        assert "contentType" in dumped
        assert "mediaUrl" in dumped
        # Should NOT have snake_case keys
        assert "content_type" not in dumped
        assert "media_url" not in dumped

    def test_dump_without_aliases_uses_snake_case(self):
        """Test model_dump() without alias uses snake_case."""
        schema = SomethingCreate(
            content="Test",
            contentType=ContentType.text
        )
        dumped = schema.model_dump(by_alias=False)

        # Should have snake_case keys
        assert "content_type" in dumped
        assert "media_url" in dumped


class TestSomethingResponseSchema:
    """Test SomethingResponse schema for API output."""

    def test_response_with_all_fields(self):
        """Test response schema with all fields populated."""
        response = SomethingResponse(
            id=1,
            userId="550e8400-e29b-41d4-a716-446655440000",
            content="I want to learn piano",
            contentType=ContentType.text,
            mediaUrl=None,
            meaning="User cares about personal growth",
            isMeaningUserEdited=False,
            noveltyScore=0.85,
            createdAt=datetime(2025, 1, 1, 12, 0, 0),
            updatedAt=datetime(2025, 1, 1, 12, 0, 0)
        )

        assert response.id == 1
        assert response.user_id == "550e8400-e29b-41d4-a716-446655440000"
        assert response.content == "I want to learn piano"
        assert response.meaning == "User cares about personal growth"
        assert response.novelty_score == 0.85
        assert response.is_meaning_user_edited is False

    def test_response_with_optional_fields_none(self):
        """Test response with optional fields as None."""
        response = SomethingResponse(
            id=2,
            userId="550e8400-e29b-41d4-a716-446655440000",
            contentType=ContentType.text,
            createdAt=datetime.now(),
            updatedAt=datetime.now()
        )

        assert response.content is None
        assert response.meaning is None
        assert response.novelty_score is None

    def test_response_camelcase_output(self):
        """Test response schema outputs camelCase for API."""
        response = SomethingResponse(
            id=1,
            userId="550e8400-e29b-41d4-a716-446655440000",
            content="Test",
            contentType=ContentType.text,
            createdAt=datetime.now(),
            updatedAt=datetime.now()
        )

        dumped = response.model_dump(by_alias=True)

        # Verify all camelCase fields
        assert "userId" in dumped
        assert "contentType" in dumped
        assert "mediaUrl" in dumped
        assert "isMeaningUserEdited" in dumped
        assert "noveltyScore" in dumped
        assert "createdAt" in dumped
        assert "updatedAt" in dumped

    def test_response_populate_by_name(self):
        """Test populate_by_name accepts both snake_case and camelCase."""
        # Test with camelCase
        response1 = SomethingResponse(
            id=1,
            userId="550e8400-e29b-41d4-a716-446655440000",
            contentType=ContentType.text,
            createdAt=datetime.now(),
            updatedAt=datetime.now()
        )

        # Test with snake_case
        response2 = SomethingResponse(
            id=1,
            user_id="550e8400-e29b-41d4-a716-446655440000",
            content_type=ContentType.text,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

        assert response1.user_id == response2.user_id
        assert response1.content_type == response2.content_type

    def test_response_from_attributes_config(self):
        """Test from_attributes=True allows ORM model conversion."""
        # This would be used with: SomethingResponse.model_validate(db_something)
        # Here we just verify the Config is set correctly
        assert SomethingResponse.model_config["from_attributes"] is True


class TestSomethingUpdateMeaningSchema:
    """Test SomethingUpdateMeaning schema for PATCH endpoint."""

    def test_update_meaning(self):
        """Test updating meaning field."""
        update = SomethingUpdateMeaning(meaning="Updated interpretation")
        assert update.meaning == "Updated interpretation"

    def test_update_meaning_required(self):
        """Test meaning field is required."""
        with pytest.raises(ValidationError):
            SomethingUpdateMeaning()  # Missing required 'meaning'


class TestSchemaValidation:
    """Test schema validation edge cases."""

    def test_create_with_empty_content(self):
        """Test creating with empty string content is valid."""
        schema = SomethingCreate(content="")
        assert schema.content == ""

    def test_response_with_media_only(self):
        """Test response for media-only something (no text content)."""
        response = SomethingResponse(
            id=1,
            userId="550e8400-e29b-41d4-a716-446655440000",
            content=None,
            contentType=ContentType.image,
            mediaUrl="https://example.com/image.jpg",
            createdAt=datetime.now(),
            updatedAt=datetime.now()
        )

        assert response.content is None
        assert response.content_type == ContentType.image
        assert response.media_url is not None

    def test_novelty_score_range(self):
        """Test novelty_score accepts floats in 0-1 range."""
        response = SomethingResponse(
            id=1,
            userId="550e8400-e29b-41d4-a716-446655440000",
            contentType=ContentType.text,
            noveltyScore=0.0,
            createdAt=datetime.now(),
            updatedAt=datetime.now()
        )
        assert response.novelty_score == 0.0

        response = SomethingResponse(
            id=2,
            userId="550e8400-e29b-41d4-a716-446655440000",
            contentType=ContentType.text,
            noveltyScore=1.0,
            createdAt=datetime.now(),
            updatedAt=datetime.now()
        )
        assert response.novelty_score == 1.0

        response = SomethingResponse(
            id=3,
            userId="550e8400-e29b-41d4-a716-446655440000",
            contentType=ContentType.text,
            noveltyScore=0.5,
            createdAt=datetime.now(),
            updatedAt=datetime.now()
        )
        assert response.novelty_score == 0.5

    def test_novelty_score_rejects_out_of_range(self):
        """Test novelty_score rejects values outside 0-1 range."""
        # Test value > 1.0
        with pytest.raises(ValidationError) as exc_info:
            SomethingResponse(
                id=1,
                userId="550e8400-e29b-41d4-a716-446655440000",
                contentType=ContentType.text,
                noveltyScore=1.5,
                createdAt=datetime.now(),
                updatedAt=datetime.now()
            )
        assert "less than or equal to 1" in str(exc_info.value).lower()

        # Test value < 0.0
        with pytest.raises(ValidationError) as exc_info:
            SomethingResponse(
                id=2,
                userId="550e8400-e29b-41d4-a716-446655440000",
                contentType=ContentType.text,
                noveltyScore=-0.5,
                createdAt=datetime.now(),
                updatedAt=datetime.now()
            )
        assert "greater than or equal to 0" in str(exc_info.value).lower()

    def test_invalid_content_type_rejected(self):
        """Test that invalid ContentType values are rejected."""
        with pytest.raises(ValueError) as exc_info:
            ContentType("invalid_type")
        assert "invalid_type" in str(exc_info.value).lower()

    def test_content_type_case_sensitive(self):
        """Test ContentType enum is case sensitive."""
        # Valid lowercase
        assert ContentType("text") == ContentType.text

        # Invalid uppercase should fail
        with pytest.raises(ValueError):
            ContentType("TEXT")
