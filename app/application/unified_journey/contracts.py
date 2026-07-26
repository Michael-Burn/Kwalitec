"""Immutable Unified Student Journey contracts (P2-MS001 / P2-MS002).

Experience Layer DTOs only. No persistence. No educational calculations.
Distinct from ``app.domain.learning_journey`` educational JourneyState.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any

from app.application.unified_journey.stages import (
    JourneyStage,
    resolve_journey_stage,
)

# Availability / provenance vocabulary (orchestration only).
AVAILABILITY_AVAILABLE = "available"
AVAILABILITY_UNAVAILABLE = "unavailable"
AVAILABILITY_PLACEHOLDER = "placeholder"
AVAILABILITY_VALUES = frozenset(
    {
        AVAILABILITY_AVAILABLE,
        AVAILABILITY_UNAVAILABLE,
        AVAILABILITY_PLACEHOLDER,
        "",
    }
)

SOURCE_RUNTIME_A = "runtime_a"
SOURCE_DIGITAL_TWIN = "digital_twin"
SOURCE_ADAPTIVE = "adaptive"
SOURCE_STRATEGY = "strategy"
SOURCE_EVIDENCE = "evidence"
SOURCE_EXPERIENCE = "experience"
SOURCE_PLACEHOLDER = "placeholder"

ACTION_SOURCES = frozenset(
    {
        SOURCE_RUNTIME_A,
        SOURCE_DIGITAL_TWIN,
        SOURCE_ADAPTIVE,
        SOURCE_STRATEGY,
        SOURCE_EVIDENCE,
        SOURCE_EXPERIENCE,
        SOURCE_PLACEHOLDER,
        "",
    }
)

CONTRACT_VERSION = "p2.ms005.1"

# Presentation completion / urgency vocabularies (pass-through only).
COMPLETION_UNKNOWN = ""
COMPLETION_NOT_STARTED = "not_started"
COMPLETION_IN_PROGRESS = "in_progress"
COMPLETION_COMPLETE = "complete"
COMPLETION_VALUES = frozenset(
    {
        COMPLETION_UNKNOWN,
        COMPLETION_NOT_STARTED,
        COMPLETION_IN_PROGRESS,
        COMPLETION_COMPLETE,
    }
)

URGENCY_NONE = ""
URGENCY_LOW = "low"
URGENCY_NORMAL = "normal"
URGENCY_HIGH = "high"
URGENCY_VALUES = frozenset(
    {
        URGENCY_NONE,
        URGENCY_LOW,
        URGENCY_NORMAL,
        URGENCY_HIGH,
    }
)


def _freeze_mapping(
    value: Mapping[str, Any] | None,
) -> Mapping[str, Any]:
    if value is None:
        return MappingProxyType({})
    return MappingProxyType(dict(value))


@dataclass(frozen=True)
class NextBestAction:
    """Next recommended Experience action — pass-through, not a decision.

    Populated from subsystem projections or placeholders. The Journey
    Coordinator never invents educational recommendations.
    """

    action_id: str = ""
    stage: JourneyStage = JourneyStage.DAILY_MISSION
    title: str = ""
    summary: str = ""
    cta_label: str = ""
    endpoint: str = ""
    estimated_minutes: int | None = None
    why_it_matters: str = ""
    expected_outcome: str = ""
    source: str = SOURCE_PLACEHOLDER
    availability: str = AVAILABILITY_PLACEHOLDER
    unavailable_reason: str = ""
    metadata: tuple[tuple[str, str], ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        object.__setattr__(self, "stage", resolve_journey_stage(self.stage))
        source = (self.source or "").strip().lower()
        if source not in ACTION_SOURCES:
            raise ValueError(f"unknown next-action source: {self.source!r}")
        object.__setattr__(self, "source", source)
        availability = (self.availability or "").strip().lower()
        if availability not in AVAILABILITY_VALUES:
            raise ValueError(
                f"unknown next-action availability: {self.availability!r}"
            )
        object.__setattr__(self, "availability", availability)


@dataclass(frozen=True)
class JourneyProgress:
    """Presentation progress along the unified journey — no mastery math."""

    current_stage: JourneyStage = JourneyStage.DAILY_MISSION
    stages_completed: tuple[JourneyStage, ...] = ()
    stages_remaining: tuple[JourneyStage, ...] = ()
    label: str = ""
    ratio: float | None = None
    availability: str = AVAILABILITY_PLACEHOLDER
    metadata: tuple[tuple[str, str], ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "current_stage", resolve_journey_stage(self.current_stage)
        )
        completed = tuple(
            resolve_journey_stage(stage) for stage in self.stages_completed
        )
        remaining = tuple(
            resolve_journey_stage(stage) for stage in self.stages_remaining
        )
        object.__setattr__(self, "stages_completed", completed)
        object.__setattr__(self, "stages_remaining", remaining)
        availability = (self.availability or "").strip().lower()
        if availability not in AVAILABILITY_VALUES:
            raise ValueError(
                f"unknown journey progress availability: {self.availability!r}"
            )
        object.__setattr__(self, "availability", availability)
        if self.ratio is not None:
            ratio = float(self.ratio)
            if ratio < 0.0 or ratio > 1.0:
                raise ValueError("journey progress ratio must be in [0, 1]")
            object.__setattr__(self, "ratio", ratio)


@dataclass(frozen=True)
class JourneyState:
    """Immutable Experience Layer journey state for one student.

    Orchestration snapshot only. Does not persist. Does not own educational
    truth. Distinct from Learning Journey domain ``JourneyState``.
    """

    student_id: str
    current_stage: JourneyStage = JourneyStage.DAILY_MISSION
    next_action: NextBestAction | None = None
    progress: JourneyProgress | None = None
    contract_version: str = CONTRACT_VERSION
    availability: str = AVAILABILITY_PLACEHOLDER
    unavailable_reason: str = ""
    metadata: tuple[tuple[str, str], ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        sid = (self.student_id or "").strip()
        if not sid:
            raise ValueError("student_id must be a non-empty string")
        object.__setattr__(self, "student_id", sid)
        object.__setattr__(
            self, "current_stage", resolve_journey_stage(self.current_stage)
        )
        availability = (self.availability or "").strip().lower()
        if availability not in AVAILABILITY_VALUES:
            raise ValueError(
                f"unknown journey state availability: {self.availability!r}"
            )
        object.__setattr__(self, "availability", availability)


@dataclass(frozen=True)
class JourneyContext:
    """Presentation-ready state for the active journey stage (P2-MS002).

    Canonical Experience presentation object. Assembled from existing
    Programme I subsystem outputs. Contains no educational calculations.
    Distinct from coach ``JourneyContext`` in ``src.application...coach``.

    EP-006.2: carries authored MES slots (evidence, confidence, next action,
    review point, plan drivers) for progressive disclosure on Home/Mission.
    """

    stage: JourneyStage = JourneyStage.DAILY_MISSION
    mission_title: str = ""
    mission_reason: str = ""
    estimated_duration: str = ""
    expected_outcome: str = ""
    completion_state: str = COMPLETION_UNKNOWN
    urgency: str = URGENCY_NONE
    next_transition: str = ""
    supporting_insights: tuple[str, ...] = ()
    cta_label: str = "Continue"
    cta_enabled: bool = False
    endpoint: str = ""
    estimated_minutes: int | None = None
    source: str = SOURCE_PLACEHOLDER
    availability: str = AVAILABILITY_PLACEHOLDER
    unavailable_reason: str = "engines_not_connected"
    contract_version: str = CONTRACT_VERSION
    metadata: tuple[tuple[str, str], ...] = field(default_factory=tuple)
    # EP-006.2 MES delivery slots (presentation pass-through only).
    suggested_next_action: str = ""
    review_point: str = ""
    confidence_label: str = ""
    evidence_points: tuple[str, ...] = ()
    plan_drivers: tuple[str, ...] = ()
    why_recommended: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(self, "stage", resolve_journey_stage(self.stage))
        object.__setattr__(
            self,
            "supporting_insights",
            tuple(
                str(item).strip()
                for item in (self.supporting_insights or ())
                if str(item).strip()
            ),
        )
        object.__setattr__(
            self,
            "evidence_points",
            tuple(
                str(item).strip()
                for item in (self.evidence_points or ())
                if str(item).strip()
            ),
        )
        object.__setattr__(
            self,
            "plan_drivers",
            tuple(
                str(item).strip()
                for item in (self.plan_drivers or ())
                if str(item).strip()
            ),
        )
        source = (self.source or "").strip().lower()
        if source not in ACTION_SOURCES:
            raise ValueError(f"unknown journey context source: {self.source!r}")
        object.__setattr__(self, "source", source)
        availability = (self.availability or "").strip().lower()
        if availability not in AVAILABILITY_VALUES:
            raise ValueError(
                f"unknown journey context availability: {self.availability!r}"
            )
        object.__setattr__(self, "availability", availability)
        completion = (self.completion_state or "").strip().lower()
        if completion not in COMPLETION_VALUES:
            raise ValueError(
                f"unknown journey context completion_state: "
                f"{self.completion_state!r}"
            )
        object.__setattr__(self, "completion_state", completion)
        urgency = (self.urgency or "").strip().lower()
        if urgency not in URGENCY_VALUES:
            raise ValueError(f"unknown journey context urgency: {self.urgency!r}")
        object.__setattr__(self, "urgency", urgency)
        if self.estimated_minutes is not None:
            try:
                object.__setattr__(
                    self, "estimated_minutes", int(self.estimated_minutes)
                )
            except (TypeError, ValueError) as exc:
                raise ValueError(
                    "journey context estimated_minutes must be an int or None"
                ) from exc


@dataclass(frozen=True)
class HomePrimaryMission:
    """Home primary-mission projection for the unified journey.

    Derived from ``JourneyContext`` when engines are connected.
    Placeholders are explicit when Programme I engines are not connected.
    Never invents educational behaviour.
    """

    title: str = ""
    why_it_matters: str = ""
    estimated_duration_label: str = ""
    expected_outcome: str = ""
    cta_label: str = "Continue"
    cta_enabled: bool = False
    endpoint: str = ""
    stage: JourneyStage = JourneyStage.DAILY_MISSION
    availability: str = AVAILABILITY_PLACEHOLDER
    unavailable_reason: str = "engines_not_connected"
    metadata: tuple[tuple[str, str], ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        object.__setattr__(self, "stage", resolve_journey_stage(self.stage))
        availability = (self.availability or "").strip().lower()
        if availability not in AVAILABILITY_VALUES:
            raise ValueError(
                f"unknown home mission availability: {self.availability!r}"
            )
        object.__setattr__(self, "availability", availability)


@dataclass(frozen=True)
class JourneySubsystemInputs:
    """Read-only opaque projections the coordinator may consume.

    Coordinator may read these maps. It must not modify, replace, or
    recalculate recommendations from them.
    """

    runtime_a: Mapping[str, Any] = field(default_factory=dict)
    digital_twin: Mapping[str, Any] = field(default_factory=dict)
    adaptive: Mapping[str, Any] = field(default_factory=dict)
    strategy: Mapping[str, Any] = field(default_factory=dict)
    evidence: Mapping[str, Any] = field(default_factory=dict)
    stage_hint: JourneyStage | None = None
    next_action: NextBestAction | None = None
    progress: JourneyProgress | None = None
    home_mission: HomePrimaryMission | None = None
    journey_context: JourneyContext | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "runtime_a", _freeze_mapping(self.runtime_a))
        object.__setattr__(
            self, "digital_twin", _freeze_mapping(self.digital_twin)
        )
        object.__setattr__(self, "adaptive", _freeze_mapping(self.adaptive))
        object.__setattr__(self, "strategy", _freeze_mapping(self.strategy))
        object.__setattr__(self, "evidence", _freeze_mapping(self.evidence))
        if self.stage_hint is not None:
            object.__setattr__(
                self, "stage_hint", resolve_journey_stage(self.stage_hint)
            )


def empty_next_best_action(
    *,
    stage: JourneyStage | str = JourneyStage.DAILY_MISSION,
) -> NextBestAction:
    """Placeholder next action when no subsystem projection is available."""
    resolved = resolve_journey_stage(stage)
    return NextBestAction(
        action_id="placeholder.next",
        stage=resolved,
        title="Continue your learning journey",
        summary="",
        cta_label="Continue",
        endpoint="",
        why_it_matters="",
        expected_outcome="",
        source=SOURCE_PLACEHOLDER,
        availability=AVAILABILITY_PLACEHOLDER,
        unavailable_reason="engines_not_connected",
    )


def empty_journey_progress(
    *,
    current_stage: JourneyStage | str = JourneyStage.DAILY_MISSION,
) -> JourneyProgress:
    """Placeholder progress when no subsystem projection is available."""
    resolved = resolve_journey_stage(current_stage)
    return JourneyProgress(
        current_stage=resolved,
        stages_completed=(),
        stages_remaining=(),
        label="",
        ratio=None,
        availability=AVAILABILITY_PLACEHOLDER,
    )


def empty_home_primary_mission() -> HomePrimaryMission:
    """Placeholder Home mission card when engines are not connected."""
    return HomePrimaryMission(
        title="Today's primary mission",
        why_it_matters="",
        estimated_duration_label="",
        expected_outcome="",
        cta_label="Continue",
        cta_enabled=False,
        endpoint="",
        stage=JourneyStage.DAILY_MISSION,
        availability=AVAILABILITY_PLACEHOLDER,
        unavailable_reason="engines_not_connected",
    )


def empty_journey_context(
    *,
    stage: JourneyStage | str = JourneyStage.DAILY_MISSION,
) -> JourneyContext:
    """Placeholder JourneyContext when Programme I engines are not connected."""
    resolved = resolve_journey_stage(stage)
    return JourneyContext(
        stage=resolved,
        mission_title="Today's primary mission",
        mission_reason="",
        estimated_duration="",
        expected_outcome="",
        completion_state=COMPLETION_UNKNOWN,
        urgency=URGENCY_NONE,
        next_transition="",
        supporting_insights=(),
        cta_label="Continue",
        cta_enabled=False,
        endpoint="",
        estimated_minutes=None,
        source=SOURCE_PLACEHOLDER,
        availability=AVAILABILITY_PLACEHOLDER,
        unavailable_reason="engines_not_connected",
    )


def home_mission_from_context(context: JourneyContext) -> HomePrimaryMission:
    """Project Home primary-mission fields from a JourneyContext."""
    return HomePrimaryMission(
        title=context.mission_title,
        why_it_matters=context.mission_reason,
        estimated_duration_label=context.estimated_duration,
        expected_outcome=context.expected_outcome,
        cta_label=context.cta_label or "Continue",
        cta_enabled=context.cta_enabled,
        endpoint=context.endpoint,
        stage=context.stage,
        availability=context.availability,
        unavailable_reason=context.unavailable_reason,
        metadata=context.metadata
        + (("source", context.source), ("via", "journey_context")),
    )


def next_action_from_context(context: JourneyContext) -> NextBestAction:
    """Project a NextBestAction from a JourneyContext (pass-through)."""
    return NextBestAction(
        action_id=f"journey_context.{context.stage.value}",
        stage=context.stage,
        title=context.mission_title,
        summary=context.mission_reason,
        cta_label=context.cta_label or "Continue",
        endpoint=context.endpoint,
        estimated_minutes=context.estimated_minutes,
        why_it_matters=context.mission_reason,
        expected_outcome=context.expected_outcome,
        source=context.source,
        availability=context.availability,
        unavailable_reason=context.unavailable_reason,
        metadata=context.metadata + (("via", "journey_context"),),
    )


def empty_journey_state(student_id: str) -> JourneyState:
    """Placeholder journey state for a student."""
    stage = JourneyStage.DAILY_MISSION
    return JourneyState(
        student_id=student_id,
        current_stage=stage,
        next_action=empty_next_best_action(stage=stage),
        progress=empty_journey_progress(current_stage=stage),
        availability=AVAILABILITY_PLACEHOLDER,
        unavailable_reason="engines_not_connected",
    )
