"""
Database model tests for Pookie backend.

Tests CRUD operations, relationships, cascade behaviors, and constraints
for all database models as specified in Story 1.3 acceptance criteria.
"""
import pytest
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.models import (
    Base, User, Something, Circle, Intention, IntentionCare, Story,
    SomethingCircle, Action, ActionIntention, StoryAction
)
import uuid
from datetime import datetime


# Test database URL - must use PostgreSQL for PostgreSQL-specific types (JSONB, ARRAY, ENUM)
# Set TEST_DATABASE_URL or DATABASE_URL environment variable to your PostgreSQL connection string
TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    os.getenv("DATABASE_URL")
)

if not TEST_DATABASE_URL:
    raise RuntimeError(
        "TEST_DATABASE_URL or DATABASE_URL environment variable must be set.\n"
        "Example: export DATABASE_URL='postgresql://postgres:PASSWORD@HOST:5432/postgres'\n"
        "See README.md for Supabase connection string format."
    )

# Validate it's PostgreSQL (not SQLite)
if not TEST_DATABASE_URL.startswith("postgresql://"):
    raise RuntimeError(
        f"Tests require PostgreSQL database, got: {TEST_DATABASE_URL[:20]}...\n"
        "PostgreSQL-specific types (JSONB, ARRAY, ENUM) are not supported in SQLite."
    )


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database session for each test.

    This fixture:
    1. Creates all tables in PostgreSQL
    2. Provides a session for the test
    3. Cleans up by dropping all tables after the test

    Note: Uses real PostgreSQL database with create/drop for isolation.
    """
    engine = create_engine(TEST_DATABASE_URL)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    yield session

    session.close()
    Base.metadata.drop_all(engine)
    engine.dispose()


class TestUserModel:
    """Test User model CRUD operations and constraints."""

    def test_create_user(self, db_session):
        """Test creating a user with all fields."""
        user = User(
            email="test@example.com",
            vibe_profile={"preferences": ["fitness", "productivity"]}
        )
        db_session.add(user)
        db_session.commit()

        assert user.id is not None
        assert user.email == "test@example.com"
        assert user.vibe_profile == {"preferences": ["fitness", "productivity"]}
        assert user.created_at is not None
        assert user.updated_at is not None

    def test_user_email_unique_constraint(self, db_session):
        """Test that duplicate emails are rejected."""
        user1 = User(email="duplicate@example.com")
        db_session.add(user1)
        db_session.commit()

        user2 = User(email="duplicate@example.com")
        db_session.add(user2)

        with pytest.raises(Exception):  # IntegrityError
            db_session.commit()

    def test_user_vibe_profile_jsonb(self, db_session):
        """Test that vibe_profile accepts valid JSON."""
        user = User(
            email="json@example.com",
            vibe_profile={
                "taste_vector": [0.5, 0.8, 0.2],
                "preferences": {"music": "jazz", "books": "sci-fi"}
            }
        )
        db_session.add(user)
        db_session.commit()

        retrieved = db_session.query(User).filter_by(email="json@example.com").first()
        assert retrieved.vibe_profile["preferences"]["music"] == "jazz"

    def test_user_cascade_delete(self, db_session):
        """Test that deleting user cascades to somethings, circles, intentions, stories, actions."""
        user = User(email="cascade@example.com")
        db_session.add(user)
        db_session.commit()

        # Add related entities
        something = Something(user_id=user.id, content="Test something")
        circle = Circle(user_id=user.id, circle_name="Test Circle")
        intention = Intention(user_id=user.id, intention_text="Test intention")
        story = Story(user_id=user.id, story_text="Test story")
        action = Action(user_id=user.id, action_text="Test action", time_elapsed=30)

        db_session.add_all([something, circle, intention, story, action])
        db_session.commit()

        something_id = something.id
        circle_id = circle.id
        intention_id = intention.id
        story_id = story.id
        action_id = action.id

        # Delete user
        db_session.delete(user)
        db_session.commit()

        # Verify cascade deletion
        assert db_session.query(Something).filter_by(id=something_id).first() is None
        assert db_session.query(Circle).filter_by(id=circle_id).first() is None
        assert db_session.query(Intention).filter_by(id=intention_id).first() is None
        assert db_session.query(Story).filter_by(id=story_id).first() is None
        assert db_session.query(Action).filter_by(id=action_id).first() is None


class TestSomethingModel:
    """Test Something model with content types and meaning."""

    def test_create_something_text(self, db_session):
        """Test creating something with text content."""
        user = User(email="somethings@example.com")
        db_session.add(user)
        db_session.commit()

        something = Something(
            user_id=user.id,
            content="I want to get jacked and learn piano",
            content_type="text",
            meaning="User cares about self-improvement",
            novelty_score=0.85
        )
        db_session.add(something)
        db_session.commit()

        assert something.id is not None
        assert something.content == "I want to get jacked and learn piano"
        assert something.content_type == "text"
        assert something.meaning == "User cares about self-improvement"
        assert something.novelty_score == 0.85
        assert something.is_meaning_user_edited is False

    def test_create_something_with_media(self, db_session):
        """Test creating something with image/video content."""
        user = User(email="media@example.com")
        db_session.add(user)
        db_session.commit()

        something = Something(
            user_id=user.id,
            content=None,
            content_type="image",
            media_url="https://example.com/photo.jpg",
            meaning="User captured a fitness milestone photo"
        )
        db_session.add(something)
        db_session.commit()

        assert something.content_type == "image"
        assert something.media_url == "https://example.com/photo.jpg"
        assert something.content is None

    def test_something_user_edited_meaning(self, db_session):
        """Test is_meaning_user_edited flag."""
        user = User(email="edited@example.com")
        db_session.add(user)
        db_session.commit()

        something = Something(
            user_id=user.id,
            content="Learning piano",
            meaning="To impress my partner",
            is_meaning_user_edited=True
        )
        db_session.add(something)
        db_session.commit()

        assert something.is_meaning_user_edited is True


class TestSomethingCircleModel:
    """Test SomethingCircle junction table for many-to-many relationships."""

    def test_create_something_circle_link(self, db_session):
        """Test creating many-to-many link between something and circles."""
        user = User(email="link@example.com")
        db_session.add(user)
        db_session.commit()

        circle1 = Circle(user_id=user.id, circle_name="Fitness")
        circle2 = Circle(user_id=user.id, circle_name="Relationships")
        something = Something(user_id=user.id, content="Learn piano to impress my partner")
        db_session.add_all([circle1, circle2, something])
        db_session.commit()

        # Link to multiple circles
        link1 = SomethingCircle(
            something_id=something.id,
            circle_id=circle1.id,
            is_user_assigned=False,
            confidence_score=0.85
        )
        link2 = SomethingCircle(
            something_id=something.id,
            circle_id=circle2.id,
            is_user_assigned=True
        )
        db_session.add_all([link1, link2])
        db_session.commit()

        assert link1.id is not None
        assert link1.confidence_score == 0.85
        assert link1.is_user_assigned is False
        assert link2.is_user_assigned is True
        assert link2.confidence_score is None

    def test_something_circle_unique_constraint(self, db_session):
        """Test that duplicate something-circle links are rejected."""
        user = User(email="unique@example.com")
        db_session.add(user)
        db_session.commit()

        circle = Circle(user_id=user.id, circle_name="Test")
        something = Something(user_id=user.id, content="Test")
        db_session.add_all([circle, something])
        db_session.commit()

        link1 = SomethingCircle(something_id=something.id, circle_id=circle.id)
        db_session.add(link1)
        db_session.commit()

        # Try to create duplicate
        link2 = SomethingCircle(something_id=something.id, circle_id=circle.id)
        db_session.add(link2)

        with pytest.raises(Exception):  # IntegrityError
            db_session.commit()

    def test_something_circle_cascade_delete(self, db_session):
        """Test cascade deletion when something or circle is deleted."""
        user = User(email="cascade@example.com")
        db_session.add(user)
        db_session.commit()

        circle = Circle(user_id=user.id, circle_name="Test")
        something = Something(user_id=user.id, content="Test")
        db_session.add_all([circle, something])
        db_session.commit()

        link = SomethingCircle(something_id=something.id, circle_id=circle.id)
        db_session.add(link)
        db_session.commit()

        link_id = link.id

        # Delete circle
        db_session.delete(circle)
        db_session.commit()

        # Link should be cascade deleted
        assert db_session.query(SomethingCircle).filter_by(id=link_id).first() is None


class TestCircleModel:
    """Test Circle model with care_frequency and relationships."""

    def test_create_circle_with_care_frequency(self, db_session):
        """Test creating circle with care_frequency field."""
        user = User(email="care@example.com")
        db_session.add(user)
        db_session.commit()

        circle = Circle(
            user_id=user.id,
            circle_name="Personal Growth",
            description="Self-improvement ideas",
            care_frequency=5
        )
        db_session.add(circle)
        db_session.commit()

        assert circle.id is not None
        assert circle.circle_name == "Personal Growth"
        assert circle.care_frequency == 5

    def test_circle_default_care_frequency(self, db_session):
        """Test care_frequency defaults to 0."""
        user = User(email="default@example.com")
        db_session.add(user)
        db_session.flush()  # Flush to generate user.id

        circle = Circle(user_id=user.id, circle_name="Test")
        db_session.add(circle)
        db_session.commit()

        assert circle.care_frequency == 0


class TestIntentionModel:
    """Test Intention model with ENUM status constraint."""

    def test_create_intention_with_valid_status(self, db_session):
        """Test creating intention with valid ENUM status."""
        user = User(email="intention@example.com")
        db_session.add(user)
        db_session.commit()

        intention = Intention(
            user_id=user.id,
            intention_text="Get fit this year",
            status="active"
        )
        db_session.add(intention)
        db_session.commit()

        assert intention.id is not None
        assert intention.status == "active"

    def test_intention_status_enum_values(self, db_session):
        """Test all valid ENUM status values."""
        user = User(email="enum@example.com")
        db_session.add(user)
        db_session.commit()

        for status in ["active", "completed", "archived"]:
            intention = Intention(
                user_id=user.id,
                intention_text=f"Test {status}",
                status=status
            )
            db_session.add(intention)

        db_session.commit()

        intentions = db_session.query(Intention).all()
        statuses = [i.status for i in intentions]
        assert "active" in statuses
        assert "completed" in statuses
        assert "archived" in statuses


class TestIntentionCareModel:
    """Test IntentionCare junction table with unique constraint."""

    def test_create_intention_care_link(self, db_session):
        """Test creating many-to-many link between intention and something."""
        user = User(email="link@example.com")
        db_session.add(user)
        db_session.commit()

        intention = Intention(user_id=user.id, intention_text="Get fit")
        something = Something(user_id=user.id, content="I want to get jacked")
        db_session.add_all([intention, something])
        db_session.commit()

        link = IntentionCare(intention_id=intention.id, something_id=something.id)
        db_session.add(link)
        db_session.commit()

        assert link.id is not None
        assert link.intention.intention_text == "Get fit"
        assert link.something.content == "I want to get jacked"

    def test_intention_care_unique_constraint(self, db_session):
        """Test that duplicate intention-something links are rejected."""
        user = User(email="unique@example.com")
        db_session.add(user)
        db_session.flush()  # Flush to generate user.id

        intention = Intention(user_id=user.id, intention_text="Test")
        something = Something(user_id=user.id, content="Test")
        db_session.add_all([intention, something])
        db_session.commit()

        link1 = IntentionCare(intention_id=intention.id, something_id=something.id)
        db_session.add(link1)
        db_session.commit()

        # Try to create duplicate link
        link2 = IntentionCare(intention_id=intention.id, something_id=something.id)
        db_session.add(link2)

        with pytest.raises(Exception):  # IntegrityError
            db_session.commit()

    def test_intention_care_cascade_delete(self, db_session):
        """Test cascade deletion when intention or something is deleted."""
        user = User(email="cascade@example.com")
        db_session.add(user)
        db_session.flush()  # Flush to generate user.id

        intention = Intention(user_id=user.id, intention_text="Test")
        something = Something(user_id=user.id, content="Test")
        db_session.add_all([intention, something])
        db_session.commit()

        link = IntentionCare(intention_id=intention.id, something_id=something.id)
        db_session.add(link)
        db_session.commit()

        link_id = link.id

        # Delete intention
        db_session.delete(intention)
        db_session.commit()

        # Link should be cascade deleted
        assert db_session.query(IntentionCare).filter_by(id=link_id).first() is None


class TestActionModel:
    """Test Action model with time tracking."""

    def test_create_action(self, db_session):
        """Test creating action with time elapsed."""
        user = User(email="action@example.com")
        db_session.add(user)
        db_session.commit()

        action = Action(
            user_id=user.id,
            action_text="Hit the gym",
            time_elapsed=60
        )
        db_session.add(action)
        db_session.commit()

        assert action.id is not None
        assert action.action_text == "Hit the gym"
        assert action.time_elapsed == 60
        assert action.completed_at is not None

    def test_action_default_completed_at(self, db_session):
        """Test completed_at defaults to now()."""
        user = User(email="default@example.com")
        db_session.add(user)
        db_session.commit()

        action = Action(user_id=user.id, action_text="Test", time_elapsed=30)
        db_session.add(action)
        db_session.commit()

        assert action.completed_at is not None


class TestActionIntentionModel:
    """Test ActionIntention junction table."""

    def test_create_action_intention_link(self, db_session):
        """Test creating many-to-many link between action and intention."""
        user = User(email="link@example.com")
        db_session.add(user)
        db_session.commit()

        intention = Intention(user_id=user.id, intention_text="Get fit")
        action = Action(user_id=user.id, action_text="Hit the gym", time_elapsed=60)
        db_session.add_all([intention, action])
        db_session.commit()

        link = ActionIntention(action_id=action.id, intention_id=intention.id)
        db_session.add(link)
        db_session.commit()

        assert link.id is not None
        assert link.action.action_text == "Hit the gym"
        assert link.intention.intention_text == "Get fit"

    def test_action_intention_unique_constraint(self, db_session):
        """Test that duplicate action-intention links are rejected."""
        user = User(email="unique@example.com")
        db_session.add(user)
        db_session.commit()

        intention = Intention(user_id=user.id, intention_text="Test")
        action = Action(user_id=user.id, action_text="Test", time_elapsed=10)
        db_session.add_all([intention, action])
        db_session.commit()

        link1 = ActionIntention(action_id=action.id, intention_id=intention.id)
        db_session.add(link1)
        db_session.commit()

        # Try to create duplicate
        link2 = ActionIntention(action_id=action.id, intention_id=intention.id)
        db_session.add(link2)

        with pytest.raises(Exception):  # IntegrityError
            db_session.commit()


class TestStoryModel:
    """Test Story model with action relationships."""

    def test_create_story(self, db_session):
        """Test creating story."""
        user = User(email="story@example.com")
        db_session.add(user)
        db_session.commit()

        story = Story(
            user_id=user.id,
            story_text="Hit the gym for 1 hour and felt great"
        )
        db_session.add(story)
        db_session.commit()

        assert story.id is not None
        assert story.story_text == "Hit the gym for 1 hour and felt great"
        assert story.completed_at is not None
        assert story.updated_at is not None


class TestStoryActionModel:
    """Test StoryAction junction table."""

    def test_create_story_action_link(self, db_session):
        """Test creating many-to-many link between story and action."""
        user = User(email="link@example.com")
        db_session.add(user)
        db_session.commit()

        action = Action(user_id=user.id, action_text="Hit the gym", time_elapsed=60)
        story = Story(user_id=user.id, story_text="Weekly gym sessions summary")
        db_session.add_all([action, story])
        db_session.commit()

        link = StoryAction(story_id=story.id, action_id=action.id)
        db_session.add(link)
        db_session.commit()

        assert link.id is not None
        assert link.action.action_text == "Hit the gym"
        assert link.story.story_text == "Weekly gym sessions summary"

    def test_story_action_unique_constraint(self, db_session):
        """Test that duplicate story-action links are rejected."""
        user = User(email="unique@example.com")
        db_session.add(user)
        db_session.commit()

        action = Action(user_id=user.id, action_text="Test", time_elapsed=10)
        story = Story(user_id=user.id, story_text="Test")
        db_session.add_all([action, story])
        db_session.commit()

        link1 = StoryAction(story_id=story.id, action_id=action.id)
        db_session.add(link1)
        db_session.commit()

        # Try to create duplicate
        link2 = StoryAction(story_id=story.id, action_id=action.id)
        db_session.add(link2)

        with pytest.raises(Exception):  # IntegrityError
            db_session.commit()

    def test_story_action_cascade_delete(self, db_session):
        """Test cascade deletion when story or action is deleted."""
        user = User(email="cascade@example.com")
        db_session.add(user)
        db_session.commit()

        action = Action(user_id=user.id, action_text="Test", time_elapsed=10)
        story = Story(user_id=user.id, story_text="Test")
        db_session.add_all([action, story])
        db_session.commit()

        link = StoryAction(story_id=story.id, action_id=action.id)
        db_session.add(link)
        db_session.commit()

        link_id = link.id

        # Delete story
        db_session.delete(story)
        db_session.commit()

        # Link should be cascade deleted
        assert db_session.query(StoryAction).filter_by(id=link_id).first() is None


class TestIndexes:
    """Test that indexes are created correctly."""

    def test_user_email_index(self, db_session):
        """Test that email index exists and works."""
        # Create test users
        for i in range(100):
            user = User(email=f"user{i}@example.com")
            db_session.add(user)
        db_session.commit()

        # Query using indexed column (should be fast)
        result = db_session.query(User).filter_by(email="user50@example.com").first()
        assert result is not None
        assert result.email == "user50@example.com"
