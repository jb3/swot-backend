"""
Create users table.

Revision ID: 7810416428c4
Revises:
Create Date: 2019-11-21 15:08:55.551246

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '7810416428c4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Upgrade the database to create the users table."""
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('username', sa.String(50), unique=True, nullable=False),
        sa.Column('password', sa.Unicode(200), nullable=False),
        sa.Column('email', sa.String(50), unique=True, nullable=False),
        sa.Column('type', sa.String(20), nullable=False)
    )


def downgrade() -> None:
    """Downgrade the database to drop the users table."""
    op.drop_table("users")
