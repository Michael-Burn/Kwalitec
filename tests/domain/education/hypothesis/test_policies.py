"""Policy tests for Educational Hypothesis."""

from __future__ import annotations

import pytest

from domain.education.foundation.enums import DiagnosisType
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import DiagnosisId
from domain.education.hypothesis import (
    DiagnosisReference,
    HypothesisKind,
    HypothesisRevisionPolicy,
    HypothesisStatus,
    HypothesisValidationPolicy,
    Plausibility,
    PlausibilityLevel,
    RevisionForm,
)
from tests.domain.education.hypothesis.conftest import (
    make_competitor,
    make_diagnosis_ref,
    make_reason,
)


@pytest.mark.parametrize("kind", list(HypothesisKind))
def test_compatible_diagnosis_types_non_empty(kind: HypothesisKind) -> None:
    compatible = HypothesisValidationPolicy.compatible_diagnosis_types(kind)
    assert len(compatible) >= 1
    for diagnosis_type in compatible:
        assert isinstance(diagnosis_type, DiagnosisType)


def test_assert_compatible_with_diagnosis_accepts_lawful() -> None:
    HypothesisValidationPolicy.assert_compatible_with_diagnosis(
        HypothesisKind.TRANSFER_LIMITATION,
        [
            DiagnosisReference(
                diagnosis_id=DiagnosisId("d1"),
                diagnosis_type=DiagnosisType.TRANSFER_WEAKNESS,
            )
        ],
    )


def test_assert_compatible_rejects_contradiction() -> None:
    with pytest.raises(EducationalInvariantViolation):
        HypothesisValidationPolicy.assert_compatible_with_diagnosis(
            HypothesisKind.TRANSFER_LIMITATION,
            [
                DiagnosisReference(
                    diagnosis_id=DiagnosisId("d1"),
                    diagnosis_type=DiagnosisType.PREREQUISITE_GAP,
                )
            ],
        )


def test_assert_explanation_rejects_blank() -> None:
    with pytest.raises(EducationalInvariantViolation):
        HypothesisValidationPolicy.assert_explanation("   ")


def test_assert_competing_hypotheses_distinct_from_primary() -> None:
    with pytest.raises(EducationalInvariantViolation):
        HypothesisValidationPolicy.assert_competing_hypotheses(
            [
                make_competitor(
                    hypothesis_kind=HypothesisKind.PREREQUISITE_DEFICIENCY,
                    explanation="Same as primary",
                )
            ],
            primary_kind=HypothesisKind.PREREQUISITE_DEFICIENCY,
            primary_explanation="Same as primary",
        )


def test_assert_reasons_requires_one() -> None:
    with pytest.raises(EducationalInvariantViolation):
        HypothesisValidationPolicy.assert_reasons([])


def test_assert_reasons_accepts_valid() -> None:
    reasons = HypothesisValidationPolicy.assert_reasons([make_reason()])
    assert len(reasons) == 1


def test_revision_policy_revisable_statuses() -> None:
    for status in (
        HypothesisStatus.ACTIVE,
        HypothesisStatus.REVISED,
        HypothesisStatus.SUSPENDED,
    ):
        HypothesisRevisionPolicy.assert_revisable(status, action="revise")


def test_revision_policy_rejects_discarded() -> None:
    with pytest.raises(EducationalInvariantViolation):
        HypothesisRevisionPolicy.assert_revisable(
            HypothesisStatus.DISCARDED, action="revise"
        )


def test_revision_policy_strengthen_guard() -> None:
    with pytest.raises(EducationalInvariantViolation) as exc:
        HypothesisRevisionPolicy.assert_can_strengthen(HypothesisStatus.DISCARDED)
    assert exc.value.invariant == "EducationalHypothesis.strengthen.not_discarded"


def test_revision_policy_discard_already() -> None:
    with pytest.raises(EducationalInvariantViolation):
        HypothesisRevisionPolicy.assert_can_discard(HypothesisStatus.DISCARDED)


def test_revision_policy_plausibility_suspended() -> None:
    with pytest.raises(EducationalInvariantViolation):
        HypothesisRevisionPolicy.assert_plausibility_allows_strength_change(
            Plausibility.suspended(), action="strengthen"
        )


def test_revision_form_validation() -> None:
    assert (
        HypothesisRevisionPolicy.assert_revision_form(RevisionForm.SHIFT)
        is RevisionForm.SHIFT
    )
    assert HypothesisRevisionPolicy.assert_revision_form(None) is None
    with pytest.raises(EducationalInvariantViolation):
        HypothesisRevisionPolicy.assert_revision_form("shift")  # type: ignore[arg-type]


def test_next_status_after_revision() -> None:
    assert (
        HypothesisRevisionPolicy.next_status_after_revision(
            HypothesisStatus.ACTIVE
        )
        is HypothesisStatus.REVISED
    )
    assert (
        HypothesisRevisionPolicy.next_status_after_revision(
            HypothesisStatus.ACTIVE, suspend=True
        )
        is HypothesisStatus.SUSPENDED
    )


def test_assert_diagnosis_references_type() -> None:
    with pytest.raises(EducationalInvariantViolation):
        HypothesisValidationPolicy.assert_diagnosis_references(
            ["not-a-ref"]  # type: ignore[list-item]
        )


def test_assert_student_id() -> None:
    assert HypothesisValidationPolicy.assert_student_id("student-ada") == "student-ada"
    with pytest.raises(EducationalInvariantViolation):
        HypothesisValidationPolicy.assert_student_id("student ada")


@pytest.mark.parametrize(
    ("kind", "diagnosis_type"),
    [
        (
            HypothesisKind.PREREQUISITE_DEFICIENCY,
            DiagnosisType.PREREQUISITE_GAP,
        ),
        (
            HypothesisKind.REPRESENTATION_MISMATCH,
            DiagnosisType.CONCEPTUAL_MISUNDERSTANDING,
        ),
        (
            HypothesisKind.WEAK_ABSTRACTION,
            DiagnosisType.INCOMPLETE_UNDERSTANDING,
        ),
        (HypothesisKind.SURFACE_MEMORISATION, DiagnosisType.WEAK_RETENTION),
        (HypothesisKind.PROCEDURAL_FIXATION, DiagnosisType.PROCEDURAL_WEAKNESS),
        (HypothesisKind.TRANSFER_LIMITATION, DiagnosisType.TRANSFER_WEAKNESS),
        (
            HypothesisKind.CONFIDENCE_CALIBRATION_ISSUE,
            DiagnosisType.FALSE_CONFIDENCE,
        ),
        (
            HypothesisKind.CONFIDENCE_CALIBRATION_ISSUE,
            DiagnosisType.LOW_CONFIDENCE,
        ),
    ],
)
def test_primary_kind_diagnosis_pairs(
    kind: HypothesisKind, diagnosis_type: DiagnosisType
) -> None:
    HypothesisValidationPolicy.assert_compatible_with_diagnosis(
        kind,
        [make_diagnosis_ref(diagnosis_type=diagnosis_type, hypothesis_kind=kind)],
    )


def test_plausibility_level_working_allows_strength_change() -> None:
    HypothesisRevisionPolicy.assert_plausibility_allows_strength_change(
        Plausibility.of(PlausibilityLevel.WORKING), action="strengthen"
    )
