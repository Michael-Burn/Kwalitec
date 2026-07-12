"""DecisionState — in-memory audit materialisation of a Decision.

Not ORM / Alembic persistence. Materialises Decision payloads for audit,
thrashing control, and lineage without mutating Twin beliefs.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum

from app.domain.decision.decision import Decision


class JournalLinkage(StrEnum):
    """Optional journal outcome linkage when recorded (product path later)."""

    NONE = "none"
    ACCEPTED = "accepted"
    DISMISSED = "dismissed"
    DEFERRED = "deferred"


@dataclass(frozen=True)
class DecisionState:
    """Materialised decision context for audit / history (in-memory).

    Answers: what was decided, among which candidates, with which reasons,
    and optionally what happened next. Does not answer Twin mastery or
    readiness preparedness.

    Attributes:
        decision: Frozen Decision payload.
        twin_student_id: Twin identity reference used as input.
        readiness_derivation_id: Readiness derivation id when present.
        journal_linkage: Accept / dismiss / defer when recorded.
        materialised_at: Optional materialisation timestamp.
        decision_state_id: Optional audit identity for this materialisation.
        consumer_projection_tags: Optional hooks to Recommendation / Mission.
        superseded_by: Optional later DecisionState identity.
    """

    decision: Decision
    twin_student_id: str
    readiness_derivation_id: str | None = None
    journal_linkage: JournalLinkage = JournalLinkage.NONE
    materialised_at: datetime | None = None
    decision_state_id: str | None = None
    consumer_projection_tags: tuple[str, ...] = ()
    superseded_by: str | None = None

    @classmethod
    def materialise(
        cls,
        decision: Decision,
        *,
        readiness_derivation_id: str | None = None,
        journal_linkage: JournalLinkage | str = JournalLinkage.NONE,
        materialised_at: datetime | None = None,
        decision_state_id: str | None = None,
        consumer_projection_tags: list[str] | tuple[str, ...] | None = None,
        superseded_by: str | None = None,
    ) -> DecisionState:
        """Materialise a Decision into an in-memory DecisionState.

        Args:
            decision: Live Decision output from Decision Engine.
            readiness_derivation_id: Optional readiness audit id.
            journal_linkage: Optional journal outcome.
            materialised_at: Optional timestamp (omit for determinism).
            decision_state_id: Optional materialisation identity.
            consumer_projection_tags: Optional Recommendation / Mission hooks.
            superseded_by: Optional later DecisionState identity.

        Returns:
            Frozen DecisionState audit artefact.
        """
        linkage = (
            journal_linkage
            if isinstance(journal_linkage, JournalLinkage)
            else JournalLinkage(journal_linkage)
        )
        return cls(
            decision=decision,
            twin_student_id=decision.scope.student_id,
            readiness_derivation_id=readiness_derivation_id,
            journal_linkage=linkage,
            materialised_at=materialised_at,
            decision_state_id=decision_state_id,
            consumer_projection_tags=tuple(consumer_projection_tags or ()),
            superseded_by=superseded_by,
        )

    def with_journal_linkage(
        self,
        journal_linkage: JournalLinkage | str,
    ) -> DecisionState:
        """Return a copy with updated journal linkage (immutable)."""
        linkage = (
            journal_linkage
            if isinstance(journal_linkage, JournalLinkage)
            else JournalLinkage(journal_linkage)
        )
        return DecisionState(
            decision=self.decision,
            twin_student_id=self.twin_student_id,
            readiness_derivation_id=self.readiness_derivation_id,
            journal_linkage=linkage,
            materialised_at=self.materialised_at,
            decision_state_id=self.decision_state_id,
            consumer_projection_tags=self.consumer_projection_tags,
            superseded_by=self.superseded_by,
        )
