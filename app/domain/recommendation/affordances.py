"""Response affordances — accept / dismiss / defer as journalable outcomes.

Structural hooks only. Accept is commitment / preference, not mastery.
Decision Journal ORM persistence is deferred.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class AffordanceOutcome(StrEnum):
    """Journalable student responses to a Recommendation."""

    ACCEPT = "accept"
    DISMISS = "dismiss"
    DEFER = "defer"


# Stable catalogue — preference / intent only; never mastery grants.
AFFORDANCE_OUTCOME_CATALOGUE: tuple[AffordanceOutcome, ...] = (
    AffordanceOutcome.ACCEPT,
    AffordanceOutcome.DISMISS,
    AffordanceOutcome.DEFER,
)


class JournalLinkageHook(StrEnum):
    """Structural Decision Journal linkage posture (not ORM persistence)."""

    AVAILABLE = "available"
    PREFERENCE_INTENT_ONLY = "preference_intent_only"
    NOT_MASTERY = "not_mastery"


@dataclass(frozen=True)
class ResponseAffordances:
    """Accept / dismiss / defer surface with journal linkage hooks.

    Attributes:
        outcomes: Stable journalable outcomes.
        journal_linkage_hooks: Structural preference/intent hooks.
        emphasis_tags: Communication emphasis (e.g. prior-dismiss respect).
        mastery_implied: Always False — accept ≠ mastery.
    """

    outcomes: tuple[AffordanceOutcome, ...] = AFFORDANCE_OUTCOME_CATALOGUE
    journal_linkage_hooks: tuple[JournalLinkageHook, ...] = (
        JournalLinkageHook.AVAILABLE,
        JournalLinkageHook.PREFERENCE_INTENT_ONLY,
        JournalLinkageHook.NOT_MASTERY,
    )
    emphasis_tags: tuple[str, ...] = ()
    mastery_implied: bool = False

    @classmethod
    def create(
        cls,
        *,
        outcomes: list[AffordanceOutcome]
        | tuple[AffordanceOutcome, ...]
        | None = None,
        journal_linkage_hooks: list[JournalLinkageHook]
        | tuple[JournalLinkageHook, ...]
        | None = None,
        emphasis_tags: list[str] | tuple[str, ...] | None = None,
    ) -> ResponseAffordances:
        """Construct ResponseAffordances with mastery_implied forced False."""
        return cls(
            outcomes=tuple(outcomes or AFFORDANCE_OUTCOME_CATALOGUE),
            journal_linkage_hooks=tuple(
                journal_linkage_hooks
                or (
                    JournalLinkageHook.AVAILABLE,
                    JournalLinkageHook.PREFERENCE_INTENT_ONLY,
                    JournalLinkageHook.NOT_MASTERY,
                )
            ),
            emphasis_tags=tuple(emphasis_tags or ()),
            mastery_implied=False,
        )

    def with_emphasis(
        self, tags: list[str] | tuple[str, ...]
    ) -> ResponseAffordances:
        """Return a copy with additional emphasis tags (selection unchanged)."""
        merged = list(self.emphasis_tags)
        for tag in tags:
            if tag not in merged:
                merged.append(tag)
        return ResponseAffordances(
            outcomes=self.outcomes,
            journal_linkage_hooks=self.journal_linkage_hooks,
            emphasis_tags=tuple(merged),
            mastery_implied=False,
        )
