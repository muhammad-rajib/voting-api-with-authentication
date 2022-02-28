"""add content column to posts table

Revision ID: a4e3df33d570
Revises: 0cf53e28be9b
Create Date: 2022-02-27 11:15:27.934003

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a4e3df33d570'
down_revision = '0cf53e28be9b'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'posts',
        sa.Column(
            'content', sa.String(), nullable=False
        )
    )

def downgrade():
    op.drop_column('posts', 'content')
