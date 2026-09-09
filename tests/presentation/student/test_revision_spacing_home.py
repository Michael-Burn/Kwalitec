"""Revision rebuilt as Spacing Scheduler home (roadmap item 3)."""

from __future__ import annotations

from datetime import date, timedelta
from pathlib import Path
from types import SimpleNamespace

import pytest
from flask import render_template

from app.application.spacing_scheduler import (
    InMemorySpacingStateStore,
    SchedulingStatus,
    SpacingSchedulerService,
    get_spacing_scheduler,
    reset_canonical_spacing_scheduler_for_tests,
)
from app.application.student_experience.revision_service import RevisionService
from app.presentation.student.view_models import revision_vm

PACKAGE_A = "CS1-EP001-PKG-1.1-PURPOSE-FUNCTION"
PACKAGE_B = "CS1-EP001-PKG-1.2-EDA-SUMMARIES"
LEARNER = "learner-revision-1"


@pytest.fixture
def spacing_service() -> SpacingSchedulerService:
    return SpacingSchedulerService(store=InMemorySpacingStateStore())


def test_revision_sections_come_only_from_spacing_scheduler(
    spacing_service: SpacingSchedulerService,
) -> None:
    """Requirement 1: Due now / Upcoming / Recently reviewed from canonical state."""
    day0 = date(2026, 9, 1)
    spacing_service.record_completed_exposure(
        learner_id=LEARNER, package_id=PACKAGE_A, completed_on=day0
    )
    spacing_service.record_completed_exposure(
        learner_id=LEARNER,
        package_id=PACKAGE_B,
        completed_on=day0 - timedelta(days=10),
    )
    # Advance B so it is overdue relative to as_of.
    state_b = spacing_service.get_state(learner_id=LEARNER, package_id=PACKAGE_B)
    assert state_b is not None
    as_of = state_b.next_due_on + timedelta(days=2)

    board = spacing_service.revision_board(learner_id=LEARNER, as_of=as_of)
    assert {e.package_id for e in board.due_now} == {PACKAGE_B}
    assert {e.package_id for e in board.upcoming} == {PACKAGE_A}
    assert {e.package_id for e in board.recently_reviewed} == {
        PACKAGE_A,
        PACKAGE_B,
    }
    assert board.due_now[0].decision.status is SchedulingStatus.OVERDUE
    assert board.upcoming[0].decision.status is SchedulingStatus.NOT_DUE

    svc = RevisionService(
        spacing_scheduler=spacing_service,
        as_of_factory=lambda: as_of,
    )
    snap = svc.revision(LEARNER)
    assert [i.package_id for i in snap.due_now] == [PACKAGE_B]
    assert [i.package_id for i in snap.upcoming] == [PACKAGE_A]
    assert snap.has_revision is True
    assert snap.due_now[0].explanation
    expl = snap.due_now[0].explanation
    assert "due" in expl or "overdue" in expl

    # No independent due calculation in RevisionService source.
    source = Path(
        "app/application/student_experience/revision_service.py"
    ).read_text(encoding="utf-8")
    assert "next_review_date" not in source
    assert "RevisionPlanner" not in source
    assert "PriorityCalculator" not in source
    assert "ROIEstimator" not in source
    assert "get_spacing_scheduler" in source or "spacing_scheduler" in source
    assert "revision_board" in source


def test_revision_honest_empty_state_when_nothing_due(
    spacing_service: SpacingSchedulerService, app
) -> None:
    """Requirement 2: empty Due now is plain language, no fabricated content."""
    svc = RevisionService(
        spacing_scheduler=spacing_service,
        as_of_factory=lambda: date(2026, 9, 9),
    )
    snap = svc.revision(LEARNER)
    assert snap.due_now == ()
    assert snap.upcoming == ()
    assert snap.recently_reviewed == ()
    assert snap.has_revision is False
    assert "Nothing is due for review yet" in snap.empty_message

    page = SimpleNamespace(
        shell=SimpleNamespace(page_title="Revision", navigation=()),
        revision=revision_vm(snap),
    )
    with app.test_request_context("/student/revision"):
        html = render_template("student/revision.html", page=page, form=None)
    assert "Due now" in html
    assert "Nothing is due for review yet" in html
    assert "highest-value" not in html.lower()
    assert "Also deserves attention" not in html
    assert "ds_empty_operational" not in html  # no fake-feeling empty graphic macro
    assert "Nothing to revise yet" not in html


def test_begin_revision_starts_session_for_due_package(
    student_client, experience_app, monkeypatch, user
) -> None:
    """Requirement 3: Begin for a due package starts a real package session."""
    reset_canonical_spacing_scheduler_for_tests()
    try:
        learner_id = str(user.id)
        scheduler = get_spacing_scheduler()
        completed = date.today() - timedelta(days=1)
        scheduler.record_completed_exposure(
            learner_id=learner_id,
            package_id=PACKAGE_A,
            completed_on=completed,
        )
        decision = scheduler.evaluate(
            learner_id=learner_id,
            package_id=PACKAGE_A,
            as_of=date.today(),
        )
        assert decision.status in {
            SchedulingStatus.DUE,
            SchedulingStatus.OVERDUE,
        }

        started = {}

        def _fake_start(**kwargs):
            started.update(kwargs)
            return SimpleNamespace(
                session_id="sess-rev-pkg-1",
                topic_title="Purpose and function",
                student_id=learner_id,
            )

        monkeypatch.setattr(
            "app.presentation.student.routes.start_student_selected_topic",
            _fake_start,
        )
        monkeypatch.setattr(
            "app.presentation.student.routes.get_experience_composition",
            lambda: None,
        )

        resp = student_client.post(
            "/student/revision/begin",
            data={"package_id": PACKAGE_A, "submit": "Begin"},
            follow_redirects=False,
        )
        assert resp.status_code in {302, 303}
        assert started.get("educational_package_id") == PACKAGE_A
        assert "/session/" in resp.headers.get("Location", "")
    finally:
        reset_canonical_spacing_scheduler_for_tests()


def test_no_ranking_or_highest_value_language_in_revision_surface() -> None:
    """Requirement 4: no priority/ranking/highest-value language remains."""
    student_facing = (
        Path("app/templates/student/revision.html"),
        Path("app/presentation/student/forms.py"),
    )
    for path in student_facing:
        text = path.read_text(encoding="utf-8").lower()
        for phrase in (
            "highest-value",
            "highest value",
            "why_recommended",
            "also deserves attention",
            "today's best revision",
            "ranking_key",
        ):
            assert phrase not in text, f"{phrase} in {path}"

    routes = Path("app/presentation/student/routes.py").read_text(encoding="utf-8")
    revision_fn = routes.split("def revision(")[1].split("\ndef ")[0]
    assert "highest-value" not in revision_fn.lower()
    assert "Adaptive Decision" not in revision_fn

    service = Path(
        "app/application/student_experience/revision_service.py"
    ).read_text(encoding="utf-8")
    assert "RevisionPlanner" not in service
    assert "PriorityCalculator" not in service
    assert "ROIEstimator" not in service
    assert "highest-value" not in service.lower()
    assert "why_recommended" not in service

    form_src = Path("app/presentation/student/forms.py").read_text(encoding="utf-8")
    assert "highest-value" not in form_src.lower()
    assert 'SubmitField("Begin")' in form_src
