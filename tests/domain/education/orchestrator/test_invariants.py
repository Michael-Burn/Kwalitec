"""Invariant enforcement for Educational Orchestrator."""

from __future__ import annotations

import pytest

from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import DecisionId, OrchestratorId
from domain.education.orchestrator import (
    ApprovedDecisionReference,
    EducationalOrchestrator,
    OrchestrationPlan,
    OrchestrationPlanId,
    OrchestrationStageKind,
)
from tests.domain.education.orchestrator.conftest import (
    advance_all_required,
    make_decision_ref,
    make_orchestrator,
    make_plan,
    make_stage,
    make_started_orchestrator,
    make_strategy_ref,
)


def test_must_reference_approved_decision() -> None:
    with pytest.raises(EducationalInvariantViolation) as exc:
        ApprovedDecisionReference(
            decision_id=DecisionId("dec-x"),
            approved=False,
        )
    assert exc.value.invariant == "ApprovedDecisionReference.approved.required"


def test_create_rejects_empty_stages() -> None:
    with pytest.raises(EducationalInvariantViolation) as exc:
        OrchestrationPlan(
            plan_id=OrchestrationPlanId("empty"),
            stages=(),
        )
    assert exc.value.invariant == "OrchestrationPlan.stages.min"


def test_create_requires_strategy_reference() -> None:
    with pytest.raises(EducationalInvariantViolation) as exc:
        EducationalOrchestrator.create(
            orchestrator_id=OrchestratorId("orch-no-strat"),
            student_id="student-ada",
            decision_reference=make_decision_ref(),
            strategy_references=[],
            plan=make_plan(),
        )
    assert exc.value.invariant == "EducationalOrchestrator.strategy.min"


def test_duplicate_stage_indexes_rejected() -> None:
    stages = [
        make_stage(stage_id="a", sequence_index=0),
        make_stage(
            stage_id="b",
            kind=OrchestrationStageKind.REFLECTION,
            sequence_index=0,
        ),
    ]
    with pytest.raises(EducationalInvariantViolation) as exc:
        make_plan(stages=stages)
    assert exc.value.invariant == "OrchestrationPlan.stages.unique_index"


def test_cannot_skip_required_stage_order() -> None:
    # Skip is not exposed via public API; advancing only completes the
    # current stage so prior required stages remain intact.
    orch = make_started_orchestrator()
    orch.advance()
    assert orch.progress.completed_required_stages == 1
    assert orch.progress.completed_stages == 1


def test_cannot_complete_twice() -> None:
    orch = make_started_orchestrator()
    advance_all_required(orch)
    orch.complete()
    with pytest.raises(EducationalInvariantViolation) as exc:
        orch.complete()
    assert exc.value.invariant == "EducationalOrchestrator.complete.already"


def test_pause_requires_reason() -> None:
    orch = make_started_orchestrator()
    with pytest.raises(EducationalInvariantViolation):
        orch.pause("   ")


def test_decision_reference_required_type() -> None:
    with pytest.raises(EducationalInvariantViolation):
        EducationalOrchestrator.create(
            orchestrator_id=OrchestratorId("orch-bad-dec"),
            student_id="student-ada",
            decision_reference="not-a-ref",  # type: ignore[arg-type]
            strategy_references=[make_strategy_ref()],
            plan=make_plan(),
        )


def test_terminate_correctly_requires_required_stages() -> None:
    orch = make_orchestrator()
    orch.start()
    # Advance only half the required stages.
    for _ in range(2):
        orch.advance()
    assert not orch.progress.required_sequence_complete
    with pytest.raises(EducationalInvariantViolation):
        orch.complete()


def test_identity_equality_distinct_from_student() -> None:
    a = make_orchestrator(orchestrator_id="orch-a", student_id="s1")
    b = make_orchestrator(orchestrator_id="orch-a", student_id="s2")
    assert a == b  # identity-based
