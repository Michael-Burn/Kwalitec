"""EI-001B generation hash columns on snapshots.

Revision ID: 202607300002
Revises: 202607300001
Create Date: 2026-07-30 07:00:00.000000

Additive columns for deterministic generation hashes and agent provenance.
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "202607300002"
down_revision: str | Sequence[str] | None = "202607300001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "ei_generation_snapshots",
        sa.Column(
            "generation_hash",
            sa.String(length=64),
            nullable=False,
            server_default="",
        ),
    )
    op.add_column(
        "ei_generation_snapshots",
        sa.Column(
            "agent_id",
            sa.String(length=128),
            nullable=False,
            server_default="",
        ),
    )
    op.add_column(
        "ei_generation_snapshots",
        sa.Column(
            "agent_version",
            sa.String(length=64),
            nullable=False,
            server_default="",
        ),
    )


def downgrade() -> None:
    op.drop_column("ei_generation_snapshots", "agent_version")
    op.drop_column("ei_generation_snapshots", "agent_id")
    op.drop_column("ei_generation_snapshots", "generation_hash")
