"""Add rating field to BlogPost

Revision ID: 988dd6469f65
Revises: 9618eb94e46a
Create Date: 2023-05-23 23:07:54.373966

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '988dd6469f65'
down_revision = '9618eb94e46a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('blog_post', schema=None) as batch_op:
        batch_op.add_column(sa.Column('rating', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('blog_post', schema=None) as batch_op:
        batch_op.drop_column('rating')

    # ### end Alembic commands ###