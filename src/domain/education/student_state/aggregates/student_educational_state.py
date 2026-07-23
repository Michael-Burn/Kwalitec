"""StudentEducationalState aggregate root — current educational condition.

Architecture Source
    STUDENT_DIGITAL_TWIN.md
    EDUCATIONAL_STATE_LIFECYCLE_ARCHITECTURE.md
Concept
    Student Educational State
"""

from __future__ import annotations

from datetime import datetime

from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import LearningEpisodeId
from domain.education.student_state.ids import (
    CheckpointId,
    EducationalTimelineId,
    MissionId,
    StudentEducationalStateId,
)
from domain.education.student_state.policies.state_validation_policy import (
    StateValidationPolicy,
)
from domain.education.student_state.value_objects.competency_state import (
    CompetencyState,
)
from domain.education.student_state.value_objects.confidence_summary import (
    ConfidenceSummary,
)
from domain.education.student_state.value_objects.educational_health import (
    EducationalHealth,
)
from domain.education.student_state.value_objects.educational_state_snapshot import (
    EducationalStateSnapshot,
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


def _coerce_episode_id(
    value: LearningEpisodeId | str,
) -> LearningEpisodeId:
    if isinstance(value, LearningEpisodeId):
        return value
    return LearningEpisodeId(value)


def _coerce_mission_reference(
    value: MissionReference | MissionId | str,
) -> MissionReference:
    if isinstance(value, MissionReference):
        return value
    if isinstance(value, MissionId):
        return MissionReference(mission_id=value)
    return MissionReference(mission_id=MissionId(value))


def _coerce_checkpoint_reference(
    value: CheckpointReference | CheckpointId | str,
) -> CheckpointReference:
    if isinstance(value, CheckpointReference):
        return value
    if isinstance(value, CheckpointId):
        return CheckpointReference(checkpoint_id=value)
    return CheckpointReference(checkpoint_id=CheckpointId(value))


def _coerce_timeline_reference(
    value: EducationalTimelineReference | EducationalTimelineId | str,
) -> EducationalTimelineReference:
    if isinstance(value, EducationalTimelineReference):
        return value
    if isinstance(value, EducationalTimelineId):
        return EducationalTimelineReference(timeline_id=value)
    return EducationalTimelineReference(timeline_id=EducationalTimelineId(value))


class StudentEducationalState:
    """Aggregate root modelling a student's current educational condition.

    Owns subject states, competency states, mastery/confidence summaries,
    overall educational health, and lightweight references to the active
    learning episode, current mission, current checkpoint, and educational
    timeline. Behaviour is exposed only through methods — no public setters.

    The aggregate models *current condition*, not historical events. It does
    not estimate mastery, run recommendation logic, build knowledge graphs,
    model forgetting curves, or invoke AI. It stores and replaces state it is
    given, and it protects its own invariants.
    """

    def __init__(
        self,
        state_id: StudentEducationalStateId,
        student_id: str,
        *,
        subject_states: list[SubjectState] | tuple[SubjectState, ...] | None = None,
        competency_states: list[CompetencyState]
        | tuple[CompetencyState, ...]
        | None = None,
        mastery_summary: MasterySummary | None = None,
        confidence_summary: ConfidenceSummary | None = None,
        educational_health: EducationalHealth | None = None,
        active_learning_episode_id: LearningEpisodeId | None = None,
        current_mission: MissionReference | None = None,
        current_checkpoint: CheckpointReference | None = None,
        educational_timeline: EducationalTimelineReference | None = None,
        last_updated_at: datetime | None = None,
    ) -> None:
        self._state_id = StateValidationPolicy.assert_identity(state_id)
        self._student_id = StateValidationPolicy.assert_student_id(student_id)
        self._subject_states = StateValidationPolicy.assert_subject_states(
            subject_states or ()
        )
        self._competency_states = StateValidationPolicy.assert_competency_states(
            competency_states or ()
        )
        self._mastery_summary = StateValidationPolicy.assert_mastery_summary(
            mastery_summary if mastery_summary is not None else MasterySummary.unknown()
        )
        self._confidence_summary = StateValidationPolicy.assert_confidence_summary(
            confidence_summary
            if confidence_summary is not None
            else ConfidenceSummary.unknown()
        )
        self._educational_health = StateValidationPolicy.assert_educational_health(
            educational_health
            if educational_health is not None
            else EducationalHealth.unknown()
        )
        self._active_learning_episode_id = (
            StateValidationPolicy.assert_active_learning_episode(
                active_learning_episode_id
            )
        )
        self._current_mission = StateValidationPolicy.assert_current_mission(
            current_mission
        )
        self._current_checkpoint = StateValidationPolicy.assert_current_checkpoint(
            current_checkpoint
        )
        self._educational_timeline = StateValidationPolicy.assert_educational_timeline(
            educational_timeline
        )
        self._last_updated_at = StateValidationPolicy.assert_last_updated_at(
            last_updated_at
        )

    @classmethod
    def create(
        cls,
        state_id: StudentEducationalStateId,
        student_id: str,
        *,
        last_updated_at: datetime | None = None,
    ) -> StudentEducationalState:
        """Factory: create a new, empty StudentEducationalState for a student."""
        return cls(
            state_id=state_id,
            student_id=student_id,
            last_updated_at=last_updated_at,
        )

    # --- identity / read models (no setters) ---

    @property
    def state_id(self) -> StudentEducationalStateId:
        return self._state_id

    @property
    def student_id(self) -> str:
        return self._student_id

    @property
    def subject_states(self) -> tuple[SubjectState, ...]:
        return tuple(self._subject_states)

    @property
    def competency_states(self) -> tuple[CompetencyState, ...]:
        return tuple(self._competency_states)

    @property
    def mastery_summary(self) -> MasterySummary:
        return self._mastery_summary

    @property
    def confidence_summary(self) -> ConfidenceSummary:
        return self._confidence_summary

    @property
    def educational_health(self) -> EducationalHealth:
        return self._educational_health

    @property
    def active_learning_episode_id(self) -> LearningEpisodeId | None:
        return self._active_learning_episode_id

    @property
    def current_mission(self) -> MissionReference | None:
        return self._current_mission

    @property
    def current_checkpoint(self) -> CheckpointReference | None:
        return self._current_checkpoint

    @property
    def educational_timeline(self) -> EducationalTimelineReference | None:
        return self._educational_timeline

    @property
    def last_updated_at(self) -> datetime | None:
        return self._last_updated_at

    def subject_count(self) -> int:
        return len(self._subject_states)

    def competency_count(self) -> int:
        return len(self._competency_states)

    def has_subject(self, subject_id: object) -> bool:
        key = subject_id.value if hasattr(subject_id, "value") else subject_id
        return any(s.subject_id.value == key for s in self._subject_states)

    def subject_state_for(self, subject_id: object) -> SubjectState | None:
        key = subject_id.value if hasattr(subject_id, "value") else subject_id
        for state in self._subject_states:
            if state.subject_id.value == key:
                return state
        return None

    def has_competency(self, competency_id: object) -> bool:
        key = (
            competency_id.value
            if hasattr(competency_id, "value")
            else competency_id
        )
        return any(c.competency_id.value == key for c in self._competency_states)

    def competency_state_for(self, competency_id: object) -> CompetencyState | None:
        key = (
            competency_id.value
            if hasattr(competency_id, "value")
            else competency_id
        )
        for state in self._competency_states:
            if state.competency_id.value == key:
                return state
        return None

    def has_active_learning_episode(self) -> bool:
        return self._active_learning_episode_id is not None

    def has_current_mission(self) -> bool:
        return self._current_mission is not None

    def has_current_checkpoint(self) -> bool:
        return self._current_checkpoint is not None

    def has_educational_timeline(self) -> bool:
        return self._educational_timeline is not None

    # --- behaviour ---

    def update_subject_state(
        self,
        subject_state: SubjectState,
        *,
        occurred_at: datetime | None = None,
    ) -> None:
        """Add or replace a subject's state, keyed by subject_id."""
        if not isinstance(subject_state, SubjectState):
            raise EducationalInvariantViolation(
                "subject_state must be a SubjectState",
                invariant="StudentEducationalState.update_subject_state.type",
            )
        self._subject_states = StateValidationPolicy.assert_subject_states(
            self._upsert(
                self._subject_states,
                subject_state,
                key=lambda item: item.subject_id.value,
            )
        )
        self._touch(occurred_at)

    def update_competency(
        self,
        competency_state: CompetencyState,
        *,
        occurred_at: datetime | None = None,
    ) -> None:
        """Add or replace a competency's state, keyed by competency_id."""
        if not isinstance(competency_state, CompetencyState):
            raise EducationalInvariantViolation(
                "competency_state must be a CompetencyState",
                invariant="StudentEducationalState.update_competency.type",
            )
        self._competency_states = StateValidationPolicy.assert_competency_states(
            self._upsert(
                self._competency_states,
                competency_state,
                key=lambda item: item.competency_id.value,
            )
        )
        self._touch(occurred_at)

    def update_mastery_summary(
        self,
        mastery_summary: MasterySummary,
        *,
        occurred_at: datetime | None = None,
    ) -> None:
        """Replace the supplied mastery summary."""
        self._mastery_summary = StateValidationPolicy.assert_mastery_summary(
            mastery_summary
        )
        self._touch(occurred_at)

    def update_confidence_summary(
        self,
        confidence_summary: ConfidenceSummary,
        *,
        occurred_at: datetime | None = None,
    ) -> None:
        """Replace the supplied confidence summary."""
        self._confidence_summary = StateValidationPolicy.assert_confidence_summary(
            confidence_summary
        )
        self._touch(occurred_at)

    def update_educational_health(
        self,
        educational_health: EducationalHealth,
        *,
        occurred_at: datetime | None = None,
    ) -> None:
        """Replace the supplied educational health posture."""
        self._educational_health = StateValidationPolicy.assert_educational_health(
            educational_health
        )
        self._touch(occurred_at)

    def attach_learning_episode(
        self,
        episode_id: LearningEpisodeId | str,
        *,
        occurred_at: datetime | None = None,
    ) -> None:
        """Set the single active learning episode, replacing any prior one."""
        self._active_learning_episode_id = (
            StateValidationPolicy.assert_active_learning_episode(
                _coerce_episode_id(episode_id)
            )
        )
        self._touch(occurred_at)

    def clear_learning_episode(self, *, occurred_at: datetime | None = None) -> None:
        """Clear the active learning episode reference."""
        self._active_learning_episode_id = None
        self._touch(occurred_at)

    def attach_current_mission(
        self,
        mission: MissionReference | MissionId | str,
        *,
        occurred_at: datetime | None = None,
    ) -> None:
        """Set the single current mission reference, replacing any prior one."""
        self._current_mission = StateValidationPolicy.assert_current_mission(
            _coerce_mission_reference(mission)
        )
        self._touch(occurred_at)

    def clear_current_mission(self, *, occurred_at: datetime | None = None) -> None:
        """Clear the current mission reference."""
        self._current_mission = None
        self._touch(occurred_at)

    def attach_checkpoint(
        self,
        checkpoint: CheckpointReference | CheckpointId | str,
        *,
        occurred_at: datetime | None = None,
    ) -> None:
        """Set the single current checkpoint reference, replacing any prior one."""
        self._current_checkpoint = StateValidationPolicy.assert_current_checkpoint(
            _coerce_checkpoint_reference(checkpoint)
        )
        self._touch(occurred_at)

    def clear_checkpoint(self, *, occurred_at: datetime | None = None) -> None:
        """Clear the current checkpoint reference."""
        self._current_checkpoint = None
        self._touch(occurred_at)

    def attach_educational_timeline(
        self,
        timeline: EducationalTimelineReference | EducationalTimelineId | str,
        *,
        occurred_at: datetime | None = None,
    ) -> None:
        """Set the educational timeline reference, replacing any prior one."""
        self._educational_timeline = StateValidationPolicy.assert_educational_timeline(
            _coerce_timeline_reference(timeline)
        )
        self._touch(occurred_at)

    def clear_educational_timeline(
        self, *, occurred_at: datetime | None = None
    ) -> None:
        """Clear the educational timeline reference."""
        self._educational_timeline = None
        self._touch(occurred_at)

    def produce_snapshot(self) -> EducationalStateSnapshot:
        """Produce an immutable, accurate snapshot of current state."""
        return EducationalStateSnapshot(
            state_id=self._state_id,
            student_id=self._student_id,
            subject_states=tuple(self._subject_states),
            competency_states=tuple(self._competency_states),
            mastery_summary=self._mastery_summary,
            confidence_summary=self._confidence_summary,
            educational_health=self._educational_health,
            active_learning_episode_id=self._active_learning_episode_id,
            current_mission=self._current_mission,
            current_checkpoint=self._current_checkpoint,
            educational_timeline=self._educational_timeline,
            last_updated_at=self._last_updated_at,
        )

    # --- internals ---

    @staticmethod
    def _upsert(items, new_item, *, key):
        replaced = False
        result = []
        new_key = key(new_item)
        for item in items:
            if key(item) == new_key:
                result.append(new_item)
                replaced = True
            else:
                result.append(item)
        if not replaced:
            result.append(new_item)
        return result

    def _touch(self, occurred_at: datetime | None) -> None:
        if occurred_at is None:
            return
        self._last_updated_at = StateValidationPolicy.assert_last_updated_at(
            occurred_at
        )

    def __eq__(self, other: object) -> bool:
        if other is self:
            return True
        if not isinstance(other, StudentEducationalState):
            return NotImplemented
        return self._state_id == other._state_id

    def __hash__(self) -> int:
        return hash((type(self), self._state_id))

    def __repr__(self) -> str:
        return (
            f"StudentEducationalState(state_id={self._state_id!r}, "
            f"student_id={self._student_id!r}, "
            f"subjects={len(self._subject_states)}, "
            f"competencies={len(self._competency_states)})"
        )
