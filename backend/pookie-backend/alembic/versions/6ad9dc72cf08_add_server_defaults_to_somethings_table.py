"""add_server_defaults_to_somethings_table

Revision ID: 6ad9dc72cf08
Revises: 4ea9922607f3
Create Date: 2025-12-06 18:21:02.515387

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6ad9dc72cf08'
down_revision: Union[str, Sequence[str], None] = '4ea9922607f3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add server defaults to somethings table for content_type and is_meaning_user_edited."""
    # Add server default for content_type column
    op.alter_column(
        'somethings',
        'content_type',
        server_default='text',
        existing_type=sa.Enum('text', 'image', 'video', 'url', name='content_type'),
        existing_nullable=False
    )

    # Add server default for is_meaning_user_edited column
    op.alter_column(
        'somethings',
        'is_meaning_user_edited',
        server_default='false',
        existing_type=sa.Boolean(),
        existing_nullable=False
    )


def downgrade() -> None:
    """Remove server defaults from somethings table."""
    # Remove server default for is_meaning_user_edited
    op.alter_column(
        'somethings',
        'is_meaning_user_edited',
        server_default=None,
        existing_type=sa.Boolean(),
        existing_nullable=False
    )

    # Remove server default for content_type
    op.alter_column(
        'somethings',
        'content_type',
        server_default=None,
        existing_type=sa.Enum('text', 'image', 'video', 'url', name='content_type'),
        existing_nullable=False
    )
