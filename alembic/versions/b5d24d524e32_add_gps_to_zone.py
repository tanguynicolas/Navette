"""Add gps to zone

Revision ID: b5d24d524e32
Revises: 3a11e2d7cf7a
Create Date: 2024-05-21 14:38:53.920400

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b5d24d524e32'
down_revision: Union[str, None] = '3a11e2d7cf7a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('zone', sa.Column('gps', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('zone', 'gps')
    # ### end Alembic commands ###
