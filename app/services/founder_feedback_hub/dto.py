"""Unified read model for the Founder Feedback Hub (FH-001).

ORM entities are never exposed — adapters normalize source rows into this DTO.
Missing fields are ``None``; they are never fabricated.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Any

SOURCE_PRIVATE_BETA = "private_beta"
SOURCE_ALPHA = "alpha"
SOURCE_RESEARCH = "research"

SOURCE_LABELS: dict[str, str] = {
    SOURCE_PRIVATE_BETA: "PRIVATE BETA",
    SOURCE_ALPHA: "ALPHA",
    SOURCE_RESEARCH: "PRODUCT CHECK-IN",
}

ORIGIN_COLOURS: dict[str, str] = {
    SOURCE_PRIVATE_BETA: "blue",
    SOURCE_ALPHA: "purple",
    SOURCE_RESEARCH: "green",
}

ORIGIN_ICONS: dict[str, str] = {
    SOURCE_PRIVATE_BETA: "beta",
    SOURCE_ALPHA: "alpha",
    SOURCE_RESEARCH: "checkin",
}


@dataclass(frozen=True)
class FounderFeedbackItem:
    """Normalized Founder-facing feedback row (read-only)."""

    id: str
    source: str
    source_label: str
    student: str | None
    student_email: str | None
    subject: str | None
    category: str | None
    severity: str | None
    status: str | None
    message: str | None
    summary: str | None
    created_at: datetime | None
    updated_at: datetime | None
    link_to_original: str
    origin_icon: str
    origin_colour: str
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def native_id(self) -> int | None:
        raw = self.metadata.get("native_id")
        return int(raw) if raw is not None else None


@dataclass(frozen=True)
class HubFilters:
    """Optional Hub list filters (all applied in-process after adapters load)."""

    source: str | None = None
    severity: str | None = None
    status: str | None = None
    subject: str | None = None
    date_from: date | None = None
    date_to: date | None = None
    student: str | None = None
    keyword: str | None = None


@dataclass(frozen=True)
class HubPage:
    """Paginated Hub collection."""

    items: tuple[FounderFeedbackItem, ...]
    page: int
    per_page: int
    total: int
    filters: HubFilters
    source_counts: dict[str, int]

    @property
    def total_pages(self) -> int:
        if self.per_page <= 0:
            return 1
        return max(1, (self.total + self.per_page - 1) // self.per_page)

    @property
    def has_prev(self) -> bool:
        return self.page > 1

    @property
    def has_next(self) -> bool:
        return self.page < self.total_pages
