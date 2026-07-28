"""Decision Journal persistence models (ILE-002).

Educational narrative memory — not telemetry, not analytics.
Entries never rewrite historical recommendations; evidence appends.
"""

from __future__ import annotations

from datetime import datetime

from app.extensions import db


class DecisionJournalEntry(db.Model):
    """One significant educational interaction in the learner's journal."""

    __tablename__ = "decision_journal_entries"

    id: int = db.Column(db.Integer, primary_key=True)
    # Stable public Decision ID (never reused; survives archive).
    entry_id: str = db.Column(db.String(64), nullable=False, unique=True, index=True)
    user_id: int = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False, index=True
    )

    # Optional ILE-011 catalogue Decision ID (e.g. D-L01) — product mapping only.
    catalogue_decision_id: str = db.Column(db.String(32), nullable=False, default="")

    kind: str = db.Column(db.String(64), nullable=False, index=True)
    lifecycle_status: str = db.Column(
        db.String(32), nullable=False, default="recommended", index=True
    )

    # Educational explainability arc (student-safe language only).
    educational_context: str = db.Column(db.Text, nullable=False, default="")
    observation: str = db.Column(db.Text, nullable=False, default="")
    meaning: str = db.Column(db.Text, nullable=False, default="")
    recommendation: str = db.Column(db.Text, nullable=False, default="")
    supporting_evidence_summary: str = db.Column(db.Text, nullable=False, default="")
    qualitative_confidence: str = db.Column(
        db.String(32), nullable=False, default="emerging"
    )
    expected_benefit: str = db.Column(db.Text, nullable=False, default="")
    uncertainty: str = db.Column(db.Text, nullable=False, default="")

    student_action: str = db.Column(db.String(32), nullable=False, default="none_yet")
    outcome_summary: str = db.Column(db.Text, nullable=True)
    reflection_status: str = db.Column(
        db.String(32), nullable=False, default="pending"
    )
    reflection_note: str = db.Column(db.Text, nullable=False, default="")

    # Optional links to preference / commitment rows (never mastery).
    legacy_decision_id: int = db.Column(db.Integer, nullable=True)
    commitment_id: int = db.Column(db.Integer, nullable=True)

    recorded_at: datetime = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False, index=True
    )
    accepted_at: datetime = db.Column(db.DateTime, nullable=True)
    deferred_at: datetime = db.Column(db.DateTime, nullable=True)
    reflected_at: datetime = db.Column(db.DateTime, nullable=True)
    outcome_at: datetime = db.Column(db.DateTime, nullable=True)
    archived_at: datetime = db.Column(db.DateTime, nullable=True)
    created_at: datetime = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False
    )
    updated_at: datetime = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    user = db.relationship(
        "User",
        backref=db.backref("decision_journal_entries", lazy=True),
    )
    evidence_events = db.relationship(
        "DecisionJournalEvidenceEvent",
        back_populates="entry",
        lazy="select",
        order_by="DecisionJournalEvidenceEvent.recorded_at",
    )

    def __repr__(self) -> str:
        return (
            f"<DecisionJournalEntry {self.entry_id} "
            f"status={self.lifecycle_status} kind={self.kind}>"
        )


class DecisionJournalEvidenceEvent(db.Model):
    """Append-only evidence evolution for a journal entry.

    Never edits the original recommendation or observation snapshot.
    """

    __tablename__ = "decision_journal_evidence_events"

    id: int = db.Column(db.Integer, primary_key=True)
    entry_pk: int = db.Column(
        db.Integer,
        db.ForeignKey("decision_journal_entries.id"),
        nullable=False,
        index=True,
    )
    summary: str = db.Column(db.Text, nullable=False, default="")
    recorded_at: datetime = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False, index=True
    )

    entry = db.relationship(
        "DecisionJournalEntry",
        back_populates="evidence_events",
    )

    def __repr__(self) -> str:
        return f"<DecisionJournalEvidenceEvent entry={self.entry_pk} id={self.id}>"
