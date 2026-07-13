"""Add welcome onboarding flags to users.

Revision ID: 202607130001
Revises: 202611120001
Create Date: 2026-07-13 11:00:00.000000

Capability 4.4 — First-Time Student Experience.

Adds welcome_eligible / welcome_dismissed so the welcome modal shows once
after Study Plan + Calibration and never again after dismissal.
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "202607130001"
down_revision: Union[str, None] = "202611120001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "welcome_eligible",
                sa.Boolean(),
                nullable=False,
                server_default=sa.false(),
            )
        )
        batch_op.add_column(
            sa.Column(
                "welcome_dismissed",
                sa.Boolean(),
                nullable=False,
                server_default=sa.false(),
            )
        )


def downgrade() -> None:
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.drop_column("welcome_dismissed")
        batch_op.drop_column("welcome_eligible")
