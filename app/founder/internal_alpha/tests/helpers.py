"""Test helpers for Internal Alpha pipeline unit tests."""

from __future__ import annotations

from datetime import UTC, datetime

from app.founder.internal_alpha.models import FeedbackItem


def make_item(
    *,
    item_id: str = "abc123",
    filename: str = "alice.txt",
    contributor: str = "alice",
    week: str = "2026-W28",
    raw_text: str = "hello",
    created_at: datetime | None = None,
) -> FeedbackItem:
    return FeedbackItem(
        id=item_id,
        filename=filename,
        contributor=contributor,
        week=week,
        raw_text=raw_text,
        created_at=created_at or datetime(2026, 7, 14, 12, 0, tzinfo=UTC),
    )
