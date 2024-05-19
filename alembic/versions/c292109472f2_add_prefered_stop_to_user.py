"""Add prefered stop to user

Revision ID: c292109472f2
Revises: 74cff509450f
Create Date: 2024-05-19 17:29:53.791542

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c292109472f2'
down_revision: Union[str, None] = '74cff509450f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('id_stop', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'user', 'stop', ['id_stop'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='foreignkey')
    op.drop_column('user', 'id_stop')
    # ### end Alembic commands ###