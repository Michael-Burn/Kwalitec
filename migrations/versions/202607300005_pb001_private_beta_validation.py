"""PB-001 Private Beta Validation evidence tables.

Revision ID: 202607300005
Revises: 202607300004
Create Date: 2026-07-30 09:00:00.000000

Adds cohort enrolment, categorised feedback with auto-severity, and
founder observation checklists. Does not alter educational schema.
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "202607300005"
down_revision: Union[str, None] = "202607300004"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "private_beta_participants",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("enrolled_at", sa.DateTime(), nullable=False),
        sa.Column("cohort_label", sa.String(length=64), nullable=False),
        sa.Column("device_preference", sa.String(length=32), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("notes", sa.String(length=500), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id"),
    )
    with op.batch_alter_table("private_beta_participants", schema=None) as batch_op:
        batch_op.create_index(
            "ix_private_beta_participants_user_id", ["user_id"], unique=True
        )
        batch_op.create_index(
            "ix_private_beta_participants_enrolled_at",
            ["enrolled_at"],
            unique=False,
        )

    op.create_table(
        "private_beta_feedback",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("category", sa.String(length=64), nullable=False),
        sa.Column("severity", sa.String(length=32), nullable=False),
        sa.Column("message", sa.String(length=1000), nullable=False),
        sa.Column("current_screen", sa.String(length=128), nullable=True),
        sa.Column("subject_code", sa.String(length=64), nullable=True),
        sa.Column("browser", sa.String(length=64), nullable=True),
        sa.Column("device", sa.String(length=64), nullable=True),
        sa.Column("product_version", sa.String(length=32), nullable=False),
        sa.Column("user_agent", sa.String(length=512), nullable=True),
        sa.Column("path", sa.String(length=255), nullable=True),
        sa.Column("mission_id", sa.Integer(), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["mission_id"], ["missions.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("private_beta_feedback", schema=None) as batch_op:
        batch_op.create_index(
            "ix_private_beta_feedback_user_id", ["user_id"], unique=False
        )
        batch_op.create_index(
            "ix_private_beta_feedback_category", ["category"], unique=False
        )
        batch_op.create_index(
            "ix_private_beta_feedback_severity", ["severity"], unique=False
        )
        batch_op.create_index(
            "ix_private_beta_feedback_mission_id", ["mission_id"], unique=False
        )
        batch_op.create_index(
            "ix_private_beta_feedback_status", ["status"], unique=False
        )
        batch_op.create_index(
            "ix_private_beta_feedback_created_at", ["created_at"], unique=False
        )

    op.create_table(
        "private_beta_observations",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("observer_user_id", sa.Integer(), nullable=True),
        sa.Column("understood_onboarding", sa.Boolean(), nullable=True),
        sa.Column("knew_where_to_click", sa.Boolean(), nullable=True),
        sa.Column("understood_todays_mission", sa.Boolean(), nullable=True),
        sa.Column("understood_progress", sa.Boolean(), nullable=True),
        sa.Column("understood_tutor", sa.Boolean(), nullable=True),
        sa.Column("understood_knowledge_map", sa.Boolean(), nullable=True),
        sa.Column("became_stuck", sa.Boolean(), nullable=True),
        sa.Column("stuck_where", sa.String(length=255), nullable=True),
        sa.Column("notes", sa.String(length=1000), nullable=True),
        sa.Column("observed_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["observer_user_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("private_beta_observations", schema=None) as batch_op:
        batch_op.create_index(
            "ix_private_beta_observations_user_id", ["user_id"], unique=False
        )
        batch_op.create_index(
            "ix_private_beta_observations_observed_at",
            ["observed_at"],
            unique=False,
        )


def downgrade() -> None:
    op.drop_table("private_beta_observations")
    op.drop_table("private_beta_feedback")
    op.drop_table("private_beta_participants")
