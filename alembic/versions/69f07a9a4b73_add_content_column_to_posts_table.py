"""add content column to posts table

Revision ID: 69f07a9a4b73
Revises: 1d3dccadcb5c
Create Date: 2026-01-23 00:53:21.950825

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '69f07a9a4b73'
down_revision: Union[str, Sequence[str], None] = '1d3dccadcb5c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
