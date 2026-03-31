"""Add content column in post table

Revision ID: 97a1e1287bf6
Revises: 30dde8bc1f9f
Create Date: 2026-03-31 13:39:52.750002

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '97a1e1287bf6'
down_revision: Union[str, Sequence[str], None] = '30dde8bc1f9f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('post', 'content')
    pass
