"""AchievementProvider — earned achievements for the home surface."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class HomeAchievement:
    """Immutable achievement projection for the home surface."""

    achievement_id: str
    title: str
    description: str
    earned_at: datetime
    category: str = "general"


class AchievementProvider(ABC):
    """Outbound port for student achievements.

    Implementations live in infrastructure. Never estimates mastery or
    invents educational awards from raw evidence.
    """

    @abstractmethod
    def list_achievements(
        self, student_id: str, *, limit: int = 3
    ) -> tuple[HomeAchievement, ...]:
        """Return recent achievements for ``student_id``."""
