"""empty message

Revision ID: ca22ca895786
Revises: cca40f80d48d
Create Date: 2023-06-12 17:19:16.819393

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'ca22ca895786'
down_revision = 'cca40f80d48d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('interest', schema=None) as batch_op:
        batch_op.add_column(sa.Column('username', sa.String(length=64), nullable=True))
        batch_op.alter_column('user_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
        batch_op.create_index(batch_op.f('ix_interest_username'), ['username'], unique=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('interest', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_interest_username'))
        batch_op.alter_column('user_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
        batch_op.drop_column('username')

    # ### end Alembic commands ###