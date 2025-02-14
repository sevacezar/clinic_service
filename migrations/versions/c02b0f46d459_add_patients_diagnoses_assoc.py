"""add_patients_diagnoses_assoc

Revision ID: c02b0f46d459
Revises: 5072f8923d88
Create Date: 2025-01-25 13:45:20.707582

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c02b0f46d459'
down_revision: Union[str, None] = '5072f8923d88'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('patient_diagnosis',
    sa.Column('patient_id', sa.Integer(), nullable=False),
    sa.Column('diagnosis_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['diagnosis_id'], ['diagnoses.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['patient_id'], ['patients.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('patient_id', 'diagnosis_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('patient_diagnosis')
    # ### end Alembic commands ###
