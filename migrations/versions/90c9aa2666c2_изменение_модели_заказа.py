"""Изменение модели заказа

Revision ID: 90c9aa2666c2
Revises: 2d9a1b23c07c
Create Date: 2025-07-20 20:40:59.349884

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '90c9aa2666c2'
down_revision = '2d9a1b23c07c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('ordered_products', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.String(length=200), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('ordered_products', schema=None) as batch_op:
        batch_op.drop_column('name')

    # ### end Alembic commands ###
