"""Add daily_goal_hours to users.

Revision ID: 202608270001
Revises: 202608240002
Create Date: 2026-08-27 16:30:00.000000

Persists the Settings daily study goal preference on the User model.
Previously stored only in the Flask session (lost across browsers/devices).
Does not wire the value into progress-tracking or mastery math.
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "202608270001"
down_revision = "202608240002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table("users") as batch_op:
        batch_op.add_column(
            sa.Column(
                "daily_goal_hours",
                sa.Float(),
                nullable=False,
                server_default="2",
                comment="Preferred daily study goal in hours",
            ),
        )


def downgrade() -> None:
    with op.batch_alter_table("users") as batch_op:
        batch_op.drop_column("daily_goal_hours")
