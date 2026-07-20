"""Create V2 durable aggregate, snapshot, and evidence tables.

Revision ID: 202607190001
Revises: 202611120001
Create Date: 2026-07-19 16:00:00.000000

V2-018 follow-on — ORM/Alembic expansion for Experience / Session persistence.
Does not modify existing tables. Educational law remains in engines.
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "202607190001"
down_revision: Union[str, None] = "202611120001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "v2_aggregate_documents",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("aggregate_name", sa.String(length=128), nullable=False),
        sa.Column("aggregate_id", sa.String(length=256), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("payload", sa.Text(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "aggregate_name",
            "aggregate_id",
            name="uq_v2_aggregate_documents_name_id",
        ),
    )
    with op.batch_alter_table("v2_aggregate_documents", schema=None) as batch_op:
        batch_op.create_index(
            "ix_v2_aggregate_documents_name_id",
            ["aggregate_name", "aggregate_id"],
            unique=False,
        )

    op.create_table(
        "v2_aggregate_snapshots",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("snapshot_id", sa.String(length=64), nullable=False),
        sa.Column("aggregate_name", sa.String(length=128), nullable=False),
        sa.Column("aggregate_id", sa.String(length=256), nullable=False),
        sa.Column("sequence", sa.Integer(), nullable=False),
        sa.Column("schema_version", sa.Integer(), nullable=False),
        sa.Column("payload", sa.Text(), nullable=False),
        sa.Column("correlation_id", sa.String(length=128), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("snapshot_id"),
    )
    with op.batch_alter_table("v2_aggregate_snapshots", schema=None) as batch_op:
        batch_op.create_index(
            "ix_v2_aggregate_snapshots_snapshot_id",
            ["snapshot_id"],
            unique=False,
        )
        batch_op.create_index(
            "ix_v2_aggregate_snapshots_name_id_seq",
            ["aggregate_name", "aggregate_id", "sequence"],
            unique=False,
        )

    op.create_table(
        "v2_evidence_events",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("record_id", sa.String(length=64), nullable=False),
        sa.Column("learner_id", sa.String(length=128), nullable=False),
        sa.Column("subject_id", sa.String(length=128), nullable=False),
        sa.Column("evidence_type", sa.String(length=128), nullable=False),
        sa.Column("payload", sa.Text(), nullable=False),
        sa.Column("correlation_id", sa.String(length=128), nullable=False),
        sa.Column("causation_id", sa.String(length=128), nullable=False),
        sa.Column("recorded_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("record_id"),
    )
    with op.batch_alter_table("v2_evidence_events", schema=None) as batch_op:
        batch_op.create_index(
            "ix_v2_evidence_events_record_id",
            ["record_id"],
            unique=False,
        )
        batch_op.create_index(
            "ix_v2_evidence_events_learner_id",
            ["learner_id"],
            unique=False,
        )
        batch_op.create_index(
            "ix_v2_evidence_events_learner_subject",
            ["learner_id", "subject_id"],
            unique=False,
        )


def downgrade() -> None:
    with op.batch_alter_table("v2_evidence_events", schema=None) as batch_op:
        batch_op.drop_index("ix_v2_evidence_events_learner_subject")
        batch_op.drop_index("ix_v2_evidence_events_learner_id")
        batch_op.drop_index("ix_v2_evidence_events_record_id")
    op.drop_table("v2_evidence_events")

    with op.batch_alter_table("v2_aggregate_snapshots", schema=None) as batch_op:
        batch_op.drop_index("ix_v2_aggregate_snapshots_name_id_seq")
        batch_op.drop_index("ix_v2_aggregate_snapshots_snapshot_id")
    op.drop_table("v2_aggregate_snapshots")

    with op.batch_alter_table("v2_aggregate_documents", schema=None) as batch_op:
        batch_op.drop_index("ix_v2_aggregate_documents_name_id")
    op.drop_table("v2_aggregate_documents")
