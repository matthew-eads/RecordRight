"""add rr_id col

Revision ID: 83a2e4858eae
Revises: 252d57ccf819
Create Date: 2017-04-23 15:49:51.612387

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '83a2e4858eae'
down_revision = '252d57ccf819'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('patients', sa.Column('rr_id', sa.Integer)) 


def downgrade():
    op.drop_column('patients', 'rr_id')
