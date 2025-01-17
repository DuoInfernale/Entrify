"""Add Customer fields

Revision ID: a87df7d9ebe4
Revises: 
Create Date: 2024-09-11 20:32:25.088335

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'a87df7d9ebe4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('customer', schema=None) as batch_op:
        batch_op.add_column(sa.Column('tenant_id', sa.String(length=128), nullable=False))
        batch_op.add_column(sa.Column('client_id', sa.String(length=128), nullable=False))
        batch_op.add_column(sa.Column('client_secret', sa.String(length=128), nullable=False))
        batch_op.alter_column('name',
               existing_type=mysql.VARCHAR(length=100),
               type_=sa.String(length=128),
               existing_nullable=False)
        batch_op.alter_column('short_name',
               existing_type=mysql.VARCHAR(length=50),
               type_=sa.String(length=64),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('customer', schema=None) as batch_op:
        batch_op.alter_column('short_name',
               existing_type=sa.String(length=64),
               type_=mysql.VARCHAR(length=50),
               existing_nullable=True)
        batch_op.alter_column('name',
               existing_type=sa.String(length=128),
               type_=mysql.VARCHAR(length=100),
               existing_nullable=False)
        batch_op.drop_column('client_secret')
        batch_op.drop_column('client_id')
        batch_op.drop_column('tenant_id')

    # ### end Alembic commands ###
