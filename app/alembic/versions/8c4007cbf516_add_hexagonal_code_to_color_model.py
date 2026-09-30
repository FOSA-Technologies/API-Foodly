"""add hexagonal code to color model

Revision ID: 8c4007cbf516
Revises: 73587295ecd2
Create Date: 2026-07-04 14:08:19.263588

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8c4007cbf516'
down_revision: Union[str, Sequence[str], None] = '73587295ecd2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("colors", sa.Column("hex", sa.String, nullable=False, server_default="#FFF"))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
