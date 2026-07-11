"""Link Topic to Section for the V2 curriculum hierarchy.

Revision ID: 202610070002
Revises: 202610070001
Create Date: 2026-10-07 14:30:00.000000

This migration introduces the Topic -> Section relationship required by the
V2 curriculum hierarchy. It:

- adds a nullable ``section_id`` column to the ``topics`` table
- creates the foreign key ``topics.section_id`` -> ``sections.id``
- creates an index on ``topics.section_id``

The column is intentionally left NULLABLE and is NOT populated here. No
existing rows are modified and no data migration occurs, so existing topics
(and the study plans built on them) continue to work unchanged.

The operations are wrapped in ``batch_alter_table`` so the migration is
portable to SQLite, which does not support in-place ALTER of constraints and
requires a copy-and-move rebuild strategy.
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision: str = "202610070002"
down_revision: Union[str, None] = "202610070001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Use batch mode for SQLite compatibility (ALTER of constraints unsupported)
    with op.batch_alter_table("topics") as batch_op:
        # Add the nullable section_id column (no existing rows touched)
        batch_op.add_column(
            sa.Column(
                "section_id",
                sa.Integer(),
                nullable=True,
                comment="Optional parent Section in the V2 curriculum hierarchy",
            )
        )
        # Foreign key back to sections
        batch_op.create_foreign_key(
            "fk_topics_section_id_sections",
            "sections",
            ["section_id"],
            ["id"],
        )
        # Index for common lookups by section
        batch_op.create_index("ix_topics_section_id", ["section_id"])


def downgrade() -> None:
    with op.batch_alter_table("topics") as batch_op:
        batch_op.drop_index("ix_topics_section_id")
        batch_op.drop_constraint(
            "fk_topics_section_id_sections", type_="foreignkey"
        )
        batch_op.drop_column("section_id")