"""GetRecommendations query — recommendation presentation section."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class GetRecommendations:
    """Request a recommendation read model when packaging inputs exist."""

    student_id: str
    episode_id: str | None = None
