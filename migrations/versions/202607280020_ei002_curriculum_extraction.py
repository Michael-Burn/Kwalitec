"""EI-002 Curriculum Extraction — draft edition + provenance tables.

Revision ID: 202607280020
Revises: 202607280010
Create Date: 2026-07-28 21:00:00.000000

Additive: publication_state on ckg_graph_editions, ckg_node_provenance,
ckg_validation_reports. Does not alter V1/V2 curriculum engine, CIP, Twin,
or student runtime tables.
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "202607280020"
down_revision: str | tuple[str, ...] | None = "202607280010"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "ckg_graph_editions",
        sa.Column(
            "publication_state",
            sa.String(length=32),
            nullable=False,
            server_default="draft",
        ),
    )
    op.add_column(
        "ckg_graph_editions",
        sa.Column(
            "validation_status",
            sa.String(length=32),
            nullable=False,
            server_default="pending",
        ),
    )
    op.add_column(
        "ckg_graph_editions",
        sa.Column("source_cmp_ref", sa.String(length=512), nullable=True),
    )
    op.add_column(
        "ckg_graph_editions",
        sa.Column("source_syllabus_ref", sa.String(length=512), nullable=True),
    )
    op.create_index(
        "ix_ckg_graph_editions_publication_state",
        "ckg_graph_editions",
        ["publication_state"],
    )

    op.create_table(
        "ckg_node_provenance",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("edition_id", sa.String(length=64), nullable=False),
        sa.Column("stable_id", sa.String(length=256), nullable=False),
        sa.Column("source_document_id", sa.String(length=128), nullable=False),
        sa.Column("document_kind", sa.String(length=32), nullable=False),
        sa.Column("page_number", sa.Integer(), nullable=True),
        sa.Column("structural_path", sa.String(length=512), nullable=False),
        sa.Column("section_heading", sa.String(length=512), nullable=False),
        sa.Column(
            "paragraph_or_table_ref", sa.String(length=255), nullable=False
        ),
        sa.Column("confidence", sa.Integer(), nullable=False),
        sa.Column("extraction_method", sa.String(length=64), nullable=False),
        sa.Column("notes", sa.String(length=512), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["edition_id"],
            ["ckg_graph_editions.edition_id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "edition_id",
            "stable_id",
            name="uq_ckg_node_provenance_edition_stable",
        ),
    )
    op.create_index(
        "ix_ckg_node_provenance_edition_id",
        "ckg_node_provenance",
        ["edition_id"],
    )
    op.create_index(
        "ix_ckg_node_provenance_stable",
        "ckg_node_provenance",
        ["stable_id"],
    )
    op.create_index(
        "ix_ckg_node_provenance_document",
        "ckg_node_provenance",
        ["source_document_id"],
    )

    op.create_table(
        "ckg_validation_reports",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("report_id", sa.String(length=64), nullable=False),
        sa.Column("edition_id", sa.String(length=64), nullable=False),
        sa.Column("passed", sa.Boolean(), nullable=False),
        sa.Column("issue_count", sa.Integer(), nullable=False),
        sa.Column("report_json", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["edition_id"],
            ["ckg_graph_editions.edition_id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("report_id"),
    )
    op.create_index(
        "ix_ckg_validation_reports_edition",
        "ckg_validation_reports",
        ["edition_id"],
    )
    op.create_index(
        "ix_ckg_validation_reports_report_id",
        "ckg_validation_reports",
        ["report_id"],
        unique=True,
    )


def downgrade() -> None:
    op.drop_index(
        "ix_ckg_validation_reports_report_id",
        table_name="ckg_validation_reports",
    )
    op.drop_index(
        "ix_ckg_validation_reports_edition",
        table_name="ckg_validation_reports",
    )
    op.drop_table("ckg_validation_reports")

    op.drop_index(
        "ix_ckg_node_provenance_document", table_name="ckg_node_provenance"
    )
    op.drop_index(
        "ix_ckg_node_provenance_stable", table_name="ckg_node_provenance"
    )
    op.drop_index(
        "ix_ckg_node_provenance_edition_id", table_name="ckg_node_provenance"
    )
    op.drop_table("ckg_node_provenance")

    op.drop_index(
        "ix_ckg_graph_editions_publication_state",
        table_name="ckg_graph_editions",
    )
    op.drop_column("ckg_graph_editions", "source_syllabus_ref")
    op.drop_column("ckg_graph_editions", "source_cmp_ref")
    op.drop_column("ckg_graph_editions", "validation_status")
    op.drop_column("ckg_graph_editions", "publication_state")
