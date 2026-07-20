"""Sequencing policy and stage order tests."""

from __future__ import annotations

import pytest

from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.orchestrator import (
    OrchestrationStageKind,
    SequencingPolicy,
    StageIsExecutableSpecification,
    StageStatus,
)
from tests.domain.education.orchestrator.conftest import (
    make_canonical_stages,
    make_orchestrator,
    make_stage,
    make_started_orchestrator,
)


def test_progress_of_empty_path_rejected_by_plan() -> None:
    stages = make_canonical_stages()
    progress = SequencingPolicy.progress_of(stages)
    assert progress.total_stages == 6
    assert progress.completed_stages == 0
    assert progress.ratio == 0.0


def test_activate_first_pending() -> None:
    stages = make_canonical_stages()
    updated = SequencingPolicy.activate_first_pending(list(stages))
    active = [s for s in updated if s.is_active()]
    assert len(active) == 1
    assert active[0].sequence_index == 0


def test_assert_can_advance_returns_active() -> None:
    stages = list(make_canonical_stages())
    stages = SequencingPolicy.activate_first_pending(stages)
    current = SequencingPolicy.assert_can_advance(stages)
    assert current.is_active()


def test_no_skip_required() -> None:
    stages = [
        make_stage(
            stage_id="first",
            kind=OrchestrationStageKind.EPISODE_CREATION,
            sequence_index=0,
            required=True,
        ),
        make_stage(
            stage_id="second",
            kind=OrchestrationStageKind.EPISODE_DELIVERY,
            sequence_index=1,
            required=True,
        ),
    ]
    # Manually mark second as somehow... we can't activate second while first
    # pending via assert_can_advance — it should return first.
    nxt = SequencingPolicy.assert_can_advance(stages)
    assert nxt.stage_id.value == "first"


def test_exhausted_raises() -> None:
    stages = [
        make_stage(stage_id="only", sequence_index=0).activate().complete()
    ]
    with pytest.raises(EducationalInvariantViolation) as exc:
        SequencingPolicy.assert_can_advance(stages)
    assert exc.value.invariant == "SequencingPolicy.exhausted"


def test_replace_unknown_stage() -> None:
    stages = make_canonical_stages()
    alien = make_stage(stage_id="alien", sequence_index=99)
    with pytest.raises(EducationalInvariantViolation):
        SequencingPolicy.replace_stage(list(stages), alien)


def test_stage_executable_only_when_active_orchestrator() -> None:
    orch = make_orchestrator()
    spec = StageIsExecutableSpecification()
    assert not spec.is_satisfied_by(orch)
    orch.start()
    assert spec.is_satisfied_by(orch)
    assert spec.is_satisfied_by(orch, orch.stages[0])


def test_stage_executable_rejects_non_current() -> None:
    orch = make_started_orchestrator()
    later = orch.stages[2]
    assert not StageIsExecutableSpecification().is_satisfied_by(orch, later)


def test_ordered_by_sequence_index() -> None:
    stages = [
        make_stage(stage_id="b", sequence_index=2),
        make_stage(
            stage_id="a",
            kind=OrchestrationStageKind.EPISODE_CREATION,
            sequence_index=0,
        ),
        make_stage(
            stage_id="m",
            kind=OrchestrationStageKind.REFLECTION,
            sequence_index=1,
        ),
    ]
    ordered = SequencingPolicy.ordered(stages)
    assert [s.stage_id.value for s in ordered] == ["a", "m", "b"]


def test_advance_through_full_sequence() -> None:
    orch = make_started_orchestrator()
    completed_kinds: list[OrchestrationStageKind] = []
    while True:
        try:
            done = orch.advance()
        except EducationalInvariantViolation as exc:
            if exc.invariant == "SequencingPolicy.exhausted":
                break
            raise
        completed_kinds.append(done.kind)
        if done.status is not StageStatus.COMPLETED:
            pytest.fail("advanced stage must be completed")
    assert len(completed_kinds) == 6
    assert orch.progress.all_stages_complete
