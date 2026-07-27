"""SDT-001 Student Digital Twin foundation tables.

Revision ID: 202607270008
Revises: 202607270007
Create Date: 2026-07-27 20:00:00.000000

Additive SDT-001 schema. Does not alter CIP / CS-DOC / student experience tables.
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "202607270008"
down_revision: str | None = "202607270007"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "student_digital_twins",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("twin_id", sa.String(length=64), nullable=False),
        sa.Column("student_id", sa.String(length=128), nullable=False),
        sa.Column("display_name", sa.String(length=255), nullable=False),
        sa.Column("subject_code", sa.String(length=64), nullable=False),
        sa.Column("workspace_id", sa.String(length=128), nullable=False),
        sa.Column("external_user_id", sa.String(length=128), nullable=True),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "student_id",
            "workspace_id",
            "subject_code",
            name="uq_sdt_twin_scope",
        ),
    )
    op.create_index(
        "ix_student_digital_twins_twin_id",
        "student_digital_twins",
        ["twin_id"],
        unique=True,
    )
    op.create_index(
        "ix_sdt_twins_student", "student_digital_twins", ["student_id"], unique=False
    )

    op.create_table(
        "student_observations",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("observation_id", sa.String(length=64), nullable=False),
        sa.Column("twin_id", sa.String(length=64), nullable=False),
        sa.Column("student_id", sa.String(length=128), nullable=False),
        sa.Column("kind", sa.String(length=64), nullable=False),
        sa.Column("recorded_at", sa.DateTime(), nullable=False),
        sa.Column("curriculum_entity_id", sa.String(length=64), nullable=False),
        sa.Column("curriculum_entity_kind", sa.String(length=64), nullable=False),
        sa.Column("evidence_reference", sa.String(length=255), nullable=False),
        sa.Column("provenance", sa.String(length=255), nullable=False),
        sa.Column("metadata_json", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["twin_id"], ["student_digital_twins.twin_id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_student_observations_observation_id",
        "student_observations",
        ["observation_id"],
        unique=True,
    )
    op.create_index(
        "ix_student_observations_twin_id",
        "student_observations",
        ["twin_id"],
        unique=False,
    )
    op.create_index(
        "ix_student_observations_student_id",
        "student_observations",
        ["student_id"],
        unique=False,
    )
    op.create_index(
        "ix_sdt_obs_twin_recorded",
        "student_observations",
        ["twin_id", "recorded_at"],
        unique=False,
    )

    op.create_table(
        "mastery_records",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("mastery_id", sa.String(length=64), nullable=False),
        sa.Column("twin_id", sa.String(length=64), nullable=False),
        sa.Column("concept_id", sa.String(length=64), nullable=False),
        sa.Column("concept_title", sa.String(length=512), nullable=False),
        sa.Column("mastery_score", sa.Float(), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=False),
        sa.Column("trend", sa.String(length=32), nullable=False),
        sa.Column("evidence_count", sa.Integer(), nullable=False),
        sa.Column("supporting_evidence_json", sa.Text(), nullable=False),
        sa.Column("reason", sa.String(length=512), nullable=False),
        sa.Column("last_updated", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["twin_id"], ["student_digital_twins.twin_id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("twin_id", "concept_id", name="uq_sdt_mastery_concept"),
    )
    op.create_index(
        "ix_mastery_records_mastery_id", "mastery_records", ["mastery_id"], unique=True
    )
    op.create_index("ix_sdt_mastery_twin", "mastery_records", ["twin_id"], unique=False)

    op.create_table(
        "knowledge_gaps",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("gap_id", sa.String(length=64), nullable=False),
        sa.Column("twin_id", sa.String(length=64), nullable=False),
        sa.Column("concept_id", sa.String(length=64), nullable=False),
        sa.Column("concept_title", sa.String(length=512), nullable=False),
        sa.Column("severity", sa.String(length=32), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=False),
        sa.Column("likely_prerequisite_id", sa.String(length=64), nullable=False),
        sa.Column("likely_prerequisite_title", sa.String(length=512), nullable=False),
        sa.Column("supporting_evidence_json", sa.Text(), nullable=False),
        sa.Column("retrieval_log_id", sa.String(length=64), nullable=True),
        sa.Column("estimated_recovery_effort", sa.Float(), nullable=False),
        sa.Column("reason", sa.String(length=512), nullable=False),
        sa.Column("identified_at", sa.DateTime(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(["twin_id"], ["student_digital_twins.twin_id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_knowledge_gaps_gap_id", "knowledge_gaps", ["gap_id"], unique=True
    )
    op.create_index("ix_sdt_gaps_twin", "knowledge_gaps", ["twin_id"], unique=False)

    op.create_table(
        "learning_state_snapshots",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("snapshot_id", sa.String(length=64), nullable=False),
        sa.Column("twin_id", sa.String(length=64), nullable=False),
        sa.Column("knowledge", sa.Float(), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=False),
        sa.Column("retention", sa.Float(), nullable=False),
        sa.Column("consistency", sa.Float(), nullable=False),
        sa.Column("momentum", sa.Float(), nullable=False),
        sa.Column("exam_readiness", sa.Float(), nullable=False),
        sa.Column("evidence_count", sa.Integer(), nullable=False),
        sa.Column("reason", sa.String(length=512), nullable=False),
        sa.Column("computed_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["twin_id"], ["student_digital_twins.twin_id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_learning_state_snapshots_snapshot_id",
        "learning_state_snapshots",
        ["snapshot_id"],
        unique=True,
    )
    op.create_index(
        "ix_sdt_state_twin_computed",
        "learning_state_snapshots",
        ["twin_id", "computed_at"],
        unique=False,
    )

    op.create_table(
        "recommendations",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("recommendation_id", sa.String(length=64), nullable=False),
        sa.Column("twin_id", sa.String(length=64), nullable=False),
        sa.Column("title", sa.String(length=512), nullable=False),
        sa.Column("reason", sa.Text(), nullable=False),
        sa.Column("priority", sa.String(length=32), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=False),
        sa.Column("curriculum_entity_id", sa.String(length=64), nullable=False),
        sa.Column("supporting_evidence_json", sa.Text(), nullable=False),
        sa.Column("related_gap_id", sa.String(length=64), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(["twin_id"], ["student_digital_twins.twin_id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_recommendations_recommendation_id",
        "recommendations",
        ["recommendation_id"],
        unique=True,
    )
    op.create_index("ix_sdt_rec_twin", "recommendations", ["twin_id"], unique=False)

    op.create_table(
        "predictions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("prediction_id", sa.String(length=64), nullable=False),
        sa.Column("twin_id", sa.String(length=64), nullable=False),
        sa.Column("kind", sa.String(length=64), nullable=False),
        sa.Column("value", sa.Float(), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=False),
        sa.Column("horizon_days", sa.Integer(), nullable=False),
        sa.Column("supporting_evidence_json", sa.Text(), nullable=False),
        sa.Column("reason", sa.String(length=512), nullable=False),
        sa.Column("algorithm_version", sa.String(length=64), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(["twin_id"], ["student_digital_twins.twin_id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_predictions_prediction_id", "predictions", ["prediction_id"], unique=True
    )
    op.create_index("ix_sdt_pred_twin", "predictions", ["twin_id"], unique=False)

    op.create_table(
        "reasoning_history",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("reasoning_id", sa.String(length=64), nullable=False),
        sa.Column("twin_id", sa.String(length=64), nullable=False),
        sa.Column("triggered_by", sa.String(length=128), nullable=False),
        sa.Column("observation_ids_json", sa.Text(), nullable=False),
        sa.Column("steps_json", sa.Text(), nullable=False),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("reasoning_version", sa.String(length=64), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["twin_id"], ["student_digital_twins.twin_id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_reasoning_history_reasoning_id",
        "reasoning_history",
        ["reasoning_id"],
        unique=True,
    )
    op.create_index(
        "ix_sdt_reason_twin_created",
        "reasoning_history",
        ["twin_id", "created_at"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_sdt_reason_twin_created", table_name="reasoning_history")
    op.drop_index("ix_reasoning_history_reasoning_id", table_name="reasoning_history")
    op.drop_table("reasoning_history")

    op.drop_index("ix_sdt_pred_twin", table_name="predictions")
    op.drop_index("ix_predictions_prediction_id", table_name="predictions")
    op.drop_table("predictions")

    op.drop_index("ix_sdt_rec_twin", table_name="recommendations")
    op.drop_index("ix_recommendations_recommendation_id", table_name="recommendations")
    op.drop_table("recommendations")

    op.drop_index("ix_sdt_state_twin_computed", table_name="learning_state_snapshots")
    op.drop_index(
        "ix_learning_state_snapshots_snapshot_id", table_name="learning_state_snapshots"
    )
    op.drop_table("learning_state_snapshots")

    op.drop_index("ix_sdt_gaps_twin", table_name="knowledge_gaps")
    op.drop_index("ix_knowledge_gaps_gap_id", table_name="knowledge_gaps")
    op.drop_table("knowledge_gaps")

    op.drop_index("ix_sdt_mastery_twin", table_name="mastery_records")
    op.drop_index("ix_mastery_records_mastery_id", table_name="mastery_records")
    op.drop_table("mastery_records")

    op.drop_index("ix_sdt_obs_twin_recorded", table_name="student_observations")
    op.drop_index(
        "ix_student_observations_student_id", table_name="student_observations"
    )
    op.drop_index(
        "ix_student_observations_twin_id", table_name="student_observations"
    )
    op.drop_index(
        "ix_student_observations_observation_id", table_name="student_observations"
    )
    op.drop_table("student_observations")

    op.drop_index("ix_sdt_twins_student", table_name="student_digital_twins")
    op.drop_index(
        "ix_student_digital_twins_twin_id", table_name="student_digital_twins"
    )
    op.drop_table("student_digital_twins")
