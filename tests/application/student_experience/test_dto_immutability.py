"""DTO immutability and mapping tests."""

from __future__ import annotations

import dataclasses

import pytest

from app.application.student_experience.dto import (
    ExplanationSnapshot,
    HistorySnapshot,
    HomeSnapshot,
    JourneySnapshot,
    ProfileSnapshot,
    RevisionSnapshot,
)
from tests.application.student_experience.helpers import make_experience

SNAPSHOT_TYPES = (
    HomeSnapshot,
    JourneySnapshot,
    RevisionSnapshot,
    HistorySnapshot,
    ProfileSnapshot,
    ExplanationSnapshot,
)


@pytest.mark.parametrize("cls", SNAPSHOT_TYPES)
def test_dto_is_frozen(cls):
    assert dataclasses.is_dataclass(cls)
    assert cls.__dataclass_params__.frozen is True


def test_home_snapshot_immutable():
    snap = make_experience().get_home("stu-1")
    with pytest.raises(dataclasses.FrozenInstanceError):
        snap.greeting = "x"  # type: ignore[misc]


def test_journey_snapshot_immutable():
    snap = make_experience().get_journey("stu-1")
    with pytest.raises(dataclasses.FrozenInstanceError):
        snap.progress_percent = 0  # type: ignore[misc]


def test_revision_snapshot_immutable():
    snap = make_experience().get_revision("stu-1")
    with pytest.raises(dataclasses.FrozenInstanceError):
        snap.has_revision = False  # type: ignore[misc]


def test_history_snapshot_immutable():
    snap = make_experience().get_history("stu-1")
    with pytest.raises(dataclasses.FrozenInstanceError):
        snap.session_count = 0  # type: ignore[misc]


def test_profile_snapshot_immutable():
    snap = make_experience().get_profile("stu-1")
    with pytest.raises(dataclasses.FrozenInstanceError):
        snap.display_name = "x"  # type: ignore[misc]


def test_explanation_snapshot_immutable():
    snap = make_experience().explain("stu-1")
    with pytest.raises(dataclasses.FrozenInstanceError):
        snap.summary = "x"  # type: ignore[misc]
