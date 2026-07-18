"""Migration manager state transition tests."""

from __future__ import annotations

import pytest

from app.application.mission_adapter.exceptions import MigrationStateError
from app.application.mission_adapter.migration_manager import (
    MigrationManager,
    MigrationPhase,
)


def test_initial_legacy():
    mgr = MigrationManager()
    assert mgr.phase == MigrationPhase.LEGACY_ONLY
    assert mgr.history == (MigrationPhase.LEGACY_ONLY,)


def test_invalid_initial_raises():
    with pytest.raises(MigrationStateError):
        MigrationManager(initial_phase="nope")  # type: ignore[arg-type]


@pytest.mark.parametrize(
    ("start", "target"),
    [
        (MigrationPhase.LEGACY_ONLY, MigrationPhase.PARALLEL_VALIDATION),
        (MigrationPhase.PARALLEL_VALIDATION, MigrationPhase.LIMITED_V2),
        (MigrationPhase.PARALLEL_VALIDATION, MigrationPhase.LEGACY_ONLY),
        (MigrationPhase.LIMITED_V2, MigrationPhase.FULL_V2),
        (MigrationPhase.LIMITED_V2, MigrationPhase.PARALLEL_VALIDATION),
        (MigrationPhase.LIMITED_V2, MigrationPhase.LEGACY_ONLY),
        (MigrationPhase.FULL_V2, MigrationPhase.RETIRED_V1),
        (MigrationPhase.FULL_V2, MigrationPhase.LIMITED_V2),
        (MigrationPhase.FULL_V2, MigrationPhase.PARALLEL_VALIDATION),
        (MigrationPhase.FULL_V2, MigrationPhase.LEGACY_ONLY),
        (MigrationPhase.RETIRED_V1, MigrationPhase.FULL_V2),
    ],
)
def test_lawful_transitions(start, target):
    mgr = MigrationManager(initial_phase=start)
    assert mgr.can_transition_to(target) is True
    assert mgr.transition_to(target) == target
    assert mgr.phase == target


@pytest.mark.parametrize(
    ("start", "target"),
    [
        (MigrationPhase.LEGACY_ONLY, MigrationPhase.FULL_V2),
        (MigrationPhase.LEGACY_ONLY, MigrationPhase.RETIRED_V1),
        (MigrationPhase.LEGACY_ONLY, MigrationPhase.LIMITED_V2),
        (MigrationPhase.PARALLEL_VALIDATION, MigrationPhase.FULL_V2),
        (MigrationPhase.PARALLEL_VALIDATION, MigrationPhase.RETIRED_V1),
        (MigrationPhase.LIMITED_V2, MigrationPhase.RETIRED_V1),
        (MigrationPhase.RETIRED_V1, MigrationPhase.LEGACY_ONLY),
        (MigrationPhase.RETIRED_V1, MigrationPhase.LIMITED_V2),
    ],
)
def test_unlawful_transitions(start, target):
    mgr = MigrationManager(initial_phase=start)
    assert mgr.can_transition_to(target) is False
    with pytest.raises(MigrationStateError):
        mgr.transition_to(target)


def test_noop_same_phase():
    mgr = MigrationManager()
    assert mgr.transition_to(MigrationPhase.LEGACY_ONLY) == MigrationPhase.LEGACY_ONLY
    assert len(mgr.history) == 1


def test_history_accumulates():
    mgr = MigrationManager()
    mgr.transition_to(MigrationPhase.PARALLEL_VALIDATION)
    mgr.transition_to(MigrationPhase.LIMITED_V2)
    assert mgr.history == (
        MigrationPhase.LEGACY_ONLY,
        MigrationPhase.PARALLEL_VALIDATION,
        MigrationPhase.LIMITED_V2,
    )


def test_rollback_to_legacy():
    mgr = MigrationManager(initial_phase=MigrationPhase.LIMITED_V2)
    assert mgr.rollback_to_legacy() == MigrationPhase.LEGACY_ONLY


def test_rollback_from_legacy_noop():
    mgr = MigrationManager()
    assert mgr.rollback_to_legacy() == MigrationPhase.LEGACY_ONLY


def test_rollback_from_retired_steps_to_full():
    mgr = MigrationManager(initial_phase=MigrationPhase.RETIRED_V1)
    assert mgr.rollback_to_legacy() == MigrationPhase.FULL_V2


def test_v1_retired_flag():
    mgr = MigrationManager(initial_phase=MigrationPhase.RETIRED_V1)
    assert mgr.v1_retired() is True
    assert mgr.v2_authoritative() is True


def test_v2_authoritative_full():
    mgr = MigrationManager(initial_phase=MigrationPhase.FULL_V2)
    assert mgr.v2_authoritative() is True
    assert mgr.v1_retired() is False


def test_not_authoritative_in_parallel():
    mgr = MigrationManager(initial_phase=MigrationPhase.PARALLEL_VALIDATION)
    assert mgr.v2_authoritative() is False


def test_allowed_transitions_frozen():
    mgr = MigrationManager()
    allowed = mgr.allowed_transitions()
    assert isinstance(allowed, frozenset)
    assert MigrationPhase.PARALLEL_VALIDATION in allowed


def test_invalid_target_type():
    mgr = MigrationManager()
    with pytest.raises(MigrationStateError):
        mgr.transition_to("parallel_validation")  # type: ignore[arg-type]


def test_full_path_to_retired():
    mgr = MigrationManager()
    mgr.transition_to(MigrationPhase.PARALLEL_VALIDATION)
    mgr.transition_to(MigrationPhase.LIMITED_V2)
    mgr.transition_to(MigrationPhase.FULL_V2)
    mgr.transition_to(MigrationPhase.RETIRED_V1)
    assert mgr.phase == MigrationPhase.RETIRED_V1


@pytest.mark.parametrize("phase", list(MigrationPhase))
def test_all_phases_are_strings(phase):
    assert isinstance(phase.value, str)
