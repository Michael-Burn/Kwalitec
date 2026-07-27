"""SDT-003 Learning Graph structure tables.

Revision ID: 202607270010
Revises: 202607270009
Create Date: 2026-07-27 23:00:00.000000

Additive schema. Does not alter SDT-001 Twin or SDT-002 reasoning tables.
Stores graph structure only — no duplicated mastery inference rows.
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "202607270010"
down_revision: str | None = "202607270009"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "learning_graphs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("graph_id", sa.String(length=64), nullable=False),
        sa.Column("twin_id", sa.String(length=64), nullable=False),
        sa.Column("student_id", sa.String(length=128), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["twin_id"],
            ["student_digital_twins.twin_id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("twin_id", name="uq_lg_graph_twin"),
    )
    op.create_index(
        "ix_learning_graphs_graph_id", "learning_graphs", ["graph_id"], unique=True
    )
    op.create_index(
        "ix_lg_graphs_student", "learning_graphs", ["student_id"], unique=False
    )

    op.create_table(
        "learning_graph_nodes",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("node_id", sa.String(length=64), nullable=False),
        sa.Column("graph_id", sa.String(length=64), nullable=False),
        sa.Column("concept_id", sa.String(length=64), nullable=False),
        sa.Column("concept_title", sa.String(length=512), nullable=False),
        sa.Column("mastery_link_id", sa.String(length=64), nullable=False),
        sa.Column("projected_mastery", sa.Float(), nullable=False),
        sa.Column("projected_confidence", sa.Float(), nullable=False),
        sa.Column("projected_evidence_count", sa.Integer(), nullable=False),
        sa.Column("projected_trend", sa.String(length=32), nullable=False),
        sa.Column("last_interaction", sa.DateTime(), nullable=True),
        sa.Column("prerequisite_status", sa.String(length=32), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["graph_id"],
            ["learning_graphs.graph_id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("graph_id", "concept_id", name="uq_lg_node_concept"),
    )
    op.create_index(
        "ix_learning_graph_nodes_node_id",
        "learning_graph_nodes",
        ["node_id"],
        unique=True,
    )
    op.create_index(
        "ix_lg_nodes_graph", "learning_graph_nodes", ["graph_id"], unique=False
    )

    op.create_table(
        "learning_graph_edges",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("edge_id", sa.String(length=64), nullable=False),
        sa.Column("graph_id", sa.String(length=64), nullable=False),
        sa.Column("from_concept_id", sa.String(length=64), nullable=False),
        sa.Column("to_concept_id", sa.String(length=64), nullable=False),
        sa.Column("relationship_type", sa.String(length=64), nullable=False),
        sa.Column("strength", sa.Float(), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=False),
        sa.Column("provenance", sa.String(length=255), nullable=False),
        sa.Column("supporting_evidence_json", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["graph_id"],
            ["learning_graphs.graph_id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "graph_id",
            "from_concept_id",
            "to_concept_id",
            "relationship_type",
            name="uq_lg_edge_rel",
        ),
    )
    op.create_index(
        "ix_learning_graph_edges_edge_id",
        "learning_graph_edges",
        ["edge_id"],
        unique=True,
    )
    op.create_index(
        "ix_lg_edges_graph", "learning_graph_edges", ["graph_id"], unique=False
    )
    op.create_index(
        "ix_lg_edges_from",
        "learning_graph_edges",
        ["graph_id", "from_concept_id"],
        unique=False,
    )
    op.create_index(
        "ix_lg_edges_to",
        "learning_graph_edges",
        ["graph_id", "to_concept_id"],
        unique=False,
    )

    op.create_table(
        "learning_graph_snapshots",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("snapshot_id", sa.String(length=64), nullable=False),
        sa.Column("graph_id", sa.String(length=64), nullable=False),
        sa.Column("twin_id", sa.String(length=64), nullable=False),
        sa.Column("node_count", sa.Integer(), nullable=False),
        sa.Column("edge_count", sa.Integer(), nullable=False),
        sa.Column("reason", sa.String(length=255), nullable=False),
        sa.Column("node_concept_ids_json", sa.Text(), nullable=False),
        sa.Column("edge_ids_json", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["graph_id"],
            ["learning_graphs.graph_id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_learning_graph_snapshots_snapshot_id",
        "learning_graph_snapshots",
        ["snapshot_id"],
        unique=True,
    )
    op.create_index(
        "ix_lg_snapshots_graph_created",
        "learning_graph_snapshots",
        ["graph_id", "created_at"],
        unique=False,
    )

    op.create_table(
        "graph_update_history",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("update_id", sa.String(length=64), nullable=False),
        sa.Column("graph_id", sa.String(length=64), nullable=False),
        sa.Column("twin_id", sa.String(length=64), nullable=False),
        sa.Column("kind", sa.String(length=64), nullable=False),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("payload_json", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["graph_id"],
            ["learning_graphs.graph_id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_graph_update_history_update_id",
        "graph_update_history",
        ["update_id"],
        unique=True,
    )
    op.create_index(
        "ix_lg_updates_graph_created",
        "graph_update_history",
        ["graph_id", "created_at"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_lg_updates_graph_created", table_name="graph_update_history")
    op.drop_index("ix_graph_update_history_update_id", table_name="graph_update_history")
    op.drop_table("graph_update_history")

    op.drop_index(
        "ix_lg_snapshots_graph_created", table_name="learning_graph_snapshots"
    )
    op.drop_index(
        "ix_learning_graph_snapshots_snapshot_id",
        table_name="learning_graph_snapshots",
    )
    op.drop_table("learning_graph_snapshots")

    op.drop_index("ix_lg_edges_to", table_name="learning_graph_edges")
    op.drop_index("ix_lg_edges_from", table_name="learning_graph_edges")
    op.drop_index("ix_lg_edges_graph", table_name="learning_graph_edges")
    op.drop_index("ix_learning_graph_edges_edge_id", table_name="learning_graph_edges")
    op.drop_table("learning_graph_edges")

    op.drop_index("ix_lg_nodes_graph", table_name="learning_graph_nodes")
    op.drop_index("ix_learning_graph_nodes_node_id", table_name="learning_graph_nodes")
    op.drop_table("learning_graph_nodes")

    op.drop_index("ix_lg_graphs_student", table_name="learning_graphs")
    op.drop_index("ix_learning_graphs_graph_id", table_name="learning_graphs")
    op.drop_table("learning_graphs")
