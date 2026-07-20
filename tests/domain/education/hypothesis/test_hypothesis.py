"""Aggregate behaviour tests for EducationalHypothesis."""

from __future__ import annotations

import pytest

from domain.education.foundation.enums import DiagnosisType
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import DiagnosisId, EvidenceId, HypothesisId
from domain.education.hypothesis import (
    DiagnosisReference,
    EducationalHypothesis,
    ExplanatoryStrength,
    ExplanatoryStrengthLevel,
    HypothesisIsRevisableSpecification,
    HypothesisIsSupportedSpecification,
    HypothesisKind,
    HypothesisStatus,
    InterpretationReference,
    Plausibility,
    PlausibilityLevel,
    RevisionForm,
)
from tests.domain.education.hypothesis.conftest import (
    EVIDENCE_001,
    EVIDENCE_002,
    INTERP_001,
    make_competitor,
    make_diagnosis_ref,
    make_hypothesis,
    make_plausibility,
    make_reason,
    make_strength,
)


def test_propose_creates_active_supported_hypothesis() -> None:
    hypothesis = make_hypothesis()
    assert hypothesis.is_active()
    assert HypothesisIsSupportedSpecification().is_satisfied_by(hypothesis)
    assert HypothesisIsRevisableSpecification().is_satisfied_by(hypothesis)
    assert hypothesis.primary_diagnosis_type() is DiagnosisType.PREREQUISITE_GAP


def test_revise_updates_explanation_and_status() -> None:
    hypothesis = make_hypothesis()
    hypothesis.pull_events()
    hypothesis.revise(
        explanation="Revised: exponential-family gaps specifically on link functions",
        revision_form=RevisionForm.NARROWING,
    )
    assert hypothesis.is_revised()
    assert "link functions" in hypothesis.explanation


def test_revise_shift_kind_requires_compatible_diagnosis() -> None:
    hypothesis = make_hypothesis(
        hypothesis_kind=HypothesisKind.PREREQUISITE_DEFICIENCY,
    )
    with pytest.raises(EducationalInvariantViolation):
        hypothesis.revise(
            hypothesis_kind=HypothesisKind.CONFIDENCE_CALIBRATION_ISSUE,
            explanation="False confidence from clone success",
            revision_form=RevisionForm.SHIFT,
        )


def test_revise_shift_with_compatible_diagnosis_refs() -> None:
    hypothesis = make_hypothesis(
        hypothesis_kind=HypothesisKind.PREREQUISITE_DEFICIENCY,
    )
    hypothesis.revise(
        hypothesis_kind=HypothesisKind.TRANSFER_LIMITATION,
        explanation="Knowledge present only on drilled stems",
        diagnosis_references=[
            DiagnosisReference(
                diagnosis_id=DiagnosisId("diag-transfer"),
                diagnosis_type=DiagnosisType.TRANSFER_WEAKNESS,
            )
        ],
        revision_form=RevisionForm.SHIFT,
    )
    assert hypothesis.hypothesis_kind is HypothesisKind.TRANSFER_LIMITATION


def test_strengthen_increases_strength() -> None:
    hypothesis = make_hypothesis(
        explanatory_strength=make_strength(ExplanatoryStrengthLevel.WEAK),
        plausibility=make_plausibility(PlausibilityLevel.TENTATIVE),
    )
    hypothesis.pull_events()
    hypothesis.strengthen()
    assert hypothesis.explanatory_strength.level is ExplanatoryStrengthLevel.MODERATE
    assert hypothesis.plausibility.level is PlausibilityLevel.WORKING
    assert hypothesis.is_revised()


def test_weaken_decreases_strength() -> None:
    hypothesis = make_hypothesis(
        explanatory_strength=make_strength(ExplanatoryStrengthLevel.STRONG),
        plausibility=make_plausibility(PlausibilityLevel.STRONG),
    )
    hypothesis.weaken()
    assert hypothesis.explanatory_strength.level is ExplanatoryStrengthLevel.MODERATE


def test_discard_terminates_revisability() -> None:
    hypothesis = make_hypothesis()
    hypothesis.discard("successful prerequisite probe contradicted reading")
    assert hypothesis.is_discarded()
    assert hypothesis.discard_reason is not None
    assert not HypothesisIsRevisableSpecification().is_satisfied_by(hypothesis)
    assert not HypothesisIsSupportedSpecification().is_satisfied_by(hypothesis)


def test_discarded_cannot_strengthen() -> None:
    hypothesis = make_hypothesis()
    hypothesis.discard("retired")
    with pytest.raises(EducationalInvariantViolation) as exc:
        hypothesis.strengthen()
    assert exc.value.invariant == "EducationalHypothesis.strengthen.not_discarded"


def test_discarded_cannot_revise_or_weaken() -> None:
    hypothesis = make_hypothesis()
    hypothesis.discard("retired")
    with pytest.raises(EducationalInvariantViolation):
        hypothesis.revise(explanation="attempted revival")
    with pytest.raises(EducationalInvariantViolation):
        hypothesis.weaken()


def test_add_competing_hypothesis() -> None:
    hypothesis = make_hypothesis(
        hypothesis_kind=HypothesisKind.PREREQUISITE_DEFICIENCY,
    )
    competitor = make_competitor(
        hypothesis_kind=HypothesisKind.TRANSFER_LIMITATION,
        explanation="Errors come from transfer weakness on variant stems",
    )
    hypothesis.add_competing_hypothesis(competitor)
    assert hypothesis.competitor_count() == 1
    assert hypothesis.is_revised()


def test_cannot_add_duplicate_competitor() -> None:
    hypothesis = make_hypothesis(
        hypothesis_kind=HypothesisKind.PREREQUISITE_DEFICIENCY,
        competing_hypotheses=[
            make_competitor(
                competing_id="c1",
                hypothesis_kind=HypothesisKind.TRANSFER_LIMITATION,
                explanation="Transfer reading",
            )
        ],
    )
    with pytest.raises(EducationalInvariantViolation):
        hypothesis.add_competing_hypothesis(
            make_competitor(
                competing_id="c2",
                hypothesis_kind=HypothesisKind.TRANSFER_LIMITATION,
                explanation="Transfer reading",
            )
        )


def test_cannot_add_competitor_matching_primary() -> None:
    hypothesis = make_hypothesis(
        hypothesis_kind=HypothesisKind.PREREQUISITE_DEFICIENCY,
        explanation="Missing exponential-family intuition",
    )
    with pytest.raises(EducationalInvariantViolation):
        hypothesis.add_competing_hypothesis(
            make_competitor(
                hypothesis_kind=HypothesisKind.PREREQUISITE_DEFICIENCY,
                explanation="Missing exponential-family intuition",
            )
        )


def test_identity_equality() -> None:
    left = make_hypothesis(hypothesis_id="hyp-same")
    right = make_hypothesis(hypothesis_id="hyp-same", student_id="student-other")
    other = make_hypothesis(hypothesis_id="hyp-other")
    assert left == right
    assert left != other
    assert hash(left) == hash(right)


def test_query_helpers() -> None:
    hypothesis = make_hypothesis()
    assert hypothesis.has_diagnosis(DiagnosisId("diag-001"))
    assert hypothesis.has_interpretation(INTERP_001)
    assert hypothesis.has_evidence(EVIDENCE_001)
    assert hypothesis.has_evidence(EVIDENCE_002)
    assert hypothesis.reason_count() == 1
    assert not hypothesis.has_evidence(EvidenceId("evidence-missing"))


def test_suspend_via_plausibility_revision() -> None:
    hypothesis = make_hypothesis()
    hypothesis.revise(plausibility=Plausibility.suspended())
    assert hypothesis.is_suspended()
    assert hypothesis.plausibility.is_suspended()


def test_suspended_cannot_strengthen_in_place() -> None:
    hypothesis = make_hypothesis()
    hypothesis.revise(plausibility=Plausibility.suspended())
    with pytest.raises(EducationalInvariantViolation):
        hypothesis.strengthen()


def test_no_public_setters() -> None:
    hypothesis = make_hypothesis()
    with pytest.raises(AttributeError):
        hypothesis.status = HypothesisStatus.DISCARDED  # type: ignore[misc]


def test_repr_contains_kind() -> None:
    hypothesis = make_hypothesis()
    assert "EducationalHypothesis" in repr(hypothesis)
    assert "prerequisite_deficiency" in repr(hypothesis)


def test_propose_classmethod_direct() -> None:
    hypothesis = EducationalHypothesis.propose(
        hypothesis_id=HypothesisId("hyp-direct"),
        student_id="student-ada",
        hypothesis_kind=HypothesisKind.WEAK_ABSTRACTION,
        explanation="Student holds surface procedures without abstracting structure",
        scope=make_hypothesis().scope,
        plausibility=Plausibility.working(),
        explanatory_strength=ExplanatoryStrength.moderate(),
        diagnosis_references=[
            make_diagnosis_ref(
                hypothesis_kind=HypothesisKind.WEAK_ABSTRACTION,
            )
        ],
        reasons=[make_reason(statement="Surface success without abstraction")],
        interpretation_references=[
            InterpretationReference(interpretation_id=INTERP_001)
        ],
        evidence_ids=[EVIDENCE_001],
        known_evidence_ids=frozenset({EVIDENCE_001}),
        known_interpretation_ids=frozenset({INTERP_001}),
    )
    assert hypothesis.hypothesis_kind is HypothesisKind.WEAK_ABSTRACTION
