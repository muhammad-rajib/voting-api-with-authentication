"""add last few columns to posts

Revision ID: e7dd7a4d2160
Revises: 49c0f8d3ec87
Create Date: 2022-02-27 12:22:33.583153

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e7dd7a4d2160'
down_revision = '49c0f8d3ec87'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'posts',
        sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE')
    )
    op.add_column(
        'posts',
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()'))
    )


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
