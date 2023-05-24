"""Rating stuff

Revision ID: 3000d4cf07b4
Revises: 658bc83a7e18
Create Date: 2023-05-24 22:23:58.988523

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '3000d4cf07b4'
down_revision = '658bc83a7e18'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('like',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['post_id'], ['blog_post.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('blog_post', schema=None) as batch_op:
        batch_op.drop_column('rating')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('blog_post', schema=None) as batch_op:
        batch_op.add_column(sa.Column('rating', mysql.INTEGER(), autoincrement=False, nullable=True))

    op.drop_table('like')
    # ### end Alembic commands ###
