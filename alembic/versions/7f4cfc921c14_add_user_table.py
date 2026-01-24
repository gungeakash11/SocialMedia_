"""add user table

Revision ID: 7f4cfc921c14
Revises: 69f07a9a4b73
Create Date: 2026-01-23 23:55:30.887194

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7f4cfc921c14'
down_revision: Union[str, Sequence[str], None] = '69f07a9a4b73'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
     


def downgrade() -> None:
<<<<<<< HEAD
    op.drop_table('users', if_exists=True)  
=======
    op.drop_table('user', if_exists=True)  
>>>>>>> c2fd548 (initial commit)
    pass
