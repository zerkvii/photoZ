"""fixed

Revision ID: 64d9936f7bb4
Revises: 6699cbce66eb
Create Date: 2018-12-14 16:39:27.477067

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '64d9936f7bb4'
down_revision = '6699cbce66eb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('time_serials')
    op.drop_table('courses')
    op.drop_index('name', table_name='classes')
    op.drop_table('classes')
    op.drop_table('semasters')
    op.drop_table('class_course')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('class_course',
    sa.Column('course_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('class_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['class_id'], ['classes.id'], name='class_course_ibfk_1'),
    sa.ForeignKeyConstraint(['course_id'], ['courses.id'], name='class_course_ibfk_2'),
    sa.PrimaryKeyConstraint('course_id', 'class_id'),
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )
    op.create_table('semasters',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('name', mysql.VARCHAR(length=128), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )
    op.create_table('classes',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('name', mysql.VARCHAR(length=64), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )
    op.create_index('name', 'classes', ['name'], unique=True)
    op.create_table('courses',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('title', mysql.VARCHAR(length=128), nullable=False),
    sa.Column('teacher', mysql.VARCHAR(length=12), nullable=False),
    sa.Column('students_num', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('semaster_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['semaster_id'], ['semasters.id'], name='courses_ibfk_1'),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )
    op.create_table('time_serials',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('start_week', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('end_week', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('start_class', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('end_class', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('course_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['course_id'], ['courses.id'], name='time_serials_ibfk_1'),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###
