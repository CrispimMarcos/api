"""create tables

Revision ID: 196c0b700244
Revises: 846f6c134af3
Create Date: 2025-05-26 05:06:05.755473

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '196c0b700244'
down_revision: Union[str, None] = '846f6c134af3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('clients',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('cpf', sa.String(), nullable=False),
    sa.Column('phone', sa.String(), nullable=True),
    sa.Column('address', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('cpf'),
    sa.UniqueConstraint('email')
    )
    op.create_index(op.f('ix_clients_id'), 'clients', ['id'], unique=False)
    op.create_table('products',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('sale_price', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('barcode', sa.String(), nullable=False),
    sa.Column('section', sa.String(), nullable=False),
    sa.Column('stock', sa.Integer(), nullable=False),
    sa.Column('expiration_date', sa.Date(), nullable=True),
    sa.Column('available', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('barcode')
    )
    op.create_index(op.f('ix_products_id'), 'products', ['id'], unique=False)
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('hashed_password', sa.String(), nullable=False),
    sa.Column('role', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_table('orders',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('client_id', sa.Integer(), nullable=False),
    sa.Column('status', sa.String(), nullable=True),
    sa.Column('order_date', sa.DateTime(), nullable=False),
    sa.Column('total', sa.Numeric(precision=10, scale=2), nullable=True),
    sa.ForeignKeyConstraint(['client_id'], ['clients.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_orders_id'), 'orders', ['id'], unique=False)
    op.create_index(op.f('ix_orders_status'), 'orders', ['status'], unique=False)
    op.create_table('order_items',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('order_id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_order_items_id'), 'order_items', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_order_items_id'), table_name='order_items')
    op.drop_table('order_items')
    op.drop_index(op.f('ix_orders_status'), table_name='orders')
    op.drop_index(op.f('ix_orders_id'), table_name='orders')
    op.drop_table('orders')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_products_id'), table_name='products')
    op.drop_table('products')
    op.drop_index(op.f('ix_clients_id'), table_name='clients')
    op.drop_table('clients')
    # ### end Alembic commands ###
