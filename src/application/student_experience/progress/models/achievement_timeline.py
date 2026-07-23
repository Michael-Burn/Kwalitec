"""AchievementTimeline — chronological achievement projection."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from application.student_experience.progress.errors import JourneyInvariantViolation


@dataclass(frozen=True, slots=True)
class AchievementTimelineItem:
    """One achievement on the journey timeline."""

    achievement_id: str
    title: str
    description: str
    earned_at: datetime
    category: str = "general"

    def __post_init__(self) -> None:
        achievement_id = (self.achievement_id or "").strip()
        if not achievement_id:
            raise JourneyInvariantViolation(
                "achievement_id must be a non-empty string",
                invariant="AchievementTimelineItem.achievement_id.required",
            )
        object.__setattr__(self, "achievement_id", achievement_id)
        title = (self.title or "").strip()
        if not title:
            raise JourneyInvariantViolation(
                "title must be a non-empty string",
                invariant="AchievementTimelineItem.title.required",
            )
        object.__setattr__(self, "title", title)
        description = (self.description or "").strip()
        if not description:
            raise JourneyInvariantViolation(
                "description must be a non-empty string",
                invariant="AchievementTimelineItem.description.required",
            )
        object.__setattr__(self, "description", description)
        if not isinstance(self.earned_at, datetime):
            raise JourneyInvariantViolation(
                "earned_at must be a datetime",
                invariant="AchievementTimelineItem.earned_at.type",
            )
        category = (self.category or "").strip() or "general"
        object.__setattr__(self, "category", category)


@dataclass(frozen=True, slots=True)
class AchievementTimeline:
    """Immutable chronological achievement timeline."""

    items: tuple[AchievementTimelineItem, ...] = ()
    headline: str = "Achievements"
    has_items: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(self, "items", tuple(self.items))
        for item in self.items:
            if not isinstance(item, AchievementTimelineItem):
                raise JourneyInvariantViolation(
                    "items must contain AchievementTimelineItem values",
                    invariant="AchievementTimeline.items.type",
                )
        headline = (self.headline or "").strip()
        if not headline:
            raise JourneyInvariantViolation(
                "headline must be a non-empty string",
                invariant="AchievementTimeline.headline.required",
            )
        object.__setattr__(self, "headline", headline)
        object.__setattr__(self, "has_items", bool(self.items))
