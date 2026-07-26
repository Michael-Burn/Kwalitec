"""Stage → Programme I capability mapping (P2-MS002).

Each canonical journey stage binds to an existing Programme I capability.
The Experience Layer does not duplicate educational logic — it only routes
presentation to the owning subsystem projection.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.application.unified_journey.contracts import (
    SOURCE_ADAPTIVE,
    SOURCE_DIGITAL_TWIN,
    SOURCE_EVIDENCE,
    SOURCE_RUNTIME_A,
    SOURCE_STRATEGY,
)
from app.application.unified_journey.stages import (
    CANONICAL_JOURNEY_STAGES,
    JourneyStage,
    resolve_journey_stage,
)


@dataclass(frozen=True)
class StageCapabilityMapping:
    """Immutable mapping of one journey stage to Programme I ownership."""

    stage: JourneyStage
    primary_subsystem: str
    supporting_subsystems: tuple[str, ...]
    capability: str
    notes: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(self, "stage", resolve_journey_stage(self.stage))
        object.__setattr__(
            self,
            "supporting_subsystems",
            tuple(self.supporting_subsystems or ()),
        )


# Explicit stage → subsystem map. No educational calculations; no duplication
# of Programme I decision ownership.
STAGE_TO_SUBSYSTEM: dict[JourneyStage, StageCapabilityMapping] = {
    JourneyStage.ONBOARDING: StageCapabilityMapping(
        stage=JourneyStage.ONBOARDING,
        primary_subsystem=SOURCE_RUNTIME_A,
        supporting_subsystems=(),
        capability="Student profile / first-run plan bootstrap",
        notes="Runtime A owns profile and plan existence signals.",
    ),
    JourneyStage.PLANNING: StageCapabilityMapping(
        stage=JourneyStage.PLANNING,
        primary_subsystem=SOURCE_RUNTIME_A,
        supporting_subsystems=(SOURCE_STRATEGY,),
        capability="Study plan wizard and plan index",
        notes="Strategy may supply study_plan projection presentation only.",
    ),
    JourneyStage.DAILY_MISSION: StageCapabilityMapping(
        stage=JourneyStage.DAILY_MISSION,
        primary_subsystem=SOURCE_RUNTIME_A,
        supporting_subsystems=(SOURCE_ADAPTIVE, SOURCE_STRATEGY),
        capability="Today's mission / recommendation",
        notes=(
            "Runtime A Recommendation Bridge is primary; Adaptive / Strategy "
            "pass through when already projected for Experience."
        ),
    ),
    JourneyStage.STUDY_SESSION: StageCapabilityMapping(
        stage=JourneyStage.STUDY_SESSION,
        primary_subsystem=SOURCE_RUNTIME_A,
        supporting_subsystems=(),
        capability="Active mission session",
        notes="Runtime A Mission Start / Resume own session authority.",
    ),
    JourneyStage.SESSION_REFLECTION: StageCapabilityMapping(
        stage=JourneyStage.SESSION_REFLECTION,
        primary_subsystem=SOURCE_RUNTIME_A,
        supporting_subsystems=(SOURCE_EVIDENCE,),
        capability="Session completion reflection",
        notes="Evidence may contribute observational supporting insights only.",
    ),
    JourneyStage.WEEKLY_REVIEW: StageCapabilityMapping(
        stage=JourneyStage.WEEKLY_REVIEW,
        primary_subsystem=SOURCE_EVIDENCE,
        supporting_subsystems=(SOURCE_RUNTIME_A,),
        capability="Weekly learning review narrative",
        notes="Evidence / History projections; Runtime A remains narrative source.",
    ),
    JourneyStage.REVISION_MODE: StageCapabilityMapping(
        stage=JourneyStage.REVISION_MODE,
        primary_subsystem=SOURCE_ADAPTIVE,
        supporting_subsystems=(SOURCE_STRATEGY, SOURCE_DIGITAL_TWIN),
        capability="Revision recommendations",
        notes="Adaptive / Strategy revision plans; Twin observational support.",
    ),
    JourneyStage.EXAM_READINESS: StageCapabilityMapping(
        stage=JourneyStage.EXAM_READINESS,
        primary_subsystem=SOURCE_STRATEGY,
        supporting_subsystems=(SOURCE_ADAPTIVE, SOURCE_DIGITAL_TWIN, SOURCE_RUNTIME_A),
        capability="Exam readiness journey projection",
        notes="Strategy / Adaptive readiness signals; Twin observational support.",
    ),
    JourneyStage.LEARNING_ARCHIVE: StageCapabilityMapping(
        stage=JourneyStage.LEARNING_ARCHIVE,
        primary_subsystem=SOURCE_EVIDENCE,
        supporting_subsystems=(SOURCE_RUNTIME_A,),
        capability="Learning history archive",
        notes="Evidence / History Bridge projections from Runtime A records.",
    ),
}


def mapping_for_stage(
    stage: JourneyStage | str,
) -> StageCapabilityMapping:
    """Return the Programme I capability mapping for a journey stage."""
    resolved = resolve_journey_stage(stage)
    try:
        return STAGE_TO_SUBSYSTEM[resolved]
    except KeyError as exc:
        raise ValueError(f"no subsystem mapping for stage: {stage!r}") from exc


def primary_subsystem_for_stage(stage: JourneyStage | str) -> str:
    """Return the primary Programme I subsystem source for a stage."""
    return mapping_for_stage(stage).primary_subsystem


def all_stages_mapped() -> bool:
    """Invariant: every canonical stage has exactly one capability mapping."""
    return set(STAGE_TO_SUBSYSTEM) == set(CANONICAL_JOURNEY_STAGES)


def stage_mapping_table() -> tuple[StageCapabilityMapping, ...]:
    """Canonical ordered mapping rows for docs / tests."""
    return tuple(STAGE_TO_SUBSYSTEM[stage] for stage in CANONICAL_JOURNEY_STAGES)
