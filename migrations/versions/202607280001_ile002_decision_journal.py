"""Create Decision Journal tables (ILE-002).

Revision ID: 202607280001
Revises: 202607270013
Create Date: 2026-07-28 12:00:00.000000

Learner educational memory — observation / meaning / recommendation /
evidence / confidence / action / outcome / reflection. Does not alter Twin,
readiness, ranking, or Adaptive Assessment selection.
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "202607280001"
down_revision: str | None = "202607270013"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "decision_journal_entries",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("entry_id", sa.String(length=64), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("catalogue_decision_id", sa.String(length=32), nullable=False),
        sa.Column("kind", sa.String(length=64), nullable=False),
        sa.Column("lifecycle_status", sa.String(length=32), nullable=False),
        sa.Column("educational_context", sa.Text(), nullable=False),
        sa.Column("observation", sa.Text(), nullable=False),
        sa.Column("meaning", sa.Text(), nullable=False),
        sa.Column("recommendation", sa.Text(), nullable=False),
        sa.Column("supporting_evidence_summary", sa.Text(), nullable=False),
        sa.Column("qualitative_confidence", sa.String(length=32), nullable=False),
        sa.Column("expected_benefit", sa.Text(), nullable=False),
        sa.Column("uncertainty", sa.Text(), nullable=False),
        sa.Column("student_action", sa.String(length=32), nullable=False),
        sa.Column("outcome_summary", sa.Text(), nullable=True),
        sa.Column("reflection_status", sa.String(length=32), nullable=False),
        sa.Column("reflection_note", sa.Text(), nullable=False),
        sa.Column("legacy_decision_id", sa.Integer(), nullable=True),
        sa.Column("commitment_id", sa.Integer(), nullable=True),
        sa.Column("recorded_at", sa.DateTime(), nullable=False),
        sa.Column("accepted_at", sa.DateTime(), nullable=True),
        sa.Column("deferred_at", sa.DateTime(), nullable=True),
        sa.Column("reflected_at", sa.DateTime(), nullable=True),
        sa.Column("outcome_at", sa.DateTime(), nullable=True),
        sa.Column("archived_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("entry_id"),
    )
    with op.batch_alter_table("decision_journal_entries", schema=None) as batch_op:
        batch_op.create_index(
            "ix_decision_journal_entries_entry_id",
            ["entry_id"],
            unique=True,
        )
        batch_op.create_index(
            "ix_decision_journal_entries_user_id",
            ["user_id"],
            unique=False,
        )
        batch_op.create_index(
            "ix_decision_journal_entries_kind",
            ["kind"],
            unique=False,
        )
        batch_op.create_index(
            "ix_decision_journal_entries_lifecycle_status",
            ["lifecycle_status"],
            unique=False,
        )
        batch_op.create_index(
            "ix_decision_journal_entries_recorded_at",
            ["recorded_at"],
            unique=False,
        )

    op.create_table(
        "decision_journal_evidence_events",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("entry_pk", sa.Integer(), nullable=False),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("recorded_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["entry_pk"],
            ["decision_journal_entries.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table(
        "decision_journal_evidence_events", schema=None
    ) as batch_op:
        batch_op.create_index(
            "ix_decision_journal_evidence_events_entry_pk",
            ["entry_pk"],
            unique=False,
        )
        batch_op.create_index(
            "ix_decision_journal_evidence_events_recorded_at",
            ["recorded_at"],
            unique=False,
        )


def downgrade() -> None:
    with op.batch_alter_table(
        "decision_journal_evidence_events", schema=None
    ) as batch_op:
        batch_op.drop_index("ix_decision_journal_evidence_events_recorded_at")
        batch_op.drop_index("ix_decision_journal_evidence_events_entry_pk")
    op.drop_table("decision_journal_evidence_events")

    with op.batch_alter_table("decision_journal_entries", schema=None) as batch_op:
        batch_op.drop_index("ix_decision_journal_entries_recorded_at")
        batch_op.drop_index("ix_decision_journal_entries_lifecycle_status")
        batch_op.drop_index("ix_decision_journal_entries_kind")
        batch_op.drop_index("ix_decision_journal_entries_user_id")
        batch_op.drop_index("ix_decision_journal_entries_entry_id")
    op.drop_table("decision_journal_entries")
