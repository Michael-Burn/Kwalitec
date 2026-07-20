"""Entity tests for Educational Hypothesis domain."""

from __future__ import annotations

import pytest

from domain.education.foundation.enums import DiagnosisType, LearningDimension
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import DiagnosisId, EvidenceId
from domain.education.hypothesis import (
    CompetingHypothesis,
    CompetingHypothesisId,
    DiagnosisReference,
    HypothesisKind,
    HypothesisReason,
    HypothesisReasonId,
    HypothesisScope,
    HypothesisScopeId,
    HypothesisScopeKind,
    InterpretationReference,
    Plausibility,
)
from tests.domain.education.hypothesis.conftest import (
    CONCEPT_SELECT,
    make_competitor,
    make_reason,
    make_scope,
)


def test_diagnosis_reference_valid() -> None:
    ref = DiagnosisReference(
        diagnosis_id=DiagnosisId("diag-001"),
        diagnosis_type=DiagnosisType.PREREQUISITE_GAP,
    )
    assert "diag-001" in str(ref)


def test_diagnosis_reference_type_checks() -> None:
    with pytest.raises(EducationalInvariantViolation):
        DiagnosisReference(
            diagnosis_id="diag-001",  # type: ignore[arg-type]
            diagnosis_type=DiagnosisType.PREREQUISITE_GAP,
        )
    with pytest.raises(EducationalInvariantViolation):
        DiagnosisReference(
            diagnosis_id=DiagnosisId("diag-001"),
            diagnosis_type="prerequisite_gap",  # type: ignore[arg-type]
        )


def test_interpretation_reference() -> None:
    ref = InterpretationReference(interpretation_id="interp-001")
    assert str(ref) == "interp-001"
    with pytest.raises(EducationalInvariantViolation):
        InterpretationReference(interpretation_id="")


def test_hypothesis_reason_identity_equality() -> None:
    left = make_reason(reason_id="r1", statement="First warrant")
    right = make_reason(reason_id="r1", statement="Different statement")
    other = make_reason(reason_id="r2", statement="First warrant")
    assert left == right
    assert left != other
    assert hash(left) == hash(right)


def test_hypothesis_reason_rejects_blank_statement() -> None:
    with pytest.raises(EducationalInvariantViolation):
        HypothesisReason(
            reason_id=HypothesisReasonId("r1"),
            statement="   ",
        )


def test_hypothesis_reason_rejects_how_to_smuggling() -> None:
    with pytest.raises(EducationalInvariantViolation) as exc:
        make_reason(statement="Therefore teach with worked examples")
    assert exc.value.invariant == "HypothesisReason.no_how_to_smuggling"


def test_hypothesis_reason_duplicate_evidence_rejected() -> None:
    with pytest.raises(EducationalInvariantViolation):
        HypothesisReason(
            reason_id=HypothesisReasonId("r1"),
            statement="Patterned upstream failure",
            evidence_ids=(EvidenceId("e1"), EvidenceId("e1")),
        )


def test_hypothesis_reason_with_statement() -> None:
    reason = make_reason(statement="Original warrant")
    amended = reason.with_statement("Amended warrant")
    assert amended.statement == "Amended warrant"
    assert amended.reason_id == reason.reason_id


def test_hypothesis_scope_requires_anchor() -> None:
    with pytest.raises(EducationalInvariantViolation) as exc:
        HypothesisScope(
            scope_id=HypothesisScopeId("scope-empty"),
            statement="No anchors",
            scope_kind=HypothesisScopeKind.CONCEPT,
        )
    assert exc.value.invariant == "HypothesisScope.anchor.required"


def test_hypothesis_scope_dimension_only_anchor() -> None:
    scope = HypothesisScope(
        scope_id=HypothesisScopeId("scope-dim"),
        statement="Dimension-scoped explanation",
        scope_kind=HypothesisScopeKind.LEARNING_DIMENSION,
        learning_dimension=LearningDimension.TRANSFER,
    )
    assert scope.learning_dimension is LearningDimension.TRANSFER


def test_hypothesis_scope_duplicate_concepts_rejected() -> None:
    from domain.education.foundation.references import ConceptReference

    ref = ConceptReference(concept_id=CONCEPT_SELECT)
    with pytest.raises(EducationalInvariantViolation):
        make_scope(concepts=(ref, ref))


def test_hypothesis_scope_with_statement() -> None:
    scope = make_scope()
    amended = scope.with_statement("Narrowed to GLM facet")
    assert amended.statement == "Narrowed to GLM facet"


def test_competing_hypothesis_signature() -> None:
    competitor = make_competitor(
        hypothesis_kind=HypothesisKind.TRANSFER_LIMITATION,
        explanation="Transfer weakness on variants",
    )
    assert competitor.competitor_signature()[0] == "transfer_limitation"


def test_competing_hypothesis_rejects_how_to() -> None:
    with pytest.raises(EducationalInvariantViolation):
        CompetingHypothesis(
            competing_id=CompetingHypothesisId("c1"),
            hypothesis_kind=HypothesisKind.WEAK_ABSTRACTION,
            explanation="We should drill until fluent",
        )


def test_competing_hypothesis_plausibility_optional() -> None:
    competitor = make_competitor(plausibility=Plausibility.tentative())
    assert competitor.plausibility is not None
    assert competitor.plausibility.level.value == "tentative"
    bare = make_competitor(plausibility=None)
    assert bare.plausibility is None


def test_competing_hypothesis_with_explanation() -> None:
    competitor = make_competitor(explanation="Original reading")
    amended = competitor.with_explanation("Revised competing reading")
    assert amended.explanation == "Revised competing reading"


def test_competing_hypothesis_identity_equality() -> None:
    left = make_competitor(competing_id="c1", explanation="A")
    right = make_competitor(competing_id="c1", explanation="B")
    assert left == right
