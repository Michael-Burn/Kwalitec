"""Honest Progress presentation: Home streak, one-shot milestones, Progress page."""

from __future__ import annotations

import ast
from datetime import date
from pathlib import Path
from unittest.mock import MagicMock

from flask import get_flashed_messages

from app.application.learner_progress.index_document import merge_qualifying_date
from app.application.learner_progress.milestones import EarnedMilestone, MilestoneKind
from app.application.learner_progress.query import StreakStats
from app.application.student_experience.dto.home_snapshot import HomeSnapshot
from app.infrastructure.adapters.learner_progress import (
    qualifying_study_day_persistence as qsd_persist,
)
from app.infrastructure.adapters.learner_progress.query_adapter import (
    QualifyingStudyDayQueryAdapter,
)
from app.infrastructure.adapters.learner_progress.shown_milestones_persistence import (
    MilestonesShownPersistence,
)
from app.infrastructure.session.store import SessionDocumentStore
from app.presentation.student.services.honest_progress_service import (
    HonestProgressService,
)
from app.presentation.student.view_models import home_vm
from tests.presentation.student.helpers import render_student_home

FORBIDDEN_IMPORT_FRAGMENTS = (
    "educational_packages",
    "educational_campaigns",
    "curriculum.data",
    "curriculum/data",
    "app.curriculum.data",
)

AS_OF = date(2026, 8, 31)


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def _empty_home_html(app, *, streak: int = 0) -> str:
    snap = HomeSnapshot(
        student_id="stu-hp-1",
        greeting="Welcome back",
        examination_label="",
        has_recommendation=False,
        can_start_session=False,
    )
    page_home = home_vm(snap, unified_journey=False)
    return render_student_home(
        app,
        page_home,
        current_streak_days=streak,
        progress_href="/student/progress",
    )


def test_home_header_renders_zero_streak_without_error(app, ctx):
    html = _empty_home_html(app, streak=0)
    assert 'data-honest-progress="streak"' in html
    assert "Streak · 0" in html
    assert "don't break" not in html.lower()
    assert "broken" not in html.lower()
    assert "—" not in html
    assert 'href="/student/progress"' in html


def test_home_header_renders_genuine_streak(app, ctx):
    html = _empty_home_html(app, streak=3)
    assert 'data-honest-progress="streak"' in html
    assert "Streak · 3" in html


def test_home_signals_use_plain_streak_number(app, ctx):
    snap = HomeSnapshot(
        student_id="stu-hp-2",
        greeting="Welcome back",
        examination_label="IFoA CS1",
        has_recommendation=False,
        can_start_session=False,
    )
    page_home = home_vm(snap, unified_journey=False)
    html = render_student_home(app, page_home, current_streak_days=0)
    assert 'data-honest-progress="signals-streak"' in html
    assert "Study rhythm builds as you show up" not in html
    assert "Recent study rhythm" not in html


def test_qualifying_store_feeds_streak_stats_for_home_source():
    store = SessionDocumentStore()
    index = qsd_persist.QualifyingStudyDayIndexPersistence(store=store)
    doc = None
    for d in (date(2026, 8, 29), date(2026, 8, 30), date(2026, 8, 31)):
        doc = merge_qualifying_date(doc, learner_id="7", study_date=d)
    index.save_index(learner_id="7", document=doc)
    query = QualifyingStudyDayQueryAdapter(index=index)
    svc = HonestProgressService(study_day_query=query)
    stats = svc.streak_stats(user_id=7, as_of=AS_OF)
    assert stats.current_streak_days == 3
    assert stats.longest_streak_days == 3


def test_milestone_announced_exactly_once(app, ctx):
    store = SessionDocumentStore()
    shown = MilestonesShownPersistence(store=store)
    study_day = MagicMock()
    study_day.streak_stats.return_value = StreakStats(
        current_streak_days=7,
        longest_streak_days=7,
        qualifying_dates=(AS_OF,),
    )
    detector = MagicMock()
    milestone = EarnedMilestone(
        kind=MilestoneKind.STREAK_DAYS,
        milestone_id="streak_7",
        label="7-day study streak reached",
    )
    detector.detect_new_milestones.side_effect = [
        (milestone,),
        (),
    ]
    twin = MagicMock()
    svc = HonestProgressService(
        study_day_query=study_day,
        shown_store=shown,
        twin_query=twin,
        detector=detector,
    )
    svc._resolve_subject_code = lambda _uid: "CS1"  # type: ignore[method-assign]
    svc._section_specs = lambda _code: ((), {})  # type: ignore[method-assign]
    svc._completed_topic_ids = lambda **_kw: frozenset()  # type: ignore[method-assign]

    with app.test_request_context("/student/"):
        first = svc.announce_new_milestones_on_home(user_id=7, as_of=AS_OF)
        flashes_first = get_flashed_messages(with_categories=True)
    assert first == ("7-day study streak reached",)
    assert ("success", "7-day study streak reached") in flashes_first
    assert "streak_7" in shown.previously_shown_ids(learner_id="7")

    with app.test_request_context("/student/"):
        second = svc.announce_new_milestones_on_home(user_id=7, as_of=AS_OF)
        flashes_second = get_flashed_messages(with_categories=True)
    assert second == ()
    assert flashes_second == []
    assert detector.detect_new_milestones.call_count == 2


def test_progress_page_zero_data(app, ctx, student_client):
    response = student_client.get("/student/progress")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert 'data-honest-progress="page"' in html
    assert 'data-honest-progress="current-streak"' in html
    assert 'data-honest-progress="milestones-empty"' in html
    assert "No milestones reached yet." in html
    assert "—" not in html


def test_progress_page_with_genuine_data(app, ctx):
    store = SessionDocumentStore()
    index = qsd_persist.QualifyingStudyDayIndexPersistence(store=store)
    doc = None
    for d in (date(2026, 8, 30), date(2026, 8, 31)):
        doc = merge_qualifying_date(doc, learner_id="11", study_date=d)
    index.save_index(learner_id="11", document=doc)
    shown = MilestonesShownPersistence(store=store)
    shown.record_shown(
        learner_id="11",
        milestone_id="streak_7",
        label="7-day study streak reached",
        shown_at=AS_OF,
    )
    query = QualifyingStudyDayQueryAdapter(index=index)
    twin = MagicMock()
    twin.topics_with_estimated_knowledge.return_value = ()
    svc = HonestProgressService(
        study_day_query=query,
        shown_store=shown,
        twin_query=twin,
    )
    svc._resolve_subject_code = lambda _uid: ""  # type: ignore[method-assign]
    with app.test_request_context("/student/progress"):
        from flask import render_template

        page = svc.build_progress_page(user_id=11, as_of=AS_OF)
        html = render_template(
            "student/progress.html",
            progress=page,
            page=None,
            title=page.page_title,
        )
    assert page.current_streak_days == 2
    assert page.longest_streak_days == 2
    assert page.topics_mastered_count == 0
    assert len(page.milestones) == 1
    assert page.milestones[0].label == "7-day study streak reached"
    assert "7-day study streak reached" in html
    assert "2026-08-31" in html
    assert 'data-honest-progress="current-streak"' in html


def test_honest_progress_modules_do_not_import_content_authoring_paths():
    root = _repo_root()
    infra = root / "app/infrastructure/adapters/learner_progress"
    paths = [
        root / "app/application/learner_progress/shown_milestones.py",
        infra / "shown_milestones_persistence.py",
        root / "app/presentation/student/dto/honest_progress.py",
        root / "app/presentation/student/services/honest_progress_service.py",
    ]
    offenders: list[str] = []
    for path in paths:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            names: list[str] = []
            if isinstance(node, ast.Import):
                names = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    names = [node.module]
            for name in names:
                for frag in FORBIDDEN_IMPORT_FRAGMENTS:
                    if frag in name:
                        offenders.append(f"{path.name}: {name}")
    assert offenders == []


def test_progress_route_reachable(student_client):
    response = student_client.get("/student/progress")
    assert response.status_code == 200
    assert b"Progress" in response.data
