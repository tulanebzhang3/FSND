"""empty message

Revision ID: 37fc9fc6baa5
Revises: 58f1e2422de8
Create Date: 2020-03-30 21:41:24.764257

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '37fc9fc6baa5'
down_revision = '58f1e2422de8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('show', sa.Column('venue_id', sa.Integer(), nullable=False))
    op.drop_constraint('show_vueue_id_fkey', 'show', type_='foreignkey')
    op.create_foreign_key(None, 'show', 'Venue', ['venue_id'], ['id'])
    op.drop_column('show', 'vueue_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('show', sa.Column('vueue_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'show', type_='foreignkey')
    op.create_foreign_key('show_vueue_id_fkey', 'show', 'Venue', ['vueue_id'], ['id'])
    op.drop_column('show', 'venue_id')
    # ### end Alembic commands ###