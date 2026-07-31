"""SB-001A — student_baselines educational origin table.

Revision ID: 202607310001
Revises: 202611120001
Create Date: 2026-07-31 12:00:00.000000

Stores self-declared Baseline as the origin of Twin birth.
Does not modify study history, SCI, or Runtime C tables.
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "202607310001"
down_revision: Union[str, None] = "202611120001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "student_baselines",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("subject_key", sa.String(length=128), nullable=False),
        sa.Column("category_code", sa.String(length=64), nullable=False),
        sa.Column("subject_code", sa.String(length=64), nullable=False),
        sa.Column("runtime_authority", sa.String(length=64), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("experience", sa.String(length=64), nullable=True),
        sa.Column("position_mode", sa.String(length=64), nullable=True),
        sa.Column("curriculum_topic_code", sa.String(length=64), nullable=True),
        sa.Column("exam_history", sa.String(length=64), nullable=True),
        sa.Column("highest_mark", sa.String(length=64), nullable=True),
        sa.Column("learning_objective", sa.String(length=64), nullable=True),
        sa.Column("confidence", sa.String(length=64), nullable=True),
        sa.Column("curriculum_version", sa.String(length=64), nullable=True),
        sa.Column("study_plan_id", sa.Integer(), nullable=True),
        sa.Column("enrolment_id", sa.String(length=128), nullable=True),
        sa.Column("twin_snapshot_id", sa.String(length=64), nullable=True),
        sa.Column("supersedes_baseline_id", sa.Integer(), nullable=True),
        sa.Column("completed_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["study_plan_id"], ["study_plans.id"]),
        sa.ForeignKeyConstraint(
            ["supersedes_baseline_id"], ["student_baselines.id"]
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_student_baselines_user_subject_status",
        "student_baselines",
        ["user_id", "subject_key", "status"],
    )
    op.create_index(
        "ix_student_baselines_user_id",
        "student_baselines",
        ["user_id"],
    )


def downgrade() -> None:
    op.drop_index("ix_student_baselines_user_id", table_name="student_baselines")
    op.drop_index(
        "ix_student_baselines_user_subject_status",
        table_name="student_baselines",
    )
    op.drop_table("student_baselines")
