"""empty message

Revision ID: 1bef8f1a4eb7
Revises: 28b7f64b1413
Create Date: 2023-09-08 12:32:49.966470

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1bef8f1a4eb7'
down_revision = '28b7f64b1413'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_connection', schema=None) as batch_op:
        batch_op.drop_column('status')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_connection', schema=None) as batch_op:
        batch_op.add_column(sa.Column('status', sa.VARCHAR(length=20), autoincrement=False, nullable=True))

    # ### end Alembic commands ###
