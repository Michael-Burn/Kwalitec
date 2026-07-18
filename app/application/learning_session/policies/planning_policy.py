"""Stateless planning rules for Learning Sessions.

Constructs educational session structure from journey / topic / objectives /
effort / prior evidence. Never generates study content or estimates mastery.
"""

from __future__ import annotations

from app.domain.learning_journey.entities.journey_evidence import JourneyEvidence
from app.domain.learning_journey.entities.learning_objective import (
    LearningObjective,
    ObjectiveKind,
)
from app.domain.learning_journey.value_objects.effort_estimate import EffortEstimate

# Deterministic activity tags by objective kind (not generated study content).
_ACTIVITIES_BY_KIND: dict[str, tuple[str, ...]] = {
    ObjectiveKind.UNDERSTAND.value: (
        "read_core_notes",
        "check_definitions",
        "self_explain",
    ),
    ObjectiveKind.APPLY.value: (
        "worked_example",
        "guided_practice",
        "independent_attempt",
    ),
    ObjectiveKind.ANALYSE.value: (
        "compare_approaches",
        "diagnose_errors",
        "structure_solution",
    ),
    ObjectiveKind.REVIEW.value: (
        "spaced_review",
        "concept_check",
        "summary_recall",
    ),
    ObjectiveKind.REVISE.value: (
        "targeted_revision",
        "evidence_review",
        "weak_spot_drill",
    ),
}

_DEFAULT_ACTIVITIES: tuple[str, ...] = (
    "focused_study",
    "practice_check",
    "brief_reflection_prep",
)

_EFFORT_BY_KIND: dict[str, EffortEstimate] = {
    ObjectiveKind.UNDERSTAND.value: EffortEstimate.MEDIUM,
    ObjectiveKind.APPLY.value: EffortEstimate.MEDIUM,
    ObjectiveKind.ANALYSE.value: EffortEstimate.HIGH,
    ObjectiveKind.REVIEW.value: EffortEstimate.LOW,
    ObjectiveKind.REVISE.value: EffortEstimate.HIGH,
}


class PlanningPolicy:
    """Educational session planning rules (stateless, deterministic)."""

    @staticmethod
    def activities_for(
        objectives: list[LearningObjective] | tuple[LearningObjective, ...] | None,
    ) -> tuple[str, ...]:
        """Return deterministic activity tags for the given objectives."""
        objs = tuple(objectives or ())
        if not objs:
            return _DEFAULT_ACTIVITIES
        collected: list[str] = []
        seen: set[str] = set()
        for objective in objs:
            for tag in _ACTIVITIES_BY_KIND.get(
                objective.kind.value, _DEFAULT_ACTIVITIES
            ):
                if tag not in seen:
                    seen.add(tag)
                    collected.append(tag)
        return tuple(collected) if collected else _DEFAULT_ACTIVITIES

    @staticmethod
    def estimate_effort(
        objectives: list[LearningObjective] | tuple[LearningObjective, ...] | None,
        *,
        explicit: EffortEstimate | None = None,
        previous_evidence_count: int = 0,
    ) -> EffortEstimate:
        """Choose an effort band from objectives / explicit override / evidence.

        Prior evidence never invents mastery; thin prior evidence may raise
        effort one band for revise/review intent only.
        """
        if explicit is not None:
            return explicit
        objs = tuple(objectives or ())
        if not objs:
            return EffortEstimate.MEDIUM
        primary = objs[0]
        effort = _EFFORT_BY_KIND.get(primary.kind.value, EffortEstimate.MEDIUM)
        if (
            previous_evidence_count == 0
            and primary.kind in {ObjectiveKind.REVISE, ObjectiveKind.REVIEW}
            and effort == EffortEstimate.LOW
        ):
            return EffortEstimate.MEDIUM
        if previous_evidence_count == 0 and primary.kind == ObjectiveKind.REVISE:
            return EffortEstimate.HIGH
        return effort

    @staticmethod
    def rationale_tags(
        *,
        topic_id: str,
        objectives: list[LearningObjective] | tuple[LearningObjective, ...] | None,
        previous_evidence: (
            list[JourneyEvidence] | tuple[JourneyEvidence, ...] | None
        ) = None,
        estimated_effort: EffortEstimate,
    ) -> tuple[str, ...]:
        """Explainable planning tags (no mastery claims)."""
        tags: list[str] = [f"topic={topic_id}", f"effort={estimated_effort.value}"]
        objs = tuple(objectives or ())
        if objs:
            tags.append(f"objectives={len(objs)}")
            tags.append(f"primary_kind={objs[0].kind.value}")
        else:
            tags.append("objectives=0")
        prior = len(previous_evidence or ())
        tags.append(f"prior_evidence={prior}")
        if prior == 0:
            tags.append("no_prior_evidence")
        tags.append("no_mastery_claim")
        return tuple(tags)

    @staticmethod
    def objective_ids(
        objectives: list[LearningObjective] | tuple[LearningObjective, ...] | None,
    ) -> tuple[str, ...]:
        """Stable ordered objective identities."""
        return tuple(o.objective_id for o in (objectives or ()))
