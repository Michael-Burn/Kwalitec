"""Release notes — educational change captions for a subject version."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ReleaseNoteEntry:
    """Single educational change caption."""

    entry_id: str
    text: str
    category: str = "general"

    @classmethod
    def create(
        cls,
        entry_id: str,
        text: str,
        *,
        category: str = "general",
    ) -> ReleaseNoteEntry:
        """Construct a ReleaseNoteEntry after validating invariants."""
        return cls(
            entry_id=_require_non_empty(entry_id, "entry_id"),
            text=_require_non_empty(text, "text"),
            category=_require_non_empty(category, "category"),
        )


@dataclass(frozen=True)
class ReleaseNotes:
    """Educational change log for a subject version.

    Examples: prerequisite links, blueprint assignment updates, session estimates.
    """

    notes_id: str
    version_id: str
    entries: tuple[ReleaseNoteEntry, ...] = field(default_factory=tuple)
    headline: str = ""

    @classmethod
    def create(
        cls,
        notes_id: str,
        version_id: str,
        *,
        entries: list[ReleaseNoteEntry] | tuple[ReleaseNoteEntry, ...] | None = None,
        headline: str = "",
    ) -> ReleaseNotes:
        """Construct ReleaseNotes after validating invariants."""
        nid = _require_non_empty(notes_id, "notes_id")
        vid = _require_non_empty(version_id, "version_id")
        entries_t = tuple(entries or ())
        seen: set[str] = set()
        for entry in entries_t:
            if entry.entry_id in seen:
                raise ValueError(f"duplicate entry_id: {entry.entry_id!r}")
            seen.add(entry.entry_id)
        return cls(
            notes_id=nid,
            version_id=vid,
            entries=entries_t,
            headline=(headline or "").strip(),
        )

    @property
    def entry_count(self) -> int:
        """Number of change captions."""
        return len(self.entries)

    def with_entry(self, entry: ReleaseNoteEntry) -> ReleaseNotes:
        """Return notes with an appended entry."""
        if any(e.entry_id == entry.entry_id for e in self.entries):
            raise ValueError(f"duplicate entry_id: {entry.entry_id!r}")
        return ReleaseNotes(
            notes_id=self.notes_id,
            version_id=self.version_id,
            entries=(*self.entries, entry),
            headline=self.headline,
        )

    def texts(self) -> tuple[str, ...]:
        """Ordered entry texts."""
        return tuple(e.text for e in self.entries)


def _require_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a non-empty string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized
