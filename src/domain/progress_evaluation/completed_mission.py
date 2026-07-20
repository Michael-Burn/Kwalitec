"""CompletedMission — educational input declaring a finished mission.

Architecture Source
    EDUCATIONAL_ORCHESTRATION_MODEL.md
    SESSION_ASSEMBLY_MODEL.md
Concept
    Completed Mission
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import (
    EducationalValueObject,
    require_non_empty_text,
)
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import ConceptId, EvidenceId
from domain.mission_generation.ids import MissionSpecificationId


@dataclass(frozen=True, slots=True)
class CompletedMission(EducationalValueObject):
    """Immutable record that a MissionSpecification was completed.

    Outcome millipoints (0–1000) express success strength without inventing
    mastery. Sequence orders completions deterministically for evaluation.
    """

    mission_id: MissionSpecificationId
    student_id: str
    completion_sequence: int
    success: bool
    outcome_millipoints: int = 1000
    concept_ids: tuple[ConceptId, ...] = ()
    evidence_ids: tuple[EvidenceId, ...] = ()

    def _validate(self) -> None:
        if not isinstance(self.mission_id, MissionSpecificationId):
            raise EducationalInvariantViolation(
                "mission_id must be a MissionSpecificationId",
                invariant="CompletedMission.mission_id.type",
            )
        object.__setattr__(
            self,
            "student_id",
            require_non_empty_text(self.student_id, "student_id"),
        )
        if not isinstance(self.completion_sequence, int) or isinstance(
            self.completion_sequence, bool
        ):
            raise EducationalInvariantViolation(
                "completion_sequence must be an integer",
                invariant="CompletedMission.completion_sequence.type",
            )
        if self.completion_sequence < 1:
            raise EducationalInvariantViolation(
                "completion_sequence must be a positive integer",
                invariant="CompletedMission.completion_sequence.positive",
            )
        if not isinstance(self.success, bool):
            raise EducationalInvariantViolation(
                "success must be a boolean",
                invariant="CompletedMission.success.type",
            )
        if not isinstance(self.outcome_millipoints, int) or isinstance(
            self.outcome_millipoints, bool
        ):
            raise EducationalInvariantViolation(
                "outcome_millipoints must be an integer",
                invariant="CompletedMission.outcome_millipoints.type",
            )
        if self.outcome_millipoints < 0 or self.outcome_millipoints > 1000:
            raise EducationalInvariantViolation(
                "outcome_millipoints must be between 0 and 1000 inclusive",
                invariant="CompletedMission.outcome_millipoints.range",
            )
        if not self.success and self.outcome_millipoints > 499:
            raise EducationalInvariantViolation(
                "unsuccessful missions must declare outcome_millipoints <= 499",
                invariant="CompletedMission.outcome_millipoints.unsuccessful",
            )
        if self.success and self.outcome_millipoints < 500:
            raise EducationalInvariantViolation(
                "successful missions must declare outcome_millipoints >= 500",
                invariant="CompletedMission.outcome_millipoints.successful",
            )
        if not isinstance(self.concept_ids, tuple):
            raise EducationalInvariantViolation(
                "concept_ids must be a tuple",
                invariant="CompletedMission.concept_ids.type",
            )
        for concept_id in self.concept_ids:
            if not isinstance(concept_id, ConceptId):
                raise EducationalInvariantViolation(
                    "concept_ids must contain ConceptId values",
                    invariant="CompletedMission.concept_ids.item_type",
                )
        if not isinstance(self.evidence_ids, tuple):
            raise EducationalInvariantViolation(
                "evidence_ids must be a tuple",
                invariant="CompletedMission.evidence_ids.type",
            )
        for evidence_id in self.evidence_ids:
            if not isinstance(evidence_id, EvidenceId):
                raise EducationalInvariantViolation(
                    "evidence_ids must contain EvidenceId values",
                    invariant="CompletedMission.evidence_ids.item_type",
                )
