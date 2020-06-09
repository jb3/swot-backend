"""Added classes table

Revision ID: 12187fd04aa5
Revises: 21cb185c15e6
Create Date: 2020-06-01 01:26:36.300169

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '12187fd04aa5'
down_revision = '21cb185c15e6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('classes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('code', sa.String(), nullable=False),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('code'),
    sa.UniqueConstraint('name')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('classes')
    # ### end Alembic commands ###
