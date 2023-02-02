"""second

Revision ID: d34d5b2230ea
Revises: 67d4f9940df9
Create Date: 2023-02-02 21:34:38.134312

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd34d5b2230ea'
down_revision = '67d4f9940df9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'my_currency', ['id'])
    op.add_column('users', sa.Column('email', sa.String(length=50), nullable=True))
    op.create_unique_constraint(None, 'users', ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_column('users', 'email')
    op.drop_constraint(None, 'my_currency', type_='unique')
    # ### end Alembic commands ###
