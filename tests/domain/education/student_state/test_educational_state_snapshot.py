"""Direct construction/validation tests for EducationalStateSnapshot.

These complement the aggregate-driven snapshot tests by exercising the
snapshot value object's own invariants directly.
"""

from __future__ import annotations

import pytest

from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import LearningEpisodeId
from domain.education.student_state import (
    EducationalStateSnapshot,
    StudentEducationalStateId,
)
from tests.domain.education.student_state.conftest import (
    make_checkpoint_reference,
    make_competency_state,
    make_confidence_summary,
    make_educational_health,
    make_mastery_summary,
    make_mission_reference,
    make_subject_state,
    make_timeline_reference,
)


def _valid_kwargs(**overrides: object) -> dict[str, object]:
    base: dict[str, object] = dict(
        state_id=StudentEducationalStateId("s1"),
        student_id="student-1",
        subject_states=(),
        competency_states=(),
        mastery_summary=make_mastery_summary(),
        confidence_summary=make_confidence_summary(),
        educational_health=make_educational_health(),
        active_learning_episode_id=None,
        current_mission=None,
        current_checkpoint=None,
        educational_timeline=None,
        last_updated_at=None,
    )
    base.update(overrides)
    return base


def test_valid_construction() -> None:
    snapshot = EducationalStateSnapshot(**_valid_kwargs())
    assert snapshot.subject_count() == 0
    assert not snapshot.has_active_learning_episode()
    assert not snapshot.has_current_mission()
    assert not snapshot.has_current_checkpoint()
    assert not snapshot.has_educational_timeline()


def test_rejects_wrong_state_id_type() -> None:
    with pytest.raises(EducationalInvariantViolation):
        EducationalStateSnapshot(**_valid_kwargs(state_id="s1"))


def test_rejects_blank_student_id() -> None:
    with pytest.raises(EducationalInvariantViolation):
        EducationalStateSnapshot(**_valid_kwargs(student_id="   "))


def test_normalizes_list_inputs_to_tuples() -> None:
    snapshot = EducationalStateSnapshot(
        **_valid_kwargs(
            subject_states=[make_subject_state(subject_id="math")],
            competency_states=[make_competency_state(competency_id="algebra")],
        )
    )
    assert isinstance(snapshot.subject_states, tuple)
    assert isinstance(snapshot.competency_states, tuple)


def test_rejects_wrong_subject_state_element_type() -> None:
    with pytest.raises(EducationalInvariantViolation):
        EducationalStateSnapshot(**_valid_kwargs(subject_states=["not-a-state"]))


def test_rejects_duplicate_subject_ids() -> None:
    with pytest.raises(EducationalInvariantViolation):
        EducationalStateSnapshot(
            **_valid_kwargs(
                subject_states=[
                    make_subject_state(subject_id="math"),
                    make_subject_state(subject_id="math"),
                ]
            )
        )


def test_rejects_wrong_competency_state_element_type() -> None:
    with pytest.raises(EducationalInvariantViolation):
        EducationalStateSnapshot(**_valid_kwargs(competency_states=[object()]))


def test_rejects_duplicate_competency_ids() -> None:
    with pytest.raises(EducationalInvariantViolation):
        EducationalStateSnapshot(
            **_valid_kwargs(
                competency_states=[
                    make_competency_state(competency_id="algebra"),
                    make_competency_state(competency_id="algebra"),
                ]
            )
        )


def test_rejects_wrong_mastery_summary_type() -> None:
    with pytest.raises(EducationalInvariantViolation):
        EducationalStateSnapshot(**_valid_kwargs(mastery_summary="bad"))


def test_rejects_wrong_confidence_summary_type() -> None:
    with pytest.raises(EducationalInvariantViolation):
        EducationalStateSnapshot(**_valid_kwargs(confidence_summary="bad"))


def test_rejects_wrong_educational_health_type() -> None:
    with pytest.raises(EducationalInvariantViolation):
        EducationalStateSnapshot(**_valid_kwargs(educational_health="bad"))


def test_rejects_wrong_active_learning_episode_type() -> None:
    with pytest.raises(EducationalInvariantViolation):
        EducationalStateSnapshot(
            **_valid_kwargs(active_learning_episode_id="episode-1")
        )


def test_accepts_valid_active_learning_episode() -> None:
    snapshot = EducationalStateSnapshot(
        **_valid_kwargs(active_learning_episode_id=LearningEpisodeId("episode-1"))
    )
    assert snapshot.has_active_learning_episode()


def test_rejects_wrong_current_mission_type() -> None:
    with pytest.raises(EducationalInvariantViolation):
        EducationalStateSnapshot(**_valid_kwargs(current_mission="mission-1"))


def test_accepts_valid_current_mission() -> None:
    snapshot = EducationalStateSnapshot(
        **_valid_kwargs(current_mission=make_mission_reference())
    )
    assert snapshot.has_current_mission()


def test_rejects_wrong_current_checkpoint_type() -> None:
    with pytest.raises(EducationalInvariantViolation):
        EducationalStateSnapshot(**_valid_kwargs(current_checkpoint="checkpoint-1"))


def test_accepts_valid_current_checkpoint() -> None:
    snapshot = EducationalStateSnapshot(
        **_valid_kwargs(current_checkpoint=make_checkpoint_reference())
    )
    assert snapshot.has_current_checkpoint()


def test_rejects_wrong_educational_timeline_type() -> None:
    with pytest.raises(EducationalInvariantViolation):
        EducationalStateSnapshot(**_valid_kwargs(educational_timeline="timeline-1"))


def test_accepts_valid_educational_timeline() -> None:
    snapshot = EducationalStateSnapshot(
        **_valid_kwargs(educational_timeline=make_timeline_reference())
    )
    assert snapshot.has_educational_timeline()


def test_rejects_wrong_last_updated_at_type() -> None:
    with pytest.raises(EducationalInvariantViolation):
        EducationalStateSnapshot(**_valid_kwargs(last_updated_at="2026-01-01"))
