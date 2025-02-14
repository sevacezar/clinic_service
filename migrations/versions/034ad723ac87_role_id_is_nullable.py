"""role_id_is_nullable

Revision ID: 034ad723ac87
Revises: ee9c16857899
Create Date: 2025-01-25 23:36:27.820275

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '034ad723ac87'
down_revision: Union[str, None] = 'ee9c16857899'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'role_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'role_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###
