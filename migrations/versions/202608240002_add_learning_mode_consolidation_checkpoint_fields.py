"""Add Learning Mode consolidation checkpoint fields to study_plans.

Revision ID: 202608240002
Revises: 202608240001
Create Date: 2026-08-24 22:00:00.000000

Learning Mode disclosed consolidation checkpoints: watermark of new CLT
topics since last checkpoint, and last consolidation topic id for anti-repeat.
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "202608240002"
down_revision: str | None = "202608240001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    with op.batch_alter_table("study_plans", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "new_topics_since_consolidation_checkpoint",
                sa.Integer(),
                nullable=False,
                server_default="0",
                comment=(
                    "Learning Mode: count of newly completed CLT topics since "
                    "the last consolidation checkpoint (or skip-no-weak reset)"
                ),
            )
        )
        batch_op.add_column(
            sa.Column(
                "last_consolidation_topic_id",
                sa.Integer(),
                nullable=True,
                comment=(
                    "Topic id of the most recent Learning Mode consolidation "
                    "checkpoint"
                ),
            )
        )
        batch_op.create_foreign_key(
            "fk_study_plans_last_consolidation_topic_id",
            "topics",
            ["last_consolidation_topic_id"],
            ["id"],
        )


def downgrade() -> None:
    with op.batch_alter_table("study_plans", schema=None) as batch_op:
        batch_op.drop_constraint(
            "fk_study_plans_last_consolidation_topic_id",
            type_="foreignkey",
        )
        batch_op.drop_column("last_consolidation_topic_id")
        batch_op.drop_column("new_topics_since_consolidation_checkpoint")
