"""LP-001 Learner Lifecycle Orchestration — operation checkpoints.

Revision ID: 202607280080
Revises: 202607280070
Create Date: 2026-07-28 22:00:00.000000

Additive: llp_lifecycle_operations.

Does not alter ere_educational_decisions, tie_node_beliefs,
lee_evidence_events, CKG, V1/V2 curriculum engine, missions, or
recommendation schema.
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "202607280080"
down_revision: str | tuple[str, ...] | None = "202607280070"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "llp_lifecycle_operations",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("operation_id", sa.String(length=64), nullable=False),
        sa.Column("operation_type", sa.String(length=32), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("student_id", sa.Integer(), nullable=True),
        sa.Column("instance_id", sa.String(length=64), nullable=True),
        sa.Column("correlation_id", sa.String(length=64), nullable=True),
        sa.Column("completed_stages_json", sa.Text(), nullable=False),
        sa.Column("failed_stage", sa.String(length=64), nullable=True),
        sa.Column("failure_cause", sa.Text(), nullable=True),
        sa.Column("attempt_count", sa.Integer(), nullable=False),
        sa.Column("orchestrator_version", sa.String(length=32), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["student_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("operation_id"),
    )
    op.create_index(
        "ix_llp_lifecycle_operations_operation_id",
        "llp_lifecycle_operations",
        ["operation_id"],
        unique=False,
    )
    op.create_index(
        "ix_llp_lifecycle_operations_operation_type",
        "llp_lifecycle_operations",
        ["operation_type"],
        unique=False,
    )
    op.create_index(
        "ix_llp_lifecycle_operations_status",
        "llp_lifecycle_operations",
        ["status"],
        unique=False,
    )
    op.create_index(
        "ix_llp_lifecycle_operations_student_id",
        "llp_lifecycle_operations",
        ["student_id"],
        unique=False,
    )
    op.create_index(
        "ix_llp_lifecycle_operations_instance_id",
        "llp_lifecycle_operations",
        ["instance_id"],
        unique=False,
    )
    op.create_index(
        "ix_llp_ops_instance_status",
        "llp_lifecycle_operations",
        ["instance_id", "status"],
        unique=False,
    )
    op.create_index(
        "ix_llp_ops_student",
        "llp_lifecycle_operations",
        ["student_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_llp_ops_student", table_name="llp_lifecycle_operations")
    op.drop_index("ix_llp_ops_instance_status", table_name="llp_lifecycle_operations")
    op.drop_index(
        "ix_llp_lifecycle_operations_instance_id",
        table_name="llp_lifecycle_operations",
    )
    op.drop_index(
        "ix_llp_lifecycle_operations_student_id",
        table_name="llp_lifecycle_operations",
    )
    op.drop_index(
        "ix_llp_lifecycle_operations_status",
        table_name="llp_lifecycle_operations",
    )
    op.drop_index(
        "ix_llp_lifecycle_operations_operation_type",
        table_name="llp_lifecycle_operations",
    )
    op.drop_index(
        "ix_llp_lifecycle_operations_operation_id",
        table_name="llp_lifecycle_operations",
    )
    op.drop_table("llp_lifecycle_operations")
