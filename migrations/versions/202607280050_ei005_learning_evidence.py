"""EI-005 Learning Evidence Engine — append-only evidence event store.

Revision ID: 202607280050
Revises: 202607280040
Create Date: 2026-07-28 23:30:00.000000

Additive: lee_evidence_events.

Does not alter CKG node tables, SCI educational state schema beyond FK
targets, V1/V2 curriculum engine, Twin, missions, or recommendation schema.
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "202607280050"
down_revision: str | tuple[str, ...] | None = "202607280040"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "lee_evidence_events",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("evidence_id", sa.String(length=64), nullable=False),
        sa.Column("instance_id", sa.String(length=64), nullable=False),
        sa.Column("student_id", sa.Integer(), nullable=False),
        sa.Column("node_stable_id", sa.String(length=256), nullable=False),
        sa.Column("evidence_type", sa.String(length=64), nullable=False),
        sa.Column("occurred_at", sa.DateTime(), nullable=False),
        sa.Column("recorded_at", sa.DateTime(), nullable=False),
        sa.Column("source", sa.String(length=64), nullable=False),
        sa.Column("metadata_json", sa.Text(), nullable=False),
        sa.Column("corrects_evidence_id", sa.String(length=64), nullable=True),
        sa.ForeignKeyConstraint(
            ["instance_id"],
            ["sci_student_curriculum_instances.instance_id"],
        ),
        sa.ForeignKeyConstraint(["student_id"], ["users.id"]),
        sa.ForeignKeyConstraint(
            ["corrects_evidence_id"],
            ["lee_evidence_events.evidence_id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("evidence_id", name="uq_lee_evidence_events_evidence_id"),
    )
    op.create_index(
        "ix_lee_evidence_events_evidence_id",
        "lee_evidence_events",
        ["evidence_id"],
        unique=False,
    )
    op.create_index(
        "ix_lee_evidence_events_instance_id",
        "lee_evidence_events",
        ["instance_id"],
        unique=False,
    )
    op.create_index(
        "ix_lee_evidence_events_student_id",
        "lee_evidence_events",
        ["student_id"],
        unique=False,
    )
    op.create_index(
        "ix_lee_evidence_events_node_stable_id",
        "lee_evidence_events",
        ["node_stable_id"],
        unique=False,
    )
    op.create_index(
        "ix_lee_evidence_events_evidence_type",
        "lee_evidence_events",
        ["evidence_type"],
        unique=False,
    )
    op.create_index(
        "ix_lee_evidence_events_occurred_at",
        "lee_evidence_events",
        ["occurred_at"],
        unique=False,
    )
    op.create_index(
        "ix_lee_evidence_instance_occurred",
        "lee_evidence_events",
        ["instance_id", "occurred_at"],
        unique=False,
    )
    op.create_index(
        "ix_lee_evidence_instance_node_occurred",
        "lee_evidence_events",
        ["instance_id", "node_stable_id", "occurred_at"],
        unique=False,
    )
    op.create_index(
        "ix_lee_evidence_instance_type",
        "lee_evidence_events",
        ["instance_id", "evidence_type"],
        unique=False,
    )
    op.create_index(
        "ix_lee_evidence_student",
        "lee_evidence_events",
        ["student_id", "occurred_at"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_lee_evidence_student", table_name="lee_evidence_events")
    op.drop_index("ix_lee_evidence_instance_type", table_name="lee_evidence_events")
    op.drop_index(
        "ix_lee_evidence_instance_node_occurred", table_name="lee_evidence_events"
    )
    op.drop_index(
        "ix_lee_evidence_instance_occurred", table_name="lee_evidence_events"
    )
    op.drop_index(
        "ix_lee_evidence_events_occurred_at", table_name="lee_evidence_events"
    )
    op.drop_index(
        "ix_lee_evidence_events_evidence_type", table_name="lee_evidence_events"
    )
    op.drop_index(
        "ix_lee_evidence_events_node_stable_id", table_name="lee_evidence_events"
    )
    op.drop_index(
        "ix_lee_evidence_events_student_id", table_name="lee_evidence_events"
    )
    op.drop_index(
        "ix_lee_evidence_events_instance_id", table_name="lee_evidence_events"
    )
    op.drop_index(
        "ix_lee_evidence_events_evidence_id", table_name="lee_evidence_events"
    )
    op.drop_table("lee_evidence_events")
