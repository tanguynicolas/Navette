"""Add travel

Revision ID: 33c50f11a4dd
Revises: 00dc0e2586f0
Create Date: 2024-05-19 16:39:40.127295

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '33c50f11a4dd'
down_revision: Union[str, None] = '00dc0e2586f0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('travel',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('started_at', sa.DateTime(), nullable=True),
    sa.Column('closed_at', sa.DateTime(), nullable=True),
    sa.Column('departure', sa.String(), nullable=False),
    sa.Column('arrival', sa.String(), nullable=False),
    sa.Column('back_travel', sa.Boolean(), nullable=False),
    sa.Column('id_driver', sa.Integer(), nullable=True),
    sa.Column('id_passenger1', sa.Integer(), nullable=True),
    sa.Column('id_passenger2', sa.Integer(), nullable=True),
    sa.Column('id_passenger3', sa.Integer(), nullable=True),
    sa.Column('id_passenger4', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id_driver'], ['user.id'], ),
    sa.ForeignKeyConstraint(['id_passenger1'], ['user.id'], ),
    sa.ForeignKeyConstraint(['id_passenger2'], ['user.id'], ),
    sa.ForeignKeyConstraint(['id_passenger3'], ['user.id'], ),
    sa.ForeignKeyConstraint(['id_passenger4'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('travel')
    # ### end Alembic commands ###
