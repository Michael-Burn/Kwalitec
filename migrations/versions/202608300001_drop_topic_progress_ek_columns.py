"""Drop retired TopicProgress Estimated Knowledge columns.

Revision ID: 202608300001
Revises: 202608270001
Create Date: 2026-08-30 18:30:00.000000

ADR-027 Phase 2 Stage 4: Stack A Estimated Knowledge is permanently owned by
the Learner Twin. Drop orphaned ``mastery_score`` and ``average_accuracy``
from ``topic_progress`` only. Study Progress columns (completed,
current_stage, next_review_date, revision_count, average_confidence, etc.)
are intentionally unchanged. Stack C / SDT-001 tables are out of scope.
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "202608300001"
down_revision: str | None = "202608270001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    with op.batch_alter_table("topic_progress", schema=None) as batch_op:
        batch_op.drop_column("average_accuracy")
        batch_op.drop_column("mastery_score")


def downgrade() -> None:
    with op.batch_alter_table("topic_progress", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "mastery_score",
                sa.Float(),
                nullable=False,
                server_default="0.0",
                comment=(
                    "Internal estimate scalar 0-100; Version 1 student meaning: "
                    "Estimated Knowledge"
                ),
            ),
        )
        batch_op.add_column(
            sa.Column(
                "average_accuracy",
                sa.Float(),
                nullable=True,
                comment="Average accuracy across all study attempts (0-100)",
            ),
        )
