"""Specification: Twin state transitions are valid.

Architecture Source
    STUDENT_DIGITAL_TWIN.md
    EDUCATIONAL_STATE_LIFECYCLE_ARCHITECTURE.md
Concept
    StateTransitionIsValidSpecification
"""

from __future__ import annotations

from domain.education.digital_twin.enums import (
    LearnerActivityStatus,
    MisconceptionPresence,
    TwinStatus,
)
from domain.education.foundation.errors import EducationalInvariantViolation


class StateTransitionIsValidSpecification:
    """True when a Twin memory state transition is structurally lawful.

    Validates lifecycle transitions only. Does not diagnose educational
    meaning or choose teaching actions.
    """

    def is_satisfied_by_status(
        self, current: TwinStatus, nxt: TwinStatus
    ) -> bool:
        if current is nxt:
            return True
        if current is TwinStatus.ACTIVE and nxt is TwinStatus.ARCHIVED:
            return True
        return False

    def is_satisfied_by_learner_activity(
        self,
        current: LearnerActivityStatus,
        nxt: LearnerActivityStatus,
    ) -> bool:
        if current is nxt:
            return True
        if current is LearnerActivityStatus.JOURNEY_COMPLETE:
            return False
        return isinstance(nxt, LearnerActivityStatus)

    def is_satisfied_by_misconception_presence(
        self,
        current: MisconceptionPresence,
        nxt: MisconceptionPresence,
    ) -> bool:
        if not isinstance(current, MisconceptionPresence):
            return False
        if not isinstance(nxt, MisconceptionPresence):
            return False
        return True

    def assert_status(self, current: TwinStatus, nxt: TwinStatus) -> None:
        if not self.is_satisfied_by_status(current, nxt):
            raise EducationalInvariantViolation(
                "invalid twin status transition",
                invariant="StateTransitionIsValidSpecification.status",
            )

    def assert_learner_activity(
        self,
        current: LearnerActivityStatus,
        nxt: LearnerActivityStatus,
    ) -> None:
        if not self.is_satisfied_by_learner_activity(current, nxt):
            raise EducationalInvariantViolation(
                "invalid learner activity transition",
                invariant="StateTransitionIsValidSpecification.learner_activity",
            )

    def assert_misconception_presence(
        self,
        current: MisconceptionPresence,
        nxt: MisconceptionPresence,
    ) -> None:
        if not self.is_satisfied_by_misconception_presence(current, nxt):
            raise EducationalInvariantViolation(
                "invalid misconception presence transition",
                invariant=(
                    "StateTransitionIsValidSpecification.misconception_presence"
                ),
            )
