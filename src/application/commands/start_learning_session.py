"""StartLearningSession command."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class StartLearningSession:
    """Start an existing planned learning episode as a learning session.

    Educational content of the episode must already exist (domain-authored).
    Application only loads, invokes ``start``, commits, and publishes.
    """

    episode_id: str
