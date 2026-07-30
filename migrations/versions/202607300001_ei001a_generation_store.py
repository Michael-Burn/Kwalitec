"""EI-001A generation store tables.

Revision ID: 202607300001
Revises: 202607290001
Create Date: 2026-07-30 06:30:00.000000

Additive Curriculum Intelligence Engine persistence. Does not alter CIP
pipeline tables or Student Runtime schema.
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "202607300001"
down_revision: str | Sequence[str] | None = "202607290001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "ei_generation_chains",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("chain_id", sa.String(length=64), nullable=False),
        sa.Column("workspace_id", sa.String(length=128), nullable=False),
        sa.Column("active_snapshot_id", sa.String(length=64), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("chain_id"),
    )
    op.create_index(
        "ix_ei_generation_chains_chain_id", "ei_generation_chains", ["chain_id"]
    )
    op.create_index(
        "ix_ei_generation_chains_workspace_id",
        "ei_generation_chains",
        ["workspace_id"],
    )

    op.create_table(
        "ei_generations",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("generation_id", sa.String(length=64), nullable=False),
        sa.Column("chain_id", sa.String(length=64), nullable=False),
        sa.Column("generation_index", sa.Integer(), nullable=False),
        sa.Column("purpose", sa.String(length=128), nullable=False),
        sa.Column("parent_generation_ids_json", sa.Text(), nullable=False),
        sa.Column("source_document_ids_json", sa.Text(), nullable=False),
        sa.Column("workspace_id", sa.String(length=128), nullable=False),
        sa.Column("calibration_profile_id", sa.String(length=64), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("generation_id"),
    )
    op.create_index(
        "ix_ei_generations_generation_id", "ei_generations", ["generation_id"]
    )
    op.create_index("ix_ei_generations_chain_id", "ei_generations", ["chain_id"])
    op.create_index(
        "ix_ei_gen_chain_index", "ei_generations", ["chain_id", "generation_index"]
    )

    op.create_table(
        "ei_generation_snapshots",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("snapshot_id", sa.String(length=64), nullable=False),
        sa.Column("generation_id", sa.String(length=64), nullable=False),
        sa.Column("chain_id", sa.String(length=64), nullable=False),
        sa.Column("generation_index", sa.Integer(), nullable=False),
        sa.Column("provenance_bundle_id", sa.String(length=64), nullable=False),
        sa.Column("status", sa.String(length=64), nullable=False),
        sa.Column("metrics_json", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["generation_id"], ["ei_generations.generation_id"]
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("snapshot_id"),
    )
    op.create_index(
        "ix_ei_generation_snapshots_snapshot_id",
        "ei_generation_snapshots",
        ["snapshot_id"],
    )
    op.create_index(
        "ix_ei_generation_snapshots_chain_id",
        "ei_generation_snapshots",
        ["chain_id"],
    )
    op.create_index(
        "ix_ei_snap_chain_status",
        "ei_generation_snapshots",
        ["chain_id", "status"],
    )
    op.create_index(
        "ix_ei_snap_generation", "ei_generation_snapshots", ["generation_id"]
    )

    op.create_table(
        "ei_educational_nodes",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("snapshot_id", sa.String(length=64), nullable=False),
        sa.Column("chain_id", sa.String(length=64), nullable=False),
        sa.Column("node_id", sa.String(length=64), nullable=False),
        sa.Column("generation_local_id", sa.String(length=64), nullable=False),
        sa.Column("title", sa.String(length=512), nullable=False),
        sa.Column("kind", sa.String(length=64), nullable=False),
        sa.Column("role", sa.String(length=64), nullable=True),
        sa.Column("parent_node_id", sa.String(length=64), nullable=True),
        sa.Column("active", sa.Boolean(), nullable=False),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column("provenance_id", sa.String(length=64), nullable=True),
        sa.Column("confidence_json", sa.Text(), nullable=False),
        sa.Column("lineage_json", sa.Text(), nullable=False),
        sa.Column("provenance_json", sa.Text(), nullable=True),
        sa.Column("attributes_json", sa.Text(), nullable=False),
        sa.Column("is_rejected_record", sa.Boolean(), nullable=False),
        sa.Column("rejection_reason_code", sa.String(length=128), nullable=True),
        sa.Column("rejection_reason_label", sa.String(length=512), nullable=True),
        sa.Column("rejected_at_generation", sa.String(length=64), nullable=True),
        sa.Column("rejection_confidence", sa.Float(), nullable=True),
        sa.ForeignKeyConstraint(
            ["snapshot_id"], ["ei_generation_snapshots.snapshot_id"]
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "snapshot_id", "node_id", name="uq_ei_node_snapshot_node"
        ),
    )
    op.create_index("ix_ei_node_snap", "ei_educational_nodes", ["snapshot_id"])
    op.create_index(
        "ix_ei_node_stable", "ei_educational_nodes", ["chain_id", "node_id"]
    )

    op.create_table(
        "ei_lineage_operations",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("operation_id", sa.String(length=64), nullable=False),
        sa.Column("chain_id", sa.String(length=64), nullable=False),
        sa.Column("node_id", sa.String(length=64), nullable=False),
        sa.Column("kind", sa.String(length=32), nullable=False),
        sa.Column("generation_id", sa.String(length=64), nullable=False),
        sa.Column("generation_index", sa.Integer(), nullable=False),
        sa.Column("reason_code", sa.String(length=128), nullable=False),
        sa.Column("reason_label", sa.String(length=512), nullable=False),
        sa.Column("related_node_ids_json", sa.Text(), nullable=False),
        sa.Column("evidence_refs_json", sa.Text(), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("operation_id", name="uq_ei_lineage_operation_id"),
    )
    op.create_index(
        "ix_ei_lineage_node", "ei_lineage_operations", ["chain_id", "node_id"]
    )

    op.create_table(
        "ei_regression_reports",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("report_id", sa.String(length=64), nullable=False),
        sa.Column("chain_id", sa.String(length=64), nullable=False),
        sa.Column("candidate_generation_id", sa.String(length=64), nullable=False),
        sa.Column("candidate_snapshot_id", sa.String(length=64), nullable=False),
        sa.Column("baseline_generation_ids_json", sa.Text(), nullable=False),
        sa.Column("accepted", sa.Boolean(), nullable=False),
        sa.Column("reason", sa.String(length=512), nullable=False),
        sa.Column("candidate_metrics_json", sa.Text(), nullable=False),
        sa.Column("baseline_metrics_json", sa.Text(), nullable=False),
        sa.Column("gate_failures_json", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("report_id"),
    )
    op.create_index(
        "ix_ei_regression_reports_report_id", "ei_regression_reports", ["report_id"]
    )
    op.create_index("ix_ei_reg_chain", "ei_regression_reports", ["chain_id"])

    op.create_table(
        "ei_certification_records",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("decision_id", sa.String(length=64), nullable=False),
        sa.Column("chain_id", sa.String(length=64), nullable=False),
        sa.Column("snapshot_id", sa.String(length=64), nullable=False),
        sa.Column("outcome", sa.String(length=64), nullable=False),
        sa.Column("quality_score", sa.Float(), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=False),
        sa.Column("coverage", sa.Float(), nullable=False),
        sa.Column("hierarchy_score", sa.Float(), nullable=False),
        sa.Column("granularity_score", sa.Float(), nullable=False),
        sa.Column("warnings_json", sa.Text(), nullable=False),
        sa.Column("hard_gate_failures_json", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("decision_id"),
        sa.UniqueConstraint("snapshot_id"),
    )
    op.create_index(
        "ix_ei_certification_records_decision_id",
        "ei_certification_records",
        ["decision_id"],
    )
    op.create_index("ix_ei_cert_chain", "ei_certification_records", ["chain_id"])

    op.create_table(
        "ei_calibration_profiles",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("profile_id", sa.String(length=64), nullable=False),
        sa.Column("workspace_id", sa.String(length=128), nullable=False),
        sa.Column("granularity", sa.String(length=64), nullable=False),
        sa.Column("hierarchy", sa.String(length=64), nullable=False),
        sa.Column("topic_density", sa.String(length=64), nullable=False),
        sa.Column("difficulty_bias", sa.String(length=64), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("profile_id"),
    )
    op.create_index(
        "ix_ei_calibration_profiles_profile_id",
        "ei_calibration_profiles",
        ["profile_id"],
    )
    op.create_index("ix_ei_cal_workspace", "ei_calibration_profiles", ["workspace_id"])


def downgrade() -> None:
    op.drop_table("ei_calibration_profiles")
    op.drop_table("ei_certification_records")
    op.drop_table("ei_regression_reports")
    op.drop_table("ei_lineage_operations")
    op.drop_table("ei_educational_nodes")
    op.drop_table("ei_generation_snapshots")
    op.drop_table("ei_generations")
    op.drop_table("ei_generation_chains")
