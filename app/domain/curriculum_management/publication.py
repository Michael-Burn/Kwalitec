"""Publication — lifecycle carrier for a subject version."""

from __future__ import annotations

from dataclasses import dataclass

from app.domain.curriculum_management.publication_history import (
    PublicationHistory,
    PublicationHistoryEntry,
)
from app.domain.curriculum_management.publication_state import (
    PublicationState,
    PublicationTransitionEvent,
    is_terminal_publication_state,
    next_publication_state,
    resolve_publication_state,
)


@dataclass(frozen=True)
class Publication:
    """Publication lifecycle for a subject version.

    Responsible for lifecycle only. No educational behaviour.
    """

    publication_id: str
    version_id: str
    state: PublicationState = PublicationState.DRAFT
    history: PublicationHistory | None = None
    published_at: str | None = None
    archived_at: str | None = None

    @classmethod
    def create(
        cls,
        publication_id: str,
        version_id: str,
        *,
        state: PublicationState | str = PublicationState.DRAFT,
        history: PublicationHistory | None = None,
        published_at: str | None = None,
        archived_at: str | None = None,
    ) -> Publication:
        """Construct a Publication after validating invariants."""
        pid = _require_non_empty(publication_id, "publication_id")
        vid = _require_non_empty(version_id, "version_id")
        resolved = resolve_publication_state(state)
        hist = history or PublicationHistory.create(f"hist-{pid}", vid)
        if hist.version_id != vid:
            raise ValueError("history version_id must match publication version_id")
        pub_at = (
            None
            if published_at is None
            else _require_non_empty(published_at, "published_at")
        )
        arch_at = (
            None
            if archived_at is None
            else _require_non_empty(archived_at, "archived_at")
        )
        if resolved is PublicationState.PUBLISHED and pub_at is None:
            pub_at = "unspecified"
        if resolved is PublicationState.ARCHIVED and arch_at is None:
            arch_at = "unspecified"
        return cls(
            publication_id=pid,
            version_id=vid,
            state=resolved,
            history=hist,
            published_at=pub_at,
            archived_at=arch_at,
        )

    @property
    def is_published(self) -> bool:
        """True when state is PUBLISHED."""
        return self.state is PublicationState.PUBLISHED

    @property
    def is_archived(self) -> bool:
        """True when state is ARCHIVED."""
        return self.state is PublicationState.ARCHIVED

    @property
    def is_terminal(self) -> bool:
        """True when no further pipeline transitions are lawful."""
        return is_terminal_publication_state(self.state)

    def transition(
        self,
        event: PublicationTransitionEvent | str,
        *,
        actor_id: str | None = None,
        reason: str = "",
        occurred_at: str | None = None,
        entry_id: str | None = None,
    ) -> Publication:
        """Return a new Publication after applying a lawful transition.

        Raises:
            ValueError: When the transition is unlawful.
        """
        resolved_event = (
            event
            if isinstance(event, PublicationTransitionEvent)
            else PublicationTransitionEvent(str(event).strip().lower())
        )
        nxt = next_publication_state(self.state, resolved_event)
        if nxt is None:
            raise ValueError(
                f"Illegal publication transition: {self.state.value} "
                f"+ {resolved_event.value}"
            )
        hist = self.history or PublicationHistory.create(
            f"hist-{self.publication_id}", self.version_id
        )
        eid = entry_id or f"he-{hist.entry_count + 1}-{resolved_event.value}"
        entry = PublicationHistoryEntry.create(
            eid,
            self.state,
            nxt,
            resolved_event,
            actor_id=actor_id,
            reason=reason,
            occurred_at=occurred_at,
        )
        published_at = self.published_at
        archived_at = self.archived_at
        if nxt is PublicationState.PUBLISHED:
            published_at = occurred_at or published_at or "unspecified"
        if nxt is PublicationState.ARCHIVED:
            archived_at = occurred_at or archived_at or "unspecified"
        return Publication(
            publication_id=self.publication_id,
            version_id=self.version_id,
            state=nxt,
            history=hist.with_entry(entry),
            published_at=published_at,
            archived_at=archived_at,
        )


def _require_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a non-empty string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized
