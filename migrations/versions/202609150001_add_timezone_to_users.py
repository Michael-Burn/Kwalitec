"""Add timezone to users.

Revision ID: 202609150001
Revises: 202608300001
Create Date: 2026-09-15 15:20:00.000000

Persists the learner's IANA timezone for streak study-day derivation.
Existing accounts default to Africa/Harare (founder location). Does not
change stored event timestamps; those remain UTC.
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "202609150001"
down_revision = "202608300001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table("users") as batch_op:
        batch_op.add_column(
            sa.Column(
                "timezone",
                sa.String(length=64),
                nullable=False,
                server_default="Africa/Harare",
                comment="IANA timezone identifier for learner-local study days",
            ),
        )


def downgrade() -> None:
    with op.batch_alter_table("users") as batch_op:
        batch_op.drop_column("timezone")
