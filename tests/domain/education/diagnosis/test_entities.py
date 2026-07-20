"""Entity tests for diagnosis indicator, reason, and scope."""

from __future__ import annotations

import pytest

from domain.education.diagnosis import (
    DiagnosisIndicator,
    DiagnosisIndicatorId,
    DiagnosisReason,
    DiagnosisReasonId,
    DiagnosisScope,
    DiagnosisScopeId,
    EducationalScopeKind,
    IndicatorKind,
    InterpretationReference,
)
from domain.education.foundation.enums import LearningDimension
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import EvidenceId, LearningEpisodeId
from domain.education.foundation.references import ConceptReference
from tests.domain.education.diagnosis.conftest import (
    CONCEPT_SELECT,
    EPISODE_001,
    EVIDENCE_001,
    EVIDENCE_002,
    INTERP_001,
    make_indicator,
    make_reason,
    make_scope,
)


def test_indicator_requires_interpretation() -> None:
    with pytest.raises(EducationalInvariantViolation):
        DiagnosisIndicator(
            indicator_id=DiagnosisIndicatorId("ind-1"),
            kind=IndicatorKind.FRAGILE_EXPLANATION,
            description="Fragile explanation",
            interpretation_references=(),
            evidence_ids=(EVIDENCE_001,),
        )


def test_indicator_requires_evidence() -> None:
    with pytest.raises(EducationalInvariantViolation):
        DiagnosisIndicator(
            indicator_id=DiagnosisIndicatorId("ind-1"),
            kind=IndicatorKind.FRAGILE_EXPLANATION,
            description="Fragile explanation",
            interpretation_references=(
                InterpretationReference(interpretation_id=INTERP_001),
            ),
            evidence_ids=(),
        )


def test_indicator_rejects_duplicate_evidence() -> None:
    with pytest.raises(EducationalInvariantViolation):
        make_indicator(evidence_ids=(EVIDENCE_001, EVIDENCE_001))


def test_indicator_rejects_duplicate_interpretations() -> None:
    with pytest.raises(EducationalInvariantViolation):
        make_indicator(interpretation_ids=(INTERP_001, INTERP_001))


def test_indicator_support_signature() -> None:
    indicator = make_indicator()
    kind, interps, evidence = indicator.support_signature()
    assert kind == IndicatorKind.FRAGILE_EXPLANATION.value
    assert INTERP_001 in interps
    assert EVIDENCE_001.value in evidence


def test_indicator_with_description() -> None:
    updated = make_indicator().with_description("Amended warrant description")
    assert updated.description == "Amended warrant description"
    assert updated.indicator_id == make_indicator().indicator_id


def test_indicator_identity_equality() -> None:
    a = make_indicator(indicator_id="same", description="A")
    b = make_indicator(indicator_id="same", description="B")
    assert a == b


def test_reason_rejects_blank_statement() -> None:
    with pytest.raises(EducationalInvariantViolation):
        DiagnosisReason(
            reason_id=DiagnosisReasonId("r-1"),
            statement="   ",
        )


@pytest.mark.parametrize(
    "statement",
    [
        "Therefore teach with worked examples",
        "Recommend strategy deliberate practice",
        "Should practise more drills",
        "Priority is misconception repair",
        "Assign episode concept deepening",
    ],
)
def test_reason_rejects_how_to_smuggling(statement: str) -> None:
    with pytest.raises(EducationalInvariantViolation):
        make_reason(statement=statement)


def test_reason_signature_and_with_statement() -> None:
    reason = make_reason(statement="Patterned wrong model", code="pattern")
    assert reason.reason_signature() == ("patterned wrong model", "pattern")
    amended = reason.with_statement("Stable wrong model persists")
    assert amended.statement == "Stable wrong model persists"


def test_scope_requires_anchor() -> None:
    with pytest.raises(EducationalInvariantViolation):
        DiagnosisScope(
            scope_id=DiagnosisScopeId("scope-empty"),
            statement="Vague student is weak",
            scope_kind=EducationalScopeKind.CONCEPT,
            learning_dimension=None,
            concept_references=(),
            learning_objective_references=(),
            learning_episode_ids=(),
        )


def test_scope_accepts_dimension_only_anchor() -> None:
    scope = DiagnosisScope(
        scope_id=DiagnosisScopeId("scope-dim"),
        statement="Retention dimension implicated",
        scope_kind=EducationalScopeKind.LEARNING_DIMENSION,
        learning_dimension=LearningDimension.RETENTION,
    )
    assert scope.learning_dimension is LearningDimension.RETENTION


def test_scope_rejects_duplicate_concepts() -> None:
    with pytest.raises(EducationalInvariantViolation):
        make_scope(
            concepts=(
                ConceptReference(concept_id=CONCEPT_SELECT),
                ConceptReference(concept_id=CONCEPT_SELECT),
            )
        )


def test_scope_rejects_duplicate_episodes() -> None:
    with pytest.raises(EducationalInvariantViolation):
        make_scope(episodes=(EPISODE_001, LearningEpisodeId("episode-001")))


def test_scope_with_statement() -> None:
    scope = make_scope().with_statement("Amended educational scope statement")
    assert "Amended" in scope.statement


def test_interpretation_reference_rejects_whitespace() -> None:
    with pytest.raises(EducationalInvariantViolation):
        InterpretationReference(interpretation_id="interp 001")


def test_indicator_rejects_blank_description() -> None:
    with pytest.raises(EducationalInvariantViolation):
        make_indicator(description="  ")


@pytest.mark.parametrize("kind", list(IndicatorKind))
def test_all_indicator_kinds_constructible(kind: IndicatorKind) -> None:
    indicator = DiagnosisIndicator(
        indicator_id=DiagnosisIndicatorId(f"ind-{kind.value}"),
        kind=kind,
        description=f"Signal of {kind.value}",
        interpretation_references=(
            InterpretationReference(interpretation_id=INTERP_001),
        ),
        evidence_ids=(EVIDENCE_001, EVIDENCE_002),
    )
    assert indicator.kind is kind


def test_scope_concept_and_episode_ids() -> None:
    scope = make_scope()
    assert CONCEPT_SELECT in scope.concept_ids()
    assert EPISODE_001 in scope.episode_ids()


def test_reason_identity_equality() -> None:
    a = make_reason(reason_id="r-same", statement="One")
    b = make_reason(reason_id="r-same", statement="Two")
    assert a == b


def test_indicator_rejects_non_evidence_id() -> None:
    with pytest.raises(EducationalInvariantViolation):
        DiagnosisIndicator(
            indicator_id=DiagnosisIndicatorId("ind-bad"),
            kind=IndicatorKind.FRAGILE_EXPLANATION,
            description="Bad evidence type",
            interpretation_references=(
                InterpretationReference(interpretation_id=INTERP_001),
            ),
            evidence_ids=("evidence-001",),  # type: ignore[arg-type]
        )


def test_indicator_rejects_non_interpretation_reference() -> None:
    with pytest.raises(EducationalInvariantViolation):
        DiagnosisIndicator(
            indicator_id=DiagnosisIndicatorId("ind-bad"),
            kind=IndicatorKind.FRAGILE_EXPLANATION,
            description="Bad interp type",
            interpretation_references=("interp-001",),  # type: ignore[arg-type]
            evidence_ids=(EvidenceId("evidence-001"),),
        )
