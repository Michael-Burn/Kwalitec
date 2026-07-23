"""Specification: a MasteryAssessment's aggregates agree with its parts.

Architecture Source
    KNOWLEDGE_AND_MASTERY_EDUCATIONAL_MODEL.md
Concept
    Mastery Assessment Consistency Specification
"""

from __future__ import annotations

from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.mastery_estimation.aggregates.mastery_assessment import (
    MasteryAssessment,
)
from domain.education.mastery_estimation.policies.confidence_policy import (
    ConfidencePolicy,
)
from domain.education.mastery_estimation.policies.mastery_policy import (
    MasteryPolicy,
)
from domain.education.mastery_estimation.policies.stability_policy import (
    StabilityPolicy,
)

_TOLERANCE = 1e-6


class MasteryAssessmentConsistencySpecification:
    """A MasteryAssessment's overall figures must derive from its subjects.

    Verifies the aggregate's own invariant: overall mastery, confidence,
    and stability are always the same evidence-count-weighted aggregation
    over ``subject_assessments`` that ``MasteryPolicy``/``ConfidencePolicy``/
    ``StabilityPolicy`` would recompute — never independently supplied
    figures that could silently drift from the parts they summarise.
    """

    @staticmethod
    def is_satisfied_by(assessment: MasteryAssessment) -> bool:
        subject_scores = [a.mastery for a in assessment.subject_assessments]
        subject_confidences = [a.confidence for a in assessment.subject_assessments]
        subject_stabilities = [a.stability for a in assessment.subject_assessments]

        expected_mastery = MasteryPolicy.aggregate_subject_scores(subject_scores)
        expected_confidence = ConfidencePolicy.aggregate_subject_confidence(
            subject_confidences
        )
        expected_stability = StabilityPolicy.aggregate_subject_stability(
            subject_stabilities
        )

        return (
            abs(assessment.overall_mastery.magnitude - expected_mastery.magnitude)
            <= _TOLERANCE
            and assessment.overall_mastery.evidence_count
            == expected_mastery.evidence_count
            and abs(
                assessment.overall_confidence.score.magnitude
                - expected_confidence.score.magnitude
            )
            <= _TOLERANCE
            and abs(
                assessment.overall_stability.magnitude
                - expected_stability.magnitude
            )
            <= _TOLERANCE
        )

    @staticmethod
    def assert_satisfied_by(assessment: MasteryAssessment) -> None:
        if not MasteryAssessmentConsistencySpecification.is_satisfied_by(assessment):
            raise EducationalInvariantViolation(
                "overall mastery/confidence/stability must be the "
                "evidence-weighted aggregation of subject_assessments",
                invariant="MasteryAssessmentConsistencySpecification.aggregation",
            )
