"""Shared factories for Evidence Interpretation domain tests."""

from __future__ import annotations

import pytest

from domain.education.evidence_interpretation import (
    EducationalScopeKind,
    EvidenceCluster,
    EvidenceClusterId,
    Interpretation,
    InterpretationConfidence,
    InterpretationContext,
    InterpretationContextId,
    InterpretationId,
    InterpretationSummary,
    InterpretedPattern,
    InterpretedPatternId,
    PatternKind,
)
from domain.education.foundation.enums import ConfidenceLevel, LearningDimension
from domain.education.foundation.ids import (
    ConceptId,
    EvidenceId,
    LearningEpisodeId,
    LearningObjectiveId,
)
from domain.education.foundation.references import (
    ConceptReference,
    LearningObjectiveReference,
)

CONCEPT_SELECT = ConceptId("concept-select-mortality")
CONCEPT_ULTIMATE = ConceptId("concept-ultimate-mortality")
EPISODE_001 = LearningEpisodeId("episode-001")
EPISODE_002 = LearningEpisodeId("episode-002")
EVIDENCE_001 = EvidenceId("evidence-001")
EVIDENCE_002 = EvidenceId("evidence-002")
EVIDENCE_003 = EvidenceId("evidence-003")
KNOWN_CONCEPTS = frozenset({CONCEPT_SELECT, CONCEPT_ULTIMATE})
KNOWN_EPISODES = frozenset({EPISODE_001, EPISODE_002})
KNOWN_EVIDENCE = frozenset({EVIDENCE_001, EVIDENCE_002, EVIDENCE_003})


@pytest.fixture
def interpretation_id() -> InterpretationId:
    return InterpretationId("interp-001")


@pytest.fixture
def student_id() -> str:
    return "student-ada"


def make_confidence(
    level: ConfidenceLevel = ConfidenceLevel.HIGH,
    *,
    ratio: float | None = 0.8,
) -> InterpretationConfidence:
    return InterpretationConfidence.of(level, ratio=ratio)


def make_summary(
    *,
    text: str = "Observed repeated retrieval failures on select mortality",
    pattern_count: int = 1,
    cluster_count: int = 1,
) -> InterpretationSummary:
    return InterpretationSummary.of(
        text,
        pattern_count=pattern_count,
        cluster_count=cluster_count,
    )


def make_cluster(
    *,
    cluster_id: str = "cluster-001",
    theme: str = "retrieval failures",
    evidence_ids: tuple[EvidenceId, ...] | None = None,
    concept_id: ConceptId | None = CONCEPT_SELECT,
    learning_episode_id: LearningEpisodeId | None = EPISODE_001,
) -> EvidenceCluster:
    return EvidenceCluster(
        cluster_id=EvidenceClusterId(cluster_id),
        theme=theme,
        evidence_ids=evidence_ids
        if evidence_ids is not None
        else (EVIDENCE_001, EVIDENCE_002),
        concept_id=concept_id,
        learning_episode_id=learning_episode_id,
    )


def make_pattern(
    *,
    pattern_id: str = "pattern-001",
    kind: PatternKind = PatternKind.REPEATED_RETRIEVAL_FAILURE,
    description: str = "Repeated retrieval failures on select ages",
    evidence_ids: tuple[EvidenceId, ...] | None = None,
    occurrence_count: int | None = None,
    concept_id: ConceptId | None = CONCEPT_SELECT,
    learning_episode_id: LearningEpisodeId | None = EPISODE_001,
) -> InterpretedPattern:
    ids = evidence_ids if evidence_ids is not None else (EVIDENCE_001, EVIDENCE_002)
    count = occurrence_count if occurrence_count is not None else max(2, len(ids))
    return InterpretedPattern(
        pattern_id=InterpretedPatternId(pattern_id),
        kind=kind,
        description=description,
        evidence_ids=ids,
        occurrence_count=count,
        concept_id=concept_id,
        learning_episode_id=learning_episode_id,
    )


def make_context(
    *,
    context_id: str = "ctx-001",
    educational_scope: str = "Select mortality concept scope",
    scope_kind: EducationalScopeKind = EducationalScopeKind.CONCEPT,
    dimension: LearningDimension | None = LearningDimension.RETENTION,
    concepts: tuple[ConceptReference, ...] | None = None,
    episodes: tuple[LearningEpisodeId, ...] | None = None,
    objectives: tuple[LearningObjectiveReference, ...] | None = None,
) -> InterpretationContext:
    return InterpretationContext(
        context_id=InterpretationContextId(context_id),
        educational_scope=educational_scope,
        scope_kind=scope_kind,
        learning_dimension=dimension,
        concept_references=concepts
        if concepts is not None
        else (ConceptReference(concept_id=CONCEPT_SELECT, label="Select mortality"),),
        learning_objective_references=objectives
        if objectives is not None
        else (
            LearningObjectiveReference(
                objective_id=LearningObjectiveId("lo-select-ultimate"),
                label="Interpret select mortality tables",
            ),
        ),
        learning_episode_ids=episodes if episodes is not None else (EPISODE_001,),
    )


def make_interpretation(
    *,
    interpretation_id: str = "interp-001",
    student_id: str = "student-ada",
    clusters: list[EvidenceCluster] | None = None,
    patterns: list[InterpretedPattern] | None = None,
    context: InterpretationContext | None = None,
    confidence: InterpretationConfidence | None = None,
    summary: InterpretationSummary | None = None,
    known_evidence: frozenset[EvidenceId] | None = KNOWN_EVIDENCE,
    known_concepts: frozenset[ConceptId] | None = KNOWN_CONCEPTS,
    known_episodes: frozenset[LearningEpisodeId] | None = KNOWN_EPISODES,
    concept_references: list[ConceptReference] | None = None,
    learning_episode_ids: list[LearningEpisodeId] | None = None,
) -> Interpretation:
    cluster_list = clusters or [make_cluster()]
    pattern_list = patterns or [make_pattern()]
    return Interpretation.interpret(
        interpretation_id=InterpretationId(interpretation_id),
        student_id=student_id,
        clusters=cluster_list,
        patterns=pattern_list,
        context=context or make_context(),
        confidence=confidence or make_confidence(),
        summary=summary
        or make_summary(
            pattern_count=len(pattern_list),
            cluster_count=len(cluster_list),
        ),
        known_evidence_ids=known_evidence,
        known_concept_ids=known_concepts,
        known_episode_ids=known_episodes,
        concept_references=concept_references
        or [ConceptReference(concept_id=CONCEPT_SELECT)],
        learning_episode_ids=learning_episode_ids or [EPISODE_001],
    )
