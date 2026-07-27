"""ORM models for Learning Graph (SDT-003).

Stores graph *structure* only. Mastery scores live in SDT-001 Twin tables;
nodes hold mastery_link_id references rather than duplicated scores.
"""

from __future__ import annotations

from datetime import UTC, datetime

from app.extensions import db


def _utc_now() -> datetime:
    return datetime.now(UTC).replace(tzinfo=None)


class LgLearningGraph(db.Model):
    """Durable Learning Graph root — one per Student Digital Twin."""

    __tablename__ = "learning_graphs"
    __table_args__ = (
        db.UniqueConstraint("twin_id", name="uq_lg_graph_twin"),
        db.Index("ix_lg_graphs_student", "student_id"),
    )

    id: int = db.Column(db.Integer, primary_key=True)
    graph_id: str = db.Column(db.String(64), nullable=False, unique=True, index=True)
    twin_id: str = db.Column(
        db.String(64),
        db.ForeignKey("student_digital_twins.twin_id"),
        nullable=False,
    )
    student_id: str = db.Column(db.String(128), nullable=False)
    version: int = db.Column(db.Integer, nullable=False, default=1)
    created_at: datetime = db.Column(db.DateTime, nullable=False, default=_utc_now)
    updated_at: datetime = db.Column(
        db.DateTime, nullable=False, default=_utc_now, onupdate=_utc_now
    )

    def __repr__(self) -> str:
        return f"<LgLearningGraph {self.graph_id} twin={self.twin_id}>"


class LgGraphNode(db.Model):
    """Curriculum concept node. Structure only — no duplicated mastery rows."""

    __tablename__ = "learning_graph_nodes"
    __table_args__ = (
        db.UniqueConstraint("graph_id", "concept_id", name="uq_lg_node_concept"),
        db.Index("ix_lg_nodes_graph", "graph_id"),
    )

    id: int = db.Column(db.Integer, primary_key=True)
    node_id: str = db.Column(db.String(64), nullable=False, unique=True, index=True)
    graph_id: str = db.Column(
        db.String(64),
        db.ForeignKey("learning_graphs.graph_id"),
        nullable=False,
    )
    concept_id: str = db.Column(db.String(64), nullable=False)
    concept_title: str = db.Column(db.String(512), nullable=False, default="")
    mastery_link_id: str = db.Column(db.String(64), nullable=False, default="")
    # Cached projections for diagnostics / traversal (Twin remains SoT).
    projected_mastery: float = db.Column(db.Float, nullable=False, default=0.0)
    projected_confidence: float = db.Column(db.Float, nullable=False, default=0.0)
    projected_evidence_count: int = db.Column(db.Integer, nullable=False, default=0)
    projected_trend: str = db.Column(db.String(32), nullable=False, default="unknown")
    last_interaction: datetime | None = db.Column(db.DateTime, nullable=True)
    prerequisite_status: str = db.Column(
        db.String(32), nullable=False, default="unknown"
    )
    updated_at: datetime = db.Column(db.DateTime, nullable=False, default=_utc_now)


class LgGraphEdge(db.Model):
    """Directed relationship between two concept nodes."""

    __tablename__ = "learning_graph_edges"
    __table_args__ = (
        db.UniqueConstraint(
            "graph_id",
            "from_concept_id",
            "to_concept_id",
            "relationship_type",
            name="uq_lg_edge_rel",
        ),
        db.Index("ix_lg_edges_graph", "graph_id"),
        db.Index("ix_lg_edges_from", "graph_id", "from_concept_id"),
        db.Index("ix_lg_edges_to", "graph_id", "to_concept_id"),
    )

    id: int = db.Column(db.Integer, primary_key=True)
    edge_id: str = db.Column(db.String(64), nullable=False, unique=True, index=True)
    graph_id: str = db.Column(
        db.String(64),
        db.ForeignKey("learning_graphs.graph_id"),
        nullable=False,
    )
    from_concept_id: str = db.Column(db.String(64), nullable=False)
    to_concept_id: str = db.Column(db.String(64), nullable=False)
    relationship_type: str = db.Column(db.String(64), nullable=False)
    strength: float = db.Column(db.Float, nullable=False, default=1.0)
    confidence: float = db.Column(db.Float, nullable=False, default=0.0)
    provenance: str = db.Column(db.String(255), nullable=False, default="")
    supporting_evidence_json: str = db.Column(db.Text, nullable=False, default="[]")
    created_at: datetime = db.Column(db.DateTime, nullable=False, default=_utc_now)


class LgGraphSnapshot(db.Model):
    """Append-only structural snapshots."""

    __tablename__ = "learning_graph_snapshots"
    __table_args__ = (
        db.Index("ix_lg_snapshots_graph_created", "graph_id", "created_at"),
    )

    id: int = db.Column(db.Integer, primary_key=True)
    snapshot_id: str = db.Column(
        db.String(64), nullable=False, unique=True, index=True
    )
    graph_id: str = db.Column(
        db.String(64),
        db.ForeignKey("learning_graphs.graph_id"),
        nullable=False,
    )
    twin_id: str = db.Column(db.String(64), nullable=False)
    node_count: int = db.Column(db.Integer, nullable=False, default=0)
    edge_count: int = db.Column(db.Integer, nullable=False, default=0)
    reason: str = db.Column(db.String(255), nullable=False, default="")
    node_concept_ids_json: str = db.Column(db.Text, nullable=False, default="[]")
    edge_ids_json: str = db.Column(db.Text, nullable=False, default="[]")
    created_at: datetime = db.Column(db.DateTime, nullable=False, default=_utc_now)


class LgGraphUpdateHistory(db.Model):
    """Append-only graph update audit trail."""

    __tablename__ = "graph_update_history"
    __table_args__ = (
        db.Index("ix_lg_updates_graph_created", "graph_id", "created_at"),
    )

    id: int = db.Column(db.Integer, primary_key=True)
    update_id: str = db.Column(db.String(64), nullable=False, unique=True, index=True)
    graph_id: str = db.Column(
        db.String(64),
        db.ForeignKey("learning_graphs.graph_id"),
        nullable=False,
    )
    twin_id: str = db.Column(db.String(64), nullable=False)
    kind: str = db.Column(db.String(64), nullable=False)
    summary: str = db.Column(db.Text, nullable=False, default="")
    payload_json: str = db.Column(db.Text, nullable=False, default="{}")
    created_at: datetime = db.Column(db.DateTime, nullable=False, default=_utc_now)
