"""Value object tests for Educational Digital Twin."""

from __future__ import annotations

import pytest

from domain.education.digital_twin import (
    ConfidenceProfile,
    LearningTrajectory,
    MasteryBand,
    MasteryState,
    RetentionBand,
    RetentionState,
    TrajectoryPoint,
    TrajectoryPointKind,
)
from domain.education.foundation.enums import ConfidenceLevel
from domain.education.foundation.errors import EducationalInvariantViolation


@pytest.mark.parametrize("band", list(MasteryBand))
def test_mastery_state_accepts_all_bands(band: MasteryBand) -> None:
    state = MasteryState.of(band)
    assert state.band is band
    assert str(state) == band.value


@pytest.mark.parametrize("ratio", [0.0, 0.25, 0.5, 0.75, 1.0])
def test_mastery_state_accepts_ratio(ratio: float) -> None:
    state = MasteryState.of(MasteryBand.PROFICIENT, ratio=ratio)
    assert state.ratio == ratio


@pytest.mark.parametrize("ratio", [-0.01, 1.01, True])
def test_mastery_state_rejects_bad_ratio(ratio: object) -> None:
    with pytest.raises(EducationalInvariantViolation):
        MasteryState.of(MasteryBand.DEVELOPING, ratio=ratio)  # type: ignore[arg-type]


def test_mastery_unknown_factory() -> None:
    assert MasteryState.unknown().band is MasteryBand.UNKNOWN


@pytest.mark.parametrize("band", list(RetentionBand))
def test_retention_state_accepts_all_bands(band: RetentionBand) -> None:
    state = RetentionState.of(band, ratio=0.4)
    assert state.band is band
    assert "0.40" in str(state)


@pytest.mark.parametrize("ratio", [-0.1, 1.5])
def test_retention_state_rejects_bad_ratio(ratio: float) -> None:
    with pytest.raises(EducationalInvariantViolation):
        RetentionState.of(RetentionBand.STABLE, ratio=ratio)


def test_retention_unknown_factory() -> None:
    assert RetentionState.unknown().band is RetentionBand.UNKNOWN


@pytest.mark.parametrize("level", list(ConfidenceLevel))
def test_confidence_profile_accepts_all_levels(level: ConfidenceLevel) -> None:
    profile = ConfidenceProfile.of(level)
    assert profile.overall is level


@pytest.mark.parametrize("ratio", [-0.2, 2.0])
def test_confidence_profile_rejects_bad_ratio(ratio: float) -> None:
    with pytest.raises(EducationalInvariantViolation):
        ConfidenceProfile.of(ConfidenceLevel.HIGH, ratio=ratio)


def test_confidence_unknown_factory() -> None:
    assert ConfidenceProfile.unknown().overall is ConfidenceLevel.UNKNOWN


def test_trajectory_empty_and_append() -> None:
    traj = LearningTrajectory.empty()
    assert traj.length() == 0
    assert traj.next_sequence() == 1
    point = TrajectoryPoint(
        sequence=1, kind=TrajectoryPointKind.CREATED, label="created"
    )
    nxt = traj.with_appended(point)
    assert nxt.length() == 1
    assert nxt.last() == point
    assert traj.length() == 0  # immutability


def test_trajectory_rejects_non_increasing_sequence() -> None:
    traj = LearningTrajectory.of(
        TrajectoryPoint(sequence=1, kind=TrajectoryPointKind.CREATED, label="a")
    )
    with pytest.raises(EducationalInvariantViolation):
        traj.with_appended(
            TrajectoryPoint(sequence=1, kind=TrajectoryPointKind.EVIDENCE, label="b")
        )


def test_trajectory_rejects_unordered_construction() -> None:
    with pytest.raises(EducationalInvariantViolation):
        LearningTrajectory.of(
            TrajectoryPoint(sequence=2, kind=TrajectoryPointKind.CREATED, label="a"),
            TrajectoryPoint(sequence=1, kind=TrajectoryPointKind.EVIDENCE, label="b"),
        )


@pytest.mark.parametrize("kind", list(TrajectoryPointKind))
def test_trajectory_point_kinds(kind: TrajectoryPointKind) -> None:
    point = TrajectoryPoint(sequence=1, kind=kind, label=kind.value)
    assert point.kind is kind


def test_trajectory_point_rejects_blank_label() -> None:
    with pytest.raises(EducationalInvariantViolation):
        TrajectoryPoint(sequence=1, kind=TrajectoryPointKind.CREATED, label="  ")
