"""EI-006 Twin Inference Engine — derived node belief store.

Revision ID: 202607280060
Revises: 202607280050
Create Date: 2026-07-28 23:45:00.000000

Additive: tie_node_beliefs.

Does not alter lee_evidence_events (immutable), CKG node content, V1/V2
curriculum engine, missions, or recommendation schema.
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "202607280060"
down_revision: str | tuple[str, ...] | None = "202607280050"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "tie_node_beliefs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("belief_id", sa.String(length=64), nullable=False),
        sa.Column("instance_id", sa.String(length=64), nullable=False),
        sa.Column("node_stable_id", sa.String(length=256), nullable=False),
        sa.Column("mastery_level", sa.Float(), nullable=False),
        sa.Column("confidence_score", sa.Float(), nullable=False),
        sa.Column("learning_state", sa.String(length=32), nullable=False),
        sa.Column("supporting_evidence_json", sa.Text(), nullable=False),
        sa.Column("rationale_summary", sa.Text(), nullable=False),
        sa.Column("explanation_json", sa.Text(), nullable=False),
        sa.Column("inference_timestamp", sa.DateTime(), nullable=False),
        sa.Column("inference_version", sa.String(length=32), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["instance_id"],
            ["sci_student_curriculum_instances.instance_id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("belief_id", name="uq_tie_node_beliefs_belief_id"),
        sa.UniqueConstraint(
            "instance_id",
            "node_stable_id",
            name="uq_tie_node_beliefs_instance_node",
        ),
    )
    op.create_index(
        "ix_tie_node_beliefs_belief_id",
        "tie_node_beliefs",
        ["belief_id"],
        unique=False,
    )
    op.create_index(
        "ix_tie_node_beliefs_instance_id",
        "tie_node_beliefs",
        ["instance_id"],
        unique=False,
    )
    op.create_index(
        "ix_tie_node_beliefs_node_stable_id",
        "tie_node_beliefs",
        ["node_stable_id"],
        unique=False,
    )
    op.create_index(
        "ix_tie_beliefs_instance_state",
        "tie_node_beliefs",
        ["instance_id", "learning_state"],
        unique=False,
    )
    op.create_index(
        "ix_tie_beliefs_version",
        "tie_node_beliefs",
        ["inference_version"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_tie_beliefs_version", table_name="tie_node_beliefs")
    op.drop_index("ix_tie_beliefs_instance_state", table_name="tie_node_beliefs")
    op.drop_index(
        "ix_tie_node_beliefs_node_stable_id", table_name="tie_node_beliefs"
    )
    op.drop_index("ix_tie_node_beliefs_instance_id", table_name="tie_node_beliefs")
    op.drop_index("ix_tie_node_beliefs_belief_id", table_name="tie_node_beliefs")
    op.drop_table("tie_node_beliefs")
