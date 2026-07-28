"""EI-007 Educational Reasoning Engine — derived decision store.

Revision ID: 202607280070
Revises: 202607280060
Create Date: 2026-07-28 21:15:00.000000

Additive: ere_educational_decisions.

Does not alter tie_node_beliefs, lee_evidence_events, CKG node content,
V1/V2 curriculum engine, missions, or recommendation schema.
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "202607280070"
down_revision: str | tuple[str, ...] | None = "202607280060"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "ere_educational_decisions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("decision_id", sa.String(length=64), nullable=False),
        sa.Column("instance_id", sa.String(length=64), nullable=False),
        sa.Column("decision_type", sa.String(length=64), nullable=False),
        sa.Column("curriculum_target", sa.String(length=256), nullable=False),
        sa.Column("priority", sa.Float(), nullable=False),
        sa.Column("rank_position", sa.Integer(), nullable=False),
        sa.Column("rationale_summary", sa.Text(), nullable=False),
        sa.Column("prerequisite_chain_json", sa.Text(), nullable=False),
        sa.Column("estimated_effort_minutes", sa.Integer(), nullable=False),
        sa.Column("expected_educational_outcome", sa.String(length=64), nullable=False),
        sa.Column("supporting_beliefs_json", sa.Text(), nullable=False),
        sa.Column("supporting_curriculum_json", sa.Text(), nullable=False),
        sa.Column("supporting_evidence_json", sa.Text(), nullable=False),
        sa.Column("applied_rules_json", sa.Text(), nullable=False),
        sa.Column("explanation_json", sa.Text(), nullable=False),
        sa.Column("reasoned_at", sa.DateTime(), nullable=False),
        sa.Column("reasoning_version", sa.String(length=32), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["instance_id"],
            ["sci_student_curriculum_instances.instance_id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "decision_id", name="uq_ere_educational_decisions_decision_id"
        ),
        sa.UniqueConstraint(
            "instance_id",
            "decision_type",
            "curriculum_target",
            name="uq_ere_decisions_instance_type_target",
        ),
    )
    op.create_index(
        "ix_ere_educational_decisions_decision_id",
        "ere_educational_decisions",
        ["decision_id"],
        unique=False,
    )
    op.create_index(
        "ix_ere_educational_decisions_instance_id",
        "ere_educational_decisions",
        ["instance_id"],
        unique=False,
    )
    op.create_index(
        "ix_ere_educational_decisions_decision_type",
        "ere_educational_decisions",
        ["decision_type"],
        unique=False,
    )
    op.create_index(
        "ix_ere_educational_decisions_curriculum_target",
        "ere_educational_decisions",
        ["curriculum_target"],
        unique=False,
    )
    op.create_index(
        "ix_ere_decisions_instance_rank",
        "ere_educational_decisions",
        ["instance_id", "rank_position"],
        unique=False,
    )
    op.create_index(
        "ix_ere_decisions_version",
        "ere_educational_decisions",
        ["reasoning_version"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_ere_decisions_version", table_name="ere_educational_decisions")
    op.drop_index(
        "ix_ere_decisions_instance_rank", table_name="ere_educational_decisions"
    )
    op.drop_index(
        "ix_ere_educational_decisions_curriculum_target",
        table_name="ere_educational_decisions",
    )
    op.drop_index(
        "ix_ere_educational_decisions_decision_type",
        table_name="ere_educational_decisions",
    )
    op.drop_index(
        "ix_ere_educational_decisions_instance_id",
        table_name="ere_educational_decisions",
    )
    op.drop_index(
        "ix_ere_educational_decisions_decision_id",
        table_name="ere_educational_decisions",
    )
    op.drop_table("ere_educational_decisions")
