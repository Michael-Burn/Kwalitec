"""Add sql_mission_id evidence companion FK on runtime_mission_instances.

Revision ID: 202608240001
Revises: 202607310002
Create Date: 2026-08-24 20:00:00.000000

Phase 1 runtime-identity unification: nullable unique FK from Runtime C
mission instances to SQL missions (evidence substrate for StudyAttempt).
Does not alter Stage A mission generation or StudyAttempt schema.
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "202608240001"
down_revision: Union[str, None] = "202607310002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("runtime_mission_instances", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("sql_mission_id", sa.Integer(), nullable=True)
        )
        batch_op.create_foreign_key(
            "fk_runtime_mission_instances_sql_mission_id",
            "missions",
            ["sql_mission_id"],
            ["id"],
        )
        batch_op.create_index(
            "ix_runtime_mission_instances_sql_mission_id",
            ["sql_mission_id"],
            unique=True,
        )


def downgrade() -> None:
    # SQLite batch recreate: drop column (and its FK) without requiring the
    # named constraint to exist under every dialect/create_all path.
    with op.batch_alter_table("runtime_mission_instances", schema=None) as batch_op:
        batch_op.drop_index("ix_runtime_mission_instances_sql_mission_id")
        batch_op.drop_column("sql_mission_id")
