"""add color_id to size_id

Revision ID: 2268cf0ca64d
Revises: fa4012eb8db8
Create Date: 2026-07-08 17:27:44.879129

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2268cf0ca64d'
down_revision: Union[str, Sequence[str], None] = 'fa4012eb8db8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("products_sizes", sa.Column("color_id",sa.Integer, sa.ForeignKey('colors.id', ondelete="CASCADE") ,primary_key=True, nullable=False))


def downgrade() -> None:
    """Downgrade schema."""
    pass
