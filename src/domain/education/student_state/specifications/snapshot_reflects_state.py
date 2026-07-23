"""Specification: a snapshot accurately reflects its source aggregate.

Architecture Source
    STUDENT_DIGITAL_TWIN.md
Concept
    SnapshotReflectsStateSpecification
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.student_state.value_objects.educational_state_snapshot import (
    EducationalStateSnapshot,
)

if TYPE_CHECKING:
    from domain.education.student_state.aggregates.student_educational_state import (
        StudentEducationalState,
    )


class SnapshotReflectsStateSpecification:
    """True when a snapshot is a faithful, accurate mirror of the aggregate.

    Guards against snapshots silently drifting from aggregate state — the
    snapshot must never invent or omit information.
    """

    def is_satisfied_by(
        self,
        state: StudentEducationalState,
        snapshot: EducationalStateSnapshot,
    ) -> bool:
        if snapshot.state_id != state.state_id:
            return False
        if snapshot.student_id != state.student_id:
            return False
        if snapshot.subject_states != state.subject_states:
            return False
        if snapshot.competency_states != state.competency_states:
            return False
        if snapshot.mastery_summary != state.mastery_summary:
            return False
        if snapshot.confidence_summary != state.confidence_summary:
            return False
        if snapshot.educational_health != state.educational_health:
            return False
        if snapshot.active_learning_episode_id != state.active_learning_episode_id:
            return False
        if snapshot.current_mission != state.current_mission:
            return False
        if snapshot.current_checkpoint != state.current_checkpoint:
            return False
        if snapshot.educational_timeline != state.educational_timeline:
            return False
        if snapshot.last_updated_at != state.last_updated_at:
            return False
        return True

    def assert_satisfied_by(
        self,
        state: StudentEducationalState,
        snapshot: EducationalStateSnapshot,
    ) -> None:
        if not self.is_satisfied_by(state, snapshot):
            raise EducationalInvariantViolation(
                "snapshot does not accurately reflect student educational state",
                invariant="SnapshotReflectsStateSpecification.unsatisfied",
            )
