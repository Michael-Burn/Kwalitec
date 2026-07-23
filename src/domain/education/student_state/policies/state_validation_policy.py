"""Policy validating Student Educational State aggregate shapes.

Architecture Source
    STUDENT_DIGITAL_TWIN.md
Concept
    State Validation Policy
"""

from __future__ import annotations

from datetime import datetime

from domain.education.foundation.base import require_identity_value
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


class StateValidationPolicy:
    """Validates StudentEducationalState shapes — no educational reasoning."""

    @staticmethod
    def assert_identity(
        state_id: StudentEducationalStateId,
    ) -> StudentEducationalStateId:
        if not isinstance(state_id, StudentEducationalStateId):
            raise EducationalInvariantViolation(
                "state must possess a StudentEducationalStateId identity",
                invariant="StudentEducationalState.identity.required",
            )
        return state_id

    @staticmethod
    def assert_student_id(student_id: str) -> str:
        return require_identity_value(student_id, "student_id")

    @staticmethod
    def assert_subject_states(
        subject_states: list[SubjectState] | tuple[SubjectState, ...],
    ) -> list[SubjectState]:
        items = list(subject_states)
        seen: set[str] = set()
        for state in items:
            if not isinstance(state, SubjectState):
                raise EducationalInvariantViolation(
                    "subject_states must contain SubjectState value objects",
                    invariant="StudentEducationalState.subject_states.type",
                )
            key = state.subject_id.value
            if key in seen:
                raise EducationalInvariantViolation(
                    "duplicate subject_id in student educational state",
                    invariant="StudentEducationalState.subject_states.unique",
                )
            seen.add(key)
        return items

    @staticmethod
    def assert_competency_states(
        competency_states: list[CompetencyState] | tuple[CompetencyState, ...],
    ) -> list[CompetencyState]:
        items = list(competency_states)
        seen: set[str] = set()
        for state in items:
            if not isinstance(state, CompetencyState):
                raise EducationalInvariantViolation(
                    "competency_states must contain CompetencyState value objects",
                    invariant="StudentEducationalState.competency_states.type",
                )
            key = state.competency_id.value
            if key in seen:
                raise EducationalInvariantViolation(
                    "duplicate competency_id in student educational state",
                    invariant="StudentEducationalState.competency_states.unique",
                )
            seen.add(key)
        return items

    @staticmethod
    def assert_mastery_summary(mastery_summary: MasterySummary) -> MasterySummary:
        if not isinstance(mastery_summary, MasterySummary):
            raise EducationalInvariantViolation(
                "state must own a MasterySummary",
                invariant="StudentEducationalState.mastery_summary.required",
            )
        return mastery_summary

    @staticmethod
    def assert_confidence_summary(
        confidence_summary: ConfidenceSummary,
    ) -> ConfidenceSummary:
        if not isinstance(confidence_summary, ConfidenceSummary):
            raise EducationalInvariantViolation(
                "state must own a ConfidenceSummary",
                invariant="StudentEducationalState.confidence_summary.required",
            )
        return confidence_summary

    @staticmethod
    def assert_educational_health(
        educational_health: EducationalHealth,
    ) -> EducationalHealth:
        if not isinstance(educational_health, EducationalHealth):
            raise EducationalInvariantViolation(
                "state must own an EducationalHealth",
                invariant="StudentEducationalState.educational_health.required",
            )
        return educational_health

    @staticmethod
    def assert_active_learning_episode(
        episode_id: LearningEpisodeId | None,
    ) -> LearningEpisodeId | None:
        if episode_id is None:
            return None
        if not isinstance(episode_id, LearningEpisodeId):
            raise EducationalInvariantViolation(
                "active_learning_episode_id must be a LearningEpisodeId",
                invariant="StudentEducationalState.active_learning_episode.type",
            )
        return episode_id

    @staticmethod
    def assert_current_mission(
        mission: MissionReference | None,
    ) -> MissionReference | None:
        if mission is None:
            return None
        if not isinstance(mission, MissionReference):
            raise EducationalInvariantViolation(
                "current_mission must be a MissionReference",
                invariant="StudentEducationalState.current_mission.type",
            )
        return mission

    @staticmethod
    def assert_current_checkpoint(
        checkpoint: CheckpointReference | None,
    ) -> CheckpointReference | None:
        if checkpoint is None:
            return None
        if not isinstance(checkpoint, CheckpointReference):
            raise EducationalInvariantViolation(
                "current_checkpoint must be a CheckpointReference",
                invariant="StudentEducationalState.current_checkpoint.type",
            )
        return checkpoint

    @staticmethod
    def assert_educational_timeline(
        timeline: EducationalTimelineReference | None,
    ) -> EducationalTimelineReference | None:
        if timeline is None:
            return None
        if not isinstance(timeline, EducationalTimelineReference):
            raise EducationalInvariantViolation(
                "educational_timeline must be an EducationalTimelineReference",
                invariant="StudentEducationalState.educational_timeline.type",
            )
        return timeline

    @staticmethod
    def assert_last_updated_at(
        last_updated_at: datetime | None,
    ) -> datetime | None:
        if last_updated_at is None:
            return None
        if not isinstance(last_updated_at, datetime):
            raise EducationalInvariantViolation(
                "last_updated_at must be a datetime",
                invariant="StudentEducationalState.last_updated_at.type",
            )
        return last_updated_at
