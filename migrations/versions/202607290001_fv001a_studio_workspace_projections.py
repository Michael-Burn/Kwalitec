"""FV-001A durable Curriculum Studio workspace projections.

Revision ID: 202607290001
Revises: 202607280080
Create Date: 2026-07-29 21:20:00.000000

Persists Founder workflow stage + publication facts so Curriculum Studio
survives process restart. Does not alter curriculum extraction, student
schema, or recommendation engines.
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "202607290001"
down_revision: str | Sequence[str] | None = "202607280080"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "studio_workspace_projections",
        sa.Column("workspace_id", sa.String(length=128), nullable=False),
        sa.Column("subject_code", sa.String(length=64), nullable=False),
        sa.Column("subject_title", sa.String(length=255), nullable=False),
        sa.Column("version_label", sa.String(length=64), nullable=False),
        sa.Column("version_id", sa.String(length=128), nullable=True),
        sa.Column("status", sa.String(length=64), nullable=False),
        sa.Column("current_stage", sa.String(length=64), nullable=False),
        sa.Column("highest_stage_reached", sa.String(length=64), nullable=False),
        sa.Column("facts_json", sa.Text(), nullable=False),
        sa.Column("structure_json", sa.Text(), nullable=False),
        sa.Column("workflow_history_json", sa.Text(), nullable=False),
        sa.Column("metadata_json", sa.Text(), nullable=False),
        sa.Column("estimated_workload_hours", sa.Float(), nullable=True),
        sa.Column("notes", sa.Text(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("workspace_id"),
    )
    with op.batch_alter_table("studio_workspace_projections", schema=None) as batch_op:
        batch_op.create_index(
            "ix_studio_workspace_projections_subject_code",
            ["subject_code"],
            unique=False,
        )
        batch_op.create_index(
            "ix_studio_workspace_projections_current_stage",
            ["current_stage"],
            unique=False,
        )


def downgrade() -> None:
    with op.batch_alter_table("studio_workspace_projections", schema=None) as batch_op:
        batch_op.drop_index("ix_studio_workspace_projections_current_stage")
        batch_op.drop_index("ix_studio_workspace_projections_subject_code")
    op.drop_table("studio_workspace_projections")
