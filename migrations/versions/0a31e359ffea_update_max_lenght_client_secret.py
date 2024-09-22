"""Update max lenght client_secret

Revision ID: 0a31e359ffea
Revises: a87df7d9ebe4
Create Date: 2024-09-13 16:58:39.980479

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '0a31e359ffea'
down_revision = 'a87df7d9ebe4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('customer', schema=None) as batch_op:
        batch_op.alter_column('client_secret',
               existing_type=mysql.VARCHAR(length=128),
               type_=sa.String(length=255),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('customer', schema=None) as batch_op:
        batch_op.alter_column('client_secret',
               existing_type=sa.String(length=255),
               type_=mysql.VARCHAR(length=128),
               existing_nullable=False)

    # ### end Alembic commands ###