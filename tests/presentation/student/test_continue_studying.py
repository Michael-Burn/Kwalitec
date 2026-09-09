"""Continue-studying invite, duration honesty, and factual telemetry."""

from __future__ import annotations

from dataclasses import replace

from app.application.session_experience.dto.completion_snapshot import (
    CompletionSnapshot,
)
from app.application.student_experience.dto.home_snapshot import HomeSnapshot
from app.models.alpha_infrastructure import PresentationEvent
from app.presentation.formatting import format_duration_estimate
from app.presentation.student.services.student_home_service import (
    StudentHomeService,
)
from app.presentation.student.view_models import home_vm
from app.services.presentation_telemetry_service import (
    ALLOWED_EVENTS,
    EVENT_CONTINUATION_PROMPT_SHOWN,
    EVENT_CONTINUATION_SELECTED,
    EVENT_DAILY_MISSION_COMPLETED,
    EVENT_SECOND_SESSION_COMPLETED,
    EVENT_SECOND_SESSION_STARTED,
    PresentationTelemetryService,
)
from tests.application.platform_integration.helpers import make_user
from tests.test_dx006b_student_home import _page


def test_duration_estimate_communicates_planning_not_guarantee():
    assert format_duration_estimate(60) == "About 1 hour planned"
    assert format_duration_estimate(30) == "About 30 minutes planned"
    assert "planned" in format_duration_estimate(45)
    assert format_duration_estimate(60) != "About 1 hour"
    assert format_duration_estimate(60) != "1 hour"


def test_continuation_prompt_only_after_day_complete(app, ctx):
    incomplete = home_vm(
        HomeSnapshot(
            student_id="1",
            examination_label="CS1",
            has_recommendation=True,
            recommendation_title="Open",
            can_start_session=True,
        ),
        unified_journey=False,
    )
    with app.test_request_context("/student/"):
        open_page = StudentHomeService().build_home(_page(incomplete))
    assert open_page.state != "day_complete"
    assert open_page.show_continuation_invite is False
    assert open_page.continuation_prompt == ""

    complete = replace(incomplete, day_complete=True, primary_cta_enabled=False)
    with app.test_request_context("/student/"):
        done_page = StudentHomeService().build_home(_page(complete))
    assert done_page.state == "day_complete"
    assert done_page.show_continuation_invite is True
    assert done_page.continuation_prompt == "Want to keep studying?"
    assert done_page.mission is not None
    assert done_page.mission.primary_label == "Choose a topic"
    href = done_page.mission.primary_href or ""
    assert "study" in href
    assert "continue_study=1" in href
    assert "next session" not in done_page.continuation_prompt.lower()
    assert "next session" not in done_page.day_complete_message.lower()


def test_continuation_prompt_live_render(app, ctx):
    """Live rendering check for the day-complete continuation invite."""
    from html import unescape
    from pathlib import Path

    from flask import render_template_string

    home = home_vm(
        HomeSnapshot(
            student_id="1",
            examination_label="CS1",
            has_recommendation=True,
            recommendation_title="Done",
            can_start_session=False,
        ),
        unified_journey=False,
    )
    home = replace(home, day_complete=True)
    fragment = (
        "{% if home.state == 'day_complete' and home.mission %}"
        "{% set m = home.mission %}"
        '<p data-day-complete="true">{{ home.day_complete_message }}</p>'
        "{% if home.show_continuation_invite"
        " and m.primary_kind == 'link' and m.primary_href %}"
        '<p data-continuation-prompt="true">'
        "{{ home.continuation_prompt }}</p>"
        '<a href="{{ m.primary_href }}" '
        'data-home-action="continue-studying">'
        "{{ m.primary_label }}</a>"
        "{% endif %}{% endif %}"
    )
    with app.test_request_context("/student/"):
        page = StudentHomeService().build_home(_page(home))
        html = unescape(render_template_string(fragment, home=page))
    assert "Want to keep studying?" in html
    assert "Choose a topic" in html
    assert 'data-continuation-prompt="true"' in html
    assert "continue_study=1" in html
    assert "Today's recommended session is finished." in html
    assert "here's your next session" not in html.lower()
    assert "here is your next session" not in html.lower()
    home_src = Path(app.root_path, "templates", "student", "home.html").read_text(
        encoding="utf-8"
    )
    assert 'data-continuation-prompt="true"' in home_src
    assert 'data-home-action="continue-studying"' in home_src
    assert "show_continuation_invite" in home_src


def test_continuation_telemetry_events_are_allowlisted():
    required = {
        EVENT_DAILY_MISSION_COMPLETED,
        EVENT_CONTINUATION_PROMPT_SHOWN,
        EVENT_CONTINUATION_SELECTED,
        EVENT_SECOND_SESSION_STARTED,
        EVENT_SECOND_SESSION_COMPLETED,
    }
    assert required <= set(ALLOWED_EVENTS)


def test_continuation_funnel_telemetry_is_factual_only(ctx):
    user = make_user("cont-telemetry@example.com")

    PresentationTelemetryService.record(
        EVENT_DAILY_MISSION_COMPLETED,
        user_id=user.id,
        resource_type="session",
        resource_id="lsr-daily",
        path="/session/lsr-daily/complete",
        context={"session_id": "lsr-daily", "mission_id": "mission_1"},
    )
    PresentationTelemetryService.record(
        EVENT_CONTINUATION_PROMPT_SHOWN,
        user_id=user.id,
        path="/student/",
        context={"surface": "home"},
    )
    PresentationTelemetryService.record(
        EVENT_CONTINUATION_SELECTED,
        user_id=user.id,
        path="/student/study",
        context={"surface": "study"},
    )
    PresentationTelemetryService.record(
        EVENT_SECOND_SESSION_STARTED,
        user_id=user.id,
        resource_type="session",
        resource_id="lsr-second",
        path="/student/study/start",
        context={"session_id": "lsr-second", "topic_id": "topic_a"},
    )
    PresentationTelemetryService.record(
        EVENT_SECOND_SESSION_COMPLETED,
        user_id=user.id,
        resource_type="session",
        resource_id="lsr-second",
        path="/session/lsr-second/complete",
        context={"session_id": "lsr-second"},
    )

    rows = (
        PresentationEvent.query.filter_by(user_id=user.id)
        .order_by(PresentationEvent.id.asc())
        .all()
    )
    types = [r.event_type for r in rows]
    assert types == [
        EVENT_DAILY_MISSION_COMPLETED,
        EVENT_CONTINUATION_PROMPT_SHOWN,
        EVENT_CONTINUATION_SELECTED,
        EVENT_SECOND_SESSION_STARTED,
        EVENT_SECOND_SESSION_COMPLETED,
    ]
    for row in rows:
        assert row.context_json is not None
        assert "wanted" not in row.context_json.lower()
        assert "intent" not in row.context_json.lower()
        assert "inference" not in row.context_json.lower()


def test_completion_snapshot_metadata_drives_daily_event_gate():
    snap = CompletionSnapshot(
        session_id="s1",
        student_id="1",
        metadata=(("mission_completed", "true"),),
    )
    meta = dict(snap.metadata)
    assert meta.get("mission_completed") == "true"
    snap_no = CompletionSnapshot(
        session_id="s2",
        student_id="1",
        metadata=(("mission_completed", "false"),),
    )
    assert dict(snap_no.metadata).get("mission_completed") == "false"
