"""Widen learning_objectives.description to unbounded TEXT.

Revision ID: 202607130002
Revises: 202607130001
Create Date: 2026-07-13 15:50:00.000000

Internal Alpha hotfix — CM1 Learning Objective Storage.

Official IFoA Learning Objective descriptions can exceed VARCHAR(500)
(CM1 longest prefixed text ~659 characters). Store the complete official
syllabus wording without truncation. Existing CS1/CB2 rows are preserved.
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "202607130002"
down_revision: str | None = "202607130001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    with op.batch_alter_table("learning_objectives", schema=None) as batch_op:
        batch_op.alter_column(
            "description",
            existing_type=sa.String(length=500),
            type_=sa.Text(),
            existing_nullable=False,
            existing_comment=(
                "What students should be able to do "
                "(e.g., 'Solve linear equations')"
            ),
            comment=(
                "What students should be able to do "
                "(full official syllabus text)"
            ),
        )


def downgrade() -> None:
    with op.batch_alter_table("learning_objectives", schema=None) as batch_op:
        batch_op.alter_column(
            "description",
            existing_type=sa.Text(),
            type_=sa.String(length=500),
            existing_nullable=False,
            existing_comment=(
                "What students should be able to do "
                "(full official syllabus text)"
            ),
            comment=(
                "What students should be able to do "
                "(e.g., 'Solve linear equations')"
            ),
        )
