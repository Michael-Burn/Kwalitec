"""Optional Decision history input for anti-thrash context.

Dismiss ≠ mastery. History informs preference / thrashing control only.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum

from app.domain.decision.action_types import ActionFamily


class HistoryOutcome(StrEnum):
    """Recorded response to a prior Decision / recommendation."""

    ACCEPTED = "accepted"
    DISMISSED = "dismissed"
    DEFERRED = "deferred"
    SUPERSEDED = "superseded"


@dataclass(frozen=True)
class HistoryEntry:
    """One prior Decision response for anti-thrash context.

    Attributes:
        family: Action family previously selected / offered.
        curriculum_entity_id: Syllabus identity when applicable.
        outcome: Accept / dismiss / defer / superseded.
        decided_at: Optional timestamp (omit for deterministic equality).
        decision_id: Optional prior Decision / DecisionState identity.
    """

    family: ActionFamily
    curriculum_entity_id: str | None = None
    outcome: HistoryOutcome = HistoryOutcome.DISMISSED
    decided_at: datetime | None = None
    decision_id: str | None = None

    @classmethod
    def create(
        cls,
        family: ActionFamily | str,
        *,
        curriculum_entity_id: str | None = None,
        outcome: HistoryOutcome | str = HistoryOutcome.DISMISSED,
        decided_at: datetime | None = None,
        decision_id: str | None = None,
    ) -> HistoryEntry:
        """Construct a HistoryEntry."""
        fam = family if isinstance(family, ActionFamily) else ActionFamily(family)
        out = (
            outcome if isinstance(outcome, HistoryOutcome) else HistoryOutcome(outcome)
        )
        entity = None
        if curriculum_entity_id is not None:
            stripped = curriculum_entity_id.strip()
            entity = stripped or None
        return cls(
            family=fam,
            curriculum_entity_id=entity,
            outcome=out,
            decided_at=decided_at,
            decision_id=decision_id,
        )


@dataclass(frozen=True)
class DecisionHistory:
    """Ordered prior Decision responses consumed as anti-thrash context.

    Attributes:
        entries: Prior history entries (most recent last by convention).
    """

    entries: tuple[HistoryEntry, ...] = ()

    @classmethod
    def create(
        cls,
        entries: list[HistoryEntry] | tuple[HistoryEntry, ...] | None = None,
    ) -> DecisionHistory:
        """Construct a DecisionHistory."""
        return cls(entries=tuple(entries or ()))

    def dismissed_keys(self) -> frozenset[tuple[ActionFamily, str | None]]:
        """Return (family, entity) keys dismissed — dismiss ≠ mastery."""
        return frozenset(
            (e.family, e.curriculum_entity_id)
            for e in self.entries
            if e.outcome == HistoryOutcome.DISMISSED
        )
