"""Map Concept ↔ ConceptDTO."""

from __future__ import annotations

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
from infrastructure.persistence.dto.subject_knowledge import (
    ApplicationContextDTO,
    ConceptBoundaryDTO,
    ConceptDTO,
    DependencyDTO,
    LearningObjectiveDTO,
    MasteryIndicatorDTO,
    MisconceptionDTO,
    RepresentationDTO,
    TransferContextDTO,
)
from infrastructure.persistence.mappers.codec import enum_value, id_value, optional_enum_value


class SubjectKnowledgeMapper:
    """Pure structural mapper for Concept aggregates."""

    @staticmethod
    def to_persistence(concept: Concept) -> ConceptDTO:
        return ConceptDTO(
            concept_id=id_value(concept.concept_id),
            canonical_name=concept.canonical_name,
            core_meaning=concept.core_meaning,
            boundary=ConceptBoundaryDTO(
                inclusion=concept.boundary.inclusion,
                exclusion=concept.boundary.exclusion,
                key_contrast=concept.boundary.key_contrast,
            ),
            learning_objectives=tuple(
                _objective_to_dto(item) for item in concept.learning_objectives
            ),
            representations=tuple(
                _representation_to_dto(item) for item in concept.representations
            ),
            misconceptions=tuple(
                _misconception_to_dto(item) for item in concept.misconceptions
            ),
            application_contexts=tuple(
                _application_to_dto(item) for item in concept.application_contexts
            ),
            transfer_contexts=tuple(
                _transfer_to_dto(item) for item in concept.transfer_contexts
            ),
            dependencies=tuple(
                DependencyDTO(
                    target_concept_id=id_value(edge.target_concept_id),
                    kind=enum_value(edge.kind),
                    description=edge.description,
                )
                for edge in concept.dependencies
            ),
        )

    @staticmethod
    def to_domain(dto: ConceptDTO) -> Concept:
        return Concept(
            concept_id=ConceptId(dto.concept_id),
            canonical_name=dto.canonical_name,
            core_meaning=dto.core_meaning,
            boundary=ConceptBoundary(
                inclusion=dto.boundary.inclusion,
                exclusion=dto.boundary.exclusion,
                key_contrast=dto.boundary.key_contrast,
            ),
            learning_objectives=[
                _objective_from_dto(item) for item in dto.learning_objectives
            ],
            representations=[
                _representation_from_dto(item) for item in dto.representations
            ],
            misconceptions=[
                _misconception_from_dto(item) for item in dto.misconceptions
            ],
            application_contexts=[
                _application_from_dto(item) for item in dto.application_contexts
            ],
            transfer_contexts=[
                _transfer_from_dto(item) for item in dto.transfer_contexts
            ],
            dependencies=[
                Dependency(
                    target_concept_id=ConceptId(edge.target_concept_id),
                    kind=DependencyKind(edge.kind),
                    description=edge.description,
                )
                for edge in dto.dependencies
            ],
        )


def _indicator_to_dto(indicator: MasteryIndicator) -> MasteryIndicatorDTO:
    return MasteryIndicatorDTO(
        description=indicator.description,
        observable_signal=indicator.observable_signal,
        dimension=optional_enum_value(indicator.dimension),
    )


def _indicator_from_dto(dto: MasteryIndicatorDTO) -> MasteryIndicator:
    dimension = (
        LearningDimension(dto.dimension) if dto.dimension is not None else None
    )
    return MasteryIndicator(
        description=dto.description,
        observable_signal=dto.observable_signal,
        dimension=dimension,
    )


def _objective_to_dto(objective: LearningObjective) -> LearningObjectiveDTO:
    return LearningObjectiveDTO(
        objective_id=id_value(objective.objective_id),
        concept_id=id_value(objective.concept_id),
        statement=objective.statement,
        success_criteria=tuple(objective.success_criteria),
        mastery_indicators=tuple(
            _indicator_to_dto(item) for item in objective.mastery_indicators
        ),
    )


def _objective_from_dto(dto: LearningObjectiveDTO) -> LearningObjective:
    return LearningObjective(
        objective_id=LearningObjectiveId(dto.objective_id),
        concept_id=ConceptId(dto.concept_id),
        statement=dto.statement,
        success_criteria=tuple(dto.success_criteria),
        mastery_indicators=tuple(
            _indicator_from_dto(item) for item in dto.mastery_indicators
        ),
    )


def _representation_to_dto(item: Representation) -> RepresentationDTO:
    return RepresentationDTO(
        representation_id=id_value(item.representation_id),
        concept_id=id_value(item.concept_id),
        kind=enum_value(item.kind),
        description=item.description,
        educational_purpose=item.educational_purpose,
    )


def _representation_from_dto(dto: RepresentationDTO) -> Representation:
    return Representation(
        representation_id=RepresentationId(dto.representation_id),
        concept_id=ConceptId(dto.concept_id),
        kind=RepresentationKind(dto.kind),
        description=dto.description,
        educational_purpose=dto.educational_purpose,
    )


def _misconception_to_dto(item: Misconception) -> MisconceptionDTO:
    return MisconceptionDTO(
        misconception_id=id_value(item.misconception_id),
        concept_id=id_value(item.concept_id),
        description=item.description,
        incorrect_reasoning=item.incorrect_reasoning,
        likely_causes=tuple(item.likely_causes),
        observable_evidence=tuple(item.observable_evidence),
        recommended_teaching_intentions=tuple(
            enum_value(value) for value in item.recommended_teaching_intentions
        ),
        recommended_strategies=tuple(
            enum_value(value) for value in item.recommended_strategies
        ),
        repair_evidence=tuple(item.repair_evidence),
    )


def _misconception_from_dto(dto: MisconceptionDTO) -> Misconception:
    return Misconception(
        misconception_id=MisconceptionId(dto.misconception_id),
        concept_id=ConceptId(dto.concept_id),
        description=dto.description,
        incorrect_reasoning=dto.incorrect_reasoning,
        likely_causes=tuple(dto.likely_causes),
        observable_evidence=tuple(dto.observable_evidence),
        recommended_teaching_intentions=tuple(
            TeachingIntentionType(value)
            for value in dto.recommended_teaching_intentions
        ),
        recommended_strategies=tuple(
            TeachingStrategyType(value) for value in dto.recommended_strategies
        ),
        repair_evidence=tuple(dto.repair_evidence),
    )


def _application_to_dto(item: ApplicationContext) -> ApplicationContextDTO:
    return ApplicationContextDTO(
        context_id=id_value(item.context_id),
        concept_id=id_value(item.concept_id),
        description=item.description,
        task_demand=item.task_demand,
        assumptions=item.assumptions,
        constraints=item.constraints,
    )


def _application_from_dto(dto: ApplicationContextDTO) -> ApplicationContext:
    return ApplicationContext(
        context_id=ApplicationContextId(dto.context_id),
        concept_id=ConceptId(dto.concept_id),
        description=dto.description,
        task_demand=dto.task_demand,
        assumptions=dto.assumptions,
        constraints=dto.constraints,
    )


def _transfer_to_dto(item: TransferContext) -> TransferContextDTO:
    base = (
        id_value(item.base_application_context_id)
        if item.base_application_context_id is not None
        else None
    )
    return TransferContextDTO(
        context_id=id_value(item.context_id),
        concept_id=id_value(item.concept_id),
        description=item.description,
        surface_variation=item.surface_variation,
        underlying_demand=item.underlying_demand,
        transfer_level=enum_value(item.transfer_level),
        base_application_context_id=base,
    )


def _transfer_from_dto(dto: TransferContextDTO) -> TransferContext:
    base = (
        ApplicationContextId(dto.base_application_context_id)
        if dto.base_application_context_id is not None
        else None
    )
    return TransferContext(
        context_id=TransferContextId(dto.context_id),
        concept_id=ConceptId(dto.concept_id),
        description=dto.description,
        surface_variation=dto.surface_variation,
        underlying_demand=dto.underlying_demand,
        transfer_level=TransferLevel(dto.transfer_level),
        base_application_context_id=base,
    )
