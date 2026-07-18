"""Publication history — immutable lifecycle transition log."""

from __future__ import annotations

from dataclasses import dataclass, field

from app.domain.curriculum_management.publication_state import (
    PublicationState,
    PublicationTransitionEvent,
    resolve_publication_state,
)


@dataclass(frozen=True)
class PublicationHistoryEntry:
    """Single immutable publication state transition record."""

    entry_id: str
    from_state: PublicationState
    to_state: PublicationState
    event: PublicationTransitionEvent
    actor_id: str | None = None
    reason: str = ""
    occurred_at: str | None = None

    @classmethod
    def create(
        cls,
        entry_id: str,
        from_state: PublicationState | str,
        to_state: PublicationState | str,
        event: PublicationTransitionEvent | str,
        *,
        actor_id: str | None = None,
        reason: str = "",
        occurred_at: str | None = None,
    ) -> PublicationHistoryEntry:
        """Construct a history entry after validating invariants."""
        resolved_event = (
            event
            if isinstance(event, PublicationTransitionEvent)
            else PublicationTransitionEvent(str(event).strip().lower())
        )
        return cls(
            entry_id=_require_non_empty(entry_id, "entry_id"),
            from_state=resolve_publication_state(from_state),
            to_state=resolve_publication_state(to_state),
            event=resolved_event,
            actor_id=(
                None
                if actor_id is None
                else _require_non_empty(actor_id, "actor_id")
            ),
            reason=(reason or "").strip(),
            occurred_at=(
                None
                if occurred_at is None
                else _require_non_empty(occurred_at, "occurred_at")
            ),
        )


@dataclass(frozen=True)
class PublicationHistory:
    """Ordered immutable log of publication transitions for a version."""

    history_id: str
    version_id: str
    entries: tuple[PublicationHistoryEntry, ...] = field(default_factory=tuple)

    @classmethod
    def create(
        cls,
        history_id: str,
        version_id: str,
        *,
        entries: (
            list[PublicationHistoryEntry] | tuple[PublicationHistoryEntry, ...] | None
        ) = None,
    ) -> PublicationHistory:
        """Construct PublicationHistory after validating invariants."""
        hid = _require_non_empty(history_id, "history_id")
        vid = _require_non_empty(version_id, "version_id")
        entries_t = tuple(entries or ())
        seen: set[str] = set()
        for entry in entries_t:
            if entry.entry_id in seen:
                raise ValueError(f"duplicate entry_id: {entry.entry_id!r}")
            seen.add(entry.entry_id)
        return cls(history_id=hid, version_id=vid, entries=entries_t)

    @property
    def entry_count(self) -> int:
        """Number of recorded transitions."""
        return len(self.entries)

    def with_entry(self, entry: PublicationHistoryEntry) -> PublicationHistory:
        """Return history with an appended entry."""
        if any(e.entry_id == entry.entry_id for e in self.entries):
            raise ValueError(f"duplicate entry_id: {entry.entry_id!r}")
        return PublicationHistory(
            history_id=self.history_id,
            version_id=self.version_id,
            entries=(*self.entries, entry),
        )

    def latest(self) -> PublicationHistoryEntry | None:
        """Most recent transition, or None when empty."""
        if not self.entries:
            return None
        return self.entries[-1]


def _require_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a non-empty string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized
