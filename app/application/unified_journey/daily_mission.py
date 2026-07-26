"""Immutable DailyMission presentation DTO (P2-MS003).

Experience Layer only. Derived entirely from ``JourneyContext``.
Distinct from Mission Engine ``DailyMission`` educational artefacts.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from app.application.unified_journey.contracts import (
    COMPLETION_COMPLETE,
    COMPLETION_IN_PROGRESS,
    COMPLETION_NOT_STARTED,
    COMPLETION_UNKNOWN,
    COMPLETION_VALUES,
    CONTRACT_VERSION,
    URGENCY_HIGH,
    URGENCY_LOW,
    URGENCY_NONE,
    URGENCY_NORMAL,
    URGENCY_VALUES,
)
from app.application.unified_journey.stages import (
    JourneyStage,
    resolve_journey_stage,
)

# Presentation priority vocabulary (maps from JourneyContext.urgency).
PRIORITY_NONE = ""
PRIORITY_LOW = "low"
PRIORITY_NORMAL = "normal"
PRIORITY_HIGH = "high"
PRIORITY_VALUES = frozenset(
    {
        PRIORITY_NONE,
        PRIORITY_LOW,
        PRIORITY_NORMAL,
        PRIORITY_HIGH,
    }
)

COMPLETION_STATUS_LABELS: dict[str, str] = {
    COMPLETION_UNKNOWN: "",
    COMPLETION_NOT_STARTED: "Not Started",
    COMPLETION_IN_PROGRESS: "In Progress",
    COMPLETION_COMPLETE: "Completed",
}


@dataclass(frozen=True)
class MissionStartAction:
    """Presentation CTA for starting or continuing today's mission."""

    label: str = "Start Today's Mission"
    enabled: bool = False
    endpoint: str = ""


@dataclass(frozen=True)
class DailyMission:
    """Canonical Home presentation model for today's mission.

    Presentation-only. Assembled from ``JourneyContext``. Never invents
    educational recommendations or modifies Programme I outputs.

    Distinct from ``app.application.mission_engine.dto.daily_mission.DailyMission``.
    """

    title: str = ""
    reason: str = ""
    estimated_duration: str = ""
    expected_outcome: str = ""
    priority: str = PRIORITY_NONE
    completion_status: str = COMPLETION_UNKNOWN
    start_action: MissionStartAction = field(default_factory=MissionStartAction)
    mission_summary: str = ""
    stage: JourneyStage = JourneyStage.DAILY_MISSION
    contract_version: str = CONTRACT_VERSION
    metadata: tuple[tuple[str, str], ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        object.__setattr__(self, "stage", resolve_journey_stage(self.stage))
        priority = (self.priority or "").strip().lower()
        if priority not in PRIORITY_VALUES:
            raise ValueError(f"unknown daily mission priority: {self.priority!r}")
        object.__setattr__(self, "priority", priority)
        completion = (self.completion_status or "").strip().lower()
        if completion not in COMPLETION_VALUES:
            raise ValueError(
                f"unknown daily mission completion_status: "
                f"{self.completion_status!r}"
            )
        object.__setattr__(self, "completion_status", completion)
        if not isinstance(self.start_action, MissionStartAction):
            raise TypeError("start_action must be a MissionStartAction")

    @property
    def completion_status_label(self) -> str:
        """Student-facing completion label (UI state only)."""
        return COMPLETION_STATUS_LABELS.get(self.completion_status, "")

    @property
    def is_not_started(self) -> bool:
        return self.completion_status in {
            COMPLETION_UNKNOWN,
            COMPLETION_NOT_STARTED,
            "",
        }

    @property
    def is_in_progress(self) -> bool:
        return self.completion_status == COMPLETION_IN_PROGRESS

    @property
    def is_completed(self) -> bool:
        return self.completion_status == COMPLETION_COMPLETE


def priority_from_urgency(urgency: str) -> str:
    """Map JourneyContext urgency onto presentation priority (pass-through)."""
    value = (urgency or "").strip().lower()
    if value not in URGENCY_VALUES or value == URGENCY_NONE:
        return PRIORITY_NONE
    if value == URGENCY_HIGH:
        return PRIORITY_HIGH
    if value == URGENCY_LOW:
        return PRIORITY_LOW
    if value == URGENCY_NORMAL:
        return PRIORITY_NORMAL
    return PRIORITY_NONE


def empty_daily_mission() -> DailyMission:
    """Placeholder DailyMission when JourneyContext is unavailable."""
    return DailyMission(
        title="Today's Mission",
        reason="",
        estimated_duration="",
        expected_outcome="",
        priority=PRIORITY_NONE,
        completion_status=COMPLETION_UNKNOWN,
        start_action=MissionStartAction(
            label="Continue",
            enabled=False,
            endpoint="",
        ),
        mission_summary="",
        stage=JourneyStage.DAILY_MISSION,
        metadata=(("availability", "placeholder"),),
    )
