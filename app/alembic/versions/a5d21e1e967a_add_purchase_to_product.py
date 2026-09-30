"""add purchase to product

Revision ID: a5d21e1e967a
Revises: 
Create Date: 2026-07-02 01:23:40.933309

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from psycopg2._psycopg import Column

# revision identifiers, used by Alembic.
revision: str = 'a5d21e1e967a'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("products", sa.Column("purchase_price",sa.Integer, nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
