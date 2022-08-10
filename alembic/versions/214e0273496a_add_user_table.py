"""Add user table

Revision ID: 214e0273496a
Revises: 1d55f01809ee
Create Date: 2022-08-09 07:18:47.195293

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '214e0273496a'
down_revision = '1d55f01809ee'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email'),
                    )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
