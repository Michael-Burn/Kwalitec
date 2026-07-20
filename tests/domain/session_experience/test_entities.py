"""Entity tests for Learning Session Experience domain."""

from __future__ import annotations

import pytest

from app.domain.session_experience.learning_session import LearningSessionStatus
from app.domain.session_experience.session_navigation import (
    assert_linear_advance,
    can_advance,
    next_surface,
    previous_surface,
)
from app.domain.session_experience.session_workspace import SessionSurface
from tests.domain.session_experience.helpers import (
    make_activity,
    make_begin_action,
    make_completion,
    make_progress,
    make_reflection,
    make_session,
    make_workspace,
)


def test_workspace_create_and_navigate():
    ws = make_workspace()
    assert ws.is_on(SessionSurface.OVERVIEW)
    moved = ws.navigate_to(SessionSurface.ACTIVITY)
    assert moved.is_on("activity")
    assert moved.session_id == "sess-1"


def test_workspace_rejects_empty_ids():
    with pytest.raises(ValueError):
        make_workspace(workspace_id="")
    with pytest.raises(ValueError):
        make_workspace(student_id=" ")
    with pytest.raises(ValueError):
        make_workspace(session_id="")


def test_learning_session_begin_action():
    session = make_session(objective="Master equity method", activity_count=3)
    assert session.can_begin
    assert session.begin_action is not None
    assert session.begin_action.label == "Begin Session"


def test_begin_action_requires_session_id():
    action = make_begin_action(enabled=True, session_id=None)
    assert not action.can_begin


def test_session_status_transition_copy():
    session = make_session()
    updated = session.with_status(LearningSessionStatus.IN_PROGRESS)
    assert updated.status is LearningSessionStatus.IN_PROGRESS
    assert session.status is LearningSessionStatus.READY


def test_progress_percent_and_complete():
    progress = make_progress(
        activities_completed=2, activities_remaining=2, activities_total=4
    )
    assert progress.progress_percent == 50
    assert not progress.is_complete
    done = make_progress(
        activities_completed=4, activities_remaining=0, activities_total=4
    )
    assert done.is_complete


def test_progress_rejects_invalid_ratio():
    with pytest.raises(ValueError):
        make_progress(overall_progress=1.5)


def test_activity_projection_hints_and_final():
    activity = make_activity(
        question="What is the equity method?",
        hints=["Think ownership influence"],
        activity_index=3,
        activities_total=3,
    )
    assert activity.has_hints
    assert activity.is_final_activity


def test_activity_index_bounds():
    with pytest.raises(ValueError):
        make_activity(activity_index=0)
    with pytest.raises(ValueError):
        make_activity(activity_index=5, activities_total=3)


def test_reflection_rejects_scoring_language():
    with pytest.raises(ValueError):
        make_reflection(key_insight="You scored 90 points")


def test_reflection_defaults_prompt():
    reflection = make_reflection(key_insight="Ownership influence matters")
    assert reflection.reflection_prompt
    assert len(reflection.reflection_prompt) > 10


def test_completion_readiness_label():
    completion = make_completion(exam_readiness_change=0.04)
    assert "improved" in completion.exam_readiness_change_label.lower()
    assert completion.can_return_home


def test_linear_navigation_helpers():
    assert next_surface(SessionSurface.OVERVIEW) is SessionSurface.ACTIVITY
    assert previous_surface(SessionSurface.ACTIVITY) is SessionSurface.OVERVIEW
    assert can_advance(SessionSurface.SUMMARY)
    assert not can_advance(SessionSurface.COMPLETE)
    assert assert_linear_advance("overview", "activity") is SessionSurface.ACTIVITY


def test_linear_navigation_rejects_skip():
    with pytest.raises(ValueError):
        assert_linear_advance(SessionSurface.OVERVIEW, SessionSurface.REFLECTION)


def test_session_topics_cleaned():
    session = make_session(topics=[" Equity ", "", "Leases"])
    assert session.topics == ("Equity", "Leases")
    assert session.topic_count == 2
