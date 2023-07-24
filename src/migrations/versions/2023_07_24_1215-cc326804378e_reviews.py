"""reviews

Revision ID: cc326804378e
Revises: 6f4a9c76a149
Create Date: 2023-07-24 12:15:32.573677

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'cc326804378e'
down_revision = '6f4a9c76a149'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('review',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('form_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('review_time', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['form_id'], ['form.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_review_id'), 'review', ['id'], unique=False)
    op.create_table('answer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('item_id', sa.Integer(), nullable=False),
    sa.Column('review_id', sa.Integer(), nullable=False),
    sa.Column('promt', postgresql.JSON(astext_type=sa.Text()), nullable=False),
    sa.ForeignKeyConstraint(['item_id'], ['item.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['review_id'], ['review.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('answer')
    op.drop_index(op.f('ix_review_id'), table_name='review')
    op.drop_table('review')
    # ### end Alembic commands ###
