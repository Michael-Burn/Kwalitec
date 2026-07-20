"""Lifecycle behaviour for EducationalOrchestrator."""

from __future__ import annotations

import pytest

from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import LearningEpisodeId
from domain.education.orchestrator import (
    OrchestrationCompleted,
    OrchestrationIsValidSpecification,
    OrchestrationPaused,
    OrchestrationStageKind,
    OrchestrationStarted,
    StageIsExecutableSpecification,
)
from tests.domain.education.orchestrator.conftest import (
    advance_all_required,
    make_orchestrator,
    make_started_orchestrator,
)


def test_create_is_planned_and_valid() -> None:
    orch = make_orchestrator()
    assert orch.is_planned()
    assert OrchestrationIsValidSpecification().is_satisfied_by(orch)
    assert orch.stage_count() == 6
    assert orch.strategy_count() == 1


def test_start_activates_first_stage_and_emits_event() -> None:
    orch = make_orchestrator()
    orch.start()
    assert orch.is_active()
    events = orch.pull_events()
    assert len(events) == 1
    assert isinstance(events[0], OrchestrationStarted)
    assert events[0].first_stage_id == orch.state.current_stage_id
    assert StageIsExecutableSpecification().is_satisfied_by(orch)


def test_cannot_start_twice() -> None:
    orch = make_started_orchestrator()
    with pytest.raises(EducationalInvariantViolation) as exc:
        orch.start()
    assert exc.value.invariant == "EducationalOrchestrator.start.status"


def test_advance_completes_active_and_activates_next() -> None:
    orch = make_started_orchestrator()
    first_id = orch.state.current_stage_id
    completed = orch.advance()
    assert completed.stage_id == first_id
    assert completed.is_completed()
    assert orch.state.current_stage_id != first_id
    assert orch.progress.completed_stages == 1


def test_pause_and_resume() -> None:
    orch = make_started_orchestrator()
    orch.pause("session capacity reached")
    assert orch.is_paused()
    events = orch.pull_events()
    assert any(isinstance(e, OrchestrationPaused) for e in events)
    orch.resume()
    assert orch.is_active()


def test_cannot_resume_completed() -> None:
    orch = make_started_orchestrator()
    advance_all_required(orch)
    orch.complete()
    with pytest.raises(EducationalInvariantViolation) as exc:
        orch.resume()
    assert exc.value.invariant == "EducationalOrchestrator.resume.completed"


def test_complete_emits_event_and_terminates() -> None:
    orch = make_started_orchestrator()
    advance_all_required(orch)
    orch.complete()
    assert orch.is_completed()
    assert orch.is_terminal()
    events = orch.pull_events()
    assert any(isinstance(e, OrchestrationCompleted) for e in events)


def test_cannot_complete_with_incomplete_required_stages() -> None:
    orch = make_started_orchestrator()
    with pytest.raises(EducationalInvariantViolation) as exc:
        orch.complete()
    assert exc.value.invariant == (
        "EducationalOrchestrator.complete.required_stages"
    )


def test_cannot_pause_when_planned() -> None:
    orch = make_orchestrator()
    with pytest.raises(EducationalInvariantViolation):
        orch.pause("too early")


def test_cannot_advance_when_paused() -> None:
    orch = make_started_orchestrator()
    orch.pause("break")
    with pytest.raises(EducationalInvariantViolation):
        orch.advance()


def test_register_episode_on_creation_stage() -> None:
    orch = make_started_orchestrator()
    assert orch.stages[0].kind is OrchestrationStageKind.EPISODE_CREATION
    orch.register_episode(LearningEpisodeId("ep-new-001"))
    assert orch.has_episode(LearningEpisodeId("ep-new-001"))
    assert orch.episode_count() == 1
    bound = orch.stage_by_id(orch.state.current_stage_id)  # type: ignore[arg-type]
    assert bound.episode_id == LearningEpisodeId("ep-new-001")


def test_register_episode_rejects_wrong_stage() -> None:
    orch = make_started_orchestrator()
    orch.advance()  # leave episode creation
    with pytest.raises(EducationalInvariantViolation) as exc:
        orch.register_episode(LearningEpisodeId("ep-late"))
    assert (
        exc.value.invariant
        == "EducationalOrchestrator.register_episode.stage_kind"
    )


def test_full_happy_path_lifecycle() -> None:
    orch = make_orchestrator(orchestrator_id="orch-happy")
    orch.start()
    orch.register_episode(LearningEpisodeId("ep-happy"))
    while not orch.progress.all_stages_complete:
        orch.advance()
    orch.complete()
    assert orch.is_completed()
    assert orch.progress.ratio == 1.0
    assert orch.progress.evidence_points_complete


def test_equality_by_identity() -> None:
    left = make_orchestrator(orchestrator_id="same")
    right = make_orchestrator(orchestrator_id="same")
    other = make_orchestrator(orchestrator_id="other")
    assert left == right
    assert left != other
    assert hash(left) == hash(right)


def test_pull_events_clears_pending() -> None:
    orch = make_orchestrator()
    orch.start()
    first = orch.pull_events()
    second = orch.pull_events()
    assert len(first) == 1
    assert second == []
