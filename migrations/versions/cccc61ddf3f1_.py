"""empty message

Revision ID: cccc61ddf3f1
Revises: 3e9de17c8e4e
Create Date: 2024-09-15 18:42:48.770320

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cccc61ddf3f1'
down_revision = '3e9de17c8e4e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('password_credential',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('key_id', sa.String(length=128), nullable=False),
    sa.Column('application_id', sa.String(length=128), nullable=False),
    sa.Column('additional_data', sa.JSON(), nullable=True),
    sa.Column('display_name', sa.String(length=256), nullable=False),
    sa.Column('end_date_time', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['application_id'], ['application.app_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('password_credential')
    # ### end Alembic commands ###