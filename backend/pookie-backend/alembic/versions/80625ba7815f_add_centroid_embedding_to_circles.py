"""add_centroid_embedding_to_circles

Revision ID: 80625ba7815f
Revises: 05adc5953209
Create Date: 2025-12-07 19:32:29.890066

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '80625ba7815f'
down_revision: Union[str, Sequence[str], None] = '05adc5953209'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add centroid_embedding column to circles table
    # ARRAY(sa.Float) for PostgreSQL - 384 dimensions for sentence-transformers embeddings
    op.add_column(
        'circles',
        sa.Column('centroid_embedding', sa.ARRAY(sa.Float), nullable=True)
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Remove centroid_embedding column
    op.drop_column('circles', 'centroid_embedding')
