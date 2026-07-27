"""AME-001 Adaptive Mission Engine tables.

Revision ID: 202607270011
Revises: 202607270010
Create Date: 2026-07-27 24:00:00.000000

Additive schema. Does not alter SDT-001 Twin, SDT-002 reasoning, or SDT-003
Learning Graph tables. Does not duplicate Twin mastery / gap / recommendation
rows.
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "202607270011"
down_revision: str | None = "202607270010"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "adaptive_missions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("mission_id", sa.String(length=64), nullable=False),
        sa.Column("twin_id", sa.String(length=64), nullable=False),
        sa.Column("student_id", sa.String(length=128), nullable=False),
        sa.Column("mission_date", sa.Date(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("goal", sa.String(length=512), nullable=False),
        sa.Column("priority", sa.String(length=32), nullable=False),
        sa.Column("educational_objective", sa.Text(), nullable=False),
        sa.Column("primary_concept_id", sa.String(length=64), nullable=False),
        sa.Column("concepts_json", sa.Text(), nullable=False),
        sa.Column("estimated_duration_minutes", sa.Integer(), nullable=False),
        sa.Column("reason_summary", sa.Text(), nullable=False),
        sa.Column("educational_explanation", sa.Text(), nullable=False),
        sa.Column("expected_outcome", sa.Text(), nullable=False),
        sa.Column("success_criteria_json", sa.Text(), nullable=False),
        sa.Column("reflection_prompt", sa.Text(), nullable=False),
        sa.Column("evidence_json", sa.Text(), nullable=False),
        sa.Column("source_recommendation_ids_json", sa.Text(), nullable=False),
        sa.Column("source_gap_ids_json", sa.Text(), nullable=False),
        sa.Column("recovery_path_json", sa.Text(), nullable=False),
        sa.Column("reasoning_run_id", sa.String(length=64), nullable=False),
        sa.Column("schedule_json", sa.Text(), nullable=False),
        sa.Column("plan_json", sa.Text(), nullable=False),
        sa.Column("reason_json", sa.Text(), nullable=False),
        sa.Column("outcome_json", sa.Text(), nullable=False),
        sa.Column("validation_passed", sa.Boolean(), nullable=False),
        sa.Column("validation_summary", sa.Text(), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["twin_id"],
            ["student_digital_twins.twin_id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_adaptive_missions_mission_id",
        "adaptive_missions",
        ["mission_id"],
        unique=True,
    )
    op.create_index(
        "ix_ame_missions_twin_date",
        "adaptive_missions",
        ["twin_id", "mission_date"],
        unique=False,
    )
    op.create_index(
        "ix_ame_missions_student_status",
        "adaptive_missions",
        ["student_id", "status"],
        unique=False,
    )
    op.create_index(
        "ix_ame_missions_twin_status",
        "adaptive_missions",
        ["twin_id", "status"],
        unique=False,
    )

    op.create_table(
        "mission_steps",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("step_id", sa.String(length=64), nullable=False),
        sa.Column("mission_id", sa.String(length=64), nullable=False),
        sa.Column("step_order", sa.Integer(), nullable=False),
        sa.Column("activity_type", sa.String(length=64), nullable=False),
        sa.Column("concept_id", sa.String(length=64), nullable=False),
        sa.Column("title", sa.String(length=512), nullable=False),
        sa.Column("estimated_minutes", sa.Integer(), nullable=False),
        sa.Column("reason", sa.Text(), nullable=False),
        sa.Column("success_criterion", sa.Text(), nullable=False),
        sa.Column("evidence_json", sa.Text(), nullable=False),
        sa.Column("completed", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(
            ["mission_id"],
            ["adaptive_missions.mission_id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("mission_id", "step_id", name="uq_ame_step_id"),
    )
    op.create_index(
        "ix_mission_steps_step_id",
        "mission_steps",
        ["step_id"],
        unique=False,
    )
    op.create_index(
        "ix_ame_steps_mission_order",
        "mission_steps",
        ["mission_id", "step_order"],
        unique=False,
    )

    op.create_table(
        "mission_progress",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("progress_id", sa.String(length=64), nullable=False),
        sa.Column("mission_id", sa.String(length=64), nullable=False),
        sa.Column("steps_total", sa.Integer(), nullable=False),
        sa.Column("steps_completed", sa.Integer(), nullable=False),
        sa.Column("percent_complete", sa.Float(), nullable=False),
        sa.Column("last_step_id", sa.String(length=64), nullable=False),
        sa.Column("note", sa.Text(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["mission_id"],
            ["adaptive_missions.mission_id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("mission_id", name="uq_ame_progress_mission"),
    )
    op.create_index(
        "ix_mission_progress_progress_id",
        "mission_progress",
        ["progress_id"],
        unique=True,
    )

    op.create_table(
        "mission_history",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("history_id", sa.String(length=64), nullable=False),
        sa.Column("mission_id", sa.String(length=64), nullable=False),
        sa.Column("twin_id", sa.String(length=64), nullable=False),
        sa.Column("event_type", sa.String(length=64), nullable=False),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("payload_json", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["mission_id"],
            ["adaptive_missions.mission_id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_mission_history_history_id",
        "mission_history",
        ["history_id"],
        unique=True,
    )
    op.create_index(
        "ix_ame_history_mission_created",
        "mission_history",
        ["mission_id", "created_at"],
        unique=False,
    )
    op.create_index(
        "ix_ame_history_twin_created",
        "mission_history",
        ["twin_id", "created_at"],
        unique=False,
    )

    op.create_table(
        "mission_feedback",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("feedback_id", sa.String(length=64), nullable=False),
        sa.Column("mission_id", sa.String(length=64), nullable=False),
        sa.Column("twin_id", sa.String(length=64), nullable=False),
        sa.Column("rating", sa.Integer(), nullable=True),
        sa.Column("comment", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["mission_id"],
            ["adaptive_missions.mission_id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_mission_feedback_feedback_id",
        "mission_feedback",
        ["feedback_id"],
        unique=True,
    )
    op.create_index(
        "ix_ame_feedback_mission",
        "mission_feedback",
        ["mission_id"],
        unique=False,
    )

    op.create_table(
        "mission_completion",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("completion_id", sa.String(length=64), nullable=False),
        sa.Column("mission_id", sa.String(length=64), nullable=False),
        sa.Column("twin_id", sa.String(length=64), nullable=False),
        sa.Column("completed_at", sa.DateTime(), nullable=False),
        sa.Column("steps_completed", sa.Integer(), nullable=False),
        sa.Column("steps_total", sa.Integer(), nullable=False),
        sa.Column("outcome_achieved", sa.Boolean(), nullable=False),
        sa.Column("reflection_response", sa.Text(), nullable=False),
        sa.Column("feedback_summary", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(
            ["mission_id"],
            ["adaptive_missions.mission_id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("mission_id", name="uq_ame_completion_mission"),
    )
    op.create_index(
        "ix_mission_completion_completion_id",
        "mission_completion",
        ["completion_id"],
        unique=True,
    )


def downgrade() -> None:
    op.drop_table("mission_completion")
    op.drop_table("mission_feedback")
    op.drop_table("mission_history")
    op.drop_table("mission_progress")
    op.drop_table("mission_steps")
    op.drop_table("adaptive_missions")
