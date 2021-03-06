"""empty message

Revision ID: c81dbf171b47
Revises: 4e492f7dba64
Create Date: 2020-06-16 16:04:09.384728

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c81dbf171b47'
down_revision = '4e492f7dba64'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('synchronization_filter',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('updated', sa.DateTime(), nullable=True),
    sa.Column('contract_address', sa.String(), nullable=True),
    sa.Column('contract_type', sa.String(), nullable=True),
    sa.Column('filter_parameters', sa.String(), nullable=True),
    sa.Column('filter_type', sa.String(), nullable=True),
    sa.Column('max_block', sa.Integer(), nullable=True),
    sa.Column('decimals', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('contract_address')
    )
    op.create_table('synchronized_block',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('updated', sa.DateTime(), nullable=True),
    sa.Column('block_number', sa.Integer(), nullable=True),
    sa.Column('status', sa.String(), nullable=True),
    sa.Column('is_synchronized', sa.Boolean(), nullable=True),
    sa.Column('synchronization_filter_id', sa.Integer(), nullable=True),
    sa.Column('decimals', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['synchronization_filter_id'], ['synchronization_filter.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('blockchain_transaction', sa.Column('is_third_party_transaction', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('blockchain_transaction', 'is_third_party_transaction')
    op.drop_table('synchronized_block')
    op.drop_table('synchronization_filter')
    # ### end Alembic commands ###
