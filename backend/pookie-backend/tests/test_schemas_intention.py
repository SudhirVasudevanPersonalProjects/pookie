"""
Tests for intention, action, and intention_care schemas.

RED phase: Write failing tests before implementing API endpoints.
"""
import pytest
from pydantic import ValidationError
from app.schemas.intention import (
    IntentionCreate,
    IntentionUpdate,
    IntentionStatus,
)
from app.schemas.action import ActionCreate
from app.schemas.intention_care import IntentionCareLinkRequest


class TestIntentionCreate:
    def test_valid_intention_create(self):
        """Valid intention creation."""
        data = {"intentionText": "Exercise 3x per week"}
        intention = IntentionCreate(**data)
        assert intention.intention_text == "Exercise 3x per week"

    def test_intention_text_too_short(self):
        """Reject empty intention text."""
        with pytest.raises(ValidationError) as exc_info:
            IntentionCreate(intentionText="")
        errors = exc_info.value.errors()
        assert any(e["loc"] == ("intentionText",) for e in errors)

    def test_intention_text_too_long(self):
        """Reject intention text > 500 chars."""
        long_text = "x" * 501
        with pytest.raises(ValidationError) as exc_info:
            IntentionCreate(intentionText=long_text)
        errors = exc_info.value.errors()
        assert any(e["loc"] == ("intentionText",) for e in errors)

    def test_intention_text_required(self):
        """Intention text is required."""
        with pytest.raises(ValidationError) as exc_info:
            IntentionCreate()
        errors = exc_info.value.errors()
        assert any(e["loc"] == ("intentionText",) for e in errors)


class TestIntentionUpdate:
    def test_valid_intention_update_text(self):
        """Update intention text only."""
        data = {"intentionText": "Updated text"}
        update = IntentionUpdate(**data)
        assert update.intention_text == "Updated text"
        assert update.status is None

    def test_valid_intention_update_status(self):
        """Update status only."""
        data = {"status": "completed"}
        update = IntentionUpdate(**data)
        assert update.status == IntentionStatus.completed
        assert update.intention_text is None

    def test_valid_intention_update_both(self):
        """Update both text and status."""
        data = {"intentionText": "New text", "status": "archived"}
        update = IntentionUpdate(**data)
        assert update.intention_text == "New text"
        assert update.status == IntentionStatus.archived

    def test_invalid_status_value(self):
        """Reject invalid status enum."""
        with pytest.raises(ValidationError):
            IntentionUpdate(status="invalid_status")

    def test_update_text_too_long(self):
        """Reject update text > 500 chars."""
        long_text = "x" * 501
        with pytest.raises(ValidationError):
            IntentionUpdate(intentionText=long_text)


class TestActionCreate:
    def test_valid_action_create(self):
        """Valid action creation."""
        data = {
            "actionText": "Went to gym",
            "timeElapsed": 60,
        }
        action = ActionCreate(**data)
        assert action.action_text == "Went to gym"
        assert action.time_elapsed == 60
        assert action.intention_ids is None

    def test_valid_action_with_intentions(self):
        """Create action linked to intentions."""
        data = {
            "actionText": "Meditated",
            "timeElapsed": 20,
            "intentionIds": [1, 2, 3],
        }
        action = ActionCreate(**data)
        assert action.intention_ids == [1, 2, 3]

    def test_action_text_required(self):
        """Action text is required."""
        with pytest.raises(ValidationError) as exc_info:
            ActionCreate(timeElapsed=30)
        errors = exc_info.value.errors()
        assert any(e["loc"] == ("actionText",) for e in errors)

    def test_time_elapsed_required(self):
        """Time elapsed is required."""
        with pytest.raises(ValidationError) as exc_info:
            ActionCreate(actionText="Did something")
        errors = exc_info.value.errors()
        assert any(e["loc"] == ("timeElapsed",) for e in errors)

    def test_time_elapsed_negative(self):
        """Reject negative time."""
        with pytest.raises(ValidationError):
            ActionCreate(actionText="Test", timeElapsed=-10)

    def test_time_elapsed_too_large(self):
        """Reject time > 360 minutes."""
        with pytest.raises(ValidationError):
            ActionCreate(actionText="Test", timeElapsed=361)

    def test_time_elapsed_boundary_values(self):
        """Accept boundary values 0 and 360."""
        action_min = ActionCreate(actionText="Test", timeElapsed=0)
        assert action_min.time_elapsed == 0

        action_max = ActionCreate(actionText="Test", timeElapsed=360)
        assert action_max.time_elapsed == 360

    def test_action_text_too_long(self):
        """Reject action text > 500 chars."""
        long_text = "x" * 501
        with pytest.raises(ValidationError):
            ActionCreate(actionText=long_text, timeElapsed=30)


class TestIntentionCareLinkRequest:
    def test_valid_link_request(self):
        """Valid link request with multiple somethings."""
        data = {"somethingIds": [1, 2, 3]}
        req = IntentionCareLinkRequest(**data)
        assert req.something_ids == [1, 2, 3]

    def test_empty_something_ids(self):
        """Reject empty list."""
        with pytest.raises(ValidationError):
            IntentionCareLinkRequest(somethingIds=[])

    def test_something_ids_required(self):
        """Something IDs are required."""
        with pytest.raises(ValidationError) as exc_info:
            IntentionCareLinkRequest()
        errors = exc_info.value.errors()
        assert any(e["loc"] == ("somethingIds",) for e in errors)
