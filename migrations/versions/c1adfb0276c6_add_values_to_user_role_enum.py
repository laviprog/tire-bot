"""Add values to user role enum

Revision ID: c1adfb0276c6
Revises: 6d5f5442e0ae
Create Date: 2025-07-17 11:09:49.595938

"""
from typing import Sequence, Union

import advanced_alchemy
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c1adfb0276c6'
down_revision: Union[str, None] = '6d5f5442e0ae'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("ALTER TYPE role ADD VALUE IF NOT EXISTS 'WORKER'")
    op.execute("ALTER TYPE status ADD VALUE IF NOT EXISTS 'ASSIGNED'")


def downgrade() -> None:
    """Downgrade schema."""
    pass
