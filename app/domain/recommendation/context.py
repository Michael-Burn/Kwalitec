"""Optional communication-context VO for Recommendation packaging.

Shapes phrasing and affordance emphasis only — never changes selected action,
never writes Twin beliefs, never invents Mid readiness or ranking.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RecommendationContext:
    """Communication-layer adaptation input (optional).

    Attributes:
        goals_language_tags: Sitting / capacity / deadline communication only.
        journal_history_refs: Prior accept/dismiss/defer identities when available.
        confidence_framing: Only if Decision already cited Confidence as risk.
        notes: Structural notes — never selection overrides.
    """

    goals_language_tags: tuple[str, ...] = ()
    journal_history_refs: tuple[str, ...] = ()
    confidence_framing: tuple[str, ...] = ()
    notes: tuple[str, ...] = ()

    @classmethod
    def create(
        cls,
        *,
        goals_language_tags: list[str] | tuple[str, ...] | None = None,
        journal_history_refs: list[str] | tuple[str, ...] | None = None,
        confidence_framing: list[str] | tuple[str, ...] | None = None,
        notes: list[str] | tuple[str, ...] | None = None,
    ) -> RecommendationContext:
        """Construct a RecommendationContext."""
        return cls(
            goals_language_tags=tuple(goals_language_tags or ()),
            journal_history_refs=tuple(journal_history_refs or ()),
            confidence_framing=tuple(confidence_framing or ()),
            notes=tuple(notes or ()),
        )

    @classmethod
    def empty(cls) -> RecommendationContext:
        """Return an empty communication context."""
        return cls()
