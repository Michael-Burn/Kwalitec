"""Entity tests for Evidence Interpretation domain."""

from __future__ import annotations

import pytest

from domain.education.evidence_interpretation import (
    REPEATED_PATTERN_KINDS,
    EducationalScopeKind,
    EvidenceCluster,
    EvidenceClusterId,
    InterpretationContext,
    InterpretationContextId,
    InterpretedPattern,
    InterpretedPatternId,
    PatternKind,
)
from domain.education.foundation.enums import LearningDimension
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import ConceptId, LearningEpisodeId
from domain.education.foundation.references import ConceptReference
from tests.domain.education.evidence_interpretation.conftest import (
    CONCEPT_SELECT,
    EVIDENCE_001,
    EVIDENCE_002,
    EVIDENCE_003,
    make_cluster,
    make_context,
    make_pattern,
)


@pytest.mark.parametrize("kind", list(PatternKind))
def test_pattern_kinds_construct(kind: PatternKind) -> None:
    if kind in REPEATED_PATTERN_KINDS:
        ids = (EVIDENCE_001, EVIDENCE_002)
        count = 2
    else:
        ids = (EVIDENCE_001,)
        count = 1
    pattern = make_pattern(
        pattern_id=f"p-{kind.value}",
        kind=kind,
        description=f"Pattern {kind.value}",
        evidence_ids=ids,
        occurrence_count=count,
    )
    assert pattern.kind is kind
    assert pattern.is_repeated_kind() == (kind in REPEATED_PATTERN_KINDS)


@pytest.mark.parametrize("kind", list(REPEATED_PATTERN_KINDS))
def test_repeated_pattern_requires_two_evidence(kind: PatternKind) -> None:
    with pytest.raises(EducationalInvariantViolation):
        InterpretedPattern(
            pattern_id=InterpretedPatternId("p1"),
            kind=kind,
            description="Only one observation",
            evidence_ids=(EVIDENCE_001,),
            occurrence_count=2,
            concept_id=CONCEPT_SELECT,
        )


@pytest.mark.parametrize("kind", list(REPEATED_PATTERN_KINDS))
def test_repeated_pattern_requires_occurrence_two(kind: PatternKind) -> None:
    with pytest.raises(EducationalInvariantViolation):
        InterpretedPattern(
            pattern_id=InterpretedPatternId("p1"),
            kind=kind,
            description="Insufficient occurrence",
            evidence_ids=(EVIDENCE_001, EVIDENCE_002),
            occurrence_count=1,
            concept_id=CONCEPT_SELECT,
        )


def test_pattern_rejects_empty_evidence() -> None:
    with pytest.raises(EducationalInvariantViolation):
        InterpretedPattern(
            pattern_id=InterpretedPatternId("p1"),
            kind=PatternKind.EVIDENCE_SUFFICIENCY,
            description="No evidence",
            evidence_ids=(),
            occurrence_count=1,
        )


def test_pattern_rejects_duplicate_evidence_ids() -> None:
    with pytest.raises(EducationalInvariantViolation):
        InterpretedPattern(
            pattern_id=InterpretedPatternId("p1"),
            kind=PatternKind.EVIDENCE_CONSISTENCY,
            description="Dup ids",
            evidence_ids=(EVIDENCE_001, EVIDENCE_001),
            occurrence_count=1,
        )


def test_pattern_identity_equality() -> None:
    left = make_pattern(description="A")
    right = make_pattern(description="B")
    assert left == right
    assert hash(left) == hash(right)


def test_pattern_signature_and_with_methods() -> None:
    pattern = make_pattern()
    sig = pattern.pattern_signature()
    assert sig[0] == PatternKind.REPEATED_RETRIEVAL_FAILURE.value
    amended = pattern.with_description("Amended description")
    assert amended.description == "Amended description"
    assert amended.pattern_id == pattern.pattern_id
    bumped = pattern.with_occurrence_count(3)
    assert bumped.occurrence_count == 3


def test_cluster_requires_evidence() -> None:
    with pytest.raises(EducationalInvariantViolation):
        EvidenceCluster(
            cluster_id=EvidenceClusterId("c1"),
            theme="empty",
            evidence_ids=(),
        )


def test_cluster_rejects_duplicate_evidence() -> None:
    with pytest.raises(EducationalInvariantViolation):
        EvidenceCluster(
            cluster_id=EvidenceClusterId("c1"),
            theme="dup",
            evidence_ids=(EVIDENCE_001, EVIDENCE_001),
        )


def test_cluster_with_evidence_and_contains() -> None:
    cluster = make_cluster(evidence_ids=(EVIDENCE_001,))
    assert cluster.size() == 1
    assert cluster.contains(EVIDENCE_001)
    expanded = cluster.with_evidence(EVIDENCE_002)
    assert expanded.size() == 2
    with pytest.raises(EducationalInvariantViolation):
        expanded.with_evidence(EVIDENCE_001)


def test_cluster_signature_stable() -> None:
    a = make_cluster(evidence_ids=(EVIDENCE_002, EVIDENCE_001))
    b = make_cluster(evidence_ids=(EVIDENCE_001, EVIDENCE_002))
    assert a.cluster_signature() == b.cluster_signature()


def test_context_requires_educational_scope() -> None:
    with pytest.raises(EducationalInvariantViolation):
        InterpretationContext(
            context_id=InterpretationContextId("ctx"),
            educational_scope="  ",
            scope_kind=EducationalScopeKind.CONCEPT,
        )


@pytest.mark.parametrize("scope_kind", list(EducationalScopeKind))
def test_context_scope_kinds(scope_kind: EducationalScopeKind) -> None:
    ctx = make_context(scope_kind=scope_kind, educational_scope=f"Scope {scope_kind}")
    assert ctx.scope_kind is scope_kind


def test_context_rejects_duplicate_concept_refs() -> None:
    ref = ConceptReference(concept_id=CONCEPT_SELECT)
    with pytest.raises(EducationalInvariantViolation):
        make_context(concepts=(ref, ref))


def test_context_with_concept_and_episode() -> None:
    ctx = make_context(concepts=(), episodes=())
    other = ConceptId("concept-ultimate-mortality")
    expanded = ctx.with_concept_reference(ConceptReference(concept_id=other))
    assert other in expanded.concept_ids()
    with_ep = expanded.with_learning_episode(LearningEpisodeId("episode-002"))
    assert LearningEpisodeId("episode-002") in with_ep.episode_ids()


@pytest.mark.parametrize("dimension", list(LearningDimension))
def test_context_learning_dimensions(dimension: LearningDimension) -> None:
    ctx = make_context(dimension=dimension)
    assert ctx.learning_dimension is dimension


def test_pattern_rejects_wrong_id_type() -> None:
    with pytest.raises(EducationalInvariantViolation):
        InterpretedPattern(
            pattern_id="not-an-id",  # type: ignore[arg-type]
            kind=PatternKind.TREND_STABILITY,
            description="bad",
            evidence_ids=(EVIDENCE_001,),
            occurrence_count=1,
        )


def test_cluster_identity_equality() -> None:
    left = make_cluster(theme="A")
    right = make_cluster(theme="B")
    assert left == right


def test_non_repeated_kinds_allow_single_evidence() -> None:
    for kind in (
        PatternKind.EVIDENCE_CONSISTENCY,
        PatternKind.EVIDENCE_SUFFICIENCY,
        PatternKind.TREND_STABILITY,
    ):
        pattern = make_pattern(
            pattern_id=f"nr-{kind.value}",
            kind=kind,
            description=f"{kind.value} observation",
            evidence_ids=(EVIDENCE_001,),
            occurrence_count=1,
        )
        assert not pattern.is_repeated_kind()
        assert EVIDENCE_003 not in pattern.evidence_ids
