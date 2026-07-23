"""ALPHA-001 Internal Alpha infrastructure tables and onboarding flags.

Revision ID: 202607230001
Revises: 202607190002
Create Date: 2026-07-23 19:00:00.000000

Adds presentation telemetry, lightweight alpha feedback storage, and
per-user alpha onboarding completion flags. Does not alter educational
schema or Education OS tables.
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "202607230001"
down_revision: Union[str, None] = "202607190002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "alpha_onboarding_completed",
                sa.Boolean(),
                nullable=False,
                server_default=sa.false(),
            )
        )
        batch_op.add_column(
            sa.Column(
                "alpha_onboarding_skipped",
                sa.Boolean(),
                nullable=False,
                server_default=sa.false(),
            )
        )

    op.create_table(
        "presentation_events",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("event_type", sa.String(length=64), nullable=False),
        sa.Column("resource_type", sa.String(length=64), nullable=True),
        sa.Column("resource_id", sa.String(length=64), nullable=True),
        sa.Column("path", sa.String(length=255), nullable=True),
        sa.Column("correlation_id", sa.String(length=64), nullable=True),
        sa.Column("context_json", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("presentation_events", schema=None) as batch_op:
        batch_op.create_index(
            "ix_presentation_events_user_id", ["user_id"], unique=False
        )
        batch_op.create_index(
            "ix_presentation_events_event_type", ["event_type"], unique=False
        )
        batch_op.create_index(
            "ix_presentation_events_correlation_id",
            ["correlation_id"],
            unique=False,
        )
        batch_op.create_index(
            "ix_presentation_events_created_at", ["created_at"], unique=False
        )

    op.create_table(
        "alpha_feedback_submissions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("kind", sa.String(length=64), nullable=False),
        sa.Column("rating", sa.String(length=32), nullable=True),
        sa.Column("message", sa.String(length=500), nullable=True),
        sa.Column("mission_id", sa.Integer(), nullable=True),
        sa.Column("surface", sa.String(length=64), nullable=True),
        sa.Column("product_version", sa.String(length=32), nullable=False),
        sa.Column("correlation_id", sa.String(length=64), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["mission_id"], ["missions.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("alpha_feedback_submissions", schema=None) as batch_op:
        batch_op.create_index(
            "ix_alpha_feedback_submissions_user_id", ["user_id"], unique=False
        )
        batch_op.create_index(
            "ix_alpha_feedback_submissions_kind", ["kind"], unique=False
        )
        batch_op.create_index(
            "ix_alpha_feedback_submissions_mission_id",
            ["mission_id"],
            unique=False,
        )
        batch_op.create_index(
            "ix_alpha_feedback_submissions_correlation_id",
            ["correlation_id"],
            unique=False,
        )
        batch_op.create_index(
            "ix_alpha_feedback_submissions_status", ["status"], unique=False
        )
        batch_op.create_index(
            "ix_alpha_feedback_submissions_created_at",
            ["created_at"],
            unique=False,
        )


def downgrade() -> None:
    op.drop_table("alpha_feedback_submissions")
    op.drop_table("presentation_events")
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.drop_column("alpha_onboarding_skipped")
        batch_op.drop_column("alpha_onboarding_completed")
