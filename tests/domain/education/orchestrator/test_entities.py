"""Entity construction and behaviour tests."""

from __future__ import annotations

import pytest

from domain.education.foundation.enums import TeachingStrategyType
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import (
    DecisionId,
    LearningEpisodeId,
    TeachingStrategyId,
)
from domain.education.orchestrator import (
    ApprovedDecisionReference,
    EpisodeReference,
    EvidenceCollectionPointKind,
    OrchestrationPlan,
    OrchestrationPlanId,
    OrchestrationStage,
    OrchestrationStageId,
    OrchestrationStageKind,
    StageStatus,
    StrategyReference,
)
from tests.domain.education.orchestrator.conftest import make_stage


def test_approved_decision_reference_str() -> None:
    ref = ApprovedDecisionReference(decision_id=DecisionId("dec-9"))
    assert str(ref) == "dec-9"


def test_strategy_reference_str() -> None:
    ref = StrategyReference(
        strategy_id=TeachingStrategyId("s1"),
        strategy_type=TeachingStrategyType.ANALOGY,
    )
    assert "analogy" in str(ref)


def test_episode_reference() -> None:
    ref = EpisodeReference(episode_id=LearningEpisodeId("ep-1"))
    assert str(ref) == "ep-1"


def test_stage_activate_and_complete() -> None:
    stage = make_stage()
    active = stage.activate()
    assert active.status is StageStatus.ACTIVE
    done = active.complete()
    assert done.status is StageStatus.COMPLETED


def test_cannot_complete_pending_stage() -> None:
    stage = make_stage()
    with pytest.raises(EducationalInvariantViolation):
        stage.complete()


def test_cannot_activate_completed_stage() -> None:
    stage = make_stage().activate().complete()
    with pytest.raises(EducationalInvariantViolation):
        stage.activate()


def test_evidence_collection_requires_point() -> None:
    with pytest.raises(EducationalInvariantViolation):
        OrchestrationStage(
            stage_id=OrchestrationStageId("ev"),
            kind=OrchestrationStageKind.EVIDENCE_COLLECTION,
            sequence_index=0,
            label="collect",
            evidence_collection_point=None,
        )


def test_bind_episode() -> None:
    stage = make_stage(kind=OrchestrationStageKind.EPISODE_CREATION)
    bound = stage.bind_episode(LearningEpisodeId("ep-bound"))
    assert bound.episode_id == LearningEpisodeId("ep-bound")


def test_cannot_bind_episode_when_completed() -> None:
    stage = make_stage().activate().complete()
    with pytest.raises(EducationalInvariantViolation):
        stage.bind_episode(LearningEpisodeId("ep-x"))


def test_plan_stage_by_id() -> None:
    stages = (
        make_stage(stage_id="one", sequence_index=0),
        make_stage(
            stage_id="two",
            kind=OrchestrationStageKind.REFLECTION,
            sequence_index=1,
        ),
    )
    plan = OrchestrationPlan(
        plan_id=OrchestrationPlanId("p1"),
        stages=stages,
    )
    assert plan.stage_by_id(OrchestrationStageId("two")).label
    with pytest.raises(EducationalInvariantViolation):
        plan.stage_by_id(OrchestrationStageId("missing"))


def test_plan_with_stages_preserves_identity() -> None:
    plan = OrchestrationPlan(
        plan_id=OrchestrationPlanId("p2"),
        stages=(make_stage(),),
    )
    updated = plan.with_stages([make_stage().activate()])
    assert updated.plan_id == plan.plan_id
    assert updated.stages[0].is_active()


def test_stage_identity_equality() -> None:
    a = make_stage(stage_id="same", label="A")
    b = make_stage(stage_id="same", label="B")
    assert a == b


def test_is_evidence_collection_point_flag() -> None:
    stage = make_stage(
        kind=OrchestrationStageKind.EVIDENCE_COLLECTION,
        evidence_collection_point=EvidenceCollectionPointKind.AT_STAGE,
    )
    assert stage.is_evidence_collection_point()
