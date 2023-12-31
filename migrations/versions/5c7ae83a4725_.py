"""empty message

Revision ID: 5c7ae83a4725
Revises: fba79bb17999
Create Date: 2023-06-14 00:32:38.567180

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '5c7ae83a4725'
down_revision = 'fba79bb17999'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_interests')
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('user_id',
               existing_type=mysql.VARCHAR(length=64),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('user_id',
               existing_type=mysql.VARCHAR(length=64),
               nullable=False)

    op.create_table('user_interests',
    sa.Column('user_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('interest_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['interest_id'], ['interest.id'], name='user_interests_ibfk_1'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='user_interests_ibfk_2'),
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###
