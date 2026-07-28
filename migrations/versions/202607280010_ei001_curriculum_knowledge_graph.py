"""EI-001 Curriculum Knowledge Graph foundation tables.

Revision ID: 202607280010
Revises: 202607190002, 202607280002
Create Date: 2026-07-28 20:00:00.000000

Additive schema for the Curriculum Knowledge Graph (educational SoT).
Merges Alembic heads from the V2 aggregate merge lineage and ILE-005.
Does not alter V1/V2 curriculum engine tables, CIP, Twin, or student runtime.
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "202607280010"
down_revision: str | tuple[str, ...] | None = (
    "202607190002",
    "202607280002",
)
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "ckg_graph_editions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("edition_id", sa.String(length=64), nullable=False),
        sa.Column("subject_code", sa.String(length=32), nullable=False),
        sa.Column("edition_label", sa.String(length=64), nullable=False),
        sa.Column("provider", sa.String(length=64), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "subject_code",
            "edition_label",
            name="uq_ckg_graph_editions_subject_edition",
        ),
    )
    op.create_index(
        "ix_ckg_graph_editions_edition_id",
        "ckg_graph_editions",
        ["edition_id"],
        unique=True,
    )
    op.create_index(
        "ix_ckg_graph_editions_subject_code",
        "ckg_graph_editions",
        ["subject_code"],
        unique=False,
    )

    op.create_table(
        "ckg_subjects",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("stable_id", sa.String(length=128), nullable=False),
        sa.Column("graph_edition_id", sa.String(length=64), nullable=False),
        sa.Column("code", sa.String(length=32), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("provider", sa.String(length=64), nullable=False),
        sa.Column("edition_label", sa.String(length=64), nullable=False),
        sa.Column("sequence_index", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["graph_edition_id"],
            ["ckg_graph_editions.edition_id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_ckg_subjects_stable_id", "ckg_subjects", ["stable_id"], unique=True
    )
    op.create_index(
        "ix_ckg_subjects_graph_edition_id",
        "ckg_subjects",
        ["graph_edition_id"],
        unique=False,
    )

    op.create_table(
        "ckg_topics",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("stable_id", sa.String(length=128), nullable=False),
        sa.Column("subject_stable_id", sa.String(length=128), nullable=False),
        sa.Column("code", sa.String(length=64), nullable=False),
        sa.Column("title", sa.String(length=512), nullable=False),
        sa.Column("display_order", sa.Integer(), nullable=False),
        sa.Column("difficulty", sa.String(length=32), nullable=False),
        sa.Column("estimated_study_minutes", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["subject_stable_id"],
            ["ckg_subjects.stable_id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_ckg_topics_stable_id", "ckg_topics", ["stable_id"], unique=True
    )
    op.create_index(
        "ix_ckg_topics_subject_stable_id",
        "ckg_topics",
        ["subject_stable_id"],
        unique=False,
    )
    op.create_index(
        "ix_ckg_topics_subject_order",
        "ckg_topics",
        ["subject_stable_id", "display_order"],
        unique=False,
    )

    op.create_table(
        "ckg_sections",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("stable_id", sa.String(length=160), nullable=False),
        sa.Column("topic_stable_id", sa.String(length=128), nullable=False),
        sa.Column("code", sa.String(length=64), nullable=False),
        sa.Column("title", sa.String(length=512), nullable=False),
        sa.Column("display_order", sa.Integer(), nullable=False),
        sa.Column("difficulty", sa.String(length=32), nullable=False),
        sa.Column("estimated_study_minutes", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["topic_stable_id"],
            ["ckg_topics.stable_id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_ckg_sections_stable_id", "ckg_sections", ["stable_id"], unique=True
    )
    op.create_index(
        "ix_ckg_sections_topic_stable_id",
        "ckg_sections",
        ["topic_stable_id"],
        unique=False,
    )
    op.create_index(
        "ix_ckg_sections_topic_order",
        "ckg_sections",
        ["topic_stable_id", "display_order"],
        unique=False,
    )

    op.create_table(
        "ckg_subsections",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("stable_id", sa.String(length=192), nullable=False),
        sa.Column("section_stable_id", sa.String(length=160), nullable=False),
        sa.Column("code", sa.String(length=64), nullable=False),
        sa.Column("title", sa.String(length=512), nullable=False),
        sa.Column("display_order", sa.Integer(), nullable=False),
        sa.Column("difficulty", sa.String(length=32), nullable=False),
        sa.Column("estimated_study_minutes", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["section_stable_id"],
            ["ckg_sections.stable_id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_ckg_subsections_stable_id",
        "ckg_subsections",
        ["stable_id"],
        unique=True,
    )
    op.create_index(
        "ix_ckg_subsections_section_stable_id",
        "ckg_subsections",
        ["section_stable_id"],
        unique=False,
    )
    op.create_index(
        "ix_ckg_subsections_section_order",
        "ckg_subsections",
        ["section_stable_id", "display_order"],
        unique=False,
    )

    op.create_table(
        "ckg_learning_objectives",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("stable_id", sa.String(length=224), nullable=False),
        sa.Column("subsection_stable_id", sa.String(length=192), nullable=False),
        sa.Column("code", sa.String(length=64), nullable=False),
        sa.Column("statement", sa.Text(), nullable=False),
        sa.Column("cognitive_level", sa.String(length=32), nullable=False),
        sa.Column("learning_type", sa.String(length=32), nullable=False),
        sa.Column("display_order", sa.Integer(), nullable=False),
        sa.Column("difficulty", sa.String(length=32), nullable=False),
        sa.Column("estimated_study_minutes", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["subsection_stable_id"],
            ["ckg_subsections.stable_id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_ckg_learning_objectives_stable_id",
        "ckg_learning_objectives",
        ["stable_id"],
        unique=True,
    )
    op.create_index(
        "ix_ckg_learning_objectives_subsection_stable_id",
        "ckg_learning_objectives",
        ["subsection_stable_id"],
        unique=False,
    )
    op.create_index(
        "ix_ckg_los_subsection_order",
        "ckg_learning_objectives",
        ["subsection_stable_id", "display_order"],
        unique=False,
    )

    op.create_table(
        "ckg_definitions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("stable_id", sa.String(length=256), nullable=False),
        sa.Column("owner_stable_id", sa.String(length=224), nullable=False),
        sa.Column("title", sa.String(length=512), nullable=False),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column("cmp_locator", sa.String(length=255), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_ckg_definitions_stable_id",
        "ckg_definitions",
        ["stable_id"],
        unique=True,
    )
    op.create_index(
        "ix_ckg_definitions_owner",
        "ckg_definitions",
        ["owner_stable_id"],
        unique=False,
    )

    op.create_table(
        "ckg_formulas",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("stable_id", sa.String(length=256), nullable=False),
        sa.Column("owner_stable_id", sa.String(length=224), nullable=False),
        sa.Column("title", sa.String(length=512), nullable=False),
        sa.Column("notation", sa.Text(), nullable=False),
        sa.Column("latex", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_ckg_formulas_stable_id", "ckg_formulas", ["stable_id"], unique=True
    )
    op.create_index(
        "ix_ckg_formulas_owner", "ckg_formulas", ["owner_stable_id"], unique=False
    )

    op.create_table(
        "ckg_worked_examples",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("stable_id", sa.String(length=256), nullable=False),
        sa.Column("owner_stable_id", sa.String(length=224), nullable=False),
        sa.Column("title", sa.String(length=512), nullable=False),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_ckg_worked_examples_stable_id",
        "ckg_worked_examples",
        ["stable_id"],
        unique=True,
    )
    op.create_index(
        "ix_ckg_worked_examples_owner",
        "ckg_worked_examples",
        ["owner_stable_id"],
        unique=False,
    )

    op.create_table(
        "ckg_practice_exercises",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("stable_id", sa.String(length=256), nullable=False),
        sa.Column("owner_stable_id", sa.String(length=224), nullable=False),
        sa.Column("title", sa.String(length=512), nullable=False),
        sa.Column("difficulty", sa.String(length=32), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_ckg_practice_exercises_stable_id",
        "ckg_practice_exercises",
        ["stable_id"],
        unique=True,
    )
    op.create_index(
        "ix_ckg_practice_exercises_owner",
        "ckg_practice_exercises",
        ["owner_stable_id"],
        unique=False,
    )

    op.create_table(
        "ckg_reading_references",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("stable_id", sa.String(length=256), nullable=False),
        sa.Column("owner_stable_id", sa.String(length=224), nullable=False),
        sa.Column("title", sa.String(length=512), nullable=False),
        sa.Column("document_kind", sa.String(length=64), nullable=False),
        sa.Column("locator", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_ckg_reading_references_stable_id",
        "ckg_reading_references",
        ["stable_id"],
        unique=True,
    )
    op.create_index(
        "ix_ckg_reading_references_owner",
        "ckg_reading_references",
        ["owner_stable_id"],
        unique=False,
    )

    op.create_table(
        "ckg_syllabus_outcomes",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("stable_id", sa.String(length=256), nullable=False),
        sa.Column("owner_stable_id", sa.String(length=224), nullable=False),
        sa.Column("outcome_code", sa.String(length=64), nullable=False),
        sa.Column("statement_ref", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_ckg_syllabus_outcomes_stable_id",
        "ckg_syllabus_outcomes",
        ["stable_id"],
        unique=True,
    )
    op.create_index(
        "ix_ckg_syllabus_outcomes_owner",
        "ckg_syllabus_outcomes",
        ["owner_stable_id"],
        unique=False,
    )

    op.create_table(
        "ckg_lo_links",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("link_id", sa.String(length=64), nullable=False),
        sa.Column("lo_stable_id", sa.String(length=224), nullable=False),
        sa.Column("target_kind", sa.String(length=64), nullable=False),
        sa.Column("target_stable_id", sa.String(length=256), nullable=False),
        sa.Column("relationship_type", sa.String(length=64), nullable=False),
        sa.Column("sequence_index", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["lo_stable_id"],
            ["ckg_learning_objectives.stable_id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "lo_stable_id",
            "target_kind",
            "target_stable_id",
            name="uq_ckg_lo_links_lo_target",
        ),
    )
    op.create_index(
        "ix_ckg_lo_links_link_id", "ckg_lo_links", ["link_id"], unique=True
    )
    op.create_index(
        "ix_ckg_lo_links_lo_stable_id",
        "ckg_lo_links",
        ["lo_stable_id"],
        unique=False,
    )
    op.create_index(
        "ix_ckg_lo_links_target",
        "ckg_lo_links",
        ["target_stable_id"],
        unique=False,
    )

    op.create_table(
        "ckg_edges",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("edge_id", sa.String(length=128), nullable=False),
        sa.Column("from_stable_id", sa.String(length=256), nullable=False),
        sa.Column("to_stable_id", sa.String(length=256), nullable=False),
        sa.Column("relationship_type", sa.String(length=64), nullable=False),
        sa.Column("sequence_index", sa.Integer(), nullable=False),
        sa.Column("rationale", sa.String(length=512), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "from_stable_id",
            "to_stable_id",
            "relationship_type",
            name="uq_ckg_edges_from_to_type",
        ),
    )
    op.create_index(
        "ix_ckg_edges_edge_id", "ckg_edges", ["edge_id"], unique=True
    )
    op.create_index(
        "ix_ckg_edges_from", "ckg_edges", ["from_stable_id"], unique=False
    )
    op.create_index(
        "ix_ckg_edges_to", "ckg_edges", ["to_stable_id"], unique=False
    )
    op.create_index(
        "ix_ckg_edges_type", "ckg_edges", ["relationship_type"], unique=False
    )

    op.create_table(
        "ckg_id_aliases",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("old_stable_id", sa.String(length=256), nullable=False),
        sa.Column("new_stable_id", sa.String(length=256), nullable=False),
        sa.Column("reason", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("old_stable_id", name="uq_ckg_id_aliases_old"),
    )
    op.create_index(
        "ix_ckg_id_aliases_new",
        "ckg_id_aliases",
        ["new_stable_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_table("ckg_id_aliases")
    op.drop_table("ckg_edges")
    op.drop_table("ckg_lo_links")
    op.drop_table("ckg_syllabus_outcomes")
    op.drop_table("ckg_reading_references")
    op.drop_table("ckg_practice_exercises")
    op.drop_table("ckg_worked_examples")
    op.drop_table("ckg_formulas")
    op.drop_table("ckg_definitions")
    op.drop_table("ckg_learning_objectives")
    op.drop_table("ckg_subsections")
    op.drop_table("ckg_sections")
    op.drop_table("ckg_topics")
    op.drop_table("ckg_subjects")
    op.drop_table("ckg_graph_editions")
