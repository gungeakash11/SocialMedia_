"""Update Posts table with all Columns

Revision ID: 925eda7fdafa
Revises: f400474eac1c
Create Date: 2026-01-24 10:23:44.080077

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '925eda7fdafa'
down_revision: Union[str, Sequence[str], None] = 'f400474eac1c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
     op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'))
     op.add_column('posts', sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()))
     pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
