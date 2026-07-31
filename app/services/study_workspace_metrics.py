"""Adaptive Study Workspace metrics for Founder observability (KWP-013).

Aggregates presentation telemetry for workspace engagement, mission
completion, workspace interaction, insight usefulness, journey usage,
and forecast usage. Does not mutate Evidence, Progress, EI engines,
Memory, Twin, or Session runtime.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class StudyWorkspaceMetricsSnapshot:
    """Founder-facing Adaptive Study Workspace engagement summary."""

    workspace_opens: int = 0
    workspace_interactions: int = 0
    mission_completions: int = 0
    mission_starts: int = 0
    insight_usefulness_signals: int = 0
    journey_opens: int = 0
    forecast_views: int = 0
    unique_learners: int = 0
    engagement_rate: float = 0.0
    mission_completion_rate: float = 0.0
    journey_usage_rate: float = 0.0
    forecast_usage_rate: float = 0.0
    event_counts: dict[str, int] = field(default_factory=dict)

    def to_opaque(self) -> dict[str, Any]:
        return {
            "workspace_opens": self.workspace_opens,
            "workspace_interactions": self.workspace_interactions,
            "mission_completions": self.mission_completions,
            "mission_starts": self.mission_starts,
            "insight_usefulness_signals": self.insight_usefulness_signals,
            "journey_opens": self.journey_opens,
            "forecast_views": self.forecast_views,
            "unique_learners": self.unique_learners,
            "engagement_rate": round(self.engagement_rate, 4),
            "mission_completion_rate": round(self.mission_completion_rate, 4),
            "journey_usage_rate": round(self.journey_usage_rate, 4),
            "forecast_usage_rate": round(self.forecast_usage_rate, 4),
            "event_counts": dict(self.event_counts),
        }


class StudyWorkspaceMetrics:
    """Compute workspace analytics from presentation telemetry events."""

    WORKSPACE_OPEN_EVENTS = frozenset(
        {
            "dashboard_opened",
            "workspace_opened",
        }
    )
    INTERACTION_EVENTS = frozenset(
        {
            "workspace_interaction",
            "workspace_action",
            "coach_opened",
            "tutor_opened",
            "provenance_expanded",
        }
    )
    INSIGHT_EVENTS = frozenset(
        {
            "provenance_expanded",
            "feedback_submitted",
            "insight_useful",
        }
    )
    JOURNEY_EVENTS = frozenset(
        {
            "journey_opened",
            "learning_journey_opened",
        }
    )
    FORECAST_EVENTS = frozenset(
        {
            "forecast_viewed",
            "readiness_opened",
        }
    )

    @classmethod
    def from_event_counts(
        cls,
        counts: list[tuple[str, int]] | dict[str, int] | None = None,
        *,
        unique_learners: int = 0,
    ) -> StudyWorkspaceMetricsSnapshot:
        """Build snapshot from PresentationTelemetryService.count_by_type()."""
        if counts is None:
            event_map: dict[str, int] = {}
        elif isinstance(counts, dict):
            event_map = {str(k): int(v) for k, v in counts.items()}
        else:
            event_map = {str(k): int(v) for k, v in counts}

        def total(keys: frozenset[str]) -> int:
            return sum(event_map.get(k, 0) for k in keys)

        opens = total(cls.WORKSPACE_OPEN_EVENTS)
        interactions = total(cls.INTERACTION_EVENTS)
        completions = int(event_map.get("mission_completed", 0))
        starts = int(event_map.get("mission_started", 0))
        insights = total(cls.INSIGHT_EVENTS)
        journey = total(cls.JOURNEY_EVENTS)
        forecast = total(cls.FORECAST_EVENTS)

        learners = max(0, int(unique_learners))
        engagement = (opens / learners) if learners else (1.0 if opens else 0.0)
        # Cap engagement rate display helper at 1.0 for founder calmness.
        if learners:
            engagement = min(1.0, opens / max(learners, 1))
        else:
            engagement = 1.0 if opens else 0.0

        start_base = max(starts, completions)
        completion_rate = (
            (completions / start_base) if start_base else 0.0
        )
        journey_rate = (journey / opens) if opens else 0.0
        forecast_rate = (forecast / opens) if opens else 0.0

        return StudyWorkspaceMetricsSnapshot(
            workspace_opens=opens,
            workspace_interactions=interactions,
            mission_completions=completions,
            mission_starts=starts,
            insight_usefulness_signals=insights,
            journey_opens=journey,
            forecast_views=forecast,
            unique_learners=learners,
            engagement_rate=engagement,
            mission_completion_rate=min(1.0, completion_rate),
            journey_usage_rate=min(1.0, journey_rate),
            forecast_usage_rate=min(1.0, forecast_rate),
            event_counts=dict(event_map),
        )

    @classmethod
    def from_telemetry(cls) -> StudyWorkspaceMetricsSnapshot:
        """Load live presentation telemetry aggregates."""
        try:
            from app.models.alpha_infrastructure import PresentationEvent
            from app.services.presentation_telemetry_service import (
                PresentationTelemetryService,
            )

            counts = PresentationTelemetryService.count_by_type(limit_types=50)
            unique = 0
            try:
                from app.extensions import db

                unique = (
                    db.session.query(PresentationEvent.user_id)
                    .filter(
                        PresentationEvent.event_type.in_(
                            list(cls.WORKSPACE_OPEN_EVENTS)
                        ),
                        PresentationEvent.user_id.isnot(None),
                    )
                    .distinct()
                    .count()
                )
            except Exception:  # noqa: BLE001
                unique = 0
            return cls.from_event_counts(counts, unique_learners=unique)
        except Exception:  # noqa: BLE001
            return StudyWorkspaceMetricsSnapshot()
