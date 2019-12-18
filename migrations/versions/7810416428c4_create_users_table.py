"""create users table

Revision ID: 7810416428c4
Revises:
Create Date: 2019-11-21 15:08:55.551246

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7810416428c4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    """Upgrade the database to create the users table."""
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('username', sa.String(50), unique=True, nullable=False),
        sa.Column('password', sa.Unicode(200), nullable=False),
        sa.Column('email', sa.String(50), unique=True, nullable=False),
        sa.Column('type', sa.String(20), nullable=False)
    )


def downgrade():
    """Downgrade the database to drop the users table."""
    op.drop_table("users")
