"""Create research feedback and contribution tables for RIP-001.

Revision ID: 202607160001
Revises: 202607150001
Create Date: 2026-07-16 06:00:00.000000

RIP-001 — Daily Reflection & Product Check-in.

Adds structured product-feedback storage and one Contribution per
completed check-in. Does not modify educational tables.
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "202607160001"
down_revision: str | None = "202607150001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "research_feedback_submissions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("submitted_at", sa.DateTime(), nullable=False),
        sa.Column("product_version", sa.String(length=32), nullable=False),
        sa.Column("study_plan_id", sa.Integer(), nullable=True),
        sa.Column("mission_id", sa.Integer(), nullable=True),
        sa.Column("experience_rating", sa.String(length=32), nullable=False),
        sa.Column("feature_helped_most", sa.String(length=64), nullable=False),
        sa.Column("friction_area", sa.String(length=64), nullable=False),
        sa.Column("confidence_rating", sa.String(length=32), nullable=False),
        sa.Column("return_intent", sa.String(length=32), nullable=False),
        sa.Column("free_text", sa.String(length=300), nullable=True),
        sa.Column("classification", sa.String(length=32), nullable=True),
        sa.Column("submission_source", sa.String(length=32), nullable=False),
        sa.ForeignKeyConstraint(["mission_id"], ["missions.id"]),
        sa.ForeignKeyConstraint(["study_plan_id"], ["study_plans.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("research_feedback_submissions", schema=None) as batch_op:
        batch_op.create_index(
            "ix_research_feedback_submissions_user_id",
            ["user_id"],
            unique=False,
        )
        batch_op.create_index(
            "ix_research_feedback_submissions_submitted_at",
            ["submitted_at"],
            unique=False,
        )

    op.create_table(
        "research_contributions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("submission_id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["submission_id"], ["research_feedback_submissions.id"]
        ),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("submission_id"),
    )
    with op.batch_alter_table("research_contributions", schema=None) as batch_op:
        batch_op.create_index(
            "ix_research_contributions_user_id",
            ["user_id"],
            unique=False,
        )
        batch_op.create_index(
            "ix_research_contributions_created_at",
            ["created_at"],
            unique=False,
        )


def downgrade() -> None:
    with op.batch_alter_table("research_contributions", schema=None) as batch_op:
        batch_op.drop_index("ix_research_contributions_created_at")
        batch_op.drop_index("ix_research_contributions_user_id")
    op.drop_table("research_contributions")

    with op.batch_alter_table("research_feedback_submissions", schema=None) as batch_op:
        batch_op.drop_index("ix_research_feedback_submissions_submitted_at")
        batch_op.drop_index("ix_research_feedback_submissions_user_id")
    op.drop_table("research_feedback_submissions")
