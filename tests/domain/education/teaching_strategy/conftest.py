"""Shared factories for Teaching Strategy domain tests."""

from __future__ import annotations

import pytest

from domain.education.foundation.enums import (
    DiagnosisType,
    TeachingIntentionType,
    TeachingStrategyType,
)
from domain.education.foundation.ids import (
    DiagnosisId,
    HypothesisId,
    TeachingIntentionId,
    TeachingStrategyId,
)
from domain.education.teaching_strategy import (
    ComplexityLevel,
    CompositionPattern,
    DiagnosisReference,
    EffectivenessLevel,
    HypothesisReference,
    InstructionalComplexity,
    IntentionReference,
    SecondaryStrategyReference,
    StrategyConstraint,
    StrategyConstraintId,
    StrategyConstraintKind,
    StrategyEffectiveness,
    StrategyGoal,
    StrategyGoalId,
    StrategyRationale,
    StrategyRationaleId,
    TeachingStrategy,
)

DEFAULT_INTENTION = TeachingIntentionType.STRENGTHEN_PREREQUISITE
DEFAULT_STRATEGY = TeachingStrategyType.WORKED_EXAMPLE
DEFAULT_DIAGNOSIS = DiagnosisType.PREREQUISITE_GAP

# Catalogue §4 affinity defaults — one preferred primary per intention.
INTENTION_STRATEGY: dict[TeachingIntentionType, TeachingStrategyType] = {
    TeachingIntentionType.REPAIR_MISCONCEPTION: (
        TeachingStrategyType.MISCONCEPTION_CONFRONTATION
    ),
    TeachingIntentionType.BUILD_INTUITION: TeachingStrategyType.ANALOGY,
    TeachingIntentionType.STRENGTHEN_PREREQUISITE: TeachingStrategyType.WORKED_EXAMPLE,
    TeachingIntentionType.IMPROVE_TRANSFER: TeachingStrategyType.INTERLEAVING,
    TeachingIntentionType.INCREASE_PROCEDURAL_FLUENCY: (
        TeachingStrategyType.PROGRESSIVE_SCAFFOLDING
    ),
    TeachingIntentionType.CONSOLIDATE_UNDERSTANDING: (
        TeachingStrategyType.CONCEPT_COMPARISON
    ),
    TeachingIntentionType.RECOVER_CONFIDENCE: (
        TeachingStrategyType.PROGRESSIVE_SCAFFOLDING
    ),
    TeachingIntentionType.PREPARE_FOR_EXAMINATION: (
        TeachingStrategyType.EXAM_SIMULATION
    ),
    TeachingIntentionType.IMPROVE_RETENTION: TeachingStrategyType.RETRIEVAL_FIRST,
    TeachingIntentionType.CALIBRATE_CONFIDENCE_DOWNWARD: (
        TeachingStrategyType.SOCRATIC_QUESTIONING
    ),
    TeachingIntentionType.CONNECT_FRAGMENTED_KNOWLEDGE: (
        TeachingStrategyType.CONCEPT_MAPPING
    ),
    TeachingIntentionType.STRENGTHEN_APPLICATION: (
        TeachingStrategyType.PROGRESSIVE_SCAFFOLDING
    ),
    TeachingIntentionType.COMPLETE_MISSING_FACETS: (
        TeachingStrategyType.GUIDED_DISCOVERY
    ),
}

INTENTION_DIAGNOSIS: dict[TeachingIntentionType, DiagnosisType] = {
    TeachingIntentionType.REPAIR_MISCONCEPTION: DiagnosisType.MISCONCEPTION,
    TeachingIntentionType.BUILD_INTUITION: DiagnosisType.CONCEPTUAL_MISUNDERSTANDING,
    TeachingIntentionType.STRENGTHEN_PREREQUISITE: DiagnosisType.PREREQUISITE_GAP,
    TeachingIntentionType.IMPROVE_TRANSFER: DiagnosisType.TRANSFER_WEAKNESS,
    TeachingIntentionType.INCREASE_PROCEDURAL_FLUENCY: (
        DiagnosisType.PROCEDURAL_WEAKNESS
    ),
    TeachingIntentionType.CONSOLIDATE_UNDERSTANDING: (
        DiagnosisType.INCOMPLETE_UNDERSTANDING
    ),
    TeachingIntentionType.RECOVER_CONFIDENCE: DiagnosisType.LOW_CONFIDENCE,
    TeachingIntentionType.PREPARE_FOR_EXAMINATION: (
        DiagnosisType.EXAM_TECHNIQUE_WEAKNESS
    ),
    TeachingIntentionType.IMPROVE_RETENTION: DiagnosisType.WEAK_RETENTION,
    TeachingIntentionType.CALIBRATE_CONFIDENCE_DOWNWARD: (
        DiagnosisType.FALSE_CONFIDENCE
    ),
    TeachingIntentionType.CONNECT_FRAGMENTED_KNOWLEDGE: (
        DiagnosisType.KNOWLEDGE_FRAGMENTATION
    ),
    TeachingIntentionType.STRENGTHEN_APPLICATION: DiagnosisType.APPLICATION_WEAKNESS,
    TeachingIntentionType.COMPLETE_MISSING_FACETS: (
        DiagnosisType.INCOMPLETE_UNDERSTANDING
    ),
}

CANONICAL_SECONDARIES: dict[CompositionPattern, tuple[TeachingStrategyType, ...]] = {
    CompositionPattern.ANALOGY_TO_GUIDED_PRACTICE: (
        TeachingStrategyType.WORKED_EXAMPLE,
        TeachingStrategyType.PROGRESSIVE_SCAFFOLDING,
    ),
    CompositionPattern.MISCONCEPTION_REPAIR_ARC: (
        TeachingStrategyType.COUNTEREXAMPLE,
        TeachingStrategyType.ERROR_LED_TEACHING,
    ),
    CompositionPattern.MODELLING_TO_INDEPENDENCE: (
        TeachingStrategyType.PROGRESSIVE_SCAFFOLDING,
        TeachingStrategyType.FADED_GUIDANCE,
    ),
    CompositionPattern.RETENTION_ARC: (
        TeachingStrategyType.DIRECT_EXPLANATION,
        TeachingStrategyType.SPACED_REINFORCEMENT,
    ),
    CompositionPattern.DISCRIMINATION_TO_EXAM: (
        TeachingStrategyType.INTERLEAVING,
        TeachingStrategyType.EXAM_SIMULATION,
    ),
    CompositionPattern.DISCOVERY_DEEPENING: (
        TeachingStrategyType.SOCRATIC_QUESTIONING,
        TeachingStrategyType.CONCEPT_MAPPING,
        TeachingStrategyType.RETRIEVAL_AFTER_INSTRUCTION,
    ),
    CompositionPattern.INTUITION_TO_FORM: (
        TeachingStrategyType.DUAL_REPRESENTATION,
        TeachingStrategyType.DIRECT_EXPLANATION,
        TeachingStrategyType.CONCEPT_COMPARISON,
    ),
}

CANONICAL_PRIMARY: dict[CompositionPattern, TeachingStrategyType] = {
    CompositionPattern.ANALOGY_TO_GUIDED_PRACTICE: TeachingStrategyType.ANALOGY,
    CompositionPattern.MISCONCEPTION_REPAIR_ARC: (
        TeachingStrategyType.MISCONCEPTION_CONFRONTATION
    ),
    CompositionPattern.MODELLING_TO_INDEPENDENCE: TeachingStrategyType.WORKED_EXAMPLE,
    CompositionPattern.RETENTION_ARC: TeachingStrategyType.RETRIEVAL_FIRST,
    CompositionPattern.DISCRIMINATION_TO_EXAM: (
        TeachingStrategyType.CONCEPT_COMPARISON
    ),
    CompositionPattern.DISCOVERY_DEEPENING: TeachingStrategyType.GUIDED_DISCOVERY,
    CompositionPattern.INTUITION_TO_FORM: TeachingStrategyType.ANALOGY,
}


@pytest.fixture
def strategy_id() -> TeachingStrategyId:
    return TeachingStrategyId("ts-001")


@pytest.fixture
def student_id() -> str:
    return "student-ada"


def make_effectiveness(
    level: EffectivenessLevel = EffectivenessLevel.MODERATE,
    *,
    rationale: str | None = "expected instructional efficacy",
) -> StrategyEffectiveness:
    return StrategyEffectiveness.of(level, rationale=rationale)


def make_complexity(
    level: ComplexityLevel = ComplexityLevel.MODERATE,
    *,
    rationale: str | None = "instructional demand estimate",
) -> InstructionalComplexity:
    return InstructionalComplexity.of(level, rationale=rationale)


def make_goal(
    *,
    goal_id: str = "goal-001",
    statement: str | None = None,
    strategy_type: TeachingStrategyType = DEFAULT_STRATEGY,
    expected_evidence_hint: str | None = "Student narrates decision points",
) -> StrategyGoal:
    return StrategyGoal(
        goal_id=StrategyGoalId(goal_id),
        statement=statement
        or f"Pursue {strategy_type.value.replace('_', ' ')} as instructional approach",
        strategy_type=strategy_type,
        expected_evidence_hint=expected_evidence_hint,
    )


def make_rationale(
    *,
    rationale_id: str = "rationale-001",
    statement: str = (
        "Selected because diagnosis and intention require this instructional approach"
    ),
) -> StrategyRationale:
    return StrategyRationale(
        rationale_id=StrategyRationaleId(rationale_id),
        statement=statement,
        diagnosis_link="aligned with referenced diagnosis",
        intention_link="serves named teaching intention",
    )


def make_constraint(
    *,
    constraint_id: str = "constraint-001",
    kind: StrategyConstraintKind = StrategyConstraintKind.REQUIRE_INTENTION_REFERENCE,
    statement: str | None = None,
    forbidden_strategy_type: TeachingStrategyType | None = None,
    max_complexity: ComplexityLevel | None = None,
) -> StrategyConstraint:
    return StrategyConstraint(
        constraint_id=StrategyConstraintId(constraint_id),
        kind=kind,
        statement=statement or f"Constraint {kind.value}",
        forbidden_strategy_type=forbidden_strategy_type,
        max_complexity=max_complexity,
    )


def make_intention_ref(
    *,
    intention_id: TeachingIntentionId | str = "ti-001",
    intention_type: TeachingIntentionType = DEFAULT_INTENTION,
) -> IntentionReference:
    if isinstance(intention_id, str):
        intention_id = TeachingIntentionId(intention_id)
    return IntentionReference(
        intention_id=intention_id,
        intention_type=intention_type,
    )


def make_diagnosis_ref(
    *,
    diagnosis_id: DiagnosisId | str = "diag-001",
    diagnosis_type: DiagnosisType = DEFAULT_DIAGNOSIS,
) -> DiagnosisReference:
    if isinstance(diagnosis_id, str):
        diagnosis_id = DiagnosisId(diagnosis_id)
    return DiagnosisReference(
        diagnosis_id=diagnosis_id,
        diagnosis_type=diagnosis_type,
    )


def make_hypothesis_ref(
    *,
    hypothesis_id: HypothesisId | str = "hyp-001",
) -> HypothesisReference:
    if isinstance(hypothesis_id, str):
        hypothesis_id = HypothesisId(hypothesis_id)
    return HypothesisReference(hypothesis_id=hypothesis_id)


def make_secondary(
    strategy_type: TeachingStrategyType,
    sequence_order: int,
) -> SecondaryStrategyReference:
    return SecondaryStrategyReference(
        strategy_type=strategy_type,
        sequence_order=sequence_order,
    )


def make_strategy(
    *,
    strategy_id: str | TeachingStrategyId = "ts-001",
    student_id: str = "student-ada",
    primary_strategy: TeachingStrategyType | None = None,
    intention_type: TeachingIntentionType = DEFAULT_INTENTION,
    goal: StrategyGoal | None = None,
    rationale: StrategyRationale | None = None,
    effectiveness: StrategyEffectiveness | None = None,
    complexity: InstructionalComplexity | None = None,
    intention_references: list[IntentionReference] | None = None,
    diagnosis_references: list[DiagnosisReference] | None = None,
    hypothesis_references: list[HypothesisReference] | None = None,
    secondary_strategies: list[SecondaryStrategyReference] | None = None,
    constraints: list[StrategyConstraint] | None = None,
    composition_pattern: CompositionPattern | None = None,
    select: bool = False,
) -> TeachingStrategy:
    if isinstance(strategy_id, str):
        strategy_id = TeachingStrategyId(strategy_id)
    primary = primary_strategy or INTENTION_STRATEGY[intention_type]
    diagnosis_type = INTENTION_DIAGNOSIS[intention_type]
    strategy = TeachingStrategy.create(
        strategy_id=strategy_id,
        student_id=student_id,
        primary_strategy=primary,
        goal=goal or make_goal(strategy_type=primary),
        rationale=rationale or make_rationale(),
        effectiveness=effectiveness or make_effectiveness(),
        complexity=complexity or make_complexity(),
        intention_references=intention_references
        if intention_references is not None
        else [make_intention_ref(intention_type=intention_type)],
        diagnosis_references=diagnosis_references
        if diagnosis_references is not None
        else [make_diagnosis_ref(diagnosis_type=diagnosis_type)],
        hypothesis_references=hypothesis_references
        if hypothesis_references is not None
        else [make_hypothesis_ref()],
        secondary_strategies=secondary_strategies,
        constraints=constraints,
        composition_pattern=composition_pattern,
    )
    if select:
        strategy.select()
    return strategy
