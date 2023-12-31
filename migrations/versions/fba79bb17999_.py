"""empty message

Revision ID: fba79bb17999
Revises: 27deabb2f5c1
Create Date: 2023-06-13 23:49:34.898907

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fba79bb17999'
down_revision = '27deabb2f5c1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_interests',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('interest_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['interest_id'], ['interest.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_interests')
    # ### end Alembic commands ###
