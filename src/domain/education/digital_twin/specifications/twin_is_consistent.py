"""Specification: Educational Digital Twin is internally consistent.

Architecture Source
    STUDENT_DIGITAL_TWIN.md
Concept
    TwinIsConsistentSpecification
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from domain.education.foundation.errors import EducationalInvariantViolation

if TYPE_CHECKING:
    from domain.education.digital_twin.aggregates.educational_digital_twin import (
        EducationalDigitalTwin,
    )


class TwinIsConsistentSpecification:
    """True when Twin owns required memory and histories remain coherent.

    Consistency is structural memory integrity — not educational correctness
    of mastery estimates.
    """

    def is_satisfied_by(self, twin: EducationalDigitalTwin) -> bool:
        if twin.learner_state is None:
            return False
        if twin.learner_state.student_id != twin.student_id:
            return False
        if twin.retention is None or twin.confidence is None:
            return False
        if twin.trajectory is None:
            return False
        # Histories must not shrink below trajectory-backed memory floors.
        if twin.evidence_count() < 0 or twin.intervention_count() < 0:
            return False
        evidence_ids = [e.evidence_id.value for e in twin.evidence_history]
        if len(evidence_ids) != len(set(evidence_ids)):
            return False
        entry_ids = [e.entry_id.value for e in twin.evidence_history]
        if len(entry_ids) != len(set(entry_ids)):
            return False
        intervention_entry_ids = [e.entry_id.value for e in twin.intervention_history]
        if len(intervention_entry_ids) != len(set(intervention_entry_ids)):
            return False
        concept_ids = [c.concept_id.value for c in twin.concept_states]
        if len(concept_ids) != len(set(concept_ids)):
            return False
        misc_ids = [m.misconception_id.value for m in twin.misconception_states]
        if len(misc_ids) != len(set(misc_ids)):
            return False
        # Trajectory must have at least the creation point for living twins.
        if twin.trajectory.length() < 1:
            return False
        return True

    def assert_satisfied_by(self, twin: EducationalDigitalTwin) -> None:
        if not self.is_satisfied_by(twin):
            raise EducationalInvariantViolation(
                "educational digital twin is not consistent",
                invariant="TwinIsConsistentSpecification.unsatisfied",
            )
