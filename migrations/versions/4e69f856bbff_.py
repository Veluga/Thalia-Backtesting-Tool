"""empty message

Revision ID: 4e69f856bbff
Revises: 3e25adea1beb
Create Date: 2020-02-05 17:30:04.751218

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4e69f856bbff'
down_revision = '3e25adea1beb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'password_hash',
               existing_type=sa.VARCHAR(length=128),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'password_hash',
               existing_type=sa.VARCHAR(length=128),
               nullable=True)
    # ### end Alembic commands ###