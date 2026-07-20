"""Map EducationalOrchestrator ↔ OrchestratorDTO."""

from __future__ import annotations

from domain.education.foundation.enums import TeachingStrategyType
from domain.education.foundation.ids import (
    DecisionId,
    LearningEpisodeId,
    OrchestratorId,
    TeachingStrategyId,
)
from domain.education.orchestrator import (
    ApprovedDecisionReference,
    EducationalOrchestrator,
    EpisodeReference,
    EvidenceCollectionPointKind,
    OrchestrationPlan,
    OrchestrationPlanId,
    OrchestrationStage,
    OrchestrationStageId,
    OrchestrationStageKind,
    OrchestrationState,
    OrchestrationStatus,
    StageStatus,
    StrategyReference,
)
from infrastructure.persistence.dto.orchestrator import (
    ApprovedDecisionReferenceDTO,
    EpisodeReferenceDTO,
    OrchestrationPlanDTO,
    OrchestrationStageDTO,
    OrchestrationStateDTO,
    OrchestratorDTO,
    OrchestratorStrategyReferenceDTO,
)
from infrastructure.persistence.mappers.codec import (
    enum_value,
    id_value,
    optional_enum_value,
    optional_id_value,
)


class OrchestratorMapper:
    """Pure structural mapper for EducationalOrchestrator."""

    @staticmethod
    def to_persistence(orchestrator: EducationalOrchestrator) -> OrchestratorDTO:
        return OrchestratorDTO(
            orchestrator_id=id_value(orchestrator.orchestrator_id),
            student_id=orchestrator.student_id,
            decision_reference=ApprovedDecisionReferenceDTO(
                decision_id=id_value(orchestrator.decision_reference.decision_id),
                approved=orchestrator.decision_reference.approved,
            ),
            strategy_references=tuple(
                OrchestratorStrategyReferenceDTO(
                    strategy_id=id_value(ref.strategy_id),
                    strategy_type=enum_value(ref.strategy_type),
                )
                for ref in orchestrator.strategy_references
            ),
            plan=OrchestrationPlanDTO(
                plan_id=id_value(orchestrator.plan.plan_id),
                stages=tuple(
                    _stage_to_dto(stage) for stage in orchestrator.plan.stages
                ),
                label=orchestrator.plan.label,
            ),
            episode_references=tuple(
                EpisodeReferenceDTO(episode_id=id_value(ref.episode_id))
                for ref in orchestrator.episode_references
            ),
            state=OrchestrationStateDTO(
                status=enum_value(orchestrator.state.status),
                current_stage_id=optional_id_value(
                    orchestrator.state.current_stage_id
                ),
                pause_reason=orchestrator.state.pause_reason,
            ),
        )

    @staticmethod
    def to_domain(dto: OrchestratorDTO) -> EducationalOrchestrator:
        return EducationalOrchestrator(
            orchestrator_id=OrchestratorId(dto.orchestrator_id),
            student_id=dto.student_id,
            decision_reference=ApprovedDecisionReference(
                decision_id=DecisionId(dto.decision_reference.decision_id),
                approved=dto.decision_reference.approved,
            ),
            strategy_references=tuple(
                StrategyReference(
                    strategy_id=TeachingStrategyId(ref.strategy_id),
                    strategy_type=TeachingStrategyType(ref.strategy_type),
                )
                for ref in dto.strategy_references
            ),
            plan=OrchestrationPlan(
                plan_id=OrchestrationPlanId(dto.plan.plan_id),
                stages=tuple(_stage_from_dto(stage) for stage in dto.plan.stages),
                label=dto.plan.label,
            ),
            episode_references=tuple(
                EpisodeReference(episode_id=LearningEpisodeId(ref.episode_id))
                for ref in dto.episode_references
            ),
            state=OrchestrationState(
                status=OrchestrationStatus(dto.state.status),
                current_stage_id=(
                    OrchestrationStageId(dto.state.current_stage_id)
                    if dto.state.current_stage_id is not None
                    else None
                ),
                pause_reason=dto.state.pause_reason,
            ),
        )


def _stage_to_dto(stage: OrchestrationStage) -> OrchestrationStageDTO:
    return OrchestrationStageDTO(
        stage_id=id_value(stage.stage_id),
        kind=enum_value(stage.kind),
        sequence_index=stage.sequence_index,
        label=stage.label,
        required=stage.required,
        status=enum_value(stage.status),
        evidence_collection_point=optional_enum_value(
            stage.evidence_collection_point
        ),
        episode_id=optional_id_value(stage.episode_id),
    )


def _stage_from_dto(dto: OrchestrationStageDTO) -> OrchestrationStage:
    return OrchestrationStage(
        stage_id=OrchestrationStageId(dto.stage_id),
        kind=OrchestrationStageKind(dto.kind),
        sequence_index=dto.sequence_index,
        label=dto.label,
        required=dto.required,
        status=StageStatus(dto.status),
        evidence_collection_point=(
            EvidenceCollectionPointKind(dto.evidence_collection_point)
            if dto.evidence_collection_point is not None
            else None
        ),
        episode_id=(
            LearningEpisodeId(dto.episode_id) if dto.episode_id is not None else None
        ),
    )
