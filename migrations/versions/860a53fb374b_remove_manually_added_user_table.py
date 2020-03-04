"""Remove manually added user table

Revision ID: 860a53fb374b
Revises: 7810416428c4
Create Date: 2020-03-04 14:55:39.579252

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '860a53fb374b'
down_revision = '7810416428c4'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_table("users")

def downgrade():
    pass
