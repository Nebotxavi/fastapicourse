"""Add foreign key to post table

Revision ID: 5831e40220a6
Revises: 214e0273496a
Create Date: 2022-08-10 06:32:24.611664

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5831e40220a6'
down_revision = '214e0273496a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table='posts', referent_table='users', local_cols=[
                          'owner_id'], remote_cols=['id'], ondelete='CASCADE')

    pass


def downgrade() -> None:
    op.drop_constraint('post_users_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass
