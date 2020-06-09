"""Add user table

Revision ID: 37b1fd641018
Revises: 860a53fb374b
Create Date: 2020-03-04 15:00:07.202762

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '37b1fd641018'
down_revision = '860a53fb374b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('password', sa.Unicode(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('type', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('name')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    # ### end Alembic commands ###
