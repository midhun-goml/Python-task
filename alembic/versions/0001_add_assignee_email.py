"""add_assignee_email

Revision ID: 0001_add_assignee_email
Revises: 3663703a0183
Create Date: 2026-07-21 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = "0001_add_assignee_email"
down_revision = "3663703a0183"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "tickets",
        sa.Column("assignee_email", sa.String(length=254), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("tickets", "assignee_email")