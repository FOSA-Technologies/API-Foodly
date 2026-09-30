"""change is_available to product

Revision ID: fa4012eb8db8
Revises: 8cb7806a08bb
Create Date: 2026-07-04 14:57:24.148629

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fa4012eb8db8'
down_revision: Union[str, Sequence[str], None] = '8cb7806a08bb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
     op.alter_column("products", "is_avaible",new_column_name="is_available")



def downgrade() -> None:
    """Downgrade schema."""
    pass
