"""Create recommendation_commitments table (EP-008.3A).

Revision ID: 202607260001
Revises: 202611120001
Create Date: 2026-07-26 14:00:00.000000

Preference / intent commitment persistence only. Does not alter Runtime A
ranking, mastery, or readiness schema meaning.
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "202607260001"
down_revision: Union[str, None] = "202607240001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "recommendation_commitments",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("recommendation_key", sa.String(length=255), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("state", sa.String(length=32), nullable=False),
        sa.Column("deferred_reason_code", sa.String(length=64), nullable=False),
        sa.Column("deferred_reason_note", sa.String(length=140), nullable=False),
        sa.Column("expected_benefit", sa.Text(), nullable=False),
        sa.Column("review_point", sa.Text(), nullable=False),
        sa.Column("suggested_next_action", sa.Text(), nullable=False),
        sa.Column("session_id", sa.String(length=128), nullable=False),
        sa.Column("decision_id", sa.Integer(), nullable=True),
        sa.Column("committed_at", sa.DateTime(), nullable=True),
        sa.Column("deferred_at", sa.DateTime(), nullable=True),
        sa.Column("session_started_at", sa.DateTime(), nullable=True),
        sa.Column("completed_at", sa.DateTime(), nullable=True),
        sa.Column("reflected_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("recommendation_commitments", schema=None) as batch_op:
        batch_op.create_index(
            "ix_recommendation_commitments_user_id",
            ["user_id"],
            unique=False,
        )
        batch_op.create_index(
            "ix_recommendation_commitments_recommendation_key",
            ["recommendation_key"],
            unique=False,
        )


def downgrade() -> None:
    with op.batch_alter_table("recommendation_commitments", schema=None) as batch_op:
        batch_op.drop_index("ix_recommendation_commitments_recommendation_key")
        batch_op.drop_index("ix_recommendation_commitments_user_id")
    op.drop_table("recommendation_commitments")
