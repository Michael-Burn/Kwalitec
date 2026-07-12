"""Create twin_snapshots table for durable TwinRepository storage.

Revision ID: 202611120001
Revises: 202610070002
Create Date: 2026-07-12 23:00:00.000000

Capability 3.8.2 — Durable TwinRepository (SQLite / SQLAlchemy Adapter).

Adds immutable Twin snapshot storage. Does not modify existing tables.
Prior snapshots are retained as history; current = max(sequence) per scope.
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "202611120001"
down_revision: Union[str, None] = "202610070002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "twin_snapshots",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("snapshot_id", sa.String(length=64), nullable=False),
        sa.Column("student_id", sa.String(length=128), nullable=False),
        sa.Column("sitting_id", sa.String(length=128), nullable=True),
        sa.Column("curriculum_id", sa.String(length=128), nullable=True),
        sa.Column("sequence", sa.Integer(), nullable=False),
        sa.Column("format_version", sa.String(length=32), nullable=False),
        sa.Column("authorship", sa.String(length=32), nullable=False),
        sa.Column("twin_payload", sa.Text(), nullable=False),
        sa.Column("provenance_payload", sa.Text(), nullable=True),
        sa.Column("persisted_at", sa.DateTime(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("snapshot_id"),
    )
    with op.batch_alter_table("twin_snapshots", schema=None) as batch_op:
        batch_op.create_index(
            "ix_twin_snapshots_snapshot_id",
            ["snapshot_id"],
            unique=False,
        )
        batch_op.create_index(
            "ix_twin_snapshots_student_id",
            ["student_id"],
            unique=False,
        )
        batch_op.create_index(
            "ix_twin_snapshots_scope_sequence",
            ["student_id", "sitting_id", "curriculum_id", "sequence"],
            unique=False,
        )


def downgrade() -> None:
    with op.batch_alter_table("twin_snapshots", schema=None) as batch_op:
        batch_op.drop_index("ix_twin_snapshots_scope_sequence")
        batch_op.drop_index("ix_twin_snapshots_student_id")
        batch_op.drop_index("ix_twin_snapshots_snapshot_id")
    op.drop_table("twin_snapshots")
