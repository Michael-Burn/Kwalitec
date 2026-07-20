"""Policy tests for diagnosis validation and consistency."""

from __future__ import annotations

import pytest

from domain.education.diagnosis import (
    DiagnosisConsistencyPolicy,
    DiagnosisSeverityLevel,
    DiagnosisStatus,
    DiagnosisValidationPolicy,
    IndicatorKind,
)
from domain.education.foundation.enums import ConfidenceLevel, DiagnosisType
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import EvidenceId
from tests.domain.education.diagnosis.conftest import (
    EVIDENCE_001,
    EVIDENCE_002,
    INTERP_001,
    INTERP_002,
    PRIMARY_INDICATOR_FOR_TYPE,
    make_confidence,
    make_indicator,
    make_reason,
    make_severity,
)


def test_assert_indicators_rejects_empty() -> None:
    with pytest.raises(EducationalInvariantViolation):
        DiagnosisValidationPolicy.assert_indicators([])


def test_assert_reasons_rejects_empty() -> None:
    with pytest.raises(EducationalInvariantViolation):
        DiagnosisValidationPolicy.assert_reasons([])


def test_assert_indicators_rejects_duplicate_id() -> None:
    with pytest.raises(EducationalInvariantViolation):
        DiagnosisValidationPolicy.assert_indicators(
            [
                make_indicator(indicator_id="same"),
                make_indicator(
                    indicator_id="same",
                    interpretation_ids=(INTERP_002,),
                    evidence_ids=(EVIDENCE_002,),
                ),
            ]
        )


def test_assert_indicators_rejects_identical_support() -> None:
    with pytest.raises(EducationalInvariantViolation):
        DiagnosisValidationPolicy.assert_indicators(
            [
                make_indicator(indicator_id="a"),
                make_indicator(indicator_id="b"),
            ]
        )


def test_assert_reasons_rejects_duplicate_signature() -> None:
    with pytest.raises(EducationalInvariantViolation):
        DiagnosisValidationPolicy.assert_reasons(
            [
                make_reason(reason_id="a", statement="Same warrant", code="x"),
                make_reason(reason_id="b", statement="Same warrant", code="x"),
            ]
        )


def test_assert_known_evidence_rejects_unknown() -> None:
    with pytest.raises(EducationalInvariantViolation):
        DiagnosisValidationPolicy.assert_known_evidence(
            frozenset({EVIDENCE_001}),
            frozenset({EVIDENCE_001, EvidenceId("evidence-unknown")}),
        )


def test_assert_known_interpretations_rejects_unknown() -> None:
    with pytest.raises(EducationalInvariantViolation):
        DiagnosisValidationPolicy.assert_known_interpretations(
            frozenset({INTERP_001}),
            frozenset({INTERP_001, "interp-unknown"}),
        )


def test_assert_mutable_rejects_invalidated() -> None:
    with pytest.raises(EducationalInvariantViolation):
        DiagnosisValidationPolicy.assert_mutable(
            DiagnosisStatus.INVALIDATED, action="revise"
        )


@pytest.mark.parametrize("diagnosis_type", list(DiagnosisType))
def test_compatible_indicators_per_type(diagnosis_type: DiagnosisType) -> None:
    kind = PRIMARY_INDICATOR_FOR_TYPE[diagnosis_type]
    indicator = make_indicator(
        kind=kind,
        diagnosis_type=diagnosis_type,
        description=f"Compatible {kind.value}",
    )
    DiagnosisConsistencyPolicy.assert_indicators_compatible(
        diagnosis_type, (indicator,)
    )


@pytest.mark.parametrize(
    ("diagnosis_type", "bad_kind"),
    [
        (DiagnosisType.LOW_CONFIDENCE, IndicatorKind.OVERESTIMATED_CAPACITY),
        (DiagnosisType.FALSE_CONFIDENCE, IndicatorKind.UNDERESTIMATED_CAPACITY),
        (DiagnosisType.MISCONCEPTION, IndicatorKind.EXECUTION_FAILURE),
        (DiagnosisType.WEAK_RETENTION, IndicatorKind.TIMED_DEPLOYMENT_FAILURE),
    ],
)
def test_incompatible_or_contradictory_indicators(
    diagnosis_type: DiagnosisType, bad_kind: IndicatorKind
) -> None:
    indicator = make_indicator(
        kind=bad_kind,
        description=f"Bad {bad_kind.value}",
    )
    with pytest.raises(EducationalInvariantViolation):
        DiagnosisConsistencyPolicy.assert_indicators_compatible(
            diagnosis_type, (indicator,)
        )


def test_reason_negation_contradiction() -> None:
    with pytest.raises(EducationalInvariantViolation):
        DiagnosisConsistencyPolicy.assert_reasons_consistent(
            DiagnosisType.MISCONCEPTION,
            (make_reason(statement="Not a misconception after all"),),
        )


def test_very_high_confidence_requires_two_indicators() -> None:
    with pytest.raises(EducationalInvariantViolation):
        DiagnosisConsistencyPolicy.assert_confidence_severity_alignment(
            make_confidence(ConfidenceLevel.VERY_HIGH),
            make_severity(DiagnosisSeverityLevel.MODERATE),
            (make_indicator(),),
        )


def test_soft_support_cannot_warrant_severe_high() -> None:
    with pytest.raises(EducationalInvariantViolation):
        DiagnosisConsistencyPolicy.assert_confidence_severity_alignment(
            make_confidence(ConfidenceLevel.HIGH),
            make_severity(DiagnosisSeverityLevel.SEVERE),
            (
                make_indicator(
                    kind=IndicatorKind.UNDERESTIMATED_CAPACITY,
                    description="Underestimates capacity",
                ),
            ),
        )


def test_assert_consistent_happy_path() -> None:
    DiagnosisConsistencyPolicy.assert_consistent(
        DiagnosisType.CONCEPTUAL_MISUNDERSTANDING,
        (make_indicator(),),
        (make_reason(),),
        make_confidence(ConfidenceLevel.HIGH),
        make_severity(DiagnosisSeverityLevel.MODERATE),
    )


def test_compatible_indicator_kinds_helper() -> None:
    kinds = DiagnosisConsistencyPolicy.compatible_indicator_kinds(
        DiagnosisType.TRANSFER_WEAKNESS
    )
    assert IndicatorKind.VARIANT_TRANSFER_FAILURE in kinds


@pytest.mark.parametrize("status", list(DiagnosisStatus))
def test_assert_status(status: DiagnosisStatus) -> None:
    assert DiagnosisValidationPolicy.assert_status(status) is status
