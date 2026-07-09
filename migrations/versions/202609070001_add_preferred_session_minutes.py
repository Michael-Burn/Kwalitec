"""Add preferred_session_minutes to study_plans

Revision ID: 202609070001
Revises: 202607080005
Create Date: 2026-09-07 10:25:00.000000
"""

from alembic import op
import sqlalchemy as sa


revision = "202609070001"
down_revision = "0a272936a47b"
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table("study_plans") as batch_op:
        batch_op.add_column(
            sa.Column(
                "preferred_session_minutes",
                sa.Integer(),
                nullable=False,
                server_default="60",
                comment="Preferred study session length in minutes (30/45/60/90/120)",
            ),
        )


def downgrade() -> None:
    with op.batch_alter_table("study_plans") as batch_op:
        batch_op.drop_column("preferred_session_minutes")
