"""AP-001 Assessment & Learning Feedback Pipeline tables.

Revision ID: 202607270012
Revises: 202607270011
Create Date: 2026-07-27 25:00:00.000000

Additive schema. Does not alter SDT-001 Twin, SDT-002 reasoning, SDT-003
Learning Graph, or AME-001 Adaptive Mission tables. Does not duplicate Twin
mastery / gap / recommendation rows.
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "202607270012"
down_revision: str | None = "202607270011"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "assessment_events",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("event_id", sa.String(length=64), nullable=False),
        sa.Column("event_type", sa.String(length=64), nullable=False),
        sa.Column("twin_id", sa.String(length=64), nullable=False),
        sa.Column("student_id", sa.String(length=128), nullable=False),
        sa.Column("occurred_at", sa.DateTime(), nullable=False),
        sa.Column("activity_id", sa.String(length=128), nullable=False),
        sa.Column("curriculum_entity_id", sa.String(length=128), nullable=False),
        sa.Column("curriculum_entity_kind", sa.String(length=64), nullable=False),
        sa.Column("concept_ids_json", sa.Text(), nullable=False),
        sa.Column("mission_id", sa.String(length=64), nullable=False),
        sa.Column("step_id", sa.String(length=64), nullable=False),
        sa.Column("source", sa.String(length=128), nullable=False),
        sa.Column("score", sa.Float(), nullable=True),
        sa.Column("correct", sa.Boolean(), nullable=True),
        sa.Column("duration_seconds", sa.Integer(), nullable=True),
        sa.Column("metadata_json", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["twin_id"],
            ["student_digital_twins.twin_id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_assessment_events_event_id",
        "assessment_events",
        ["event_id"],
        unique=True,
    )
    op.create_index(
        "ix_ap_events_twin_occurred",
        "assessment_events",
        ["twin_id", "occurred_at"],
        unique=False,
    )
    op.create_index(
        "ix_ap_events_student_type",
        "assessment_events",
        ["student_id", "event_type"],
        unique=False,
    )
    op.create_index(
        "ix_ap_events_mission",
        "assessment_events",
        ["mission_id"],
        unique=False,
    )

    op.create_table(
        "assessment_results",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("result_id", sa.String(length=64), nullable=False),
        sa.Column("event_id", sa.String(length=64), nullable=False),
        sa.Column("twin_id", sa.String(length=64), nullable=False),
        sa.Column("event_type", sa.String(length=64), nullable=False),
        sa.Column("observation_id", sa.String(length=64), nullable=False),
        sa.Column("performance_label", sa.String(length=64), nullable=False),
        sa.Column("evidence_json", sa.Text(), nullable=False),
        sa.Column("concepts_json", sa.Text(), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=False),
        sa.Column("metadata_json", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["event_id"],
            ["assessment_events.event_id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_assessment_results_result_id",
        "assessment_results",
        ["result_id"],
        unique=True,
    )
    op.create_index(
        "ix_ap_results_twin_created",
        "assessment_results",
        ["twin_id", "created_at"],
        unique=False,
    )
    op.create_index(
        "ix_ap_results_event",
        "assessment_results",
        ["event_id"],
        unique=False,
    )

    op.create_table(
        "learning_feedback",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("feedback_id", sa.String(length=64), nullable=False),
        sa.Column("twin_id", sa.String(length=64), nullable=False),
        sa.Column("event_id", sa.String(length=64), nullable=False),
        sa.Column("result_id", sa.String(length=64), nullable=False),
        sa.Column("activity", sa.String(length=256), nullable=False),
        sa.Column("performance", sa.String(length=64), nullable=False),
        sa.Column("evidence_json", sa.Text(), nullable=False),
        sa.Column("concepts_json", sa.Text(), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=False),
        sa.Column("suggested_next_action", sa.Text(), nullable=False),
        sa.Column("timestamp", sa.DateTime(), nullable=False),
        sa.Column("source", sa.String(length=64), nullable=False),
        sa.Column("observation_id", sa.String(length=64), nullable=False),
        sa.Column("mission_id", sa.String(length=64), nullable=False),
        sa.Column("metadata_json", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(
            ["event_id"],
            ["assessment_events.event_id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_learning_feedback_feedback_id",
        "learning_feedback",
        ["feedback_id"],
        unique=True,
    )
    op.create_index(
        "ix_ap_feedback_twin_ts",
        "learning_feedback",
        ["twin_id", "timestamp"],
        unique=False,
    )
    op.create_index(
        "ix_ap_feedback_event",
        "learning_feedback",
        ["event_id"],
        unique=False,
    )

    op.create_table(
        "mission_assessment_links",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("link_id", sa.String(length=64), nullable=False),
        sa.Column("twin_id", sa.String(length=64), nullable=False),
        sa.Column("mission_id", sa.String(length=64), nullable=False),
        sa.Column("event_id", sa.String(length=64), nullable=False),
        sa.Column("observation_id", sa.String(length=64), nullable=False),
        sa.Column("step_id", sa.String(length=64), nullable=False),
        sa.Column("link_kind", sa.String(length=64), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["event_id"],
            ["assessment_events.event_id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("mission_id", "event_id", name="uq_ap_mission_event_link"),
    )
    op.create_index(
        "ix_mission_assessment_links_link_id",
        "mission_assessment_links",
        ["link_id"],
        unique=True,
    )
    op.create_index(
        "ix_ap_mission_links_twin",
        "mission_assessment_links",
        ["twin_id"],
        unique=False,
    )
    op.create_index(
        "ix_ap_mission_links_mission",
        "mission_assessment_links",
        ["mission_id"],
        unique=False,
    )

    op.create_table(
        "activity_attempts",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("attempt_id", sa.String(length=64), nullable=False),
        sa.Column("twin_id", sa.String(length=64), nullable=False),
        sa.Column("student_id", sa.String(length=128), nullable=False),
        sa.Column("activity_id", sa.String(length=128), nullable=False),
        sa.Column("activity_kind", sa.String(length=64), nullable=False),
        sa.Column("attempted_at", sa.DateTime(), nullable=False),
        sa.Column("event_id", sa.String(length=64), nullable=False),
        sa.Column("curriculum_entity_id", sa.String(length=128), nullable=False),
        sa.Column("concept_ids_json", sa.Text(), nullable=False),
        sa.Column("score", sa.Float(), nullable=True),
        sa.Column("correct", sa.Boolean(), nullable=True),
        sa.Column("duration_seconds", sa.Integer(), nullable=True),
        sa.Column("metadata_json", sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_activity_attempts_attempt_id",
        "activity_attempts",
        ["attempt_id"],
        unique=True,
    )
    op.create_index(
        "ix_ap_attempts_twin_at",
        "activity_attempts",
        ["twin_id", "attempted_at"],
        unique=False,
    )
    op.create_index(
        "ix_ap_attempts_activity",
        "activity_attempts",
        ["activity_id"],
        unique=False,
    )

    op.create_table(
        "performance_summaries",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("summary_id", sa.String(length=64), nullable=False),
        sa.Column("twin_id", sa.String(length=64), nullable=False),
        sa.Column("student_id", sa.String(length=128), nullable=False),
        sa.Column("event_count", sa.Integer(), nullable=False),
        sa.Column("attempt_count", sa.Integer(), nullable=False),
        sa.Column("correct_count", sa.Integer(), nullable=False),
        sa.Column("incorrect_count", sa.Integer(), nullable=False),
        sa.Column("mean_score", sa.Float(), nullable=True),
        sa.Column("concepts_json", sa.Text(), nullable=False),
        sa.Column("generated_at", sa.DateTime(), nullable=False),
        sa.Column("window_start", sa.DateTime(), nullable=True),
        sa.Column("window_end", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_performance_summaries_summary_id",
        "performance_summaries",
        ["summary_id"],
        unique=True,
    )
    op.create_index(
        "ix_ap_perf_twin_generated",
        "performance_summaries",
        ["twin_id", "generated_at"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_ap_perf_twin_generated", table_name="performance_summaries")
    op.drop_index(
        "ix_performance_summaries_summary_id", table_name="performance_summaries"
    )
    op.drop_table("performance_summaries")

    op.drop_index("ix_ap_attempts_activity", table_name="activity_attempts")
    op.drop_index("ix_ap_attempts_twin_at", table_name="activity_attempts")
    op.drop_index("ix_activity_attempts_attempt_id", table_name="activity_attempts")
    op.drop_table("activity_attempts")

    op.drop_index("ix_ap_mission_links_mission", table_name="mission_assessment_links")
    op.drop_index("ix_ap_mission_links_twin", table_name="mission_assessment_links")
    op.drop_index(
        "ix_mission_assessment_links_link_id", table_name="mission_assessment_links"
    )
    op.drop_table("mission_assessment_links")

    op.drop_index("ix_ap_feedback_event", table_name="learning_feedback")
    op.drop_index("ix_ap_feedback_twin_ts", table_name="learning_feedback")
    op.drop_index("ix_learning_feedback_feedback_id", table_name="learning_feedback")
    op.drop_table("learning_feedback")

    op.drop_index("ix_ap_results_event", table_name="assessment_results")
    op.drop_index("ix_ap_results_twin_created", table_name="assessment_results")
    op.drop_index("ix_assessment_results_result_id", table_name="assessment_results")
    op.drop_table("assessment_results")

    op.drop_index("ix_ap_events_mission", table_name="assessment_events")
    op.drop_index("ix_ap_events_student_type", table_name="assessment_events")
    op.drop_index("ix_ap_events_twin_occurred", table_name="assessment_events")
    op.drop_index("ix_assessment_events_event_id", table_name="assessment_events")
    op.drop_table("assessment_events")
