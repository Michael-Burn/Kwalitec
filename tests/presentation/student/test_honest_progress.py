"""Honest Progress / Stats presentation: streak, milestones, Stats page."""

from __future__ import annotations

import ast
import re
from datetime import date
from pathlib import Path
from unittest.mock import MagicMock

import pytest
from flask import get_flashed_messages, render_template

from app.application.learner_progress.index_document import merge_qualifying_date
from app.application.learner_progress.milestones import EarnedMilestone, MilestoneKind
from app.application.learner_progress.query import StreakStats
from app.application.progress_engine.dto import (
    CurriculumPosition,
    ProgressProjection,
    StudyProgress,
)
from app.application.student_experience.dto.home_snapshot import HomeSnapshot
from app.application.study_curriculum.states import TopicLearningState
from app.application.study_curriculum.types import (
    CurriculumLearningSnapshot,
    TopicCurriculumState,
)
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
from app.presentation.student.services.student_study_curriculum_service import (
    StudentStudyCurriculumPresentationService,
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
TOPIC_MASTERED = "CS1-A-T01"
TOPIC_DEVELOPING = "CS1-A-T02"
TOPIC_NOT_YET = "CS1-A-T03"
TOPIC_NOT_STARTED = "CS1-A-T04"
TOPIC_EXTRA_MASTERED = "CS1-A-T05"


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


def _topic_row(topic_id: str, state: TopicLearningState) -> TopicCurriculumState:
    return TopicCurriculumState(
        topic_id=topic_id,
        topic_code=topic_id,
        title=f"Title {topic_id}",
        section_id="S1",
        section_title="Section 1",
        state=state,
        last_practised_at=None,
        reached=state is not TopicLearningState.NOT_STARTED,
    )


def _snapshot_with_states() -> CurriculumLearningSnapshot:
    return CurriculumLearningSnapshot(
        user_id=11,
        subject_code="CS1",
        curriculum_identity="CS1:test",
        topics=(
            _topic_row(TOPIC_MASTERED, TopicLearningState.MASTERED),
            _topic_row(TOPIC_EXTRA_MASTERED, TopicLearningState.MASTERED),
            _topic_row(TOPIC_DEVELOPING, TopicLearningState.DEVELOPING),
            _topic_row(TOPIC_NOT_YET, TopicLearningState.NOT_YET_ASSESSED),
            _topic_row(TOPIC_NOT_STARTED, TopicLearningState.NOT_STARTED),
        ),
    )


def _study_progress(
    *,
    topic_ids: tuple[str, ...],
    completed: tuple[str, ...] = (),
    verified: tuple[str, ...] | None = None,
    claimed: tuple[str, ...] = (),
) -> StudyProgress:
    verified_ids = completed if verified is None else verified
    claimed_ids = tuple(claimed)
    progressed = tuple(
        tid for tid in topic_ids if tid in set(verified_ids) | set(claimed_ids)
    )
    if verified is None and not claimed_ids:
        progressed = tuple(completed)
        verified_ids = tuple(completed)
    completed_set = frozenset(progressed)
    incomplete = tuple(tid for tid in topic_ids if tid not in completed_set)
    progressed_ratio = (len(progressed) / len(topic_ids)) if topic_ids else 0.0
    verified_ratio = (len(verified_ids) / len(topic_ids)) if topic_ids else 0.0
    current = incomplete[0] if incomplete else None
    position = CurriculumPosition(
        curriculum_identity="CS1:test",
        current_topic_id=current,
        current_topic_index=(
            topic_ids.index(current) if current in topic_ids else None
        ),
        topic_count=len(topic_ids),
        completed_count=len(progressed),
        remaining_count=len(incomplete),
        coverage_ratio=progressed_ratio,
        journey_stage="in_progress",
        syllabus_complete=not incomplete,
    )
    return StudyProgress(
        curriculum_identity="CS1:test",
        topic_ids=topic_ids,
        completed_topic_ids=progressed,
        incomplete_topic_ids=incomplete,
        current_topic_id=current,
        coverage_ratio=progressed_ratio,
        journey_stage=position.journey_stage,
        syllabus_complete=position.syllabus_complete,
        completed_objective_ids=(),
        remaining_objective_ids=(),
        position=position,
        projection=ProgressProjection(
            remaining_topic_ids=incomplete,
            next_topic_id=current,
            estimated_topics_remaining=len(incomplete),
            twin_present=False,
        ),
        verified_completed_topic_ids=tuple(verified_ids),
        prior_knowledge_claimed_topic_ids=claimed_ids,
        progressed_topic_ids=progressed,
        verified_coverage_ratio=verified_ratio,
    )


class _FakeAssembler:
    def __init__(self, snapshot: CurriculumLearningSnapshot) -> None:
        self._snapshot = snapshot
        self.calls = 0
        self.kwargs: list[dict] = []

    def assemble(
        self, *, user_id: int, subject_code: str
    ) -> CurriculumLearningSnapshot:
        self.calls += 1
        self.kwargs.append({"user_id": user_id, "subject_code": subject_code})
        return self._snapshot


class _FakeProgress:
    def __init__(self, progress: StudyProgress) -> None:
        self._progress = progress
        self.calls = 0

    def get_study_progress(self, *, user_id: int, subject_code: str) -> StudyProgress:
        self.calls += 1
        return self._progress


def test_home_header_renders_zero_streak_without_error(app, ctx):
    html = _empty_home_html(app, streak=0)
    assert 'data-honest-progress="streak"' in html
    assert "Streak · 0" in html
    assert "don't break" not in html.lower()
    assert "broken" not in html.lower()
    assert "—" not in html
    assert 'href="/student/progress"' in html
    assert ">Stats<" in html


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
    assert 'data-honest-progress="streak"' in html
    assert "Streak · 0" in html
    assert 'data-honest-progress="signals-streak"' not in html
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
    assert "Stats" in html


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
    assembler = _FakeAssembler(_snapshot_with_states())
    progress = _study_progress(
        topic_ids=(
            TOPIC_MASTERED,
            TOPIC_EXTRA_MASTERED,
            TOPIC_DEVELOPING,
            TOPIC_NOT_YET,
            TOPIC_NOT_STARTED,
        ),
        completed=(TOPIC_MASTERED, TOPIC_EXTRA_MASTERED),
    )
    svc = HonestProgressService(
        study_day_query=query,
        shown_store=shown,
        assembler=assembler,
        study_progress=_FakeProgress(progress),
    )
    svc._resolve_subject_code = lambda _uid: "CS1"  # type: ignore[method-assign]
    with app.test_request_context("/student/progress"):
        page = svc.build_progress_page(user_id=11, as_of=AS_OF)
        html = render_template(
            "student/progress.html",
            progress=page,
            page=None,
            title=page.page_title,
        )
    assert page.page_title == "Stats"
    assert page.current_streak_days == 2
    assert page.longest_streak_days == 2
    assert page.topics_mastered_count == 2
    assert len(page.milestones) == 1
    assert page.milestones[0].label == "7-day study streak reached"
    assert "7-day study streak reached" in html
    assert "2026-08-31" in html
    assert 'data-honest-progress="current-streak"' in html
    assert assembler.calls == 1


def test_learning_state_counts_come_from_study_assembler(app, ctx):
    """Four-state aggregates must call the same assembler Study uses."""
    snapshot = _snapshot_with_states()
    assembler = _FakeAssembler(snapshot)
    progress = _study_progress(
        topic_ids=tuple(t.topic_id for t in snapshot.topics),
        completed=(TOPIC_MASTERED, TOPIC_EXTRA_MASTERED),
    )
    svc = HonestProgressService(
        study_day_query=MagicMock(
            streak_stats=MagicMock(
                return_value=StreakStats(
                    current_streak_days=0,
                    longest_streak_days=0,
                    qualifying_dates=(),
                )
            )
        ),
        shown_store=MilestonesShownPersistence(store=SessionDocumentStore()),
        assembler=assembler,
        study_progress=_FakeProgress(progress),
    )
    svc._resolve_subject_code = lambda _uid: "CS1"  # type: ignore[method-assign]
    with app.test_request_context("/student/progress"):
        page = svc.build_progress_page(user_id=11, as_of=AS_OF)
    assert assembler.calls == 1
    assert assembler.kwargs == [{"user_id": 11, "subject_code": "CS1"}]
    by_state = {row.state: row.count for row in page.learning_state_counts}
    assert by_state == {
        "not_started": 1,
        "not_yet_assessed": 1,
        "developing": 1,
        "mastered": 2,
    }
    assert page.topics_mastered_count == 2


def test_mastered_count_matches_study_over_full_syllabus(app, ctx):
    """Previous Twin-only mastery count is replaced by assembler full-syllabus count."""
    snapshot = _snapshot_with_states()
    assembler = _FakeAssembler(snapshot)
    progress = _study_progress(
        topic_ids=tuple(t.topic_id for t in snapshot.topics),
        completed=(TOPIC_MASTERED, TOPIC_EXTRA_MASTERED),
    )
    twin = MagicMock()
    twin.topics_with_estimated_knowledge.return_value = ()

    stats_svc = HonestProgressService(
        study_day_query=MagicMock(
            streak_stats=MagicMock(
                return_value=StreakStats(
                    current_streak_days=0,
                    longest_streak_days=0,
                    qualifying_dates=(),
                )
            )
        ),
        shown_store=MilestonesShownPersistence(store=SessionDocumentStore()),
        twin_query=twin,
        assembler=assembler,
        study_progress=_FakeProgress(progress),
    )
    stats_svc._resolve_subject_code = lambda _uid: "CS1"  # type: ignore[method-assign]

    study_svc = StudentStudyCurriculumPresentationService(
        assembler=_FakeAssembler(snapshot),
        study_progress=_FakeProgress(progress),
        why_lookup=lambda _code: {},
    )
    with app.test_request_context("/student/progress"):
        stats_page = stats_svc.build_progress_page(user_id=11, as_of=AS_OF)
    study_page = study_svc.build(user_id=11, subject_code="CS1")
    study_mastered = sum(
        1
        for section in study_page.sections
        for topic in section.topics
        if topic.state == TopicLearningState.MASTERED.value
    )
    assert stats_page.topics_mastered_count == study_mastered == 2
    assert twin.topics_with_estimated_knowledge.call_count == 0


def test_stats_section_order_matches_specification(app, ctx):
    snapshot = _snapshot_with_states()
    progress = _study_progress(
        topic_ids=tuple(t.topic_id for t in snapshot.topics),
        completed=(TOPIC_MASTERED,),
    )
    svc = HonestProgressService(
        study_day_query=MagicMock(
            streak_stats=MagicMock(
                return_value=StreakStats(
                    current_streak_days=1,
                    longest_streak_days=1,
                    qualifying_dates=(AS_OF,),
                )
            )
        ),
        shown_store=MilestonesShownPersistence(store=SessionDocumentStore()),
        assembler=_FakeAssembler(snapshot),
        study_progress=_FakeProgress(progress),
    )
    svc._resolve_subject_code = lambda _uid: "CS1"  # type: ignore[method-assign]
    with app.test_request_context("/student/progress"):
        page = svc.build_progress_page(user_id=11, as_of=AS_OF)
        html = render_template(
            "student/progress.html",
            progress=page,
            page=None,
            title=page.page_title,
        )
    order = re.findall(r'data-stats-section="([^"]+)"', html)
    assert order == ["consistency", "learning", "curriculum", "milestones"]


def test_milestone_entries_still_name_topics_after_reorder(app, ctx):
    store = SessionDocumentStore()
    shown = MilestonesShownPersistence(store=store)
    topic_label = "Estimated knowledge mastered for Conditional probability"
    shown.record_shown(
        learner_id="11",
        milestone_id="topic_ek_CS1-A-T01",
        label=topic_label,
        shown_at=AS_OF,
    )
    snapshot = _snapshot_with_states()
    progress = _study_progress(
        topic_ids=tuple(t.topic_id for t in snapshot.topics),
        completed=(TOPIC_MASTERED,),
    )
    svc = HonestProgressService(
        study_day_query=MagicMock(
            streak_stats=MagicMock(
                return_value=StreakStats(
                    current_streak_days=0,
                    longest_streak_days=0,
                    qualifying_dates=(),
                )
            )
        ),
        shown_store=shown,
        assembler=_FakeAssembler(snapshot),
        study_progress=_FakeProgress(progress),
    )
    svc._resolve_subject_code = lambda _uid: "CS1"  # type: ignore[method-assign]
    with app.test_request_context("/student/progress"):
        page = svc.build_progress_page(user_id=11, as_of=AS_OF)
        html = render_template(
            "student/progress.html",
            progress=page,
            page=None,
            title=page.page_title,
        )
    assert page.milestones[0].label == topic_label
    assert "Conditional probability" in html
    assert 'data-stats-section="milestones"' in html


def test_coverage_matches_existing_study_progress_formula(app, ctx):
    snapshot = _snapshot_with_states()
    topic_ids = tuple(t.topic_id for t in snapshot.topics)
    completed = (TOPIC_MASTERED, TOPIC_EXTRA_MASTERED)
    progress = _study_progress(topic_ids=topic_ids, completed=completed)
    fake_progress = _FakeProgress(progress)
    svc = HonestProgressService(
        study_day_query=MagicMock(
            streak_stats=MagicMock(
                return_value=StreakStats(
                    current_streak_days=0,
                    longest_streak_days=0,
                    qualifying_dates=(),
                )
            )
        ),
        shown_store=MilestonesShownPersistence(store=SessionDocumentStore()),
        assembler=_FakeAssembler(snapshot),
        study_progress=fake_progress,
    )
    svc._resolve_subject_code = lambda _uid: "CS1"  # type: ignore[method-assign]
    study_svc = StudentStudyCurriculumPresentationService(
        assembler=_FakeAssembler(snapshot),
        study_progress=_FakeProgress(progress),
        why_lookup=lambda _code: {},
    )
    with app.test_request_context("/student/progress"):
        stats_page = svc.build_progress_page(user_id=11, as_of=AS_OF)
    study_page = study_svc.build(user_id=11, subject_code="CS1")
    assert fake_progress.calls >= 1
    assert stats_page.covered_count == study_page.covered_count == 2
    assert stats_page.topic_count == study_page.topic_count == 5
    assert stats_page.syllabus_coverage_label == study_page.coverage_label
    assert stats_page.syllabus_coverage_label == "2 of 5 topics completed"
    expected_percent = int(
        round(max(0.0, min(1.0, float(progress.verified_coverage_ratio or 0.0))) * 100)
    )
    assert stats_page.syllabus_coverage_percent == expected_percent == 40


def test_stats_distinguishes_verified_completion_from_prior_knowledge_claims(app, ctx):
    snapshot = _snapshot_with_states()
    topic_ids = tuple(t.topic_id for t in snapshot.topics)
    progress = _study_progress(
        topic_ids=topic_ids,
        verified=(TOPIC_MASTERED,),
        claimed=(TOPIC_EXTRA_MASTERED,),
    )
    fake_progress = _FakeProgress(progress)
    svc = HonestProgressService(
        study_day_query=MagicMock(
            streak_stats=MagicMock(
                return_value=StreakStats(
                    current_streak_days=0,
                    longest_streak_days=0,
                    qualifying_dates=(),
                )
            )
        ),
        shown_store=MilestonesShownPersistence(store=SessionDocumentStore()),
        assembler=_FakeAssembler(snapshot),
        study_progress=fake_progress,
    )
    svc._resolve_subject_code = lambda _uid: "CS1"  # type: ignore[method-assign]
    with app.test_request_context("/student/progress"):
        page = svc.build_progress_page(user_id=11, as_of=AS_OF)
        html = render_template(
            "student/progress.html",
            progress=page,
            page=None,
            title=page.page_title,
        )
    assert page.covered_count == 1
    assert page.topic_count == 5
    assert page.syllabus_coverage_percent == 20
    assert page.syllabus_coverage_label == "1 of 5 topics completed"
    assert page.prior_knowledge_claimed_count == 1
    assert page.prior_knowledge_claim_label == "1 already knew coming in"
    assert "1 of 5 topics completed" in html
    assert "1 already knew coming in" in html
    assert 'data-honest-progress="prior-knowledge"' in html
    # Progressed union must not inflate the verified ratio shown to students.
    assert progress.coverage_ratio == pytest.approx(0.4)
    assert page.syllabus_coverage_percent != int(round(progress.coverage_ratio * 100))


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
    html = response.get_data(as_text=True)
    assert "Stats" in html
    assert 'data-stats-section="consistency"' in html
    assert re.search(
        r'class="student-nav-link is-active"[^>]*>Stats</a>',
        html,
    )
