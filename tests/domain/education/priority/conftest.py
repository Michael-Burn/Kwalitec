"""Shared factories for Educational Priority domain tests."""

from __future__ import annotations

import pytest

from domain.education.foundation.enums import DiagnosisType, LearningDimension
from domain.education.foundation.ids import (
    ConceptId,
    DiagnosisId,
    HypothesisId,
    LearningEpisodeId,
    LearningObjectiveId,
    PriorityId,
)
from domain.education.foundation.references import (
    ConceptReference,
    LearningObjectiveReference,
)
from domain.education.priority import (
    DiagnosisReference,
    EducationalPriority,
    HypothesisReference,
    InstructionalImpact,
    InstructionalImpactLevel,
    PriorityConstraint,
    PriorityConstraintId,
    PriorityConstraintKind,
    PriorityFactor,
    PriorityFactorId,
    PriorityFactorKind,
    PriorityScope,
    PriorityScopeId,
    PriorityScopeKind,
    PriorityScore,
    PriorityScoreBand,
    Urgency,
    UrgencyLevel,
)

CONCEPT_SELECT = ConceptId("concept-select-mortality")
CONCEPT_ULTIMATE = ConceptId("concept-ultimate-mortality")
EPISODE_001 = LearningEpisodeId("episode-001")
EPISODE_002 = LearningEpisodeId("episode-002")
DIAGNOSIS_001 = DiagnosisId("diag-001")
DIAGNOSIS_002 = DiagnosisId("diag-002")
HYPOTHESIS_001 = HypothesisId("hyp-001")
HYPOTHESIS_002 = HypothesisId("hyp-002")

DEFAULT_DIAGNOSIS_TYPE = DiagnosisType.PREREQUISITE_GAP


@pytest.fixture
def priority_id() -> PriorityId:
    return PriorityId("prio-001")


@pytest.fixture
def student_id() -> str:
    return "student-ada"


def make_score(
    band: PriorityScoreBand = PriorityScoreBand.HIGH,
    *,
    ratio: float | None = 0.7,
    rationale: str | None = "instructional ordering for primary need",
) -> PriorityScore:
    return PriorityScore.of(band, ratio=ratio, rationale=rationale)


def make_urgency(
    level: UrgencyLevel = UrgencyLevel.ELEVATED,
    *,
    rationale: str | None = "material educational pressure",
) -> Urgency:
    return Urgency.of(level, rationale=rationale)


def make_impact(
    level: InstructionalImpactLevel = InstructionalImpactLevel.SUBSTANTIAL,
    *,
    statement: str = "Unlocks dependent objective progress",
) -> InstructionalImpact:
    return InstructionalImpact.of(level, statement)


def make_scope(
    *,
    scope_id: str = "scope-001",
    statement: str = "Order prerequisite repair ahead of GLM fitting practice",
    scope_kind: PriorityScopeKind = PriorityScopeKind.COMPETING_DIAGNOSES,
    dimension: LearningDimension | None = LearningDimension.UNDERSTANDING,
    concepts: tuple[ConceptReference, ...] | None = None,
    objectives: tuple[LearningObjectiveReference, ...] | None = None,
    episodes: tuple[LearningEpisodeId, ...] | None = None,
) -> PriorityScope:
    return PriorityScope(
        scope_id=PriorityScopeId(scope_id),
        statement=statement,
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


def make_factor(
    *,
    factor_id: str = "factor-001",
    kind: PriorityFactorKind = PriorityFactorKind.PREREQUISITE_IMPORTANCE,
    contribution: float = 0.85,
    rationale: str | None = None,
) -> PriorityFactor:
    return PriorityFactor(
        factor_id=PriorityFactorId(factor_id),
        kind=kind,
        contribution=contribution,
        rationale=rationale or f"Educational factor {kind.value}",
    )


def make_constraint(
    *,
    constraint_id: str = "constraint-001",
    kind: PriorityConstraintKind = (
        PriorityConstraintKind.PROTECT_PREREQUISITE_OVER_EXTENSION
    ),
    statement: str | None = None,
    related_factor_kind: PriorityFactorKind | None = None,
    max_urgency: UrgencyLevel | None = None,
    max_score_band: PriorityScoreBand | None = None,
) -> PriorityConstraint:
    return PriorityConstraint(
        constraint_id=PriorityConstraintId(constraint_id),
        kind=kind,
        statement=statement or f"Constraint {kind.value}",
        related_factor_kind=related_factor_kind,
        max_urgency=max_urgency,
        max_score_band=max_score_band,
    )


def make_diagnosis_ref(
    *,
    diagnosis_id: DiagnosisId | str = DIAGNOSIS_001,
    diagnosis_type: DiagnosisType = DEFAULT_DIAGNOSIS_TYPE,
) -> DiagnosisReference:
    if isinstance(diagnosis_id, str):
        diagnosis_id = DiagnosisId(diagnosis_id)
    return DiagnosisReference(
        diagnosis_id=diagnosis_id,
        diagnosis_type=diagnosis_type,
    )


def make_hypothesis_ref(
    *,
    hypothesis_id: HypothesisId | str = HYPOTHESIS_001,
) -> HypothesisReference:
    if isinstance(hypothesis_id, str):
        hypothesis_id = HypothesisId(hypothesis_id)
    return HypothesisReference(hypothesis_id=hypothesis_id)


def make_priority(
    *,
    priority_id: str | PriorityId = "prio-001",
    student_id: str = "student-ada",
    scope: PriorityScope | None = None,
    diagnosis_references: list[DiagnosisReference] | None = None,
    hypothesis_references: list[HypothesisReference] | None = None,
    factors: list[PriorityFactor] | None = None,
    constraints: list[PriorityConstraint] | None = None,
    score: PriorityScore | None = None,
    urgency: Urgency | None = None,
    instructional_impact: InstructionalImpact | None = None,
    calculate: bool = True,
) -> EducationalPriority:
    if isinstance(priority_id, str):
        priority_id = PriorityId(priority_id)
    resolved_factors = factors if factors is not None else [make_factor()]
    kwargs: dict = {
        "priority_id": priority_id,
        "student_id": student_id,
        "scope": scope or make_scope(),
        "diagnosis_references": diagnosis_references
        if diagnosis_references is not None
        else [make_diagnosis_ref()],
        "hypothesis_references": hypothesis_references
        if hypothesis_references is not None
        else [make_hypothesis_ref()],
        "factors": resolved_factors,
        "constraints": constraints,
    }
    if calculate and score is None and urgency is None and instructional_impact is None:
        return EducationalPriority.assign(**kwargs)
    return EducationalPriority.assign(
        **kwargs,
        score=score or make_score(),
        urgency=urgency or make_urgency(),
        instructional_impact=instructional_impact or make_impact(),
    )
