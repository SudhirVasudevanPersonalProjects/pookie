"""Fix intention status to use ENUM type

Revision ID: 28977c402797
Revises: 8f33b4d7c4dd
Create Date: 2025-12-05 15:58:45.153877

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '28977c402797'
down_revision: Union[str, Sequence[str], None] = '8f33b4d7c4dd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create ENUM type
    intention_status_enum = sa.Enum('active', 'completed', 'archived', name='intention_status')
    intention_status_enum.create(op.get_bind(), checkfirst=True)

    # Convert existing data and alter column type
    op.execute("ALTER TABLE intentions ALTER COLUMN status TYPE intention_status USING status::intention_status")
    op.alter_column('intentions', 'status', nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    # Convert column back to TEXT
    op.alter_column('intentions', 'status',
               existing_type=sa.Enum('active', 'completed', 'archived', name='intention_status'),
               type_=sa.TEXT(),
               nullable=True)

    # Drop ENUM type
    intention_status_enum = sa.Enum('active', 'completed', 'archived', name='intention_status')
    intention_status_enum.drop(op.get_bind(), checkfirst=True)
