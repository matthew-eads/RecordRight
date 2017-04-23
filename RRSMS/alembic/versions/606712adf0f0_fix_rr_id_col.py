"""fix rr_id col

Revision ID: 606712adf0f0
Revises: 83a2e4858eae
Create Date: 2017-04-23 16:40:11.179946

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '606712adf0f0'
down_revision = '83a2e4858eae'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column('patients', 'rr_id')
    op.add_column('patients', sa.Column('rr_id', sa.Integer, unique=True)) 



def downgrade():
    pass
