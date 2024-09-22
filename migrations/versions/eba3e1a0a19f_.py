"""empty message

Revision ID: eba3e1a0a19f
Revises: 7d4ab25ec2ed
Create Date: 2024-09-17 18:43:18.469885

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eba3e1a0a19f'
down_revision = '7d4ab25ec2ed'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('enterprise_application',
    sa.Column('app_id', sa.String(length=128), nullable=False),
    sa.Column('display_name', sa.String(length=256), nullable=False),
    sa.PrimaryKeyConstraint('app_id')
    )
    op.create_table('saml_certificate',
    sa.Column('key_id', sa.String(length=128), nullable=False),
    sa.Column('certificate_display_name', sa.String(length=256), nullable=False),
    sa.Column('end_date_time', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('key_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('saml_certificate')
    op.drop_table('enterprise_application')
    # ### end Alembic commands ###