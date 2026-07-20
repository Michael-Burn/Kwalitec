"""High-volume matrices exercising Evidence Interpretation domain surface area."""

from __future__ import annotations

import pytest

from domain.education.evidence_interpretation import (
    REPEATED_PATTERN_KINDS,
    ClusteringPolicy,
    EducationalScopeKind,
    InterpretationIsActionableSpecification,
    InterpretationIsConsistentSpecification,
    InterpretationStatus,
    InterpretationValidationPolicy,
    PatternKind,
)
from domain.education.foundation.enums import ConfidenceLevel, LearningDimension
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import ConceptId, EvidenceId, LearningEpisodeId
from domain.education.foundation.references import ConceptReference
from tests.domain.education.evidence_interpretation.conftest import (
    CONCEPT_SELECT,
    CONCEPT_ULTIMATE,
    EPISODE_001,
    EPISODE_002,
    EVIDENCE_001,
    EVIDENCE_002,
    EVIDENCE_003,
    KNOWN_CONCEPTS,
    KNOWN_EPISODES,
    KNOWN_EVIDENCE,
    make_cluster,
    make_confidence,
    make_context,
    make_interpretation,
    make_pattern,
    make_summary,
)

PATTERN_KINDS = list(PatternKind)
SCOPE_KINDS = list(EducationalScopeKind)
CONFIDENCE_LEVELS = [
    ConfidenceLevel.VERY_LOW,
    ConfidenceLevel.LOW,
    ConfidenceLevel.MEDIUM,
    ConfidenceLevel.HIGH,
    ConfidenceLevel.VERY_HIGH,
]
DIMENSIONS = list(LearningDimension)
STUDENTS = tuple(f"student-{i}" for i in range(1, 8))


def _compatible_confidence(kind: PatternKind) -> ConfidenceLevel:
    if kind in {
        PatternKind.REPEATED_REFLECTION_THEME,
        PatternKind.REPEATED_CONFIDENCE_MISMATCH,
    }:
        return ConfidenceLevel.MEDIUM
    if kind is PatternKind.TREND_STABILITY:
        return ConfidenceLevel.MEDIUM
    return ConfidenceLevel.HIGH


def _pattern_args(kind: PatternKind) -> dict:
    if kind in REPEATED_PATTERN_KINDS:
        return {
            "kind": kind,
            "evidence_ids": (EVIDENCE_001, EVIDENCE_002),
            "occurrence_count": 2,
            "description": f"Observed {kind.value.replace('_', ' ')}",
        }
    return {
        "kind": kind,
        "evidence_ids": (EVIDENCE_001,),
        "occurrence_count": 1,
        "description": f"Observed {kind.value.replace('_', ' ')}",
    }


def _cluster_for(kind: PatternKind):
    if kind in REPEATED_PATTERN_KINDS:
        return make_cluster(evidence_ids=(EVIDENCE_001, EVIDENCE_002))
    return make_cluster(evidence_ids=(EVIDENCE_001,))


@pytest.mark.parametrize("kind", PATTERN_KINDS)
@pytest.mark.parametrize("student", STUDENTS)
def test_interpret_per_pattern_kind_and_student(
    kind: PatternKind, student: str
) -> None:
    args = _pattern_args(kind)
    cluster = _cluster_for(kind)
    confidence = make_confidence(_compatible_confidence(kind))
    interp = make_interpretation(
        interpretation_id=f"interp-{kind.value}-{student}",
        student_id=student,
        clusters=[cluster],
        patterns=[make_pattern(pattern_id=f"p-{kind.value}", **args)],
        confidence=confidence,
        summary=make_summary(
            text=f"Observed {kind.value.replace('_', ' ')} for {student}",
            pattern_count=1,
            cluster_count=1,
        ),
    )
    assert interp.student_id == student
    assert interp.patterns[0].kind is kind
    assert InterpretationIsActionableSpecification().is_satisfied_by(interp)
    assert InterpretationIsConsistentSpecification().is_satisfied_by(interp)


@pytest.mark.parametrize("level", CONFIDENCE_LEVELS)
@pytest.mark.parametrize("ratio", [None, 0.0, 0.25, 0.5, 0.75, 1.0])
def test_confidence_matrix(level: ConfidenceLevel, ratio: float | None) -> None:
    measure = make_confidence(level, ratio=ratio)
    assert measure.level is level
    assert measure.is_at_least(ConfidenceLevel.VERY_LOW)


@pytest.mark.parametrize("scope_kind", SCOPE_KINDS)
@pytest.mark.parametrize("dimension", DIMENSIONS)
def test_context_scope_and_dimension_matrix(
    scope_kind: EducationalScopeKind, dimension: LearningDimension
) -> None:
    interp = make_interpretation(
        interpretation_id=f"interp-{scope_kind.value}-{dimension.value}",
        context=make_context(
            context_id=f"ctx-{scope_kind.value}-{dimension.value}",
            educational_scope=f"Scope {scope_kind.value} {dimension.value}",
            scope_kind=scope_kind,
            dimension=dimension,
        ),
    )
    assert interp.context.scope_kind is scope_kind
    assert interp.context.learning_dimension is dimension


@pytest.mark.parametrize(
    "status_action",
    ["revise", "invalidate"],
)
@pytest.mark.parametrize("student", STUDENTS[:4])
def test_mutation_matrix(status_action: str, student: str) -> None:
    interp = make_interpretation(
        interpretation_id=f"interp-mut-{status_action}-{student}",
        student_id=student,
    )
    interp.pull_events()
    if status_action == "revise":
        interp.revise(
            confidence=make_confidence(ConfidenceLevel.MEDIUM),
            summary=make_summary(
                text=f"Revised observational summary for {student}",
                pattern_count=1,
                cluster_count=1,
            ),
        )
        assert interp.is_revised()
    elif status_action == "invalidate":
        interp.invalidate(f"void-{student}")
        assert interp.is_invalidated()


@pytest.mark.parametrize("concept_value", [c.value for c in KNOWN_CONCEPTS])
@pytest.mark.parametrize("episode_value", [e.value for e in KNOWN_EPISODES])
def test_known_reference_matrix(concept_value: str, episode_value: str) -> None:
    concept_id = ConceptId(concept_value)
    episode_id = LearningEpisodeId(episode_value)
    InterpretationValidationPolicy.assert_known_concepts(KNOWN_CONCEPTS, {concept_id})
    InterpretationValidationPolicy.assert_known_episodes(KNOWN_EPISODES, {episode_id})
    interp = make_interpretation(
        interpretation_id=f"interp-{concept_value}-{episode_value}",
        clusters=[
            make_cluster(
                cluster_id=f"c-{concept_value}-{episode_value}",
                concept_id=concept_id,
                learning_episode_id=episode_id,
            )
        ],
        patterns=[
            make_pattern(
                pattern_id=f"p-{concept_value}-{episode_value}",
                description=f"Obs {concept_value} {episode_value}",
                concept_id=concept_id,
                learning_episode_id=episode_id,
            )
        ],
        context=make_context(
            context_id=f"ctx-{concept_value}-{episode_value}",
            concepts=(ConceptReference(concept_id=concept_id),),
            episodes=(episode_id,),
        ),
        concept_references=[ConceptReference(concept_id=concept_id)],
        learning_episode_ids=[episode_id],
        summary=make_summary(
            text=f"Observed pattern for {concept_value}",
            pattern_count=1,
            cluster_count=1,
        ),
    )
    assert interp.has_concept(concept_id)
    assert interp.has_learning_episode(episode_id)


@pytest.mark.parametrize("kind", PATTERN_KINDS)
def test_duplicate_pattern_signature_rejected_per_kind(kind: PatternKind) -> None:
    args = _pattern_args(kind)
    cluster = _cluster_for(kind)
    with pytest.raises(EducationalInvariantViolation):
        make_interpretation(
            clusters=[cluster],
            patterns=[
                make_pattern(pattern_id="a", **args),
                make_pattern(pattern_id="b", **args),
            ],
            confidence=make_confidence(_compatible_confidence(kind)),
            summary=make_summary(pattern_count=2, cluster_count=1),
        )


@pytest.mark.parametrize("kind", list(REPEATED_PATTERN_KINDS))
def test_repeated_kinds_require_occurrence(kind: PatternKind) -> None:
    with pytest.raises(EducationalInvariantViolation):
        make_pattern(
            kind=kind,
            description=f"bad {kind.value}",
            evidence_ids=(EVIDENCE_001, EVIDENCE_002),
            occurrence_count=1,
        )


@pytest.mark.parametrize("kind", PATTERN_KINDS)
def test_clustering_consistent_per_kind(kind: PatternKind) -> None:
    args = _pattern_args(kind)
    cluster = _cluster_for(kind)
    pattern = make_pattern(pattern_id=f"p-{kind.value}", **args)
    ClusteringPolicy.assert_consistent(
        (cluster,),
        (pattern,),
        make_confidence(_compatible_confidence(kind)),
    )


@pytest.mark.parametrize("i", range(20))
def test_merge_distinct_patterns(i: int) -> None:
    primary = make_interpretation(interpretation_id=f"primary-{i}")
    other = make_interpretation(
        interpretation_id=f"other-{i}",
        clusters=[
            make_cluster(
                cluster_id=f"cluster-other-{i}",
                theme=f"theme-{i}",
                evidence_ids=(EVIDENCE_001, EVIDENCE_003),
            )
        ],
        patterns=[
            make_pattern(
                pattern_id=f"pattern-other-{i}",
                kind=PatternKind.REPEATED_TRANSFER_FAILURE,
                description=f"Distinct transfer failure pattern {i}",
                evidence_ids=(EVIDENCE_001, EVIDENCE_003),
            )
        ],
        summary=make_summary(
            text=f"Observed distinct transfer failures {i}",
            pattern_count=1,
            cluster_count=1,
        ),
    )
    primary.merge(other)
    assert primary.pattern_count() == 2
    assert other.status is InterpretationStatus.MERGED


@pytest.mark.parametrize("evidence_value", [e.value for e in KNOWN_EVIDENCE])
def test_known_evidence_matrix(evidence_value: str) -> None:
    evidence_id = EvidenceId(evidence_value)
    InterpretationValidationPolicy.assert_known_evidence(KNOWN_EVIDENCE, {evidence_id})
    # Single-evidence non-repeated pattern when only one id; else pair with 001.
    if evidence_id == EVIDENCE_001:
        cluster = make_cluster(evidence_ids=(EVIDENCE_001,))
        pattern = make_pattern(
            kind=PatternKind.EVIDENCE_SUFFICIENCY,
            description=f"Sufficiency for {evidence_value}",
            evidence_ids=(EVIDENCE_001,),
            occurrence_count=1,
        )
    else:
        cluster = make_cluster(evidence_ids=(EVIDENCE_001, evidence_id))
        pattern = make_pattern(
            description=f"Retrieval involving {evidence_value}",
            evidence_ids=(EVIDENCE_001, evidence_id),
        )
    interp = make_interpretation(
        interpretation_id=f"interp-ev-{evidence_value}",
        clusters=[cluster],
        patterns=[pattern],
        confidence=make_confidence(ConfidenceLevel.HIGH),
        summary=make_summary(
            text=f"Observed evidence involvement of {evidence_value}",
            pattern_count=1,
            cluster_count=1,
        ),
    )
    assert interp.has_evidence(evidence_id)


@pytest.mark.parametrize("status", list(InterpretationStatus))
def test_status_enum_values(status: InterpretationStatus) -> None:
    assert isinstance(status.value, str)
    assert InterpretationValidationPolicy.assert_status(status) is status


@pytest.mark.parametrize(
    "pair",
    [
        (CONCEPT_SELECT, EPISODE_001),
        (CONCEPT_SELECT, EPISODE_002),
        (CONCEPT_ULTIMATE, EPISODE_001),
        (CONCEPT_ULTIMATE, EPISODE_002),
    ],
)
@pytest.mark.parametrize("kind", PATTERN_KINDS[:5])
def test_concept_episode_pattern_matrix(
    pair: tuple[ConceptId, LearningEpisodeId], kind: PatternKind
) -> None:
    concept_id, episode_id = pair
    args = _pattern_args(kind)
    cluster = _cluster_for(kind)
    cluster = make_cluster(
        cluster_id=f"c-{concept_id.value}-{episode_id.value}-{kind.value}",
        theme=f"{kind.value}",
        evidence_ids=cluster.evidence_ids,
        concept_id=concept_id,
        learning_episode_id=episode_id,
    )
    pattern = make_pattern(
        pattern_id=f"p-{concept_id.value}-{episode_id.value}-{kind.value}",
        concept_id=concept_id,
        learning_episode_id=episode_id,
        **args,
    )
    interp = make_interpretation(
        interpretation_id=f"i-{concept_id.value}-{episode_id.value}-{kind.value}",
        clusters=[cluster],
        patterns=[pattern],
        context=make_context(
            concepts=(ConceptReference(concept_id=concept_id),),
            episodes=(episode_id,),
        ),
        concept_references=[ConceptReference(concept_id=concept_id)],
        learning_episode_ids=[episode_id],
        confidence=make_confidence(_compatible_confidence(kind)),
        summary=make_summary(
            text=f"Observed {kind.value.replace('_', ' ')}",
            pattern_count=1,
            cluster_count=1,
        ),
    )
    assert interp.has_concept(concept_id)
    assert interp.has_learning_episode(episode_id)
