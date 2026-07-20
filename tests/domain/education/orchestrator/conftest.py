"""Shared factories for Educational Orchestrator domain tests."""

from __future__ import annotations

import pytest

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
    StrategyReference,
)

DECISION_001 = DecisionId("dec-001")
STRATEGY_001 = TeachingStrategyId("strategy-001")
STRATEGY_002 = TeachingStrategyId("strategy-002")
EPISODE_001 = LearningEpisodeId("episode-001")
DEFAULT_STRATEGY = TeachingStrategyType.DIRECT_EXPLANATION

CANONICAL_STAGE_KINDS = (
    OrchestrationStageKind.EPISODE_CREATION,
    OrchestrationStageKind.EPISODE_DELIVERY,
    OrchestrationStageKind.EVIDENCE_COLLECTION,
    OrchestrationStageKind.REFLECTION,
    OrchestrationStageKind.TWIN_UPDATE,
    OrchestrationStageKind.NEXT_RECOMMENDATION,
)


@pytest.fixture
def orchestrator_id() -> OrchestratorId:
    return OrchestratorId("orch-001")


@pytest.fixture
def student_id() -> str:
    return "student-ada"


def make_decision_ref(
    *,
    decision_id: DecisionId | str = DECISION_001,
    approved: bool = True,
) -> ApprovedDecisionReference:
    if isinstance(decision_id, str):
        decision_id = DecisionId(decision_id)
    return ApprovedDecisionReference(decision_id=decision_id, approved=approved)


def make_strategy_ref(
    *,
    strategy_id: TeachingStrategyId | str = STRATEGY_001,
    strategy_type: TeachingStrategyType = DEFAULT_STRATEGY,
) -> StrategyReference:
    if isinstance(strategy_id, str):
        strategy_id = TeachingStrategyId(strategy_id)
    return StrategyReference(
        strategy_id=strategy_id,
        strategy_type=strategy_type,
    )


def make_episode_ref(
    *,
    episode_id: LearningEpisodeId | str = EPISODE_001,
) -> EpisodeReference:
    if isinstance(episode_id, str):
        episode_id = LearningEpisodeId(episode_id)
    return EpisodeReference(episode_id=episode_id)


def make_stage(
    *,
    stage_id: str = "stage-001",
    kind: OrchestrationStageKind = OrchestrationStageKind.EPISODE_DELIVERY,
    sequence_index: int = 0,
    label: str | None = None,
    required: bool = True,
    evidence_collection_point: EvidenceCollectionPointKind | None = None,
    episode_id: LearningEpisodeId | None = None,
) -> OrchestrationStage:
    if kind is OrchestrationStageKind.EVIDENCE_COLLECTION and (
        evidence_collection_point is None
    ):
        evidence_collection_point = EvidenceCollectionPointKind.AFTER_EPISODE
    return OrchestrationStage(
        stage_id=OrchestrationStageId(stage_id),
        kind=kind,
        sequence_index=sequence_index,
        label=label or f"Stage {kind.value}",
        required=required,
        evidence_collection_point=evidence_collection_point,
        episode_id=episode_id,
    )


def make_canonical_stages() -> list[OrchestrationStage]:
    stages: list[OrchestrationStage] = []
    for index, kind in enumerate(CANONICAL_STAGE_KINDS):
        evidence = None
        if kind is OrchestrationStageKind.EVIDENCE_COLLECTION:
            evidence = EvidenceCollectionPointKind.AFTER_EPISODE
        stages.append(
            make_stage(
                stage_id=f"stage-{index}-{kind.value}",
                kind=kind,
                sequence_index=index,
                evidence_collection_point=evidence,
            )
        )
    return stages


def make_plan(
    *,
    plan_id: str = "plan-001",
    stages: list[OrchestrationStage] | None = None,
    label: str = "canonical orchestration plan",
) -> OrchestrationPlan:
    resolved = stages if stages is not None else make_canonical_stages()
    return OrchestrationPlan(
        plan_id=OrchestrationPlanId(plan_id),
        stages=tuple(resolved),
        label=label,
    )


def make_orchestrator(
    *,
    orchestrator_id: str | OrchestratorId = "orch-001",
    student_id: str = "student-ada",
    decision_reference: ApprovedDecisionReference | None = None,
    strategy_references: list[StrategyReference] | None = None,
    plan: OrchestrationPlan | None = None,
    episode_references: list[EpisodeReference] | None = None,
    strategy_type: TeachingStrategyType = DEFAULT_STRATEGY,
) -> EducationalOrchestrator:
    if isinstance(orchestrator_id, str):
        orchestrator_id = OrchestratorId(orchestrator_id)
    return EducationalOrchestrator.create(
        orchestrator_id=orchestrator_id,
        student_id=student_id,
        decision_reference=decision_reference or make_decision_ref(),
        strategy_references=strategy_references
        if strategy_references is not None
        else [make_strategy_ref(strategy_type=strategy_type)],
        plan=plan or make_plan(),
        episode_references=episode_references,
    )


def make_started_orchestrator(**kwargs) -> EducationalOrchestrator:
    orch = make_orchestrator(**kwargs)
    orch.start()
    return orch


def advance_all_required(orch: EducationalOrchestrator) -> None:
    """Advance until required stages are complete (may leave optional pending)."""
    while not orch.progress.required_sequence_complete:
        orch.advance()
