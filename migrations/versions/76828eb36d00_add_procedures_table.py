"""Add procedures table

Revision ID: 76828eb36d00
Revises: 
Create Date: 2024-10-30 23:24:57.069090

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '76828eb36d00'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('services')
    op.drop_table('employees')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('employees',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=100), nullable=False),
    sa.Column('position', sa.VARCHAR(length=100), nullable=True),
    sa.Column('phone', sa.VARCHAR(length=20), nullable=True),
    sa.Column('email', sa.VARCHAR(length=100), nullable=True),
    sa.Column('service_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['service_id'], ['services.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('services',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=100), nullable=False),
    sa.Column('service_type', sa.VARCHAR(length=10), nullable=True),
    sa.Column('duration', sa.INTEGER(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
