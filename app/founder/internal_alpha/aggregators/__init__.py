"""Weekly aggregation of classified Internal Alpha feedback."""

from __future__ import annotations

from collections import Counter
from datetime import UTC, datetime
from types import MappingProxyType

from app.founder.internal_alpha.config import (
    InternalAlphaPipelineConfig,
    default_config,
)
from app.founder.internal_alpha.dto import DuplicateRelation
from app.founder.internal_alpha.models import ClassifiedFeedback, WeeklySummary


class WeeklyAggregator:
    """Produce category, duplicate, contributor, and total counts.

    No report generation — statistics only.
    """

    def __init__(self, config: InternalAlphaPipelineConfig | None = None) -> None:
        self._config = config or default_config()

    def aggregate(
        self,
        classified: tuple[ClassifiedFeedback, ...] | list[ClassifiedFeedback],
        duplicates: tuple[DuplicateRelation, ...] | list[DuplicateRelation],
        *,
        week: str,
        generated_at: datetime | None = None,
    ) -> WeeklySummary:
        """Aggregate observations for one week.

        Args:
            classified: Classified feedback items.
            duplicates: Detected duplicate relationships.
            week: Week label.
            generated_at: Optional timestamp; defaults to UTC now.

        Returns:
            WeeklySummary with category, duplicate, and contributor counts.
        """
        category_counter: Counter[str] = Counter()
        for category in self._config.categories:
            category_counter[category] = 0
        for item in classified:
            category_counter[item.category] += 1

        contributor_counter: Counter[str] = Counter(
            item.feedback_item.contributor for item in classified
        )

        stamp = generated_at if generated_at is not None else datetime.now(tz=UTC)
        return WeeklySummary(
            week=week,
            total_feedback=len(classified),
            category_counts=MappingProxyType(dict(category_counter)),
            duplicate_count=len(duplicates),
            generated_at=stamp,
            contributor_counts=MappingProxyType(dict(contributor_counter)),
        )
