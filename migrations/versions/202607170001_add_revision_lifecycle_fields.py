"""Add Revision lifecycle presentation fields to study_plans.

Revision ID: 202607170001
Revises: 202607160003
Create Date: 2026-07-17 18:00:00.000000

V1SP-001A — Learning Lifecycle Completion.

Persists revision entry timestamp and one-time acknowledgement only.
Lifecycle stage itself remains derived from Study Progress (authoritative).
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "202607170001"
down_revision: str | None = "202607160003"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    with op.batch_alter_table("study_plans", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "revision_entered_at",
                sa.DateTime(),
                nullable=True,
            )
        )
        batch_op.add_column(
            sa.Column(
                "revision_acknowledged",
                sa.Boolean(),
                nullable=False,
                server_default=sa.false(),
            )
        )


def downgrade() -> None:
    with op.batch_alter_table("study_plans", schema=None) as batch_op:
        batch_op.drop_column("revision_acknowledged")
        batch_op.drop_column("revision_entered_at")
