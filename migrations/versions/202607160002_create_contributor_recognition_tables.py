"""Create contributor recognition tables for RIP-002.

Revision ID: 202607160002
Revises: 202607160001
Create Date: 2026-07-16 07:00:00.000000

RIP-002 — Contributor Recognition.

Adds badge awards and Founder feedback review marks. Does not modify
educational tables.
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "202607160002"
down_revision: str | None = "202607160001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "research_contributor_badges",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("badge_slug", sa.String(length=32), nullable=False),
        sa.Column("awarded_at", sa.DateTime(), nullable=False),
        sa.Column("trigger_contribution_id", sa.Integer(), nullable=True),
        sa.Column("trigger_submission_id", sa.Integer(), nullable=True),
        sa.Column("awarded_by_user_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["trigger_contribution_id"], ["research_contributions.id"]
        ),
        sa.ForeignKeyConstraint(
            ["trigger_submission_id"], ["research_feedback_submissions.id"]
        ),
        sa.ForeignKeyConstraint(["awarded_by_user_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id", "badge_slug", name="uq_user_badge_slug"),
    )
    with op.batch_alter_table("research_contributor_badges", schema=None) as batch_op:
        batch_op.create_index(
            "ix_research_contributor_badges_user_id",
            ["user_id"],
            unique=False,
        )
        batch_op.create_index(
            "ix_research_contributor_badges_badge_slug",
            ["badge_slug"],
            unique=False,
        )
        batch_op.create_index(
            "ix_research_contributor_badges_awarded_at",
            ["awarded_at"],
            unique=False,
        )

    op.create_table(
        "research_feedback_reviews",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("submission_id", sa.Integer(), nullable=False),
        sa.Column("founder_user_id", sa.Integer(), nullable=False),
        sa.Column("is_helpful", sa.Boolean(), nullable=False),
        sa.Column("is_insightful", sa.Boolean(), nullable=False),
        sa.Column("is_implemented", sa.Boolean(), nullable=False),
        sa.Column("reviewed_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["founder_user_id"], ["users.id"]),
        sa.ForeignKeyConstraint(
            ["submission_id"], ["research_feedback_submissions.id"]
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("submission_id"),
    )
    with op.batch_alter_table("research_feedback_reviews", schema=None) as batch_op:
        batch_op.create_index(
            "ix_research_feedback_reviews_reviewed_at",
            ["reviewed_at"],
            unique=False,
        )


def downgrade() -> None:
    with op.batch_alter_table("research_feedback_reviews", schema=None) as batch_op:
        batch_op.drop_index("ix_research_feedback_reviews_reviewed_at")
    op.drop_table("research_feedback_reviews")

    with op.batch_alter_table("research_contributor_badges", schema=None) as batch_op:
        batch_op.drop_index("ix_research_contributor_badges_awarded_at")
        batch_op.drop_index("ix_research_contributor_badges_badge_slug")
        batch_op.drop_index("ix_research_contributor_badges_user_id")
    op.drop_table("research_contributor_badges")
