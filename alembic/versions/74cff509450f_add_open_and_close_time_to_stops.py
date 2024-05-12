"""Add open and close time to stops

Revision ID: 74cff509450f
Revises: 01361d0b247e
Create Date: 2024-05-12 22:09:05.494699

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '74cff509450f'
down_revision: Union[str, None] = '01361d0b247e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('stop', sa.Column('open_at', sa.Time(), nullable=True))
    op.add_column('stop', sa.Column('close_at', sa.Time(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('stop', 'close_at')
    op.drop_column('stop', 'open_at')
    # ### end Alembic commands ###
