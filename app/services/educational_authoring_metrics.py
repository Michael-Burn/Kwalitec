"""Educational Authoring metrics for Founder observability (KWP-015).

Mission / episode completion, duration, abandonment, Tomorrow Preview,
Start Tomorrow, reflection completion, and difficult / successful
episodes. Does not mutate Evidence, Progress, EI engines, Memory,
Twin, Knowledge Architecture, or Mission Runtime.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class EducationalAuthoringMetricsSnapshot:
    """Founder-facing Educational Authoring / Learning Episode summary."""

    mission_completions: int = 0
    episode_completions: int = 0
    episode_starts: int = 0
    average_episode_duration_minutes: float = 0.0
    episode_abandonments: int = 0
    tomorrow_preview_opens: int = 0
    start_tomorrow_usage: int = 0
    reflection_completions: int = 0
    most_difficult_episodes: tuple[str, ...] = ()
    most_successful_episodes: tuple[str, ...] = ()
    unique_learners: int = 0
    event_counts: dict[str, int] = field(default_factory=dict)

    def to_opaque(self) -> dict[str, Any]:
        return {
            "mission_completions": self.mission_completions,
            "episode_completions": self.episode_completions,
            "episode_starts": self.episode_starts,
            "average_episode_duration_minutes": round(
                self.average_episode_duration_minutes, 2
            ),
            "episode_abandonments": self.episode_abandonments,
            "tomorrow_preview_opens": self.tomorrow_preview_opens,
            "start_tomorrow_usage": self.start_tomorrow_usage,
            "reflection_completions": self.reflection_completions,
            "most_difficult_episodes": list(self.most_difficult_episodes),
            "most_successful_episodes": list(self.most_successful_episodes),
            "unique_learners": self.unique_learners,
            "event_counts": dict(self.event_counts),
        }


class EducationalAuthoringMetrics:
    """Aggregate Educational Authoring analytics for Platform Intelligence."""

    MISSION_COMPLETE_EVENTS = frozenset(
        {
            "mission_completed",
        }
    )
    EPISODE_COMPLETE_EVENTS = frozenset(
        {
            "episode_completed",
            "learning_episode_completed",
        }
    )
    EPISODE_START_EVENTS = frozenset(
        {
            "episode_started",
            "learning_episode_started",
        }
    )
    EPISODE_ABANDON_EVENTS = frozenset(
        {
            "episode_abandoned",
            "learning_episode_abandoned",
        }
    )
    TOMORROW_PREVIEW_EVENTS = frozenset(
        {
            "tomorrow_preview_opened",
            "tomorrow_preview_viewed",
        }
    )
    START_TOMORROW_EVENTS = frozenset(
        {
            "start_tomorrow_used",
            "start_early_used",
        }
    )
    REFLECTION_EVENTS = frozenset(
        {
            "reflection_completed",
            "episode_reflection_completed",
        }
    )

    @classmethod
    def from_event_counts(
        cls,
        counts: list[tuple[str, int]] | dict[str, int] | None = None,
        *,
        unique_learners: int = 0,
        average_episode_duration_minutes: float = 0.0,
        most_difficult_episodes: tuple[str, ...] | list[str] | None = None,
        most_successful_episodes: tuple[str, ...] | list[str] | None = None,
    ) -> EducationalAuthoringMetricsSnapshot:
        if counts is None:
            event_map: dict[str, int] = {}
        elif isinstance(counts, dict):
            event_map = {str(k): int(v) for k, v in counts.items()}
        else:
            event_map = {str(k): int(v) for k, v in counts}

        def _sum(events: frozenset[str]) -> int:
            return sum(event_map.get(e, 0) for e in events)

        return EducationalAuthoringMetricsSnapshot(
            mission_completions=_sum(cls.MISSION_COMPLETE_EVENTS),
            episode_completions=_sum(cls.EPISODE_COMPLETE_EVENTS),
            episode_starts=_sum(cls.EPISODE_START_EVENTS),
            average_episode_duration_minutes=float(
                average_episode_duration_minutes or 0.0
            ),
            episode_abandonments=_sum(cls.EPISODE_ABANDON_EVENTS),
            tomorrow_preview_opens=_sum(cls.TOMORROW_PREVIEW_EVENTS),
            start_tomorrow_usage=_sum(cls.START_TOMORROW_EVENTS),
            reflection_completions=_sum(cls.REFLECTION_EVENTS),
            most_difficult_episodes=tuple(most_difficult_episodes or ()),
            most_successful_episodes=tuple(most_successful_episodes or ()),
            unique_learners=int(unique_learners or 0),
            event_counts=event_map,
        )

    @classmethod
    def from_telemetry(cls) -> EducationalAuthoringMetricsSnapshot:
        """Build from PresentationTelemetryService when available."""
        try:
            from app.services.presentation_telemetry_service import (
                PresentationTelemetryService,
            )

            counts = PresentationTelemetryService.count_by_type()
            return cls.from_event_counts(counts)
        except Exception:  # noqa: BLE001
            return EducationalAuthoringMetricsSnapshot()
