"""GetTeachingPlan query."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class GetTeachingPlan:
    """Load a teaching plan projection from a Learning Episode."""

    episode_id: str
