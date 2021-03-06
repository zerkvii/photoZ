"""add one to one relationship

Revision ID: a474ba1b297a
Revises: 6f872ddde5cd
Create Date: 2018-12-14 14:17:00.585293

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'a474ba1b297a'
down_revision = '6f872ddde5cd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('courses', 'time_serial_id')
    op.add_column('time_serials', sa.Column('course_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'time_serials', 'courses', ['course_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'time_serials', type_='foreignkey')
    op.drop_column('time_serials', 'course_id')
    op.add_column('courses', sa.Column('time_serial_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
