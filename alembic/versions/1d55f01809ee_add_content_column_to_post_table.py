"""add content column to post table

Revision ID: 1d55f01809ee
Revises: 30091452f968
Create Date: 2022-08-09 07:14:31.618027

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1d55f01809ee'
down_revision = '30091452f968'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
