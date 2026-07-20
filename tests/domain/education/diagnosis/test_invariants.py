"""Invariant tests for EducationalDiagnosis aggregate."""

from __future__ import annotations

import pytest

from domain.education.diagnosis import (
    DiagnosisSeverityLevel,
    EducationalScopeKind,
    IndicatorKind,
)
from domain.education.foundation.enums import ConfidenceLevel, DiagnosisType
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import EvidenceId
from tests.domain.education.diagnosis.conftest import (
    EVIDENCE_001,
    EVIDENCE_002,
    EVIDENCE_003,
    INTERP_002,
    make_confidence,
    make_diagnosis,
    make_indicator,
    make_reason,
    make_scope,
    make_severity,
)


def test_must_reference_interpretation() -> None:
    # Indicator construction itself requires interpretation; empty indicators
    # rejected at aggregate level.
    with pytest.raises(EducationalInvariantViolation):
        make_diagnosis(indicators=[])


def test_must_reference_evidence() -> None:
    with pytest.raises(EducationalInvariantViolation):
        make_indicator(evidence_ids=())


def test_must_possess_confidence() -> None:
    with pytest.raises(EducationalInvariantViolation):
        from domain.education.diagnosis import EducationalDiagnosis
        from domain.education.foundation.ids import DiagnosisId

        EducationalDiagnosis.create(
            diagnosis_id=DiagnosisId("diag-no-conf"),
            student_id="student-ada",
            diagnosis_type=DiagnosisType.CONCEPTUAL_MISUNDERSTANDING,
            scope=make_scope(),
            confidence="high",  # type: ignore[arg-type]
            severity=make_severity(),
            indicators=[make_indicator()],
            reasons=[make_reason()],
        )


def test_must_possess_severity() -> None:
    with pytest.raises(EducationalInvariantViolation):
        from domain.education.diagnosis import EducationalDiagnosis
        from domain.education.foundation.ids import DiagnosisId

        EducationalDiagnosis.create(
            diagnosis_id=DiagnosisId("diag-no-sev"),
            student_id="student-ada",
            diagnosis_type=DiagnosisType.CONCEPTUAL_MISUNDERSTANDING,
            scope=make_scope(),
            confidence=make_confidence(),
            severity="moderate",  # type: ignore[arg-type]
            indicators=[make_indicator()],
            reasons=[make_reason()],
        )


def test_must_identify_educational_scope() -> None:
    with pytest.raises(EducationalInvariantViolation):
        from domain.education.diagnosis import EducationalDiagnosis
        from domain.education.foundation.ids import DiagnosisId

        EducationalDiagnosis.create(
            diagnosis_id=DiagnosisId("diag-no-scope"),
            student_id="student-ada",
            diagnosis_type=DiagnosisType.CONCEPTUAL_MISUNDERSTANDING,
            scope="vague",  # type: ignore[arg-type]
            confidence=make_confidence(),
            severity=make_severity(),
            indicators=[make_indicator()],
            reasons=[make_reason()],
        )


def test_cannot_duplicate_reasons() -> None:
    with pytest.raises(EducationalInvariantViolation):
        make_diagnosis(
            reasons=[
                make_reason(reason_id="a", statement="Same educational warrant"),
                make_reason(reason_id="b", statement="Same educational warrant"),
            ]
        )


def test_cannot_contradict_itself_via_reason() -> None:
    with pytest.raises(EducationalInvariantViolation):
        make_diagnosis(
            diagnosis_type=DiagnosisType.PREREQUISITE_GAP,
            reasons=[
                make_reason(statement="Not a prerequisite gap in this case"),
            ],
        )


def test_cannot_contradict_itself_via_indicator() -> None:
    with pytest.raises(EducationalInvariantViolation):
        make_diagnosis(
            diagnosis_type=DiagnosisType.LOW_CONFIDENCE,
            indicators=[
                make_indicator(
                    kind=IndicatorKind.OVERESTIMATED_CAPACITY,
                    description="Overestimates capacity",
                )
            ],
            confidence=make_confidence(ConfidenceLevel.MEDIUM),
            severity=make_severity(DiagnosisSeverityLevel.MODERATE),
        )


def test_cannot_exist_without_support() -> None:
    with pytest.raises(EducationalInvariantViolation):
        make_diagnosis(indicators=[])


def test_duplicate_support_rejected() -> None:
    with pytest.raises(EducationalInvariantViolation):
        make_diagnosis(
            indicators=[
                make_indicator(indicator_id="a"),
                make_indicator(indicator_id="b"),
            ]
        )


def test_unknown_evidence_rejected() -> None:
    with pytest.raises(EducationalInvariantViolation):
        make_diagnosis(
            indicators=[
                make_indicator(
                    evidence_ids=(EVIDENCE_001, EvidenceId("evidence-ghost"))
                )
            ]
        )


def test_unknown_interpretation_rejected() -> None:
    with pytest.raises(EducationalInvariantViolation):
        make_diagnosis(
            indicators=[
                make_indicator(interpretation_ids=("interp-ghost",)),
            ]
        )


def test_scope_statement_required() -> None:
    diagnosis = make_diagnosis(
        scope=make_scope(
            statement="Relative to objective, transfer collapses under variation",
            scope_kind=EducationalScopeKind.LEARNING_OBJECTIVE,
        )
    )
    assert diagnosis.scope.statement


@pytest.mark.parametrize("diagnosis_type", list(DiagnosisType))
def test_all_catalogue_types_constructible(diagnosis_type: DiagnosisType) -> None:
    diagnosis = make_diagnosis(
        diagnosis_id=f"diag-inv-{diagnosis_type.value}",
        diagnosis_type=diagnosis_type,
    )
    assert diagnosis.diagnosis_type is diagnosis_type
    assert diagnosis.supporting_interpretation_ids()
    assert diagnosis.supporting_evidence_ids()


def test_support_consistency_across_merge_reject_duplicate() -> None:
    primary = make_diagnosis(diagnosis_id="primary")
    other = make_diagnosis(diagnosis_id="other")
    with pytest.raises(EducationalInvariantViolation):
        primary.merge_support(other)


def test_confidence_validation_unknown_rejected() -> None:
    with pytest.raises(EducationalInvariantViolation):
        make_confidence(ConfidenceLevel.UNKNOWN)


@pytest.mark.parametrize("level", list(DiagnosisSeverityLevel))
def test_severity_validation_all_levels(level: DiagnosisSeverityLevel) -> None:
    diagnosis = make_diagnosis(
        diagnosis_id=f"diag-sev-{level.value}",
        severity=make_severity(level),
        confidence=make_confidence(ConfidenceLevel.MEDIUM),
    )
    assert diagnosis.severity.level is level


def test_revised_retains_invariants() -> None:
    diagnosis = make_diagnosis()
    diagnosis.revise(
        indicators=[
            make_indicator(
                indicator_id="ind-rev",
                interpretation_ids=(INTERP_002,),
                evidence_ids=(EVIDENCE_002, EVIDENCE_003),
                description="Revised warrant from second interpretation",
            )
        ],
        reasons=[
            make_reason(
                reason_id="r-rev",
                statement="Revised educational warrant",
            )
        ],
    )
    assert diagnosis.is_revised()
    assert diagnosis.has_interpretation(INTERP_002)
    assert diagnosis.has_evidence(EVIDENCE_002)
