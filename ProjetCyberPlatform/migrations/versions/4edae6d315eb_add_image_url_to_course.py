"""Add image_url to Course

Revision ID: 4edae6d315eb
Revises: a1a8f23505c4
Create Date: 2024-12-12 11:46:56.265970

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4edae6d315eb'
down_revision = 'a1a8f23505c4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cart',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('course_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['course_id'], ['course.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('course', schema=None) as batch_op:
        batch_op.add_column(sa.Column('image_url', sa.String(length=200), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('course', schema=None) as batch_op:
        batch_op.drop_column('image_url')

    op.drop_table('cart')
    # ### end Alembic commands ###
