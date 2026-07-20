"""Merge Alembic heads after V2 aggregate tables.

Revision ID: 202607190002
Revises: 202607170003, 202607190001
Create Date: 2026-07-19 17:00:00.000000

Merges the V1SP-003 index branch with the V2 aggregate persistence branch.
"""

from __future__ import annotations

from typing import Sequence, Union

revision: str = "202607190002"
down_revision: Union[str, tuple[str, ...], None] = (
    "202607170003",
    "202607190001",
)
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
