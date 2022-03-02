"""add foreign key to posts

Revision ID: 49c0f8d3ec87
Revises: d984548352be
Create Date: 2022-02-27 12:03:08.097656

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '49c0f8d3ec87'
down_revision = 'd984548352be'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'posts',
        sa.Column('owner_id', sa.Integer(), nullable=False)
    )
    op.create_foreign_key(
            'post_user_fk',
            source_table='posts',
            referent_table='users',
            local_cols=['owner_id'],
            remote_cols=['id'],
            ondelete='CASCADE'
    )


def downgrade():
    op.drop_constraint('post_user_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')