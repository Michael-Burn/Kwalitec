"""Invariant enforcement tests for Educational Hypothesis."""

from __future__ import annotations

import pytest

from domain.education.foundation.enums import DiagnosisType
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import DiagnosisId, EvidenceId, HypothesisId
from domain.education.hypothesis import (
    DiagnosisReference,
    EducationalHypothesis,
    ExplanatoryStrength,
    HypothesisKind,
    HypothesisReason,
    HypothesisReasonId,
    InterpretationReference,
    Plausibility,
)
from tests.domain.education.hypothesis.conftest import (
    EVIDENCE_001,
    INTERP_001,
    KNOWN_EVIDENCE,
    KNOWN_INTERPRETATIONS,
    make_competitor,
    make_diagnosis_ref,
    make_hypothesis,
    make_reason,
    make_scope,
    make_strength,
)


def test_must_reference_diagnosis() -> None:
    with pytest.raises(EducationalInvariantViolation) as exc:
        EducationalHypothesis.propose(
            hypothesis_id=HypothesisId("hyp-no-diag"),
            student_id="student-ada",
            hypothesis_kind=HypothesisKind.PREREQUISITE_DEFICIENCY,
            explanation="Missing exponential-family intuition",
            scope=make_scope(),
            plausibility=Plausibility.working(),
            explanatory_strength=ExplanatoryStrength.moderate(),
            diagnosis_references=[],
            reasons=[make_reason()],
        )
    assert exc.value.invariant == (
        "EducationalHypothesis.diagnosis_references.min_one"
    )


def test_must_possess_plausibility() -> None:
    with pytest.raises(EducationalInvariantViolation) as exc:
        EducationalHypothesis(
            hypothesis_id=HypothesisId("hyp-no-plaus"),
            student_id="student-ada",
            hypothesis_kind=HypothesisKind.PREREQUISITE_DEFICIENCY,
            explanation="Missing exponential-family intuition",
            scope=make_scope(),
            plausibility="working",  # type: ignore[arg-type]
            explanatory_strength=ExplanatoryStrength.moderate(),
            diagnosis_references=[make_diagnosis_ref()],
            reasons=[make_reason()],
        )
    assert exc.value.invariant == "EducationalHypothesis.plausibility.required"


def test_must_possess_explanatory_strength() -> None:
    with pytest.raises(EducationalInvariantViolation) as exc:
        EducationalHypothesis(
            hypothesis_id=HypothesisId("hyp-no-strength"),
            student_id="student-ada",
            hypothesis_kind=HypothesisKind.PREREQUISITE_DEFICIENCY,
            explanation="Missing exponential-family intuition",
            scope=make_scope(),
            plausibility=Plausibility.working(),
            explanatory_strength="moderate",  # type: ignore[arg-type]
            diagnosis_references=[make_diagnosis_ref()],
            reasons=[make_reason()],
        )
    assert (
        exc.value.invariant
        == "EducationalHypothesis.explanatory_strength.required"
    )


def test_cannot_duplicate_competing_hypotheses() -> None:
    competitor = make_competitor(
        competing_id="c1",
        hypothesis_kind=HypothesisKind.TRANSFER_LIMITATION,
        explanation="Same competing reading",
    )
    duplicate = make_competitor(
        competing_id="c2",
        hypothesis_kind=HypothesisKind.TRANSFER_LIMITATION,
        explanation="Same competing reading",
    )
    with pytest.raises(EducationalInvariantViolation) as exc:
        make_hypothesis(
            competing_hypotheses=[competitor, duplicate],
        )
    assert "competitors" in (exc.value.invariant or "")


def test_cannot_contradict_supporting_diagnosis() -> None:
    with pytest.raises(EducationalInvariantViolation) as exc:
        make_hypothesis(
            hypothesis_kind=HypothesisKind.PREREQUISITE_DEFICIENCY,
            diagnosis_references=[
                DiagnosisReference(
                    diagnosis_id=DiagnosisId("diag-false-conf"),
                    diagnosis_type=DiagnosisType.FALSE_CONFIDENCE,
                )
            ],
        )
    assert "contradiction" in (exc.value.invariant or "") or "compatible" in (
        exc.value.invariant or ""
    )


def test_incompatible_diagnosis_type_rejected() -> None:
    with pytest.raises(EducationalInvariantViolation):
        make_hypothesis(
            hypothesis_kind=HypothesisKind.CONFIDENCE_CALIBRATION_ISSUE,
            diagnosis_references=[
                DiagnosisReference(
                    diagnosis_id=DiagnosisId("diag-prereq"),
                    diagnosis_type=DiagnosisType.PREREQUISITE_GAP,
                )
            ],
        )


def test_must_remain_revisable_until_discard() -> None:
    hypothesis = make_hypothesis()
    hypothesis.revise(explanation="First revision of the explanation")
    hypothesis.revise(explanation="Second revision of the explanation")
    assert hypothesis.is_revised()
    hypothesis.discard("replaced by better reading")
    with pytest.raises(EducationalInvariantViolation):
        hypothesis.revise(explanation="illegal after discard")


def test_discarded_cannot_be_strengthened() -> None:
    hypothesis = make_hypothesis(
        explanatory_strength=make_strength(),
    )
    hypothesis.discard("done")
    with pytest.raises(EducationalInvariantViolation) as exc:
        hypothesis.strengthen()
    assert exc.value.invariant == "EducationalHypothesis.strengthen.not_discarded"


def test_duplicate_reasons_rejected() -> None:
    reason = make_reason(reason_id="r1", statement="Same warrant", code="code-a")
    duplicate = HypothesisReason(
        reason_id=HypothesisReasonId("r2"),
        statement="Same warrant",
        code="code-a",
    )
    with pytest.raises(EducationalInvariantViolation):
        make_hypothesis(reasons=[reason, duplicate])


def test_unknown_evidence_rejected_when_known_set() -> None:
    with pytest.raises(EducationalInvariantViolation):
        make_hypothesis(
            evidence_ids=[EvidenceId("evidence-unknown")],
            known_evidence=KNOWN_EVIDENCE,
            reasons=[make_reason(evidence_ids=())],
        )


def test_unknown_interpretation_rejected_when_known_set() -> None:
    with pytest.raises(EducationalInvariantViolation):
        make_hypothesis(
            interpretation_references=[
                InterpretationReference(interpretation_id="interp-unknown")
            ],
            known_interpretations=KNOWN_INTERPRETATIONS,
        )


def test_explanation_rejects_strategy_smuggling() -> None:
    with pytest.raises(EducationalInvariantViolation):
        make_hypothesis(explanation="Therefore teach with deliberate practice")


def test_explanation_rejects_unfalsifiable_claims() -> None:
    with pytest.raises(EducationalInvariantViolation):
        make_hypothesis(explanation="Student is just bad at maths")


def test_requires_at_least_one_reason() -> None:
    with pytest.raises(EducationalInvariantViolation):
        EducationalHypothesis.propose(
            hypothesis_id=HypothesisId("hyp-no-reason"),
            student_id="student-ada",
            hypothesis_kind=HypothesisKind.PREREQUISITE_DEFICIENCY,
            explanation="Missing exponential-family intuition",
            scope=make_scope(),
            plausibility=Plausibility.working(),
            explanatory_strength=ExplanatoryStrength.moderate(),
            diagnosis_references=[make_diagnosis_ref()],
            reasons=[],
        )


def test_duplicate_diagnosis_references_rejected() -> None:
    ref = make_diagnosis_ref(diagnosis_id="diag-001")
    with pytest.raises(EducationalInvariantViolation):
        make_hypothesis(diagnosis_references=[ref, ref])


def test_known_evidence_allows_referenced() -> None:
    hypothesis = make_hypothesis(
        evidence_ids=[EVIDENCE_001],
        interpretation_references=[
            InterpretationReference(interpretation_id=INTERP_001)
        ],
        known_evidence=frozenset({EVIDENCE_001}),
        known_interpretations=frozenset({INTERP_001}),
        reasons=[make_reason(evidence_ids=(EVIDENCE_001,))],
    )
    assert hypothesis.has_evidence(EVIDENCE_001)
