"""add_due_date_to_todos

Revision ID: a1b2c3d4e5f6
Revises: 08f7a7527cac
Create Date: 2026-09-06 18:15:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a1b2c3d4e5f6"
down_revision: Union[str, None] = "08f7a7527cac"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("todos", sa.Column("due_date", sa.Date(), nullable=True))


def downgrade() -> None:
    op.drop_column("todos", "due_date")
