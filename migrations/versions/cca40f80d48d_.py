"""empty message

Revision ID: cca40f80d48d
Revises: 9325736ef196
Create Date: 2023-06-10 15:01:43.060678

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cca40f80d48d'
down_revision = '9325736ef196'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.String(length=64), nullable=False))
        batch_op.create_unique_constraint(None, ['user_id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_column('user_id')

    # ### end Alembic commands ###
