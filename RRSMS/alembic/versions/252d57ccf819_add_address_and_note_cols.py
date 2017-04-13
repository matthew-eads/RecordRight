"""add address and note cols

Revision ID: 252d57ccf819
Revises: 
Create Date: 2017-04-13 04:02:23.167242

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '252d57ccf819'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('patients', sa.Column('address', sa.String()))
    op.add_column('patients', sa.Column('notes', sa.String()))


def downgrade():
    pass
