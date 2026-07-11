"""Create sections table for V2 curriculum architecture.

Revision ID: 202610070001
Revises: 202609070004
Create Date: 2026-10-07 14:00:00.000000

This migration introduces the ``sections`` table required by the V2
curriculum architecture. It does NOT modify any existing tables; it only
adds the new table, its indexes, and the foreign key back to ``curricula``.
"""

from __future__ import annotations

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "202610070001"
down_revision: Union[str, None] = "202609070004"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create the sections table (FK to curricula; no existing tables touched)
    op.create_table(
        "sections",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("curriculum_id", sa.Integer(), nullable=False),
        sa.Column(
            "official_id",
            sa.String(length=100),
            nullable=True,
            comment="Canonical identifier from the official syllabus source",
        ),
        sa.Column(
            "code",
            sa.String(length=50),
            nullable=True,
            comment="Short human-readable code for the section (e.g. 'S1')",
        ),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column(
            "exam_weight",
            sa.Float(),
            nullable=True,
            comment="Relative weighting of this section in the exam",
        ),
        sa.Column(
            "display_order",
            sa.Integer(),
            nullable=False,
            server_default="0",
            comment="Ordering of the section within the curriculum",
        ),
        sa.Column(
            "estimated_hours",
            sa.Float(),
            nullable=True,
            comment="Estimated study hours required to cover this section",
        ),
        sa.Column(
            "difficulty",
            sa.String(length=50),
            nullable=True,
            comment="Difficulty rating (e.g. 'Easy', 'Medium', 'Hard')",
        ),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["curriculum_id"], ["curricula.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    # Indexes for common lookups
    op.create_index("ix_sections_curriculum_id", "sections", ["curriculum_id"])
    op.create_index("ix_sections_official_id", "sections", ["official_id"])
    op.create_index("ix_sections_code", "sections", ["code"])
    op.create_index("ix_sections_display_order", "sections", ["display_order"])


def downgrade() -> None:
    op.drop_index("ix_sections_display_order", table_name="sections")
    op.drop_index("ix_sections_code", table_name="sections")
    op.drop_index("ix_sections_official_id", table_name="sections")
    op.drop_index("ix_sections_curriculum_id", table_name="sections")
    op.drop_table("sections")