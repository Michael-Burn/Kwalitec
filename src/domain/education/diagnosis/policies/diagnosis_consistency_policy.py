"""Policy governing internal consistency of an educational diagnosis.

Architecture Source
    EDUCATIONAL_DIAGNOSIS_MODEL.md
Concept
    Diagnosis Consistency Policy
"""

from __future__ import annotations

from domain.education.diagnosis.entities.diagnosis_indicator import DiagnosisIndicator
from domain.education.diagnosis.entities.diagnosis_reason import DiagnosisReason
from domain.education.diagnosis.enums import DiagnosisSeverityLevel, IndicatorKind
from domain.education.diagnosis.value_objects.diagnosis_confidence import (
    DiagnosisConfidence,
)
from domain.education.diagnosis.value_objects.diagnosis_severity import (
    DiagnosisSeverity,
)
from domain.education.foundation.enums import ConfidenceLevel, DiagnosisType
from domain.education.foundation.errors import EducationalInvariantViolation

# Indicator kinds that lawfully support each deficiency category.
_COMPATIBLE_INDICATORS: dict[DiagnosisType, frozenset[IndicatorKind]] = {
    DiagnosisType.CONCEPTUAL_MISUNDERSTANDING: frozenset(
        {
            IndicatorKind.FRAGILE_EXPLANATION,
            IndicatorKind.PARTIAL_FACET_GRASP,
            IndicatorKind.CONFLICTING_SIGNAL,
        }
    ),
    DiagnosisType.PROCEDURAL_WEAKNESS: frozenset(
        {
            IndicatorKind.EXECUTION_FAILURE,
            IndicatorKind.TASK_APPLICATION_FAILURE,
            IndicatorKind.CONFLICTING_SIGNAL,
        }
    ),
    DiagnosisType.WEAK_RETENTION: frozenset(
        {
            IndicatorKind.DELAYED_RETRIEVAL_COLLAPSE,
            IndicatorKind.CONFLICTING_SIGNAL,
        }
    ),
    DiagnosisType.KNOWLEDGE_FRAGMENTATION: frozenset(
        {
            IndicatorKind.ISOLATED_LOCAL_SUCCESS,
            IndicatorKind.VARIANT_TRANSFER_FAILURE,
            IndicatorKind.CONFLICTING_SIGNAL,
        }
    ),
    DiagnosisType.PREREQUISITE_GAP: frozenset(
        {
            IndicatorKind.UPSTREAM_CAPABILITY_ABSENCE,
            IndicatorKind.FRAGILE_EXPLANATION,
            IndicatorKind.CONFLICTING_SIGNAL,
        }
    ),
    DiagnosisType.MISCONCEPTION: frozenset(
        {
            IndicatorKind.STABLE_WRONG_MODEL,
            IndicatorKind.PATTERNED_ERROR,
            IndicatorKind.CONFLICTING_SIGNAL,
        }
    ),
    DiagnosisType.LOW_CONFIDENCE: frozenset(
        {
            IndicatorKind.UNDERESTIMATED_CAPACITY,
            IndicatorKind.CONFLICTING_SIGNAL,
        }
    ),
    DiagnosisType.FALSE_CONFIDENCE: frozenset(
        {
            IndicatorKind.OVERESTIMATED_CAPACITY,
            IndicatorKind.CONFLICTING_SIGNAL,
        }
    ),
    DiagnosisType.EXAM_TECHNIQUE_WEAKNESS: frozenset(
        {
            IndicatorKind.TIMED_DEPLOYMENT_FAILURE,
            IndicatorKind.CONFLICTING_SIGNAL,
        }
    ),
    DiagnosisType.APPLICATION_WEAKNESS: frozenset(
        {
            IndicatorKind.TASK_APPLICATION_FAILURE,
            IndicatorKind.EXECUTION_FAILURE,
            IndicatorKind.CONFLICTING_SIGNAL,
        }
    ),
    DiagnosisType.TRANSFER_WEAKNESS: frozenset(
        {
            IndicatorKind.VARIANT_TRANSFER_FAILURE,
            IndicatorKind.ISOLATED_LOCAL_SUCCESS,
            IndicatorKind.CONFLICTING_SIGNAL,
        }
    ),
    DiagnosisType.INCOMPLETE_UNDERSTANDING: frozenset(
        {
            IndicatorKind.PARTIAL_FACET_GRASP,
            IndicatorKind.FRAGILE_EXPLANATION,
            IndicatorKind.CONFLICTING_SIGNAL,
        }
    ),
}

# Direct contradictions: indicator kinds that deny the named deficiency class.
_CONTRADICTORY_INDICATORS: dict[DiagnosisType, frozenset[IndicatorKind]] = {
    DiagnosisType.LOW_CONFIDENCE: frozenset({IndicatorKind.OVERESTIMATED_CAPACITY}),
    DiagnosisType.FALSE_CONFIDENCE: frozenset({IndicatorKind.UNDERESTIMATED_CAPACITY}),
    DiagnosisType.MISCONCEPTION: frozenset({IndicatorKind.UNDERESTIMATED_CAPACITY}),
    DiagnosisType.WEAK_RETENTION: frozenset({IndicatorKind.OVERESTIMATED_CAPACITY}),
}

# Reason statement fragments that negate specific deficiency categories.
_NEGATION_FRAGMENTS: dict[DiagnosisType, tuple[str, ...]] = {
    DiagnosisType.CONCEPTUAL_MISUNDERSTANDING: (
        "not a conceptual misunderstanding",
        "not conceptual misunderstanding",
        "adequate conceptual grasp",
    ),
    DiagnosisType.PROCEDURAL_WEAKNESS: (
        "not a procedural weakness",
        "not procedural weakness",
        "adequate procedural fluency",
    ),
    DiagnosisType.WEAK_RETENTION: (
        "not weak retention",
        "retention is intact",
        "not a retention problem",
    ),
    DiagnosisType.KNOWLEDGE_FRAGMENTATION: (
        "not knowledge fragmentation",
        "knowledge is integrated",
    ),
    DiagnosisType.PREREQUISITE_GAP: (
        "not a prerequisite gap",
        "prerequisites are intact",
        "no prerequisite gap",
    ),
    DiagnosisType.MISCONCEPTION: (
        "not a misconception",
        "not proven misconception",
        "no misconception",
    ),
    DiagnosisType.LOW_CONFIDENCE: (
        "not low confidence",
        "confidence is calibrated",
        "not under-confident",
    ),
    DiagnosisType.FALSE_CONFIDENCE: (
        "not false confidence",
        "confidence is calibrated",
        "not overconfident",
    ),
    DiagnosisType.EXAM_TECHNIQUE_WEAKNESS: (
        "not exam technique",
        "not an exam technique weakness",
    ),
    DiagnosisType.APPLICATION_WEAKNESS: (
        "not an application weakness",
        "not application weakness",
        "application is adequate",
    ),
    DiagnosisType.TRANSFER_WEAKNESS: (
        "not a transfer weakness",
        "not transfer weakness",
        "transfer is intact",
    ),
    DiagnosisType.INCOMPLETE_UNDERSTANDING: (
        "not incomplete understanding",
        "understanding is complete",
    ),
}

class DiagnosisConsistencyPolicy:
    """Enforces that a diagnosis does not contradict itself.

    Consistency concerns educational coherence of type, indicators, reasons,
    confidence, and severity. It does not prioritise, recommend, or hypothesise.
    """

    @staticmethod
    def assert_indicators_compatible(
        diagnosis_type: DiagnosisType,
        indicators: tuple[DiagnosisIndicator, ...] | list[DiagnosisIndicator],
    ) -> None:
        allowed = _COMPATIBLE_INDICATORS[diagnosis_type]
        contradictory = _CONTRADICTORY_INDICATORS.get(diagnosis_type, frozenset())
        for indicator in indicators:
            if indicator.kind in contradictory:
                raise EducationalInvariantViolation(
                    f"indicator {indicator.kind.value} contradicts diagnosis "
                    f"type {diagnosis_type.value}",
                    invariant="DiagnosisConsistencyPolicy.indicator.contradiction",
                )
            if indicator.kind not in allowed:
                raise EducationalInvariantViolation(
                    f"indicator {indicator.kind.value} is incompatible with "
                    f"diagnosis type {diagnosis_type.value}",
                    invariant="DiagnosisConsistencyPolicy.indicator.compatible",
                )

    @staticmethod
    def assert_reasons_consistent(
        diagnosis_type: DiagnosisType,
        reasons: tuple[DiagnosisReason, ...] | list[DiagnosisReason],
    ) -> None:
        negations = _NEGATION_FRAGMENTS.get(diagnosis_type, ())
        for reason in reasons:
            lowered = reason.statement.casefold()
            for fragment in negations:
                if fragment in lowered:
                    raise EducationalInvariantViolation(
                        "diagnosis cannot contradict itself: reason negates "
                        f"diagnosis type {diagnosis_type.value}",
                        invariant="DiagnosisConsistencyPolicy.reason.contradiction",
                    )

    @staticmethod
    def assert_confidence_severity_alignment(
        confidence: DiagnosisConfidence,
        severity: DiagnosisSeverity,
        indicators: tuple[DiagnosisIndicator, ...] | list[DiagnosisIndicator],
    ) -> None:
        """Very high confidence requires adequate support breadth."""
        if confidence.level is ConfidenceLevel.VERY_HIGH and len(indicators) < 2:
            raise EducationalInvariantViolation(
                "VERY_HIGH diagnosis confidence requires at least two "
                "supporting indicators",
                invariant="DiagnosisConsistencyPolicy.confidence.support_breadth",
            )
        # Soft metacognitive-only support cannot alone warrant severe severity
        # at very high confidence.
        soft_only = all(
            i.kind
            in {
                IndicatorKind.UNDERESTIMATED_CAPACITY,
                IndicatorKind.OVERESTIMATED_CAPACITY,
                IndicatorKind.CONFLICTING_SIGNAL,
            }
            for i in indicators
        )
        if (
            soft_only
            and severity.is_at_least(DiagnosisSeverityLevel.SEVERE)
            and confidence.is_at_least(ConfidenceLevel.HIGH)
        ):
            raise EducationalInvariantViolation(
                "soft metacognitive indicators alone cannot warrant "
                "SEVERE severity at HIGH or greater confidence",
                invariant="DiagnosisConsistencyPolicy.soft_support.severity",
            )

    @staticmethod
    def assert_consistent(
        diagnosis_type: DiagnosisType,
        indicators: tuple[DiagnosisIndicator, ...] | list[DiagnosisIndicator],
        reasons: tuple[DiagnosisReason, ...] | list[DiagnosisReason],
        confidence: DiagnosisConfidence,
        severity: DiagnosisSeverity,
    ) -> None:
        DiagnosisConsistencyPolicy.assert_indicators_compatible(
            diagnosis_type, indicators
        )
        DiagnosisConsistencyPolicy.assert_reasons_consistent(diagnosis_type, reasons)
        DiagnosisConsistencyPolicy.assert_confidence_severity_alignment(
            confidence, severity, indicators
        )

    @staticmethod
    def compatible_indicator_kinds(
        diagnosis_type: DiagnosisType,
    ) -> frozenset[IndicatorKind]:
        return _COMPATIBLE_INDICATORS[diagnosis_type]
