"""empty message

Revision ID: 8d60d42e0a09
Revises: 456a0e0e8874
Create Date: 2019-03-07 10:13:51.752839

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8d60d42e0a09'
down_revision = '456a0e0e8874'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('faqs', sa.Column('question', sa.String(length=2000), nullable=False))
    op.create_unique_constraint(None, 'faqs', ['question'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'faqs', type_='unique')
    op.drop_column('faqs', 'question')
    # ### end Alembic commands ###