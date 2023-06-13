"""add to_review field

Revision ID: a3bc14d04d80
Revises: 6a25fedb58cd
Create Date: 2023-06-13 17:22:04.647155

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a3bc14d04d80'
down_revision = '6a25fedb58cd'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('form', sa.Column('to_review', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('form', 'to_review')
    # ### end Alembic commands ###