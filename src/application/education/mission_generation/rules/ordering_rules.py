"""OrderingRules — deterministic mission priority ordering."""

from __future__ import annotations

from collections.abc import Sequence

from application.education.mission_generation.enums import MissionType
from application.education.mission_generation.models.mission import Mission
from application.education.mission_generation.models.mission_ordering import (
    MissionOrdering,
)

# Prerequisite missions sort ahead of non-prerequisite work for the same subject.
_TYPE_TIEBREAK: dict[MissionType, int] = {
    MissionType.REVISE_PREREQUISITE: 0,
    MissionType.STRENGTHEN_FOUNDATION: 1,
    MissionType.CONFIDENCE_RECOVERY: 2,
    MissionType.REVIEW_CONCEPT: 3,
    MissionType.PRACTICE_QUESTIONS: 4,
    MissionType.CONSOLIDATE_KNOWLEDGE: 5,
    MissionType.REVISION_SESSION: 6,
    MissionType.CHECKPOINT_PREPARATION: 7,
    MissionType.MIXED_PRACTICE: 8,
    MissionType.MAINTENANCE_REVIEW: 9,
}


class OrderingRules:
    """Deterministically ranks missions for execution.

    Sort key (descending priority, then prerequisite preference, then stable
    type/scope tie-breakers):

    1. priority_magnitude (desc)
    2. type tie-break (asc — prerequisites first)
    3. subject_id (asc)
    4. competency_id (asc)
    5. mission_id (asc)
    """

    @staticmethod
    def sort_key(mission: Mission) -> tuple:
        return (
            -mission.ordering.priority_magnitude,
            _TYPE_TIEBREAK.get(mission.mission_type, 50),
            mission.subject_id or "",
            mission.competency_id or "",
            mission.mission_id.value,
        )

    @staticmethod
    def prioritise(missions: Sequence[Mission]) -> tuple[Mission, ...]:
        ordered = sorted(missions, key=OrderingRules.sort_key)
        ranked: list[Mission] = []
        for index, mission in enumerate(ordered, start=1):
            ordering = MissionOrdering(
                rank=index,
                priority_magnitude=mission.ordering.priority_magnitude,
            )
            ranked.append(mission.with_ordering(ordering))
        return tuple(ranked)

    @staticmethod
    def ensure_prerequisites_before_dependents(
        missions: Sequence[Mission],
    ) -> tuple[Mission, ...]:
        """Ensure revise-prerequisite missions precede same-subject work.

        Already covered by sort_key type tie-break; re-exported for the
        milestone vocabulary (StudyPrerequisite rule).
        """
        return OrderingRules.prioritise(missions)
