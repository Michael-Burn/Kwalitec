"""Add archived column to study_plans.

Revision ID: 202609070004
Revises: 202609070003
Create Date: 2026-09-07 21:00:00.000000
"""

from __future__ import annotations

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "202609070004"
down_revision: Union[str, None] = "202609070003"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("study_plans") as batch_op:
        batch_op.add_column(
            sa.Column(
                "archived",
                sa.Boolean(),
                nullable=False,
                server_default=sa.false(),
                comment="Archived plans are hidden from active scheduling but preserved",
            )
        )


def downgrade() -> None:
    with op.batch_alter_table("study_plans") as batch_op:
        batch_op.drop_column("archived")