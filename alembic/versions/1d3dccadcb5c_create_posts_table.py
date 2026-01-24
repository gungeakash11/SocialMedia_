"""create posts table

Revision ID: 1d3dccadcb5c
Revises: 
Create Date: 2026-01-23 00:39:57.454277

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1d3dccadcb5c'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('posts',
    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
    sa.Column('title', sa.String(), nullable=False)
    )


def downgrade() -> None:
    op.drop_table('posts', if_exists=True)
