"""Add stops to city

Revision ID: 01361d0b247e
Revises: 776dbea94165
Create Date: 2024-05-10 14:24:02.359841

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '01361d0b247e'
down_revision: Union[str, None] = '776dbea94165'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('stop',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('address', sa.String(length=150), nullable=False),
    sa.Column('picture', sa.String(length=2048), nullable=True),
    sa.Column('mac_beacon', sa.String(length=17), nullable=True),
    sa.Column('id_city', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id_city'], ['city.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('mac_beacon')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('stop')
    # ### end Alembic commands ###
