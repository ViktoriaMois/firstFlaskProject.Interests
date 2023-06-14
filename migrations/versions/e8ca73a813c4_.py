"""empty message

Revision ID: e8ca73a813c4
Revises: 5c7ae83a4725
Create Date: 2023-06-14 00:33:17.333649

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'e8ca73a813c4'
down_revision = '5c7ae83a4725'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('token',
               existing_type=mysql.VARCHAR(length=256),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('token',
               existing_type=mysql.VARCHAR(length=256),
               nullable=False)

    # ### end Alembic commands ###
