"""Shared factories for Subject Knowledge domain tests."""

from __future__ import annotations

import pytest

from domain.education.foundation.enums import (
    DependencyKind,
    LearningDimension,
    RepresentationKind,
    TeachingIntentionType,
    TeachingStrategyType,
    TransferLevel,
)
from domain.education.foundation.ids import (
    ConceptId,
    LearningObjectiveId,
    MisconceptionId,
)
from domain.education.subject_knowledge import (
    ApplicationContext,
    ApplicationContextId,
    Concept,
    ConceptBoundary,
    Dependency,
    LearningObjective,
    MasteryIndicator,
    Misconception,
    Representation,
    RepresentationId,
    TransferContext,
    TransferContextId,
)


@pytest.fixture
def concept_id() -> ConceptId:
    return ConceptId("concept-force-of-mortality")


@pytest.fixture
def other_concept_id() -> ConceptId:
    return ConceptId("concept-present-value")


@pytest.fixture
def boundary() -> ConceptBoundary:
    return ConceptBoundary(
        inclusion="instantaneous mortality rate at a given age",
        exclusion="crude annual mortality rates without continuous basis",
        key_contrast="force of mortality vs qx",
    )


@pytest.fixture
def mastery_indicator() -> MasteryIndicator:
    return MasteryIndicator(
        description="explains why a method applies",
        observable_signal="states conditions of use correctly",
        dimension=LearningDimension.UNDERSTANDING,
    )


def make_objective(
    concept_id: ConceptId,
    *,
    objective_id: str = "lo-001",
    statement: str = "Explain force of mortality and compute a survival probability",
) -> LearningObjective:
    return LearningObjective(
        objective_id=LearningObjectiveId(objective_id),
        concept_id=concept_id,
        statement=statement,
        success_criteria=(
            "states definition accurately",
            "computes under constant force",
        ),
        mastery_indicators=(
            MasteryIndicator(
                description="accurate definition and paraphrase",
                observable_signal="gives formal and accessible paraphrase",
            ),
        ),
    )


def make_concept(
    concept_id: ConceptId | None = None,
    *,
    name: str = "Force of mortality",
    objective_id: str = "lo-001",
) -> Concept:
    cid = concept_id or ConceptId("concept-force-of-mortality")
    objective = make_objective(cid, objective_id=objective_id)
    return Concept.create(
        concept_id=cid,
        canonical_name=name,
        core_meaning=(
            "The instantaneous rate of mortality at a given age — "
            "the continuous analogue of a mortality rate."
        ),
        boundary=ConceptBoundary(
            inclusion="instantaneous mortality intensity",
            exclusion="discrete annual rates alone",
            key_contrast="mu_x versus qx",
        ),
        initial_objective=objective,
    )


def make_misconception(
    concept_id: ConceptId,
    *,
    misconception_id: str = "misc-001",
) -> Misconception:
    return Misconception(
        misconception_id=MisconceptionId(misconception_id),
        concept_id=concept_id,
        description="Treats continuous and discrete models as freely interchangeable",
        incorrect_reasoning=(
            "Notation differs only cosmetically so formulae may be swapped"
        ),
        likely_causes=("over-exposure to continuous examples",),
        observable_evidence=("applies continuous formula to discrete schedule",),
        recommended_teaching_intentions=(
            TeachingIntentionType.REPAIR_MISCONCEPTION,
        ),
        recommended_strategies=(TeachingStrategyType.COUNTEREXAMPLE,),
        repair_evidence=("refuses free substitution and explains payment timing",),
    )


def make_representation(
    concept_id: ConceptId,
    *,
    representation_id: str = "rep-001",
    kind: RepresentationKind = RepresentationKind.SYMBOLIC,
) -> Representation:
    return Representation(
        representation_id=RepresentationId(representation_id),
        concept_id=concept_id,
        kind=kind,
        description="Symbolic expression for force of mortality",
        educational_purpose="Make the continuous intensity inspectable",
    )


def make_application_context(
    concept_id: ConceptId,
    *,
    context_id: str = "app-001",
) -> ApplicationContext:
    return ApplicationContext(
        context_id=ApplicationContextId(context_id),
        concept_id=concept_id,
        description="Compute survival probability under constant force",
        task_demand="derive and evaluate tpx under constant mu",
        assumptions="constant force of mortality",
        constraints="syllabus-legitimate continuous model",
    )


def make_transfer_context(
    concept_id: ConceptId,
    *,
    context_id: str = "xfer-001",
    base: ApplicationContextId | None = None,
    level: TransferLevel = TransferLevel.NEAR,
) -> TransferContext:
    return TransferContext(
        context_id=TransferContextId(context_id),
        concept_id=concept_id,
        description="Reworded contract with altered rate basis",
        surface_variation="different wording and interest/mortality basis",
        underlying_demand="same contingent present-value structure",
        transfer_level=level,
        base_application_context_id=base,
    )


def make_dependency(
    target: ConceptId,
    *,
    kind: DependencyKind = DependencyKind.REQUIRED_PREREQUISITE,
    description: str = "Required conceptual foundation",
) -> Dependency:
    return Dependency(
        target_concept_id=target,
        kind=kind,
        description=description,
    )
