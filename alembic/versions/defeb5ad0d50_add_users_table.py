"""Add users table

Revision ID: defeb5ad0d50
Revises: 97a1e1287bf6
Create Date: 2026-03-31 13:47:18.599750

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'defeb5ad0d50'
down_revision: Union[str, Sequence[str], None] = '97a1e1287bf6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id',sa.Integer(),nullable=False, primary_key=True),
                    sa.Column('email',sa.String(),nullable=False, unique=True),
                    sa.Column('password',sa.String(),nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'),nullable=False)
                    )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
