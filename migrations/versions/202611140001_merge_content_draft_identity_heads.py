"""Merge content_drafts head with canonical curriculum identity head.

Revision ID: 202611140001
Revises: 202611130001, 202609160001
Create Date: 2026-09-19 14:15:00.000000

Unifies the twin/content_drafts branch (via 202611130001) with the
canonical curriculum identity branch (202609160001) into a single head.
"""

from __future__ import annotations

from collections.abc import Sequence

# revision identifiers, used by Alembic.
revision: str = "202611140001"
down_revision: tuple[str, str] = ("202611130001", "202609160001")
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
