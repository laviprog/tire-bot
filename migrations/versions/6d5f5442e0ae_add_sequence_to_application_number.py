"""Add sequence to application number

Revision ID: 6d5f5442e0ae
Revises: f765414f1d94
Create Date: 2025-07-16 21:04:10.219244

"""
from typing import Sequence, Union

import advanced_alchemy
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6d5f5442e0ae'
down_revision: Union[str, None] = 'f765414f1d94'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(sa.schema.CreateSequence(sa.Sequence('application_number_seq')))

    op.alter_column(
        'applications',
        'number',
        server_default=sa.text("nextval('application_number_seq')")
    )


def downgrade() -> None:
    # Удаляем server_default
    op.alter_column(
        'applications',
        'number',
        server_default=None
    )

    op.execute(sa.schema.DropSequence(sa.Sequence('application_number_seq')))
