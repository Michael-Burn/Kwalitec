"""EI-003 Founder Curriculum Publishing — review, audit, snapshots.

Revision ID: 202607280030
Revises: 202607280020
Create Date: 2026-07-28 22:00:00.000000

Additive: review/publication fields on ckg_graph_editions;
ckg_node_review_states, ckg_editorial_audit_events,
ckg_publication_records, ckg_edition_snapshots.

Does not alter V1/V2 curriculum engine, CIP, Twin, or student runtime tables.
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "202607280030"
down_revision: str | tuple[str, ...] | None = "202607280020"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "ckg_graph_editions",
        sa.Column(
            "review_status",
            sa.String(length=32),
            nullable=False,
            server_default="pending",
        ),
    )
    op.add_column(
        "ckg_graph_editions",
        sa.Column("review_completed_at", sa.DateTime(), nullable=True),
    )
    op.add_column(
        "ckg_graph_editions",
        sa.Column("approved_by", sa.String(length=128), nullable=True),
    )
    op.add_column(
        "ckg_graph_editions",
        sa.Column("published_at", sa.DateTime(), nullable=True),
    )
    op.add_column(
        "ckg_graph_editions",
        sa.Column("published_by", sa.String(length=128), nullable=True),
    )
    op.add_column(
        "ckg_graph_editions",
        sa.Column("previous_edition_id", sa.String(length=64), nullable=True),
    )
    op.add_column(
        "ckg_graph_editions",
        sa.Column("publication_rationale", sa.Text(), nullable=True),
    )
    op.create_index(
        "ix_ckg_graph_editions_review_status",
        "ckg_graph_editions",
        ["review_status"],
    )

    op.create_table(
        "ckg_node_review_states",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("edition_id", sa.String(length=64), nullable=False),
        sa.Column("stable_id", sa.String(length=256), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("reviewer", sa.String(length=128), nullable=True),
        sa.Column("notes", sa.Text(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["edition_id"],
            ["ckg_graph_editions.edition_id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "edition_id",
            "stable_id",
            name="uq_ckg_node_review_edition_stable",
        ),
    )
    op.create_index(
        "ix_ckg_node_review_states_edition_id",
        "ckg_node_review_states",
        ["edition_id"],
    )
    op.create_index(
        "ix_ckg_node_review_states_stable_id",
        "ckg_node_review_states",
        ["stable_id"],
    )
    op.create_index(
        "ix_ckg_node_review_status",
        "ckg_node_review_states",
        ["edition_id", "status"],
    )

    op.create_table(
        "ckg_editorial_audit_events",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("event_id", sa.String(length=64), nullable=False),
        sa.Column("edition_id", sa.String(length=64), nullable=False),
        sa.Column("action", sa.String(length=64), nullable=False),
        sa.Column("actor", sa.String(length=128), nullable=False),
        sa.Column("stable_id", sa.String(length=256), nullable=True),
        sa.Column("detail_json", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["edition_id"],
            ["ckg_graph_editions.edition_id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("event_id"),
    )
    op.create_index(
        "ix_ckg_editorial_audit_edition",
        "ckg_editorial_audit_events",
        ["edition_id"],
    )
    op.create_index(
        "ix_ckg_editorial_audit_action",
        "ckg_editorial_audit_events",
        ["action"],
    )
    op.create_index(
        "ix_ckg_editorial_audit_events_event_id",
        "ckg_editorial_audit_events",
        ["event_id"],
        unique=True,
    )

    op.create_table(
        "ckg_publication_records",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("record_id", sa.String(length=64), nullable=False),
        sa.Column("edition_id", sa.String(length=64), nullable=False),
        sa.Column("subject_code", sa.String(length=32), nullable=False),
        sa.Column("publisher", sa.String(length=128), nullable=False),
        sa.Column("published_at", sa.DateTime(), nullable=False),
        sa.Column("previous_edition_id", sa.String(length=64), nullable=True),
        sa.Column("publication_rationale", sa.Text(), nullable=False),
        sa.Column("validation_status", sa.String(length=32), nullable=False),
        sa.Column("review_status", sa.String(length=32), nullable=False),
        sa.Column("review_completed_at", sa.DateTime(), nullable=True),
        sa.Column("snapshot_id", sa.String(length=64), nullable=True),
        sa.Column("detail_json", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["edition_id"],
            ["ckg_graph_editions.edition_id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("record_id"),
    )
    op.create_index(
        "ix_ckg_publication_records_edition",
        "ckg_publication_records",
        ["edition_id"],
    )
    op.create_index(
        "ix_ckg_publication_records_subject",
        "ckg_publication_records",
        ["subject_code"],
    )
    op.create_index(
        "ix_ckg_publication_records_record_id",
        "ckg_publication_records",
        ["record_id"],
        unique=True,
    )

    op.create_table(
        "ckg_edition_snapshots",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("snapshot_id", sa.String(length=64), nullable=False),
        sa.Column("edition_id", sa.String(length=64), nullable=False),
        sa.Column("subject_code", sa.String(length=32), nullable=False),
        sa.Column("capture_reason", sa.String(length=64), nullable=False),
        sa.Column("snapshot_json", sa.Text(), nullable=False),
        sa.Column("node_count", sa.Integer(), nullable=False),
        sa.Column("edge_count", sa.Integer(), nullable=False),
        sa.Column("captured_at", sa.DateTime(), nullable=False),
        sa.Column("captured_by", sa.String(length=128), nullable=False),
        sa.ForeignKeyConstraint(
            ["edition_id"],
            ["ckg_graph_editions.edition_id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("snapshot_id"),
    )
    op.create_index(
        "ix_ckg_edition_snapshots_edition",
        "ckg_edition_snapshots",
        ["edition_id"],
    )
    op.create_index(
        "ix_ckg_edition_snapshots_subject_code",
        "ckg_edition_snapshots",
        ["subject_code"],
    )
    op.create_index(
        "ix_ckg_edition_snapshots_snapshot_id",
        "ckg_edition_snapshots",
        ["snapshot_id"],
        unique=True,
    )


def downgrade() -> None:
    op.drop_index(
        "ix_ckg_edition_snapshots_snapshot_id",
        table_name="ckg_edition_snapshots",
    )
    op.drop_index(
        "ix_ckg_edition_snapshots_subject_code",
        table_name="ckg_edition_snapshots",
    )
    op.drop_index(
        "ix_ckg_edition_snapshots_edition",
        table_name="ckg_edition_snapshots",
    )
    op.drop_table("ckg_edition_snapshots")

    op.drop_index(
        "ix_ckg_publication_records_record_id",
        table_name="ckg_publication_records",
    )
    op.drop_index(
        "ix_ckg_publication_records_subject",
        table_name="ckg_publication_records",
    )
    op.drop_index(
        "ix_ckg_publication_records_edition",
        table_name="ckg_publication_records",
    )
    op.drop_table("ckg_publication_records")

    op.drop_index(
        "ix_ckg_editorial_audit_events_event_id",
        table_name="ckg_editorial_audit_events",
    )
    op.drop_index(
        "ix_ckg_editorial_audit_action",
        table_name="ckg_editorial_audit_events",
    )
    op.drop_index(
        "ix_ckg_editorial_audit_edition",
        table_name="ckg_editorial_audit_events",
    )
    op.drop_table("ckg_editorial_audit_events")

    op.drop_index(
        "ix_ckg_node_review_status",
        table_name="ckg_node_review_states",
    )
    op.drop_index(
        "ix_ckg_node_review_states_stable_id",
        table_name="ckg_node_review_states",
    )
    op.drop_index(
        "ix_ckg_node_review_states_edition_id",
        table_name="ckg_node_review_states",
    )
    op.drop_table("ckg_node_review_states")

    op.drop_index(
        "ix_ckg_graph_editions_review_status",
        table_name="ckg_graph_editions",
    )
    op.drop_column("ckg_graph_editions", "publication_rationale")
    op.drop_column("ckg_graph_editions", "previous_edition_id")
    op.drop_column("ckg_graph_editions", "published_by")
    op.drop_column("ckg_graph_editions", "published_at")
    op.drop_column("ckg_graph_editions", "approved_by")
    op.drop_column("ckg_graph_editions", "review_completed_at")
    op.drop_column("ckg_graph_editions", "review_status")
