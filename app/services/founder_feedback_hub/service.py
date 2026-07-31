"""Founder Feedback Hub — read-only multi-source aggregation (FH-001).

Aggregates Private Beta, Alpha, and Research (Product Check-in) feedback into
one normalized collection without merging tables, dual-writing, or changing
student submission flows.
"""

from __future__ import annotations

from app.services.founder_feedback_hub.adapters import (
    DEFAULT_ADAPTERS,
    FeedbackSourceAdapter,
    apply_hub_filters,
    count_by_source,
    sort_newest_first,
)
from app.services.founder_feedback_hub.dto import (
    SOURCE_ALPHA,
    SOURCE_LABELS,
    SOURCE_PRIVATE_BETA,
    SOURCE_RESEARCH,
    FounderFeedbackItem,
    HubFilters,
    HubPage,
)

DEFAULT_PER_PAGE = 25
MAX_PER_PAGE = 100


class FounderFeedbackHubService:
    """Load, normalize, filter, sort, and paginate Founder feedback."""

    def __init__(
        self,
        adapters: tuple[FeedbackSourceAdapter, ...] | None = None,
    ) -> None:
        self._adapters = adapters or DEFAULT_ADAPTERS

    def list_items(
        self,
        filters: HubFilters | None = None,
        *,
        page: int = 1,
        per_page: int = DEFAULT_PER_PAGE,
    ) -> HubPage:
        """Return a paginated Hub page (newest first).

        Args:
            filters: Optional Hub filters.
            page: 1-based page index.
            per_page: Page size (clamped to ``MAX_PER_PAGE``).

        Returns:
            ``HubPage`` of ``FounderFeedbackItem`` DTOs (never ORM entities).
        """
        filters = filters or HubFilters()
        page = max(1, int(page or 1))
        per_page = max(1, min(int(per_page or DEFAULT_PER_PAGE), MAX_PER_PAGE))

        collected: list[FounderFeedbackItem] = []
        for adapter in self._adapters:
            collected.extend(adapter.load(filters))

        # Unfiltered source counts for Hub chrome (before source filter).
        if filters.source:
            all_for_counts: list[FounderFeedbackItem] = []
            count_filters = HubFilters(
                severity=filters.severity,
                status=filters.status,
                subject=filters.subject,
                date_from=filters.date_from,
                date_to=filters.date_to,
                student=filters.student,
                keyword=filters.keyword,
            )
            for adapter in self._adapters:
                all_for_counts.extend(adapter.load(count_filters))
            all_for_counts = apply_hub_filters(all_for_counts, count_filters)
            source_counts = count_by_source(all_for_counts)
        else:
            filtered_pre = apply_hub_filters(collected, filters)
            source_counts = count_by_source(filtered_pre)

        filtered = apply_hub_filters(collected, filters)
        ordered = sort_newest_first(filtered)
        total = len(ordered)
        offset = (page - 1) * per_page
        page_items = tuple(ordered[offset : offset + per_page])

        return HubPage(
            items=page_items,
            page=page,
            per_page=per_page,
            total=total,
            filters=filters,
            source_counts=source_counts,
        )

    @staticmethod
    def source_options() -> tuple[tuple[str, str], ...]:
        """Filter dropdown choices (value, label)."""
        return (
            ("", "All"),
            (SOURCE_PRIVATE_BETA, SOURCE_LABELS[SOURCE_PRIVATE_BETA]),
            (SOURCE_ALPHA, SOURCE_LABELS[SOURCE_ALPHA]),
            (SOURCE_RESEARCH, SOURCE_LABELS[SOURCE_RESEARCH]),
        )
