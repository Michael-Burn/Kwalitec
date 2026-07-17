"""Add performance indexes for Version 1 hot paths (V1SP-003).

Revision ID: 202607170003
Revises: 202607170002
Create Date: 2026-07-17 20:30:00.000000

Evidence from baseline profiling:
- Operational Health filters missions by status + mission_date
- Analytics / readiness filter study_attempts by user_id + study_date
- Dashboard / OH filter study_plans by active / archived / revision
- Topic progress filtered by user_id (+ next_review_date / stage)
"""

from __future__ import annotations

from collections.abc import Sequence

from alembic import op

revision: str = "202607170003"
down_revision: str | None = "202607170002"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    with op.batch_alter_table("missions") as batch_op:
        batch_op.create_index(
            "ix_missions_status_mission_date",
            ["status", "mission_date"],
        )

    with op.batch_alter_table("study_attempts") as batch_op:
        batch_op.create_index(
            "ix_study_attempts_user_study_date",
            ["user_id", "study_date"],
        )

    with op.batch_alter_table("study_plans") as batch_op:
        batch_op.create_index(
            "ix_study_plans_active_archived",
            ["active", "archived"],
        )
        batch_op.create_index(
            "ix_study_plans_user_active_archived",
            ["user_id", "active", "archived"],
        )

    with op.batch_alter_table("topic_progress") as batch_op:
        batch_op.create_index(
            "ix_topic_progress_user_topic",
            ["user_id", "topic_id"],
        )
        batch_op.create_index(
            "ix_topic_progress_user_next_review",
            ["user_id", "next_review_date"],
        )
        batch_op.create_index(
            "ix_topic_progress_user_stage",
            ["user_id", "current_stage"],
        )

    with op.batch_alter_table("mission_tasks") as batch_op:
        batch_op.create_index(
            "ix_mission_tasks_mission_id",
            ["mission_id"],
        )


def downgrade() -> None:
    with op.batch_alter_table("mission_tasks") as batch_op:
        batch_op.drop_index("ix_mission_tasks_mission_id")

    with op.batch_alter_table("topic_progress") as batch_op:
        batch_op.drop_index("ix_topic_progress_user_stage")
        batch_op.drop_index("ix_topic_progress_user_next_review")
        batch_op.drop_index("ix_topic_progress_user_topic")

    with op.batch_alter_table("study_plans") as batch_op:
        batch_op.drop_index("ix_study_plans_user_active_archived")
        batch_op.drop_index("ix_study_plans_active_archived")

    with op.batch_alter_table("study_attempts") as batch_op:
        batch_op.drop_index("ix_study_attempts_user_study_date")

    with op.batch_alter_table("missions") as batch_op:
        batch_op.drop_index("ix_missions_status_mission_date")
