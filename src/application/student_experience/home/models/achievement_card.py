"""AchievementCard — earned achievement projection for home."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from application.student_experience.home.errors import HomeInvariantViolation


@dataclass(frozen=True, slots=True)
class AchievementItem:
    """One earned achievement shown on the home surface."""

    achievement_id: str
    title: str
    description: str
    earned_at: datetime
    category: str = "general"

    def __post_init__(self) -> None:
        achievement_id = (self.achievement_id or "").strip()
        if not achievement_id:
            raise HomeInvariantViolation(
                "achievement_id must be a non-empty string",
                invariant="AchievementItem.achievement_id.required",
            )
        object.__setattr__(self, "achievement_id", achievement_id)
        title = (self.title or "").strip()
        if not title:
            raise HomeInvariantViolation(
                "title must be a non-empty string",
                invariant="AchievementItem.title.required",
            )
        object.__setattr__(self, "title", title)
        object.__setattr__(self, "description", (self.description or "").strip())
        if not isinstance(self.earned_at, datetime):
            raise HomeInvariantViolation(
                "earned_at must be a datetime",
                invariant="AchievementItem.earned_at.type",
            )
        object.__setattr__(
            self, "category", (self.category or "").strip() or "general"
        )


@dataclass(frozen=True, slots=True)
class AchievementCard:
    """Immutable achievement card — recent earned achievements."""

    items: tuple[AchievementItem, ...] = ()
    headline: str = "Recent achievements"
    has_achievements: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(self, "items", tuple(self.items))
        for item in self.items:
            if not isinstance(item, AchievementItem):
                raise HomeInvariantViolation(
                    "items must contain AchievementItem values",
                    invariant="AchievementCard.items.type",
                )
        headline = (self.headline or "").strip()
        if not headline:
            raise HomeInvariantViolation(
                "headline must be a non-empty string",
                invariant="AchievementCard.headline.required",
            )
        object.__setattr__(self, "headline", headline)
        object.__setattr__(self, "has_achievements", bool(self.items))
