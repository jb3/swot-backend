"""Remove parents

Revision ID: 79814ff114c9
Revises: 1f84d2da2b69
Create Date: 2020-11-09 09:52:05.820396

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '79814ff114c9'
down_revision = '1f84d2da2b69'
branch_labels = None
depends_on = None


enum_name = 'usertype'

tmp_enum_name = 'tmp_' + enum_name

old_options = ('STUDENT', 'TEACHER', 'PARENT')
new_options = ('STUDENT', 'TEACHER')

old_type = sa.Enum(*old_options, name=enum_name)
new_type = sa.Enum(*new_options, name=enum_name)

def upgrade():
    # Rename current enum type to tmp_
    op.execute('ALTER TYPE ' + enum_name + ' RENAME TO ' + tmp_enum_name)
    # Create new enum type in db
    new_type.create(op.get_bind())
    # Update column to use new enum type
    op.execute('ALTER TABLE users ALTER COLUMN type TYPE ' + enum_name + ' USING type::text::' + enum_name)
    # Drop old enum type
    op.execute('DROP TYPE ' + tmp_enum_name)


def downgrade():
    pass
