"""Screen ↔ Journey Stage mapping (P2-MS001).

Every major Experience screen belongs to exactly one canonical stage.
Mapping is presentation / orchestration vocabulary only.
"""

from __future__ import annotations

from app.application.unified_journey.stages import (
    JourneyStage,
    resolve_journey_stage,
)
from app.domain.student_experience.experience_workspace import ExperienceSurface

# Experience surfaces → unique journey stage.
SURFACE_TO_STAGE: dict[ExperienceSurface, JourneyStage] = {
    ExperienceSurface.HOME: JourneyStage.DAILY_MISSION,
    ExperienceSurface.JOURNEY: JourneyStage.EXAM_READINESS,
    ExperienceSurface.REVISION: JourneyStage.REVISION_MODE,
    ExperienceSurface.HISTORY: JourneyStage.LEARNING_ARCHIVE,
    ExperienceSurface.PROFILE: JourneyStage.ONBOARDING,
}

# System / session destinations → unique journey stage.
ENDPOINT_TO_STAGE: dict[str, JourneyStage] = {
    "student.home": JourneyStage.DAILY_MISSION,
    "student.journey": JourneyStage.EXAM_READINESS,
    "student.revision": JourneyStage.REVISION_MODE,
    "student.history": JourneyStage.LEARNING_ARCHIVE,
    "student.profile": JourneyStage.ONBOARDING,
    "study_plan.index": JourneyStage.PLANNING,
    "study_plan.wizard": JourneyStage.PLANNING,
    "session.overview": JourneyStage.STUDY_SESSION,
    "session.activity": JourneyStage.STUDY_SESSION,
    "session.reflection": JourneyStage.SESSION_REFLECTION,
    "session.summary": JourneyStage.SESSION_REFLECTION,
    "session.complete": JourneyStage.SESSION_REFLECTION,
    # Weekly review reuses History until a dedicated surface exists.
    "student.weekly_review": JourneyStage.WEEKLY_REVIEW,
}

STAGE_TO_ENDPOINT: dict[JourneyStage, str] = {
    JourneyStage.ONBOARDING: "student.profile",
    JourneyStage.PLANNING: "study_plan.index",
    JourneyStage.DAILY_MISSION: "student.home",
    JourneyStage.STUDY_SESSION: "session.overview",
    JourneyStage.SESSION_REFLECTION: "session.reflection",
    JourneyStage.WEEKLY_REVIEW: "student.history",
    JourneyStage.REVISION_MODE: "student.revision",
    JourneyStage.EXAM_READINESS: "student.journey",
    JourneyStage.LEARNING_ARCHIVE: "student.history",
}


def stage_for_surface(surface: ExperienceSurface | str) -> JourneyStage:
    """Return the unique journey stage for an Experience surface."""
    if isinstance(surface, ExperienceSurface):
        resolved = surface
    else:
        resolved = ExperienceSurface(str(surface).strip().lower())
    try:
        return SURFACE_TO_STAGE[resolved]
    except KeyError as exc:
        raise ValueError(
            f"experience surface has no journey stage: {surface!r}"
        ) from exc


def stage_for_endpoint(endpoint: str | None) -> JourneyStage | None:
    """Return the journey stage for a Flask endpoint, if mapped."""
    if not endpoint:
        return None
    if endpoint in ENDPOINT_TO_STAGE:
        return ENDPOINT_TO_STAGE[endpoint]
    # Prefix match for nested study-plan / session routes.
    for key, stage in ENDPOINT_TO_STAGE.items():
        prefix = key.rsplit(".", 1)[0]
        if endpoint.startswith(prefix + "."):
            return stage
    return None


def endpoint_for_stage(stage: JourneyStage | str) -> str:
    """Return the primary Flask endpoint for a journey stage."""
    resolved = resolve_journey_stage(stage)
    return STAGE_TO_ENDPOINT[resolved]


def surfaces_have_unique_stages() -> bool:
    """Invariant: each Experience surface maps to a distinct stage."""
    stages = list(SURFACE_TO_STAGE.values())
    return len(stages) == len(set(stages))
