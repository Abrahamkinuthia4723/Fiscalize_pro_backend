"""Initial migration.

Revision ID: 8cc25c66e954
Revises: 
Create Date: 2024-12-31 21:19:18.611932

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8cc25c66e954'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('dbo_invnum',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('invoice_number', sa.String(length=100), nullable=False),
    sa.Column('customer_name', sa.String(length=255), nullable=False),
    sa.Column('total_amount', sa.Float(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('invlines',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('invid', sa.Integer(), nullable=False),
    sa.Column('item_name', sa.String(length=255), nullable=False),
    sa.Column('item_code', sa.String(length=100), nullable=True),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('tax_rate', sa.Float(), nullable=True),
    sa.Column('discount', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['invid'], ['dbo_invnum.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('fiscal_data',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('invid', sa.Integer(), nullable=False),
    sa.Column('qr_code_path', sa.String(length=255), nullable=False),
    sa.Column('signature', sa.String(length=255), nullable=False),
    sa.ForeignKeyConstraint(['invid'], ['invlines.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('fiscal_data')
    op.drop_table('invlines')
    op.drop_table('dbo_invnum')
    # ### end Alembic commands ###