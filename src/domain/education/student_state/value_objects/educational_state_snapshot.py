"""Educational state snapshot — immutable point-in-time capture.

Architecture Source
    STUDENT_DIGITAL_TWIN.md
Concept
    Educational State Snapshot
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from domain.education.foundation.base import EducationalValueObject
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import LearningEpisodeId
from domain.education.student_state.ids import StudentEducationalStateId
from domain.education.student_state.value_objects.competency_state import (
    CompetencyState,
)
from domain.education.student_state.value_objects.confidence_summary import (
    ConfidenceSummary,
)
from domain.education.student_state.value_objects.educational_health import (
    EducationalHealth,
)
from domain.education.student_state.value_objects.mastery_summary import (
    MasterySummary,
)
from domain.education.student_state.value_objects.state_references import (
    CheckpointReference,
    EducationalTimelineReference,
    MissionReference,
)
from domain.education.student_state.value_objects.subject_state import SubjectState


@dataclass(frozen=True, slots=True)
class EducationalStateSnapshot(EducationalValueObject):
    """Immutable, accurate capture of a StudentEducationalState aggregate.

    A snapshot is a read model. It does not diagnose, estimate, or recompute
    — it faithfully mirrors the aggregate's state at the moment it was
    produced.
    """

    state_id: StudentEducationalStateId
    student_id: str
    subject_states: tuple[SubjectState, ...]
    competency_states: tuple[CompetencyState, ...]
    mastery_summary: MasterySummary
    confidence_summary: ConfidenceSummary
    educational_health: EducationalHealth
    active_learning_episode_id: LearningEpisodeId | None
    current_mission: MissionReference | None
    current_checkpoint: CheckpointReference | None
    educational_timeline: EducationalTimelineReference | None
    last_updated_at: datetime | None

    def _validate(self) -> None:
        if not isinstance(self.state_id, StudentEducationalStateId):
            raise EducationalInvariantViolation(
                "state_id must be a StudentEducationalStateId",
                invariant="EducationalStateSnapshot.state_id.type",
            )
        if not isinstance(self.student_id, str) or not self.student_id.strip():
            raise EducationalInvariantViolation(
                "student_id must be a non-empty string",
                invariant="EducationalStateSnapshot.student_id.required",
            )
        object.__setattr__(self, "subject_states", tuple(self.subject_states))
        object.__setattr__(
            self, "competency_states", tuple(self.competency_states)
        )
        seen_subjects: set[str] = set()
        for subject_state in self.subject_states:
            if not isinstance(subject_state, SubjectState):
                raise EducationalInvariantViolation(
                    "subject_states must contain SubjectState value objects",
                    invariant="EducationalStateSnapshot.subject_states.type",
                )
            key = subject_state.subject_id.value
            if key in seen_subjects:
                raise EducationalInvariantViolation(
                    "duplicate subject_id in snapshot",
                    invariant="EducationalStateSnapshot.subject_states.unique",
                )
            seen_subjects.add(key)
        seen_competencies: set[str] = set()
        for competency_state in self.competency_states:
            if not isinstance(competency_state, CompetencyState):
                raise EducationalInvariantViolation(
                    "competency_states must contain CompetencyState value objects",
                    invariant="EducationalStateSnapshot.competency_states.type",
                )
            key = competency_state.competency_id.value
            if key in seen_competencies:
                raise EducationalInvariantViolation(
                    "duplicate competency_id in snapshot",
                    invariant="EducationalStateSnapshot.competency_states.unique",
                )
            seen_competencies.add(key)
        if not isinstance(self.mastery_summary, MasterySummary):
            raise EducationalInvariantViolation(
                "mastery_summary must be a MasterySummary",
                invariant="EducationalStateSnapshot.mastery_summary.type",
            )
        if not isinstance(self.confidence_summary, ConfidenceSummary):
            raise EducationalInvariantViolation(
                "confidence_summary must be a ConfidenceSummary",
                invariant="EducationalStateSnapshot.confidence_summary.type",
            )
        if not isinstance(self.educational_health, EducationalHealth):
            raise EducationalInvariantViolation(
                "educational_health must be an EducationalHealth",
                invariant="EducationalStateSnapshot.educational_health.type",
            )
        if self.active_learning_episode_id is not None and not isinstance(
            self.active_learning_episode_id, LearningEpisodeId
        ):
            raise EducationalInvariantViolation(
                "active_learning_episode_id must be a LearningEpisodeId when set",
                invariant="EducationalStateSnapshot.active_learning_episode_id.type",
            )
        if self.current_mission is not None and not isinstance(
            self.current_mission, MissionReference
        ):
            raise EducationalInvariantViolation(
                "current_mission must be a MissionReference when set",
                invariant="EducationalStateSnapshot.current_mission.type",
            )
        if self.current_checkpoint is not None and not isinstance(
            self.current_checkpoint, CheckpointReference
        ):
            raise EducationalInvariantViolation(
                "current_checkpoint must be a CheckpointReference when set",
                invariant="EducationalStateSnapshot.current_checkpoint.type",
            )
        if self.educational_timeline is not None and not isinstance(
            self.educational_timeline, EducationalTimelineReference
        ):
            raise EducationalInvariantViolation(
                "educational_timeline must be an EducationalTimelineReference "
                "when set",
                invariant="EducationalStateSnapshot.educational_timeline.type",
            )
        if self.last_updated_at is not None and not isinstance(
            self.last_updated_at, datetime
        ):
            raise EducationalInvariantViolation(
                "last_updated_at must be a datetime when set",
                invariant="EducationalStateSnapshot.last_updated_at.type",
            )

    def subject_count(self) -> int:
        return len(self.subject_states)

    def competency_count(self) -> int:
        return len(self.competency_states)

    def has_active_learning_episode(self) -> bool:
        return self.active_learning_episode_id is not None

    def has_current_mission(self) -> bool:
        return self.current_mission is not None

    def has_current_checkpoint(self) -> bool:
        return self.current_checkpoint is not None

    def has_educational_timeline(self) -> bool:
        return self.educational_timeline is not None
