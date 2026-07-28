"""Create Educational Feedback Review table (ILE-005).

Revision ID: 202607280002
Revises: 202607280001
Create Date: 2026-07-28 14:00:00.000000

Internal Sensei educational review records for recommendation outcome
calibration. Does not alter Twin, readiness, ranking, or Adaptive
Assessment selection. Never learner-visible.
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "202607280002"
down_revision: str | None = "202607280001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "educational_feedback_reviews",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("review_id", sa.String(length=64), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("journal_entry_id", sa.String(length=64), nullable=False),
        sa.Column("observation", sa.Text(), nullable=False),
        sa.Column("original_recommendation", sa.Text(), nullable=False),
        sa.Column("later_evidence", sa.Text(), nullable=False),
        sa.Column("educational_assessment", sa.Text(), nullable=False),
        sa.Column("future_learning", sa.Text(), nullable=False),
        sa.Column("review_state", sa.String(length=64), nullable=False),
        sa.Column("evidence_quality", sa.String(length=32), nullable=False),
        sa.Column("assessment_focus", sa.String(length=64), nullable=False),
        sa.Column("rationale_summary", sa.Text(), nullable=False),
        sa.Column("learner_visible", sa.Boolean(), nullable=False),
        sa.Column("recorded_at", sa.DateTime(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_educational_feedback_reviews_review_id",
        "educational_feedback_reviews",
        ["review_id"],
        unique=True,
    )
    op.create_index(
        "ix_educational_feedback_reviews_user_id",
        "educational_feedback_reviews",
        ["user_id"],
        unique=False,
    )
    op.create_index(
        "ix_educational_feedback_reviews_journal_entry_id",
        "educational_feedback_reviews",
        ["journal_entry_id"],
        unique=False,
    )
    op.create_index(
        "ix_educational_feedback_reviews_review_state",
        "educational_feedback_reviews",
        ["review_state"],
        unique=False,
    )
    op.create_index(
        "ix_educational_feedback_reviews_recorded_at",
        "educational_feedback_reviews",
        ["recorded_at"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        "ix_educational_feedback_reviews_recorded_at",
        table_name="educational_feedback_reviews",
    )
    op.drop_index(
        "ix_educational_feedback_reviews_review_state",
        table_name="educational_feedback_reviews",
    )
    op.drop_index(
        "ix_educational_feedback_reviews_journal_entry_id",
        table_name="educational_feedback_reviews",
    )
    op.drop_index(
        "ix_educational_feedback_reviews_user_id",
        table_name="educational_feedback_reviews",
    )
    op.drop_index(
        "ix_educational_feedback_reviews_review_id",
        table_name="educational_feedback_reviews",
    )
    op.drop_table("educational_feedback_reviews")
