"""added classmethod to blogpost

Revision ID: 12d4dd621cbd
Revises: aa4d980efcd5
Create Date: 2020-09-28 11:01:51.447109

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '12d4dd621cbd'
down_revision = 'aa4d980efcd5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('blogposts', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'blogposts', 'users', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'blogposts', type_='foreignkey')
    op.drop_column('blogposts', 'user_id')
    # ### end Alembic commands ###