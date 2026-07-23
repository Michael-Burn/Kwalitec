"""Adapter navigation / CTA regression for PX-002 continuous journey."""

from __future__ import annotations

from adapters.flask.navigation import (
    path_for_action,
    primary_cta_href,
    student_flow_nav,
)


def test_continuous_journey_action_paths() -> None:
    assert path_for_action("continue_mission") == "/eos/mission/"
    assert path_for_action("resume_session") == "/eos/session/"
    assert path_for_action("review_reflection") == "/eos/reflection/"
    assert path_for_action("open_reflection") == "/eos/reflection/"
    assert path_for_action("prepare_checkpoint") == "/eos/mission/"
    assert path_for_action("return_home") == "/eos/dashboard/"
    assert path_for_action("view_progress") == "/eos/journey/"


def test_student_flow_nav_preserves_context_ids() -> None:
    nav = student_flow_nav(student_id="ada", session_id="sess-1")
    assert "student_id=ada" in nav["dashboard"]
    assert "session_id=sess-1" in nav["session"]
    assert "session_id=sess-1" in nav["resume_session"]
    assert "session_id=sess-1" in nav["review_reflection"]
    assert nav["prepare_checkpoint"].startswith("/eos/mission/")


def test_primary_cta_href_is_state_aware() -> None:
    href = primary_cta_href(
        "continue_mission", student_id="ada", session_id="sess-1"
    )
    assert href.startswith("/eos/mission/")
    assert "student_id=ada" in href

    reflection = primary_cta_href(
        "review_reflection", student_id="ada", session_id="sess-1"
    )
    assert reflection.startswith("/eos/reflection/")
    assert "session_id=sess-1" in reflection
