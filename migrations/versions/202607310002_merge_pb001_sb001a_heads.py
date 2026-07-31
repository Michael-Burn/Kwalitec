"""Merge Alembic heads: PB-001 and SB-001A.

Revision ID: 202607310002
Revises: 202607300005, 202607310001
Create Date: 2026-07-31 14:00:00.000000

RC-003 production cutover — empty merge only.
Does not rewrite migration history or alter schema.
Joins live production head ``202607300005`` (PB-001) with
SB-001A ``student_baselines`` head ``202607310001``.
"""

from __future__ import annotations

from typing import Sequence, Union

revision: str = "202607310002"
down_revision: Union[str, tuple[str, ...], None] = (
    "202607300005",
    "202607310001",
)
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
