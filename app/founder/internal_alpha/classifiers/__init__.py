"""Rule-based feedback classification (configurable keyword rules)."""

from __future__ import annotations

from app.founder.internal_alpha.config import (
    InternalAlphaPipelineConfig,
    default_config,
)
from app.founder.internal_alpha.models import ClassifiedFeedback, FeedbackItem


class RuleBasedClassifier:
    """Classify feedback using configurable keyword rules.

    Rules live in :class:`InternalAlphaPipelineConfig`. Categories can be
    extended by configuration alone — the classifier does not hardcode rules.
    """

    def __init__(self, config: InternalAlphaPipelineConfig | None = None) -> None:
        self._config = config or default_config()

    def classify(self, item: FeedbackItem) -> ClassifiedFeedback:
        """Classify a single feedback item.

        Args:
            item: Raw feedback observation.

        Returns:
            ClassifiedFeedback with category and confidence in ``[0, 1]``.
        """
        category, confidence = self._match(item.raw_text)
        return ClassifiedFeedback(
            feedback_item=item,
            category=category,
            confidence=confidence,
            duplicate_of=None,
        )

    def classify_many(
        self, items: tuple[FeedbackItem, ...] | list[FeedbackItem]
    ) -> tuple[ClassifiedFeedback, ...]:
        """Classify many items in stable input order."""

        return tuple(self.classify(item) for item in items)

    def _match(self, text: str) -> tuple[str, float]:
        haystack = text.casefold()
        best_category: str | None = None
        best_hits = 0
        best_keyword_count = 1

        # Preserve configured category order for deterministic tie-breaking.
        for category in self._config.categories:
            keywords = self._config.keyword_rules.get(category, ())
            if not keywords:
                continue
            hits = sum(1 for kw in keywords if kw.casefold() in haystack)
            if hits > best_hits:
                best_hits = hits
                best_category = category
                best_keyword_count = max(len(keywords), 1)

        if best_category is None or best_hits == 0:
            return self._config.default_category, 0.0

        confidence = min(1.0, best_hits / best_keyword_count)
        # Keep a readable floor when at least one keyword matches.
        confidence = max(confidence, min(1.0, 0.35 + 0.15 * (best_hits - 1)))
        return best_category, round(confidence, 4)
