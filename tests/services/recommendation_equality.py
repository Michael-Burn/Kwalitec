"""Semantic equality helpers for recommendation list comparisons.

``generated_at`` is a time-of-generation stamp (second-truncated UTC), not
recommendation content. Full-list ``==`` flakes when two
``generate_recommendations`` calls straddle a second boundary.
"""

from __future__ import annotations

from typing import Any


def recommendation_rows_without_generated_at(
    rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Return shallow copies of recommendation rows without ``generated_at``."""
    cleaned: list[dict[str, Any]] = []
    for row in rows:
        item = dict(row)
        item.pop("generated_at", None)
        cleaned.append(item)
    return cleaned


def assert_recommendations_content_equal(
    left: list[dict[str, Any]],
    right: list[dict[str, Any]],
) -> None:
    """Assert recommendation lists match on content, ignoring ``generated_at``."""
    assert recommendation_rows_without_generated_at(left) == (
        recommendation_rows_without_generated_at(right)
    )
