"""Unit tests for WeeklyAggregator."""

from __future__ import annotations

from datetime import UTC, datetime

from app.founder.internal_alpha.aggregators import WeeklyAggregator
from app.founder.internal_alpha.classifiers import RuleBasedClassifier
from app.founder.internal_alpha.dto import DuplicateRelation
from app.founder.internal_alpha.tests.helpers import make_item


class TestWeeklyAggregator:
    def test_counts_categories_and_contributors(self) -> None:
        items = (
            make_item(
                item_id="1",
                contributor="alice",
                raw_text="architecture layering problem",
            ),
            make_item(
                item_id="2",
                contributor="bob",
                filename="bob.txt",
                raw_text="bug crash exception",
            ),
            make_item(
                item_id="3",
                contributor="alice",
                filename="alice2.txt",
                raw_text="completely unrelated text",
            ),
        )
        classified = RuleBasedClassifier().classify_many(items)
        duplicates = (
            DuplicateRelation(
                source_id="3",
                target_id="1",
                reason="identical",
                similarity=1.0,
            ),
        )
        stamp = datetime(2026, 7, 14, 15, 0, tzinfo=UTC)
        summary = WeeklyAggregator().aggregate(
            classified,
            duplicates,
            week="2026-W28",
            generated_at=stamp,
        )
        assert summary.week == "2026-W28"
        assert summary.total_feedback == 3
        assert summary.duplicate_count == 1
        assert summary.category_counts["Architecture"] >= 1
        assert summary.category_counts["Bug"] >= 1
        assert summary.contributor_counts["alice"] == 2
        assert summary.contributor_counts["bob"] == 1
        assert summary.generated_at == stamp
        # All configured categories present (zero-filled).
        assert "UX" in summary.category_counts
