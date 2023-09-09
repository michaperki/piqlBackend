"""Add status column and status enum type to Game table

Revision ID: 879fd6bd096c
Revises: 4755a6357938
Create Date: 2023-09-08 21:07:31.409792

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '879fd6bd096c'
down_revision = 'a7631872674d'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("CREATE TYPE status AS ENUM ('Pending', 'Active', 'Scheduled')")

def downgrade():
    op.execute("DROP TYPE status")
