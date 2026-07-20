"""Policy aligning Teaching Intention with Priority and Diagnosis.

Architecture Source
    TEACHING_INTENTION_MODEL.md
Concept
    Intention Alignment Policy
"""

from __future__ import annotations

from domain.education.foundation.enums import DiagnosisType, TeachingIntentionType
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.teaching_intention.entities.intention_reference import (
    DiagnosisReference,
    PriorityReference,
)

# Primary + specialised lawful mappings (Teaching Intention Model §7).
_LAWFUL_BY_DIAGNOSIS: dict[DiagnosisType, frozenset[TeachingIntentionType]] = {
    DiagnosisType.CONCEPTUAL_MISUNDERSTANDING: frozenset(
        {
            TeachingIntentionType.BUILD_INTUITION,
            TeachingIntentionType.CONSOLIDATE_UNDERSTANDING,
        }
    ),
    DiagnosisType.PROCEDURAL_WEAKNESS: frozenset(
        {
            TeachingIntentionType.INCREASE_PROCEDURAL_FLUENCY,
        }
    ),
    DiagnosisType.WEAK_RETENTION: frozenset(
        {
            TeachingIntentionType.IMPROVE_RETENTION,
        }
    ),
    DiagnosisType.KNOWLEDGE_FRAGMENTATION: frozenset(
        {
            TeachingIntentionType.CONNECT_FRAGMENTED_KNOWLEDGE,
            TeachingIntentionType.CONSOLIDATE_UNDERSTANDING,
        }
    ),
    DiagnosisType.PREREQUISITE_GAP: frozenset(
        {
            TeachingIntentionType.STRENGTHEN_PREREQUISITE,
        }
    ),
    DiagnosisType.MISCONCEPTION: frozenset(
        {
            TeachingIntentionType.REPAIR_MISCONCEPTION,
        }
    ),
    DiagnosisType.LOW_CONFIDENCE: frozenset(
        {
            TeachingIntentionType.RECOVER_CONFIDENCE,
        }
    ),
    DiagnosisType.FALSE_CONFIDENCE: frozenset(
        {
            TeachingIntentionType.CALIBRATE_CONFIDENCE_DOWNWARD,
        }
    ),
    DiagnosisType.EXAM_TECHNIQUE_WEAKNESS: frozenset(
        {
            TeachingIntentionType.PREPARE_FOR_EXAMINATION,
        }
    ),
    DiagnosisType.APPLICATION_WEAKNESS: frozenset(
        {
            TeachingIntentionType.STRENGTHEN_APPLICATION,
            TeachingIntentionType.IMPROVE_TRANSFER,
        }
    ),
    DiagnosisType.TRANSFER_WEAKNESS: frozenset(
        {
            TeachingIntentionType.IMPROVE_TRANSFER,
        }
    ),
    DiagnosisType.INCOMPLETE_UNDERSTANDING: frozenset(
        {
            TeachingIntentionType.CONSOLIDATE_UNDERSTANDING,
            TeachingIntentionType.COMPLETE_MISSING_FACETS,
            TeachingIntentionType.BUILD_INTUITION,
        }
    ),
}


class IntentionAlignmentPolicy:
    """Ensures Teaching Intention does not contradict Priority / Diagnosis.

    Alignment answers whether the named educational change is a lawful
    response to the referenced diagnoses under the Priority. It does not
    choose teaching strategies or construct episodes.
    """

    @staticmethod
    def lawful_intention_types_for(
        diagnosis_type: DiagnosisType,
    ) -> frozenset[TeachingIntentionType]:
        if not isinstance(diagnosis_type, DiagnosisType):
            raise EducationalInvariantViolation(
                "diagnosis_type must be a DiagnosisType",
                invariant="IntentionAlignmentPolicy.diagnosis_type.type",
            )
        return _LAWFUL_BY_DIAGNOSIS[diagnosis_type]

    @staticmethod
    def is_type_aligned_with_diagnosis(
        intention_type: TeachingIntentionType,
        diagnosis_type: DiagnosisType,
    ) -> bool:
        return (
            intention_type
            in IntentionAlignmentPolicy.lawful_intention_types_for(diagnosis_type)
        )

    @staticmethod
    def assert_aligned_with_diagnoses(
        intention_type: TeachingIntentionType,
        diagnosis_references: tuple[DiagnosisReference, ...]
        | list[DiagnosisReference],
    ) -> None:
        """Reject intention types that contradict referenced diagnoses.

        When multiple diagnoses are referenced, the intention must be lawful
        for at least one (primary) diagnosis. Exam preparation must not be
        paired solely with misconception without repair alignment.
        """
        if not diagnosis_references:
            raise EducationalInvariantViolation(
                "alignment requires at least one diagnosis reference",
                invariant="IntentionAlignmentPolicy.diagnosis_references.min_one",
            )
        aligned = any(
            IntentionAlignmentPolicy.is_type_aligned_with_diagnosis(
                intention_type, ref.diagnosis_type
            )
            for ref in diagnosis_references
        )
        if not aligned:
            types = ", ".join(
                sorted({ref.diagnosis_type.value for ref in diagnosis_references})
            )
            raise EducationalInvariantViolation(
                f"intention type {intention_type.value} is not aligned with "
                f"referenced diagnosis types ({types})",
                invariant="IntentionAlignmentPolicy.diagnosis_alignment",
            )
        IntentionAlignmentPolicy._assert_no_exam_over_misconception(
            intention_type, diagnosis_references
        )

    @staticmethod
    def _assert_no_exam_over_misconception(
        intention_type: TeachingIntentionType,
        diagnosis_references: tuple[DiagnosisReference, ...]
        | list[DiagnosisReference],
    ) -> None:
        diagnosis_types = {ref.diagnosis_type for ref in diagnosis_references}
        if (
            intention_type is TeachingIntentionType.PREPARE_FOR_EXAMINATION
            and DiagnosisType.MISCONCEPTION in diagnosis_types
            and DiagnosisType.EXAM_TECHNIQUE_WEAKNESS not in diagnosis_types
        ):
            raise EducationalInvariantViolation(
                "cannot adopt exam preparation intention while misconception "
                "remains the governing diagnosis without exam-technique need",
                invariant="IntentionAlignmentPolicy.exam_vs_misconception",
            )

    @staticmethod
    def assert_priority_not_contradicted(
        priority_references: tuple[PriorityReference, ...] | list[PriorityReference],
        diagnosis_references: tuple[DiagnosisReference, ...]
        | list[DiagnosisReference],
        intention_type: TeachingIntentionType,
    ) -> None:
        """Priority is the governing instructional order; intention must honour it.

        Contradiction means: missing priority reference, or intention type
        unlawful for every referenced diagnosis that the priority surfaces.
        """
        if not priority_references:
            raise EducationalInvariantViolation(
                "teaching intention cannot contradict Priority "
                "(priority reference required)",
                invariant="IntentionAlignmentPolicy.priority.required",
            )
        IntentionAlignmentPolicy.assert_aligned_with_diagnoses(
            intention_type, diagnosis_references
        )

    @staticmethod
    def is_aligned(
        intention_type: TeachingIntentionType,
        priority_references: tuple[PriorityReference, ...] | list[PriorityReference],
        diagnosis_references: tuple[DiagnosisReference, ...]
        | list[DiagnosisReference],
    ) -> bool:
        try:
            IntentionAlignmentPolicy.assert_priority_not_contradicted(
                priority_references,
                diagnosis_references,
                intention_type,
            )
        except EducationalInvariantViolation:
            return False
        return True
