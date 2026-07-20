"""Shared factories for Teaching Intention domain tests."""

from __future__ import annotations

import pytest

from domain.education.foundation.enums import (
    DiagnosisType,
    LearningDimension,
    TeachingIntentionType,
)
from domain.education.foundation.ids import (
    ConceptId,
    DiagnosisId,
    HypothesisId,
    LearningObjectiveId,
    MisconceptionId,
    PriorityId,
    TeachingIntentionId,
)
from domain.education.foundation.references import (
    ConceptReference,
    LearningObjectiveReference,
    MisconceptionReference,
)
from domain.education.teaching_intention import (
    DiagnosisReference,
    ExpectedOutcome,
    HypothesisReference,
    IntentionConstraint,
    IntentionConstraintId,
    IntentionConstraintKind,
    IntentionGoal,
    IntentionGoalId,
    IntentionScope,
    IntentionScopeId,
    IntentionScopeKind,
    IntentionStrength,
    IntentionStrengthLevel,
    PriorityReference,
    TeachingIntention,
)

CONCEPT_SELECT = ConceptId("concept-select-mortality")
DIAGNOSIS_001 = DiagnosisId("diag-001")
DIAGNOSIS_002 = DiagnosisId("diag-002")
HYPOTHESIS_001 = HypothesisId("hyp-001")
HYPOTHESIS_002 = HypothesisId("hyp-002")
PRIORITY_001 = PriorityId("prio-001")
PRIORITY_002 = PriorityId("prio-002")
MISCONCEPTION_001 = MisconceptionId("misc-001")

DEFAULT_INTENTION_TYPE = TeachingIntentionType.STRENGTHEN_PREREQUISITE
DEFAULT_DIAGNOSIS_TYPE = DiagnosisType.PREREQUISITE_GAP

# Catalogue-aligned defaults for each intention type.
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
    TeachingIntentionType.STRENGTHEN_APPLICATION: (
        DiagnosisType.APPLICATION_WEAKNESS
    ),
    TeachingIntentionType.COMPLETE_MISSING_FACETS: (
        DiagnosisType.INCOMPLETE_UNDERSTANDING
    ),
}


@pytest.fixture
def intention_id() -> TeachingIntentionId:
    return TeachingIntentionId("ti-001")


@pytest.fixture
def student_id() -> str:
    return "student-ada"


def make_strength(
    level: IntentionStrengthLevel = IntentionStrengthLevel.MODERATE,
    *,
    rationale: str | None = "commitment to educational change",
) -> IntentionStrength:
    return IntentionStrength.of(level, rationale=rationale)


def make_outcome(
    *,
    statement: str = "Restore prerequisite capability for dependent objective",
    success_evidence: str = (
        "Successful probes on prerequisite; reduced downstream failures"
    ),
) -> ExpectedOutcome:
    return ExpectedOutcome.of(statement, success_evidence)


def make_goal(
    *,
    goal_id: str = "goal-001",
    statement: str | None = None,
    intention_type: TeachingIntentionType = DEFAULT_INTENTION_TYPE,
    success_evidence_hint: str | None = "Probe success on upstream objective",
) -> IntentionGoal:
    return IntentionGoal(
        goal_id=IntentionGoalId(goal_id),
        statement=statement
        or f"Seek educational change: {intention_type.value.replace('_', ' ')}",
        intention_type=intention_type,
        success_evidence_hint=success_evidence_hint,
    )


def make_scope(
    *,
    scope_id: str = "scope-001",
    statement: str = "Instructional scope for prerequisite repair",
    scope_kind: IntentionScopeKind = IntentionScopeKind.PREREQUISITE_CHAIN,
    dimension: LearningDimension | None = LearningDimension.UNDERSTANDING,
    concepts: tuple[ConceptReference, ...] | None = None,
    objectives: tuple[LearningObjectiveReference, ...] | None = None,
    misconceptions: tuple[MisconceptionReference, ...] | None = None,
) -> IntentionScope:
    return IntentionScope(
        scope_id=IntentionScopeId(scope_id),
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
        misconception_references=misconceptions if misconceptions is not None else (),
    )


def make_constraint(
    *,
    constraint_id: str = "constraint-001",
    kind: IntentionConstraintKind = IntentionConstraintKind.REQUIRE_PRIORITY_REFERENCE,
    statement: str | None = None,
    forbidden_intention_type: TeachingIntentionType | None = None,
    max_strength: IntentionStrengthLevel | None = None,
) -> IntentionConstraint:
    return IntentionConstraint(
        constraint_id=IntentionConstraintId(constraint_id),
        kind=kind,
        statement=statement or f"Constraint {kind.value}",
        forbidden_intention_type=forbidden_intention_type,
        max_strength=max_strength,
    )


def make_priority_ref(
    *,
    priority_id: PriorityId | str = PRIORITY_001,
) -> PriorityReference:
    if isinstance(priority_id, str):
        priority_id = PriorityId(priority_id)
    return PriorityReference(priority_id=priority_id)


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


def make_intention(
    *,
    intention_id: str | TeachingIntentionId = "ti-001",
    student_id: str = "student-ada",
    intention_type: TeachingIntentionType = DEFAULT_INTENTION_TYPE,
    goal: IntentionGoal | None = None,
    scope: IntentionScope | None = None,
    expected_outcome: ExpectedOutcome | None = None,
    strength: IntentionStrength | None = None,
    priority_references: list[PriorityReference] | None = None,
    diagnosis_references: list[DiagnosisReference] | None = None,
    hypothesis_references: list[HypothesisReference] | None = None,
    constraints: list[IntentionConstraint] | None = None,
    activate: bool = False,
) -> TeachingIntention:
    if isinstance(intention_id, str):
        intention_id = TeachingIntentionId(intention_id)
    diagnosis_type = INTENTION_DIAGNOSIS[intention_type]
    intention = TeachingIntention.create(
        intention_id=intention_id,
        student_id=student_id,
        intention_type=intention_type,
        goal=goal or make_goal(intention_type=intention_type),
        scope=scope or make_scope(),
        expected_outcome=expected_outcome or make_outcome(),
        strength=strength or make_strength(),
        priority_references=priority_references
        if priority_references is not None
        else [make_priority_ref()],
        diagnosis_references=diagnosis_references
        if diagnosis_references is not None
        else [make_diagnosis_ref(diagnosis_type=diagnosis_type)],
        hypothesis_references=hypothesis_references
        if hypothesis_references is not None
        else [make_hypothesis_ref()],
        constraints=constraints,
    )
    if activate:
        intention.activate()
    return intention
