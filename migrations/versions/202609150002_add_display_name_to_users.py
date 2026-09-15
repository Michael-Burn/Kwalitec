"""Add display_name to users.

Revision ID: 202609150002
Revises: 202609150001
Create Date: 2026-09-15 17:40:00.000000

Persists the student-facing display name on the User model. Empty string
for existing accounts until the student sets one on Profile. Does not
derive a name from email.
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "202609150002"
down_revision = "202609150001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table("users") as batch_op:
        batch_op.add_column(
            sa.Column(
                "display_name",
                sa.String(length=80),
                nullable=False,
                server_default="",
                comment="Student-facing display name",
            ),
        )


def downgrade() -> None:
    with op.batch_alter_table("users") as batch_op:
        batch_op.drop_column("display_name")
