"""add_trigger_to_sync_auth_users_to_users_table

Revision ID: 05adc5953209
Revises: 6ad9dc72cf08
Create Date: 2025-12-07 05:51:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '05adc5953209'
down_revision: Union[str, None] = '6ad9dc72cf08'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create trigger to sync auth.users to public.users"""

    # Create function to handle new user creation
    op.execute("""
    CREATE OR REPLACE FUNCTION public.handle_new_user()
    RETURNS TRIGGER AS $$
    BEGIN
        INSERT INTO public.users (id, email, created_at, updated_at)
        VALUES (
            NEW.id,
            NEW.email,
            NOW(),
            NOW()
        )
        ON CONFLICT (id) DO NOTHING;
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql SECURITY DEFINER;
    """)

    # Create trigger on auth.users table
    op.execute("""
    DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;

    CREATE TRIGGER on_auth_user_created
        AFTER INSERT ON auth.users
        FOR EACH ROW
        EXECUTE FUNCTION public.handle_new_user();
    """)

    # Backfill existing auth users into users table
    op.execute("""
    INSERT INTO public.users (id, email, created_at, updated_at)
    SELECT
        id,
        email,
        created_at,
        updated_at
    FROM auth.users
    ON CONFLICT (id) DO NOTHING;
    """)


def downgrade() -> None:
    """Remove trigger and function"""
    op.execute("DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;")
    op.execute("DROP FUNCTION IF EXISTS public.handle_new_user();")
