"""RecommendationProjectionBuilder — map presentation inputs to a read model.

Forwards already-decided packaging. Does not select actions, score readiness,
or interpret educational meaning.
"""

from __future__ import annotations

from application.read_models.recommendations.recommendation_read_model import (
    RecommendationReadModel,
)


class RecommendationProjectionBuilder:
    """Build ``RecommendationReadModel`` from presentation-safe fields."""

    @staticmethod
    def build(
        *,
        title: str,
        subtitle: str | None = None,
        primary_action: str | None = None,
        reason_summary: str | None = None,
        estimated_minutes: int | None = None,
        can_start: bool = False,
        decision_id: str | None = None,
        recommendation_id: str | None = None,
    ) -> RecommendationReadModel:
        """Project recommendation presentation fields into an immutable read model."""
        return RecommendationReadModel(
            title=title.strip(),
            subtitle=_optional_text(subtitle),
            primary_action=_optional_text(primary_action),
            reason_summary=_optional_text(reason_summary),
            estimated_minutes=estimated_minutes,
            can_start=can_start,
            decision_id=_optional_text(decision_id),
            recommendation_id=_optional_text(recommendation_id),
        )


def _optional_text(value: str | None) -> str | None:
    if value is None:
        return None
    cleaned = value.strip()
    return cleaned or None
