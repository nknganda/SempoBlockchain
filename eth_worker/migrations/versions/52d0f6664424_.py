"""empty message

Revision ID: 52d0f6664424
Revises: 937abec76ce8
Create Date: 2020-01-05 13:09:06.474697

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '52d0f6664424'
down_revision = '937abec76ce8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('blockchain_task', sa.Column('status_text', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('blockchain_task', 'status_text')
    # ### end Alembic commands ###
