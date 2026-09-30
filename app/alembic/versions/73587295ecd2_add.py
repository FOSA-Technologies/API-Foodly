"""add

Revision ID: 73587295ecd2
Revises: a5d21e1e967a
Create Date: 2026-07-02 01:42:05.787351

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '73587295ecd2'
down_revision: Union[str, Sequence[str], None] = 'a5d21e1e967a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("products", sa.Column("purchase_price",sa.Integer, nullable=False))



def downgrade() -> None:
    """Downgrade schema."""
    pass
