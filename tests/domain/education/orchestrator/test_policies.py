"""Policy unit tests for orchestration and sequencing."""

from __future__ import annotations

import pytest

from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import OrchestratorId
from domain.education.orchestrator import (
    OrchestrationPolicy,
    OrchestrationStageKind,
    OrchestrationStatus,
)
from tests.domain.education.orchestrator.conftest import (
    make_decision_ref,
    make_stage,
    make_strategy_ref,
)


def test_assert_identity() -> None:
    oid = OrchestratorId("orch-x")
    assert OrchestrationPolicy.assert_identity(oid) is oid


def test_assert_student_id_rejects_blank() -> None:
    with pytest.raises(EducationalInvariantViolation):
        OrchestrationPolicy.assert_student_id("  ")


def test_assert_decision_reference() -> None:
    ref = make_decision_ref()
    assert OrchestrationPolicy.assert_decision_reference(ref) is ref


def test_assert_strategy_unique() -> None:
    ref = make_strategy_ref()
    with pytest.raises(EducationalInvariantViolation):
        OrchestrationPolicy.assert_strategy_references([ref, ref])


def test_lifecycle_guards() -> None:
    OrchestrationPolicy.assert_can_start(OrchestrationStatus.PLANNED)
    with pytest.raises(EducationalInvariantViolation):
        OrchestrationPolicy.assert_can_start(OrchestrationStatus.ACTIVE)

    OrchestrationPolicy.assert_can_advance(OrchestrationStatus.ACTIVE)
    with pytest.raises(EducationalInvariantViolation):
        OrchestrationPolicy.assert_can_advance(OrchestrationStatus.PAUSED)

    OrchestrationPolicy.assert_can_pause(OrchestrationStatus.ACTIVE)
    OrchestrationPolicy.assert_can_resume(OrchestrationStatus.PAUSED)
    with pytest.raises(EducationalInvariantViolation):
        OrchestrationPolicy.assert_can_resume(OrchestrationStatus.COMPLETED)


def test_assert_episode_creation_stage() -> None:
    stage = make_stage(kind=OrchestrationStageKind.EPISODE_CREATION)
    OrchestrationPolicy.assert_episode_creation_stage(stage)
    with pytest.raises(EducationalInvariantViolation):
        OrchestrationPolicy.assert_episode_creation_stage(
            make_stage(kind=OrchestrationStageKind.REFLECTION)
        )


def test_assert_can_complete() -> None:
    OrchestrationPolicy.assert_can_complete(
        OrchestrationStatus.ACTIVE,
        required_stages_complete=True,
    )
    with pytest.raises(EducationalInvariantViolation):
        OrchestrationPolicy.assert_can_complete(
            OrchestrationStatus.ACTIVE,
            required_stages_complete=False,
        )
