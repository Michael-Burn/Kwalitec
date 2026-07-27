"""CIP-002 provenance, confidence, review, validation, audit, and metrics tables.

Revision ID: 202607270006
Revises: 202607270005
Create Date: 2026-07-27 16:00:00.000000

Additive CIP-002 schema. Does not alter CIP-001 pipeline tables.
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "202607270006"
down_revision: Union[str, None] = "202607270005"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "cip_provenance_records",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("provenance_id", sa.String(length=64), nullable=False),
        sa.Column("subject_kind", sa.String(length=32), nullable=False),
        sa.Column("subject_id", sa.String(length=64), nullable=False),
        sa.Column("source_document_id", sa.Integer(), nullable=False),
        sa.Column("source_version_label", sa.String(length=64), nullable=False),
        sa.Column("source_pages_csv", sa.String(length=512), nullable=False),
        sa.Column("source_paragraphs_csv", sa.String(length=512), nullable=False),
        sa.Column("source_block_ids_csv", sa.Text(), nullable=False),
        sa.Column("parser_version", sa.String(length=64), nullable=False),
        sa.Column("mapper_version", sa.String(length=64), nullable=False),
        sa.Column("graph_builder_version", sa.String(length=64), nullable=False),
        sa.Column("pipeline_job_id", sa.String(length=64), nullable=False),
        sa.Column("extraction_id", sa.String(length=64), nullable=False),
        sa.Column("parse_id", sa.String(length=64), nullable=False),
        sa.Column("map_id", sa.String(length=64), nullable=False),
        sa.Column("graph_id", sa.String(length=64), nullable=False),
        sa.Column("chain_stage", sa.String(length=64), nullable=False),
        sa.Column("attributes_json", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("provenance_id"),
    )
    op.create_index(
        "ix_cip_provenance_records_provenance_id",
        "cip_provenance_records",
        ["provenance_id"],
    )
    op.create_index(
        "ix_cip_prov_subject",
        "cip_provenance_records",
        ["subject_kind", "subject_id"],
    )
    op.create_index(
        "ix_cip_prov_document", "cip_provenance_records", ["source_document_id"]
    )
    op.create_index("ix_cip_prov_job", "cip_provenance_records", ["pipeline_job_id"])

    op.create_table(
        "cip_provenance_evidence",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("evidence_id", sa.String(length=64), nullable=False),
        sa.Column("provenance_id", sa.String(length=64), nullable=False),
        sa.Column("page_number", sa.Integer(), nullable=True),
        sa.Column("paragraph_index", sa.Integer(), nullable=True),
        sa.Column("block_id", sa.String(length=64), nullable=True),
        sa.Column("excerpt", sa.Text(), nullable=False),
        sa.Column("evidence_role", sa.String(length=64), nullable=False),
        sa.ForeignKeyConstraint(
            ["provenance_id"], ["cip_provenance_records.provenance_id"]
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("evidence_id"),
    )
    op.create_index(
        "ix_cip_provenance_evidence_evidence_id",
        "cip_provenance_evidence",
        ["evidence_id"],
    )
    op.create_index(
        "ix_cip_prov_ev_prov", "cip_provenance_evidence", ["provenance_id"]
    )

    op.create_table(
        "cip_confidence_records",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("confidence_id", sa.String(length=64), nullable=False),
        sa.Column("subject_kind", sa.String(length=32), nullable=False),
        sa.Column("subject_id", sa.String(length=64), nullable=False),
        sa.Column("score", sa.Float(), nullable=False),
        sa.Column("band", sa.String(length=32), nullable=False),
        sa.Column("reason", sa.String(length=512), nullable=False),
        sa.Column("needs_review", sa.Boolean(), nullable=False),
        sa.Column("review_threshold", sa.Float(), nullable=False),
        sa.Column("provenance_id", sa.String(length=64), nullable=True),
        sa.Column("document_id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("confidence_id"),
    )
    op.create_index(
        "ix_cip_confidence_records_confidence_id",
        "cip_confidence_records",
        ["confidence_id"],
    )
    op.create_index(
        "ix_cip_conf_subject",
        "cip_confidence_records",
        ["subject_kind", "subject_id"],
    )
    op.create_index(
        "ix_cip_conf_needs_review", "cip_confidence_records", ["needs_review"]
    )
    op.create_index(
        "ix_cip_confidence_records_document_id",
        "cip_confidence_records",
        ["document_id"],
    )

    op.create_table(
        "cip_confidence_factors",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("factor_id", sa.String(length=64), nullable=False),
        sa.Column("confidence_id", sa.String(length=64), nullable=False),
        sa.Column("code", sa.String(length=64), nullable=False),
        sa.Column("label", sa.String(length=256), nullable=False),
        sa.Column("weight", sa.Float(), nullable=False),
        sa.Column("contribution", sa.Float(), nullable=False),
        sa.Column("detail", sa.String(length=512), nullable=False),
        sa.ForeignKeyConstraint(
            ["confidence_id"], ["cip_confidence_records.confidence_id"]
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("factor_id"),
    )
    op.create_index(
        "ix_cip_confidence_factors_factor_id",
        "cip_confidence_factors",
        ["factor_id"],
    )
    op.create_index(
        "ix_cip_conf_fac_conf", "cip_confidence_factors", ["confidence_id"]
    )

    op.create_table(
        "cip_review_records",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("review_id", sa.String(length=64), nullable=False),
        sa.Column("subject_kind", sa.String(length=32), nullable=False),
        sa.Column("subject_id", sa.String(length=64), nullable=False),
        sa.Column("document_id", sa.Integer(), nullable=False),
        sa.Column("workspace_id", sa.String(length=128), nullable=False),
        sa.Column("decision", sa.String(length=32), nullable=False),
        sa.Column("review_status", sa.String(length=32), nullable=False),
        sa.Column("verification_status", sa.String(length=32), nullable=False),
        sa.Column("actor_id", sa.String(length=128), nullable=False),
        sa.Column("reason", sa.Text(), nullable=False),
        sa.Column(
            "suggested_learning_objective", sa.String(length=128), nullable=False
        ),
        sa.Column("remap_target_id", sa.String(length=64), nullable=False),
        sa.Column("confidence_at_review", sa.Float(), nullable=False),
        sa.Column("pipeline_job_id", sa.String(length=64), nullable=False),
        sa.Column("provenance_id", sa.String(length=64), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("review_id"),
    )
    op.create_index(
        "ix_cip_review_records_review_id", "cip_review_records", ["review_id"]
    )
    op.create_index(
        "ix_cip_review_subject",
        "cip_review_records",
        ["subject_kind", "subject_id"],
    )
    op.create_index("ix_cip_review_status", "cip_review_records", ["review_status"])
    op.create_index(
        "ix_cip_review_workspace", "cip_review_records", ["workspace_id"]
    )
    op.create_index(
        "ix_cip_review_records_document_id", "cip_review_records", ["document_id"]
    )

    op.create_table(
        "cip_validation_reports",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("report_id", sa.String(length=64), nullable=False),
        sa.Column("document_id", sa.Integer(), nullable=False),
        sa.Column("graph_id", sa.String(length=64), nullable=False),
        sa.Column("map_id", sa.String(length=64), nullable=False),
        sa.Column("pipeline_job_id", sa.String(length=64), nullable=False),
        sa.Column("issue_count", sa.Integer(), nullable=False),
        sa.Column("error_count", sa.Integer(), nullable=False),
        sa.Column("warning_count", sa.Integer(), nullable=False),
        sa.Column("passed", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("report_id"),
    )
    op.create_index(
        "ix_cip_validation_reports_report_id",
        "cip_validation_reports",
        ["report_id"],
    )
    op.create_index(
        "ix_cip_val_report_document", "cip_validation_reports", ["document_id"]
    )
    op.create_index(
        "ix_cip_val_report_graph", "cip_validation_reports", ["graph_id"]
    )

    op.create_table(
        "cip_validation_issues",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("issue_id", sa.String(length=64), nullable=False),
        sa.Column("report_id", sa.String(length=64), nullable=False),
        sa.Column("kind", sa.String(length=64), nullable=False),
        sa.Column("severity", sa.String(length=32), nullable=False),
        sa.Column("message", sa.String(length=512), nullable=False),
        sa.Column("subject_kind", sa.String(length=32), nullable=False),
        sa.Column("subject_id", sa.String(length=64), nullable=False),
        sa.Column("related_ids_csv", sa.Text(), nullable=False),
        sa.Column("document_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["report_id"], ["cip_validation_reports.report_id"]
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("issue_id"),
    )
    op.create_index(
        "ix_cip_validation_issues_issue_id", "cip_validation_issues", ["issue_id"]
    )
    op.create_index(
        "ix_cip_val_issue_report", "cip_validation_issues", ["report_id"]
    )
    op.create_index("ix_cip_val_issue_kind", "cip_validation_issues", ["kind"])

    op.create_table(
        "cip_audit_events",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("event_id", sa.String(length=64), nullable=False),
        sa.Column("action", sa.String(length=64), nullable=False),
        sa.Column("actor_id", sa.String(length=128), nullable=False),
        sa.Column("subject_kind", sa.String(length=32), nullable=False),
        sa.Column("subject_id", sa.String(length=64), nullable=False),
        sa.Column("document_id", sa.Integer(), nullable=True),
        sa.Column("pipeline_job_id", sa.String(length=64), nullable=False),
        sa.Column("document_version", sa.String(length=64), nullable=False),
        sa.Column("workspace_id", sa.String(length=128), nullable=False),
        sa.Column("message", sa.String(length=512), nullable=False),
        sa.Column("attributes_json", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("event_id"),
    )
    op.create_index(
        "ix_cip_audit_events_event_id", "cip_audit_events", ["event_id"]
    )
    op.create_index("ix_cip_audit_action", "cip_audit_events", ["action"])
    op.create_index(
        "ix_cip_audit_subject",
        "cip_audit_events",
        ["subject_kind", "subject_id"],
    )
    op.create_index("ix_cip_audit_workspace", "cip_audit_events", ["workspace_id"])
    op.create_index("ix_cip_audit_job", "cip_audit_events", ["pipeline_job_id"])

    op.create_table(
        "cip_quality_metrics",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("metrics_id", sa.String(length=64), nullable=False),
        sa.Column("document_id", sa.Integer(), nullable=False),
        sa.Column("pipeline_job_id", sa.String(length=64), nullable=False),
        sa.Column("workspace_id", sa.String(length=128), nullable=False),
        sa.Column("extraction_success_rate", sa.Float(), nullable=False),
        sa.Column("parser_success_rate", sa.Float(), nullable=False),
        sa.Column("mean_mapping_confidence", sa.Float(), nullable=False),
        sa.Column("graph_completeness", sa.Float(), nullable=False),
        sa.Column("graph_consistency", sa.Float(), nullable=False),
        sa.Column("entities_requiring_review", sa.Integer(), nullable=False),
        sa.Column("founder_approvals", sa.Integer(), nullable=False),
        sa.Column("founder_corrections", sa.Integer(), nullable=False),
        sa.Column("entity_count", sa.Integer(), nullable=False),
        sa.Column("relation_count", sa.Integer(), nullable=False),
        sa.Column("validation_error_count", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("metrics_id"),
    )
    op.create_index(
        "ix_cip_quality_metrics_metrics_id", "cip_quality_metrics", ["metrics_id"]
    )
    op.create_index(
        "ix_cip_metrics_document", "cip_quality_metrics", ["document_id"]
    )
    op.create_index(
        "ix_cip_metrics_workspace", "cip_quality_metrics", ["workspace_id"]
    )
    op.create_index("ix_cip_metrics_job", "cip_quality_metrics", ["pipeline_job_id"])


def downgrade() -> None:
    op.drop_table("cip_quality_metrics")
    op.drop_table("cip_audit_events")
    op.drop_table("cip_validation_issues")
    op.drop_table("cip_validation_reports")
    op.drop_table("cip_review_records")
    op.drop_table("cip_confidence_factors")
    op.drop_table("cip_confidence_records")
    op.drop_table("cip_provenance_evidence")
    op.drop_table("cip_provenance_records")
