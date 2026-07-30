"""EI-002A workspace ↔ generation chain binding columns.

Revision ID: 202607300004
Revises: 202607300003
Create Date: 2026-07-30 10:00:00.000000

Adds explicit binding columns on studio_workspace_projections and an
index supporting one-active-chain-per-workspace lookups.
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "202607300004"
down_revision: str | Sequence[str] | None = "202607300003"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "studio_workspace_projections",
        sa.Column("active_chain_id", sa.String(length=64), nullable=True),
    )
    op.add_column(
        "studio_workspace_projections",
        sa.Column("certified_snapshot_id", sa.String(length=64), nullable=True),
    )
    op.add_column(
        "studio_workspace_projections",
        sa.Column("calibration_profile_id", sa.String(length=64), nullable=True),
    )
    op.add_column(
        "studio_workspace_projections",
        sa.Column("certification_status", sa.String(length=64), nullable=True),
    )
    op.add_column(
        "studio_workspace_projections",
        sa.Column("review_pack_ref", sa.String(length=255), nullable=True),
    )
    op.create_index(
        "ix_studio_workspace_projections_active_chain_id",
        "studio_workspace_projections",
        ["active_chain_id"],
    )
    op.create_index(
        "ix_ei_generation_chains_workspace_active",
        "ei_generation_chains",
        ["workspace_id", "active_snapshot_id"],
    )


def downgrade() -> None:
    op.drop_index(
        "ix_ei_generation_chains_workspace_active",
        table_name="ei_generation_chains",
    )
    op.drop_index(
        "ix_studio_workspace_projections_active_chain_id",
        table_name="studio_workspace_projections",
    )
    op.drop_column("studio_workspace_projections", "review_pack_ref")
    op.drop_column("studio_workspace_projections", "certification_status")
    op.drop_column("studio_workspace_projections", "calibration_profile_id")
    op.drop_column("studio_workspace_projections", "certified_snapshot_id")
    op.drop_column("studio_workspace_projections", "active_chain_id")
