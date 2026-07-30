"""EI-001D Decision Ledger + extended certification columns.

Revision ID: 202607300003
Revises: 202607300002
Create Date: 2026-07-30 08:00:00.000000

Additive Decision Ledger table and certification score columns.
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "202607300003"
down_revision: str | Sequence[str] | None = "202607300002"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "ei_certification_records",
        sa.Column(
            "evidence_quality",
            sa.Float(),
            nullable=False,
            server_default="0",
        ),
    )
    op.add_column(
        "ei_certification_records",
        sa.Column(
            "reasoning_confidence",
            sa.Float(),
            nullable=False,
            server_default="0",
        ),
    )
    op.add_column(
        "ei_certification_records",
        sa.Column(
            "decision_quality",
            sa.Float(),
            nullable=False,
            server_default="0",
        ),
    )
    op.add_column(
        "ei_certification_records",
        sa.Column(
            "failure_reasons_json",
            sa.Text(),
            nullable=False,
            server_default="[]",
        ),
    )

    op.create_table(
        "ei_decision_ledger",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("decision_id", sa.String(length=64), nullable=False),
        sa.Column("chain_id", sa.String(length=64), nullable=False),
        sa.Column("generation_index", sa.Integer(), nullable=False),
        sa.Column(
            "generation_id",
            sa.String(length=64),
            nullable=False,
            server_default="",
        ),
        sa.Column(
            "agent_id",
            sa.String(length=128),
            nullable=False,
            server_default="",
        ),
        sa.Column(
            "policy_id",
            sa.String(length=128),
            nullable=False,
            server_default="",
        ),
        sa.Column(
            "evidence_refs_json",
            sa.Text(),
            nullable=False,
            server_default="[]",
        ),
        sa.Column(
            "evidence_grade",
            sa.String(length=8),
            nullable=False,
            server_default="D",
        ),
        sa.Column(
            "confidence",
            sa.Float(),
            nullable=False,
            server_default="0",
        ),
        sa.Column(
            "reasoning_confidence",
            sa.Float(),
            nullable=False,
            server_default="0",
        ),
        sa.Column(
            "affected_node_ids_json",
            sa.Text(),
            nullable=False,
            server_default="[]",
        ),
        sa.Column(
            "decision_type",
            sa.String(length=64),
            nullable=False,
            server_default="other",
        ),
        sa.Column(
            "decision_outcome",
            sa.String(length=32),
            nullable=False,
            server_default="accepted",
        ),
        sa.Column(
            "reason",
            sa.String(length=1024),
            nullable=False,
            server_default="",
        ),
        sa.Column("detail", sa.Text(), nullable=False, server_default=""),
        sa.Column(
            "snapshot_id",
            sa.String(length=64),
            nullable=False,
            server_default="",
        ),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.UniqueConstraint("decision_id", name="uq_ei_decision_ledger_id"),
    )
    op.create_index(
        "ix_ei_decision_chain",
        "ei_decision_ledger",
        ["chain_id"],
    )


def downgrade() -> None:
    op.drop_index("ix_ei_decision_chain", table_name="ei_decision_ledger")
    op.drop_table("ei_decision_ledger")
    op.drop_column("ei_certification_records", "failure_reasons_json")
    op.drop_column("ei_certification_records", "decision_quality")
    op.drop_column("ei_certification_records", "reasoning_confidence")
    op.drop_column("ei_certification_records", "evidence_quality")
