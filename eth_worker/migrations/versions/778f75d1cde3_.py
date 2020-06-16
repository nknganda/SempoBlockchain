"""empty message

Revision ID: 778f75d1cde3
Revises: da3186c8a0f4
Create Date: 2020-06-16 14:00:02.232231

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '778f75d1cde3'
down_revision = 'da3186c8a0f4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('synchronization_filter', sa.Column('decimals', sa.Integer(), nullable=True))
    op.add_column('synchronized_block', sa.Column('decimals', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('synchronized_block', 'decimals')
    op.drop_column('synchronization_filter', 'decimals')
    # ### end Alembic commands ###