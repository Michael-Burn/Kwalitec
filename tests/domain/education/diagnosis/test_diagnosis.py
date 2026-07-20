"""Aggregate behaviour tests for EducationalDiagnosis."""

from __future__ import annotations

import pytest

from domain.education.diagnosis import (
    DiagnosisCreated,
    DiagnosisInvalidated,
    DiagnosisSeverityLevel,
    DiagnosisStatus,
    EducationalDiagnosis,
    IndicatorKind,
)
from domain.education.foundation.enums import ConfidenceLevel, DiagnosisType
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import DiagnosisId
from tests.domain.education.diagnosis.conftest import (
    EVIDENCE_001,
    EVIDENCE_002,
    EVIDENCE_003,
    INTERP_001,
    INTERP_002,
    make_confidence,
    make_diagnosis,
    make_indicator,
    make_reason,
    make_scope,
    make_severity,
)


def test_create_sets_active_and_event() -> None:
    diagnosis = make_diagnosis()
    assert diagnosis.is_active()
    assert diagnosis.status is DiagnosisStatus.ACTIVE
    events = diagnosis.pull_events()
    assert isinstance(events[0], DiagnosisCreated)


def test_revise_updates_fields() -> None:
    diagnosis = make_diagnosis()
    diagnosis.pull_events()
    diagnosis.revise(
        confidence=make_confidence(ConfidenceLevel.MEDIUM, ratio=0.55),
        severity=make_severity(DiagnosisSeverityLevel.SUBSTANTIAL),
        scope=make_scope(statement="Revised scope for incomplete facets"),
    )
    assert diagnosis.is_revised()
    assert diagnosis.confidence.level is ConfidenceLevel.MEDIUM
    assert diagnosis.severity.level is DiagnosisSeverityLevel.SUBSTANTIAL
    assert "Revised scope" in diagnosis.scope.statement


def test_revise_can_change_type_with_compatible_support() -> None:
    diagnosis = make_diagnosis(diagnosis_type=DiagnosisType.CONCEPTUAL_MISUNDERSTANDING)
    diagnosis.revise(
        diagnosis_type=DiagnosisType.INCOMPLETE_UNDERSTANDING,
        indicators=[
            make_indicator(
                kind=IndicatorKind.PARTIAL_FACET_GRASP,
                description="Partial facet grasp on boundary cases",
            )
        ],
        reasons=[
            make_reason(
                reason_id="r-incomplete",
                statement="Partial acquisition of boundary conditions",
            )
        ],
    )
    assert diagnosis.diagnosis_type is DiagnosisType.INCOMPLETE_UNDERSTANDING


def test_invalidate_is_terminal() -> None:
    diagnosis = make_diagnosis()
    diagnosis.pull_events()
    diagnosis.invalidate("contradicted by delayed probe")
    assert diagnosis.is_invalidated()
    assert isinstance(diagnosis.pull_events()[0], DiagnosisInvalidated)
    with pytest.raises(EducationalInvariantViolation):
        diagnosis.revise(confidence=make_confidence(ConfidenceLevel.LOW))
    with pytest.raises(EducationalInvariantViolation):
        diagnosis.invalidate("again")
    with pytest.raises(EducationalInvariantViolation):
        diagnosis.merge_support(make_diagnosis(diagnosis_id="other"))


def test_merge_support_absorbs_distinct_support() -> None:
    primary = make_diagnosis(diagnosis_id="primary")
    other = make_diagnosis(
        diagnosis_id="other",
        indicators=[
            make_indicator(
                indicator_id="ind-other",
                kind=IndicatorKind.PARTIAL_FACET_GRASP,
                description="Partial facet failure on assumptions",
                interpretation_ids=(INTERP_002,),
                evidence_ids=(EVIDENCE_003,),
            )
        ],
        reasons=[
            make_reason(
                reason_id="r-other",
                statement="Boundary probes reveal missing facet",
                code="boundary",
            )
        ],
    )
    primary.merge_support(other)
    assert primary.indicator_count() == 2
    assert primary.reason_count() == 2
    assert primary.has_interpretation(INTERP_002)
    assert primary.has_evidence(EVIDENCE_003)
    assert primary.is_revised()
    assert other.is_active()  # source not mutated


def test_merge_support_rejects_different_student() -> None:
    primary = make_diagnosis(diagnosis_id="primary", student_id="student-a")
    other = make_diagnosis(diagnosis_id="other", student_id="student-b")
    with pytest.raises(EducationalInvariantViolation):
        primary.merge_support(other)


def test_merge_support_rejects_different_type() -> None:
    primary = make_diagnosis(
        diagnosis_id="primary",
        diagnosis_type=DiagnosisType.MISCONCEPTION,
    )
    other = make_diagnosis(
        diagnosis_id="other",
        diagnosis_type=DiagnosisType.PROCEDURAL_WEAKNESS,
    )
    with pytest.raises(EducationalInvariantViolation):
        primary.merge_support(other)


def test_merge_support_rejects_self() -> None:
    diagnosis = make_diagnosis()
    with pytest.raises(EducationalInvariantViolation):
        diagnosis.merge_support(diagnosis)


def test_merge_support_rejects_invalidated_source() -> None:
    primary = make_diagnosis(diagnosis_id="primary")
    other = make_diagnosis(diagnosis_id="other")
    # Make other support distinct first, then invalidate
    other = make_diagnosis(
        diagnosis_id="other",
        indicators=[
            make_indicator(
                indicator_id="ind-other",
                kind=IndicatorKind.PARTIAL_FACET_GRASP,
                description="Distinct support",
                interpretation_ids=(INTERP_002,),
                evidence_ids=(EVIDENCE_003,),
            )
        ],
        reasons=[make_reason(reason_id="r-other", statement="Distinct reason")],
    )
    other.invalidate("void")
    with pytest.raises(EducationalInvariantViolation):
        primary.merge_support(other)


def test_equality_by_identity() -> None:
    a = make_diagnosis(diagnosis_id="same")
    b = make_diagnosis(diagnosis_id="same")
    assert a == b
    assert hash(a) == hash(b)


def test_queries() -> None:
    diagnosis = make_diagnosis()
    assert diagnosis.has_interpretation(INTERP_001)
    assert diagnosis.has_evidence(EVIDENCE_001)
    assert diagnosis.has_evidence(EVIDENCE_002)
    assert diagnosis.indicator_count() == 1
    assert diagnosis.reason_count() == 1
    assert "EducationalDiagnosis" in repr(diagnosis)


def test_create_classmethod_identity() -> None:
    diagnosis = EducationalDiagnosis.create(
        diagnosis_id=DiagnosisId("diag-factory"),
        student_id="student-ada",
        diagnosis_type=DiagnosisType.TRANSFER_WEAKNESS,
        scope=make_scope(),
        confidence=make_confidence(),
        severity=make_severity(),
        indicators=[
            make_indicator(
                kind=IndicatorKind.VARIANT_TRANSFER_FAILURE,
                description="Variant stems collapse transfer",
            )
        ],
        reasons=[make_reason(statement="Clone success with variant failure")],
    )
    assert diagnosis.diagnosis_id.value == "diag-factory"
