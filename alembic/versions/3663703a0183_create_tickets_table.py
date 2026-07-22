"""create_tickets_table

Revision ID: 3663703a0183
Revises: 
Create Date: 2026-07-21 22:32:36.125174

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = '3663703a0183'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'tickets',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('description', sa.String(length=500), nullable=True),
        sa.Column('priority', postgresql.ENUM('low', 'medium', 'high', 'critical', name='ticket_priority', create_type=True), nullable=False),
        sa.Column('status', postgresql.ENUM('open', 'in_progress', 'resolved', 'closed', name='ticket_status', create_type=True), nullable=False, server_default='open'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade() -> None:
    op.drop_table('tickets')
    op.execute("DROP TYPE IF EXISTS ticket_priority")
    op.execute("DROP TYPE IF EXISTS ticket_status")