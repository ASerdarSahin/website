"""Add BlogPost Model

Revision ID: 80bb211442c7
Revises: ba03b2b5b139
Create Date: 2023-05-02 03:04:15.275876

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '80bb211442c7'
down_revision = 'ba03b2b5b139'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('blog_post',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('author', sa.String(length=255), nullable=False),
    sa.Column('date_posted', sa.DateTime(), nullable=True),
    sa.Column('slug', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('slug')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('blog_post')
    # ### end Alembic commands ###