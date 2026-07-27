"""TUTOR-001 Evidence-Backed Intelligent Tutor tables.

Revision ID: 202607270013
Revises: 202607270012
Create Date: 2026-07-27 26:00:00.000000

Additive schema. Does not alter SDT-001 Twin, SDT-002 reasoning, SDT-003
Learning Graph, AME-001 Adaptive Mission, or AP-001 Assessment tables.
Stores conversations only — does not duplicate Twin learner state.
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "202607270013"
down_revision: str | None = "202607270012"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "tutor_sessions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("session_id", sa.String(length=64), nullable=False),
        sa.Column("twin_id", sa.String(length=64), nullable=False),
        sa.Column("student_id", sa.String(length=128), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("title", sa.String(length=256), nullable=False),
        sa.Column("active_mission_id", sa.String(length=64), nullable=False),
        sa.Column("memory_json", sa.Text(), nullable=False),
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
        "ix_tutor_sessions_session_id",
        "tutor_sessions",
        ["session_id"],
        unique=True,
    )
    op.create_index(
        "ix_tutor_sessions_twin_updated",
        "tutor_sessions",
        ["twin_id", "updated_at"],
        unique=False,
    )
    op.create_index(
        "ix_tutor_sessions_student_status",
        "tutor_sessions",
        ["student_id", "status"],
        unique=False,
    )

    op.create_table(
        "tutor_messages",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("message_id", sa.String(length=64), nullable=False),
        sa.Column("session_id", sa.String(length=64), nullable=False),
        sa.Column("twin_id", sa.String(length=64), nullable=False),
        sa.Column("role", sa.String(length=16), nullable=False),
        sa.Column("kind", sa.String(length=64), nullable=False),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column("concept_id", sa.String(length=64), nullable=False),
        sa.Column("mission_id", sa.String(length=64), nullable=False),
        sa.Column("context_id", sa.String(length=64), nullable=False),
        sa.Column("evidence_json", sa.Text(), nullable=False),
        sa.Column("metadata_json", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["session_id"],
            ["tutor_sessions.session_id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_tutor_messages_message_id",
        "tutor_messages",
        ["message_id"],
        unique=True,
    )
    op.create_index(
        "ix_tutor_messages_session_created",
        "tutor_messages",
        ["session_id", "created_at"],
        unique=False,
    )
    op.create_index(
        "ix_tutor_messages_twin_role",
        "tutor_messages",
        ["twin_id", "role"],
        unique=False,
    )

    op.create_table(
        "tutor_explanations",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("explanation_id", sa.String(length=64), nullable=False),
        sa.Column("session_id", sa.String(length=64), nullable=False),
        sa.Column("twin_id", sa.String(length=64), nullable=False),
        sa.Column("response_id", sa.String(length=64), nullable=False),
        sa.Column("kind", sa.String(length=64), nullable=False),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("detail", sa.Text(), nullable=False),
        sa.Column("evidence_json", sa.Text(), nullable=False),
        sa.Column("concept_ids_json", sa.Text(), nullable=False),
        sa.Column("reasoning_run_id", sa.String(length=64), nullable=False),
        sa.Column("mission_id", sa.String(length=64), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["session_id"],
            ["tutor_sessions.session_id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_tutor_explanations_explanation_id",
        "tutor_explanations",
        ["explanation_id"],
        unique=True,
    )
    op.create_index(
        "ix_tutor_explanations_twin_created",
        "tutor_explanations",
        ["twin_id", "created_at"],
        unique=False,
    )
    op.create_index(
        "ix_tutor_explanations_session",
        "tutor_explanations",
        ["session_id"],
        unique=False,
    )

    op.create_table(
        "tutor_feedback",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("feedback_id", sa.String(length=64), nullable=False),
        sa.Column("twin_id", sa.String(length=64), nullable=False),
        sa.Column("session_id", sa.String(length=64), nullable=False),
        sa.Column("response_id", sa.String(length=64), nullable=False),
        sa.Column("rating", sa.Integer(), nullable=False),
        sa.Column("comment", sa.Text(), nullable=False),
        sa.Column("helpful", sa.Boolean(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["session_id"],
            ["tutor_sessions.session_id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_tutor_feedback_feedback_id",
        "tutor_feedback",
        ["feedback_id"],
        unique=True,
    )
    op.create_index(
        "ix_tutor_feedback_twin_created",
        "tutor_feedback",
        ["twin_id", "created_at"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_tutor_feedback_twin_created", table_name="tutor_feedback")
    op.drop_index("ix_tutor_feedback_feedback_id", table_name="tutor_feedback")
    op.drop_table("tutor_feedback")
    op.drop_index("ix_tutor_explanations_session", table_name="tutor_explanations")
    op.drop_index(
        "ix_tutor_explanations_twin_created", table_name="tutor_explanations"
    )
    op.drop_index(
        "ix_tutor_explanations_explanation_id", table_name="tutor_explanations"
    )
    op.drop_table("tutor_explanations")
    op.drop_index("ix_tutor_messages_twin_role", table_name="tutor_messages")
    op.drop_index("ix_tutor_messages_session_created", table_name="tutor_messages")
    op.drop_index("ix_tutor_messages_message_id", table_name="tutor_messages")
    op.drop_table("tutor_messages")
    op.drop_index("ix_tutor_sessions_student_status", table_name="tutor_sessions")
    op.drop_index("ix_tutor_sessions_twin_updated", table_name="tutor_sessions")
    op.drop_index("ix_tutor_sessions_session_id", table_name="tutor_sessions")
    op.drop_table("tutor_sessions")
