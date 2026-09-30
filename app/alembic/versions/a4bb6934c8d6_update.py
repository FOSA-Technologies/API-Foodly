"""update

Revision ID: a4bb6934c8d6
Revises: 2268cf0ca64d
Create Date: 2026-07-08 19:52:30.997740

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import ForeignKey

# revision identifiers, used by Alembic.
revision: str = 'a4bb6934c8d6'
down_revision: Union[str, Sequence[str], None] = '2268cf0ca64d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column("products_sizes",column_name="color_id", new_column_name="color_id",type= sa.Column(sa.Integer, ForeignKey('colors.id', ondelete="CASCADE"), primary_key=False, nullable=True))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
