"""Base type for application-layer events."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime


@dataclass(frozen=True, slots=True)
class ApplicationEvent:
    """Immutable application coordination event.

    Distinct from domain events raised inside aggregates. Application events
    communicate workflow outcomes across the application boundary.
    """

    occurred_at: datetime

    def __post_init__(self) -> None:
        if self.occurred_at.tzinfo is None:
            stamped = self.occurred_at.replace(tzinfo=UTC)
            object.__setattr__(self, "occurred_at", stamped)


def utc_now() -> datetime:
    """Return a timezone-aware UTC timestamp for application events."""
    return datetime.now(tz=UTC)
