"""Policy validating Educational Digital Twin state shapes.

Architecture Source
    STUDENT_DIGITAL_TWIN.md
Concept
    State Validation Policy
"""

from __future__ import annotations

from domain.education.digital_twin.entities.concept_state import ConceptState
from domain.education.digital_twin.entities.evidence_history import (
    EvidenceHistoryEntry,
)
from domain.education.digital_twin.entities.intervention_history import (
    InterventionHistoryEntry,
)
from domain.education.digital_twin.entities.learner_state import LearnerState
from domain.education.digital_twin.entities.misconception_state import (
    MisconceptionState,
)
from domain.education.digital_twin.enums import TwinStatus
from domain.education.digital_twin.value_objects.confidence_profile import (
    ConfidenceProfile,
)
from domain.education.digital_twin.value_objects.learning_trajectory import (
    LearningTrajectory,
)
from domain.education.digital_twin.value_objects.mastery_state import MasteryState
from domain.education.digital_twin.value_objects.retention_state import RetentionState
from domain.education.foundation.base import require_identity_value
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import DigitalTwinId


class StateValidationPolicy:
    """Validates Twin-owned educational memory shapes — no educational reasoning."""

    @staticmethod
    def assert_identity(twin_id: DigitalTwinId) -> DigitalTwinId:
        if not isinstance(twin_id, DigitalTwinId):
            raise EducationalInvariantViolation(
                "twin must possess a DigitalTwinId identity",
                invariant="EducationalDigitalTwin.identity.required",
            )
        return twin_id

    @staticmethod
    def assert_student_id(student_id: str) -> str:
        return require_identity_value(student_id, "student_id")

    @staticmethod
    def assert_status(status: TwinStatus) -> TwinStatus:
        if not isinstance(status, TwinStatus):
            raise EducationalInvariantViolation(
                "status must be a TwinStatus",
                invariant="EducationalDigitalTwin.status.type",
            )
        return status

    @staticmethod
    def assert_learner_state(learner_state: LearnerState) -> LearnerState:
        if not isinstance(learner_state, LearnerState):
            raise EducationalInvariantViolation(
                "twin must own a LearnerState",
                invariant="EducationalDigitalTwin.learner_state.required",
            )
        return learner_state

    @staticmethod
    def assert_learner_matches_student(
        learner_state: LearnerState, student_id: str
    ) -> None:
        if learner_state.student_id != student_id:
            raise EducationalInvariantViolation(
                "learner state student_id must match twin student_id",
                invariant="EducationalDigitalTwin.learner_state.student_aligned",
            )

    @staticmethod
    def assert_retention(retention: RetentionState) -> RetentionState:
        if not isinstance(retention, RetentionState):
            raise EducationalInvariantViolation(
                "twin must own RetentionState",
                invariant="EducationalDigitalTwin.retention.required",
            )
        return retention

    @staticmethod
    def assert_confidence(confidence: ConfidenceProfile) -> ConfidenceProfile:
        if not isinstance(confidence, ConfidenceProfile):
            raise EducationalInvariantViolation(
                "twin must own ConfidenceProfile",
                invariant="EducationalDigitalTwin.confidence.required",
            )
        return confidence

    @staticmethod
    def assert_trajectory(trajectory: LearningTrajectory) -> LearningTrajectory:
        if not isinstance(trajectory, LearningTrajectory):
            raise EducationalInvariantViolation(
                "twin must own LearningTrajectory",
                invariant="EducationalDigitalTwin.trajectory.required",
            )
        return trajectory

    @staticmethod
    def assert_mastery(mastery: MasteryState) -> MasteryState:
        if not isinstance(mastery, MasteryState):
            raise EducationalInvariantViolation(
                "mastery must be a MasteryState",
                invariant="EducationalDigitalTwin.mastery.type",
            )
        return mastery

    @staticmethod
    def assert_concept_states(
        concept_states: list[ConceptState] | tuple[ConceptState, ...],
    ) -> list[ConceptState]:
        items = list(concept_states)
        seen_ids: set[str] = set()
        seen_concepts: set[str] = set()
        for state in items:
            if not isinstance(state, ConceptState):
                raise EducationalInvariantViolation(
                    "concept_states must contain ConceptState entities",
                    invariant="EducationalDigitalTwin.concept_states.type",
                )
            key = state.concept_state_id.value
            if key in seen_ids:
                raise EducationalInvariantViolation(
                    "duplicate concept_state_id in twin",
                    invariant="EducationalDigitalTwin.concept_states.unique_id",
                )
            seen_ids.add(key)
            concept_key = state.concept_id.value
            if concept_key in seen_concepts:
                raise EducationalInvariantViolation(
                    "duplicate concept_id in twin concept states",
                    invariant="EducationalDigitalTwin.concept_states.unique_concept",
                )
            seen_concepts.add(concept_key)
        return items

    @staticmethod
    def assert_misconception_states(
        misconception_states: list[MisconceptionState]
        | tuple[MisconceptionState, ...],
    ) -> list[MisconceptionState]:
        items = list(misconception_states)
        seen_ids: set[str] = set()
        seen_misc: set[str] = set()
        for state in items:
            if not isinstance(state, MisconceptionState):
                raise EducationalInvariantViolation(
                    "misconception_states must contain MisconceptionState entities",
                    invariant="EducationalDigitalTwin.misconception_states.type",
                )
            key = state.misconception_state_id.value
            if key in seen_ids:
                raise EducationalInvariantViolation(
                    "duplicate misconception_state_id in twin",
                    invariant="EducationalDigitalTwin.misconception_states.unique_id",
                )
            seen_ids.add(key)
            misc_key = state.misconception_id.value
            if misc_key in seen_misc:
                raise EducationalInvariantViolation(
                    "duplicate misconception_id in twin misconception states",
                    invariant=(
                        "EducationalDigitalTwin.misconception_states.unique_misconception"
                    ),
                )
            seen_misc.add(misc_key)
        return items

    @staticmethod
    def assert_evidence_history(
        entries: list[EvidenceHistoryEntry] | tuple[EvidenceHistoryEntry, ...],
    ) -> list[EvidenceHistoryEntry]:
        items = list(entries)
        seen_entry_ids: set[str] = set()
        seen_evidence_ids: set[str] = set()
        previous = 0
        for entry in items:
            if not isinstance(entry, EvidenceHistoryEntry):
                raise EducationalInvariantViolation(
                    "evidence history must contain EvidenceHistoryEntry entities",
                    invariant="EducationalDigitalTwin.evidence_history.type",
                )
            if entry.entry_id.value in seen_entry_ids:
                raise EducationalInvariantViolation(
                    "duplicate evidence history entry_id",
                    invariant="EducationalDigitalTwin.evidence_history.unique_entry",
                )
            seen_entry_ids.add(entry.entry_id.value)
            if entry.evidence_id.value in seen_evidence_ids:
                raise EducationalInvariantViolation(
                    "duplicate evidence_id in evidence history",
                    invariant="EducationalDigitalTwin.evidence_history.unique_evidence",
                )
            seen_evidence_ids.add(entry.evidence_id.value)
            if entry.sequence <= previous:
                raise EducationalInvariantViolation(
                    "evidence history sequences must be strictly increasing",
                    invariant="EducationalDigitalTwin.evidence_history.sequence",
                )
            previous = entry.sequence
        return items

    @staticmethod
    def assert_intervention_history(
        entries: list[InterventionHistoryEntry]
        | tuple[InterventionHistoryEntry, ...],
    ) -> list[InterventionHistoryEntry]:
        items = list(entries)
        seen_entry_ids: set[str] = set()
        previous = 0
        for entry in items:
            if not isinstance(entry, InterventionHistoryEntry):
                raise EducationalInvariantViolation(
                    "intervention history must contain InterventionHistoryEntry "
                    "entities",
                    invariant="EducationalDigitalTwin.intervention_history.type",
                )
            if entry.entry_id.value in seen_entry_ids:
                raise EducationalInvariantViolation(
                    "duplicate intervention history entry_id",
                    invariant=(
                        "EducationalDigitalTwin.intervention_history.unique_entry"
                    ),
                )
            seen_entry_ids.add(entry.entry_id.value)
            if entry.sequence <= previous:
                raise EducationalInvariantViolation(
                    "intervention history sequences must be strictly increasing",
                    invariant="EducationalDigitalTwin.intervention_history.sequence",
                )
            previous = entry.sequence
        return items
