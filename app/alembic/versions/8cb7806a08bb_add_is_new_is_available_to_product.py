"""add is_new, is_available to product

Revision ID: 8cb7806a08bb
Revises: 8c4007cbf516
Create Date: 2026-07-04 14:39:31.522018

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8cb7806a08bb'
down_revision: Union[str, Sequence[str], None] = '8c4007cbf516'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("products", sa.Column("is_new", sa.Boolean, nullable=False, server_default=sa.text("true")))
    op.alter_column("products", sa.Column("is_available",sa.Boolean, nullable=False, server_default=sa.text("true")))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
