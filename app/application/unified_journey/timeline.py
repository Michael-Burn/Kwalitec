"""Experience Timeline — today's journey presentation aid (P2-MS003).

Lightweight model of Mission → Study Session → Reflection → Complete.
Presentation only. Never owns educational authority.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from app.application.unified_journey.contracts import (
    COMPLETION_COMPLETE,
    COMPLETION_IN_PROGRESS,
    COMPLETION_NOT_STARTED,
    COMPLETION_UNKNOWN,
    CONTRACT_VERSION,
    JourneyContext,
)
from app.application.unified_journey.daily_mission import DailyMission
from app.application.unified_journey.stages import JourneyStage, resolve_journey_stage

TIMELINE_STATUS_PENDING = "pending"
TIMELINE_STATUS_CURRENT = "current"
TIMELINE_STATUS_COMPLETE = "complete"
TIMELINE_STATUS_VALUES = frozenset(
    {
        TIMELINE_STATUS_PENDING,
        TIMELINE_STATUS_CURRENT,
        TIMELINE_STATUS_COMPLETE,
    }
)

# Canonical today's-journey steps (presentation aid only).
_TODAY_STEPS: tuple[tuple[str, str, JourneyStage | None], ...] = (
    ("mission", "Mission", JourneyStage.DAILY_MISSION),
    ("study_session", "Study Session", JourneyStage.STUDY_SESSION),
    ("reflection", "Reflection", JourneyStage.SESSION_REFLECTION),
    ("complete", "Complete", None),
)


@dataclass(frozen=True)
class TimelineStep:
    """One step on today's Experience timeline."""

    key: str
    label: str
    status: str = TIMELINE_STATUS_PENDING
    stage: JourneyStage | None = None

    def __post_init__(self) -> None:
        status = (self.status or "").strip().lower()
        if status not in TIMELINE_STATUS_VALUES:
            raise ValueError(f"unknown timeline step status: {self.status!r}")
        object.__setattr__(self, "status", status)
        object.__setattr__(self, "key", (self.key or "").strip())
        object.__setattr__(self, "label", (self.label or "").strip())
        if self.stage is not None:
            object.__setattr__(self, "stage", resolve_journey_stage(self.stage))

    @property
    def is_current(self) -> bool:
        return self.status == TIMELINE_STATUS_CURRENT

    @property
    def is_complete(self) -> bool:
        return self.status == TIMELINE_STATUS_COMPLETE


@dataclass(frozen=True)
class ExperienceTimeline:
    """Today's journey timeline — Mission ↓ Study Session ↓ Reflection ↓ Complete."""

    steps: tuple[TimelineStep, ...] = ()
    active_index: int = 0
    contract_version: str = CONTRACT_VERSION
    metadata: tuple[tuple[str, str], ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        steps = tuple(self.steps or ())
        object.__setattr__(self, "steps", steps)
        if not steps:
            object.__setattr__(self, "active_index", 0)
            return
        index = int(self.active_index)
        if index < 0 or index >= len(steps):
            for i, step in enumerate(steps):
                if step.status == TIMELINE_STATUS_CURRENT:
                    object.__setattr__(self, "active_index", i)
                    return
            object.__setattr__(
                self, "active_index", max(0, min(index, len(steps) - 1))
            )
            return
        object.__setattr__(self, "active_index", index)

    @property
    def active_step(self) -> TimelineStep | None:
        if not self.steps:
            return None
        return self.steps[self.active_index]


def build_experience_timeline(
    *,
    completion_status: str = COMPLETION_UNKNOWN,
    stage: JourneyStage | str | None = None,
) -> ExperienceTimeline:
    """Build today's Experience timeline from presentation completion / stage.

    Does not consult educational engines. Completion drives step highlighting.
    """
    status = (completion_status or "").strip().lower()
    resolved_stage = (
        resolve_journey_stage(stage) if stage is not None else None
    )
    active = _active_step_index(status=status, stage=resolved_stage)
    steps: list[TimelineStep] = []
    for index, (key, label, step_stage) in enumerate(_TODAY_STEPS):
        if index < active:
            step_status = TIMELINE_STATUS_COMPLETE
        elif index == active:
            step_status = TIMELINE_STATUS_CURRENT
        else:
            step_status = TIMELINE_STATUS_PENDING
        if status == COMPLETION_COMPLETE and key == "complete":
            step_status = TIMELINE_STATUS_COMPLETE
        steps.append(
            TimelineStep(
                key=key,
                label=label,
                status=step_status,
                stage=step_stage,
            )
        )
    if status == COMPLETION_COMPLETE:
        active = len(steps) - 1
    else:
        for i, step in enumerate(steps):
            if step.status == TIMELINE_STATUS_CURRENT:
                active = i
                break
    return ExperienceTimeline(
        steps=tuple(steps),
        active_index=active,
        metadata=(
            ("completion_status", status),
            ("via", "experience_timeline"),
        ),
    )


def timeline_from_daily_mission(mission: DailyMission) -> ExperienceTimeline:
    """Project ExperienceTimeline from a DailyMission (presentation only)."""
    return build_experience_timeline(
        completion_status=mission.completion_status,
        stage=mission.stage,
    )


def timeline_with_reflection(mission: DailyMission) -> ExperienceTimeline:
    """Today's timeline with Reflection as the current step (presentation only).

    Used after session completion while Guided Reflection is Available or
    In Progress — before the day completion state is shown.
    """
    steps: list[TimelineStep] = []
    for index, (key, label, step_stage) in enumerate(_TODAY_STEPS):
        if index < 2:
            step_status = TIMELINE_STATUS_COMPLETE
        elif index == 2:
            step_status = TIMELINE_STATUS_CURRENT
        else:
            step_status = TIMELINE_STATUS_PENDING
        steps.append(
            TimelineStep(
                key=key,
                label=label,
                status=step_status,
                stage=step_stage,
            )
        )
    return ExperienceTimeline(
        steps=tuple(steps),
        active_index=2,
        metadata=(
            ("completion_status", mission.completion_status),
            ("via", "timeline_with_reflection"),
        ),
    )


def timeline_from_journey_context(context: JourneyContext) -> ExperienceTimeline:
    """Project ExperienceTimeline from JourneyContext (presentation only)."""
    completion = context.completion_state or COMPLETION_UNKNOWN
    if (
        completion == COMPLETION_UNKNOWN
        and context.availability == "available"
        and context.mission_title
    ):
        completion = COMPLETION_NOT_STARTED
    return build_experience_timeline(
        completion_status=completion,
        stage=context.stage,
    )


def empty_experience_timeline() -> ExperienceTimeline:
    """Default today's timeline with Mission as the current step."""
    return build_experience_timeline(completion_status=COMPLETION_NOT_STARTED)


def _active_step_index(
    *,
    status: str,
    stage: JourneyStage | None,
) -> int:
    """Resolve which timeline step is current from UI completion / stage."""
    if status == COMPLETION_COMPLETE:
        return 3  # Complete
    if status == COMPLETION_IN_PROGRESS:
        return 1  # Study Session
    if status in {COMPLETION_NOT_STARTED, COMPLETION_UNKNOWN, ""}:
        if stage is JourneyStage.STUDY_SESSION:
            return 1
        if stage is JourneyStage.SESSION_REFLECTION:
            return 2
        if stage is JourneyStage.WEEKLY_REVIEW:
            return 2
        return 0  # Mission
    if stage is JourneyStage.STUDY_SESSION:
        return 1
    if stage is JourneyStage.SESSION_REFLECTION:
        return 2
    return 0
