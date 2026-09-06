"""Study Curriculum destination: four-state map, coverage, Continue, independence."""

from __future__ import annotations

import ast
from datetime import UTC, datetime
from pathlib import Path

from flask import render_template

from app.application.progress_engine.dto import (
    CurriculumPosition,
    ProgressProjection,
    StudyProgress,
)
from app.application.study_curriculum.states import TopicLearningState
from app.application.study_curriculum.types import (
    CurriculumLearningSnapshot,
    TopicCurriculumState,
)
from app.presentation.student.services.student_home_service import (
    home_resume_continue_href,
)
from app.presentation.student.services.student_study_curriculum_service import (
    StudentStudyCurriculumPresentationService,
)
from app.presentation.student.view_models import HomePageViewModel

FIXED = datetime(2026, 9, 6, 8, 0, tzinfo=UTC)

TOPIC_MASTERED = "CS1-A-T01"
TOPIC_DEVELOPING = "CS1-A-T02"
TOPIC_NOT_YET_ASSESSED = "CS1-A-T03"
TOPIC_NOT_STARTED = "CS1-A-T04"
TOPIC_COMPLETE_DEVELOPING = "CS1-A-T05"

FORBIDDEN_IMPORT_FRAGMENTS = (
    "educational_packages",
    "educational_campaigns",
    "educational_authoring",
    "curriculum.data",
    "curriculum/data",
    "app.curriculum.data",
)


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def _progress(
    *,
    topic_ids: tuple[str, ...],
    completed: tuple[str, ...] = (),
    current_topic_id: str | None = None,
    curriculum_identity: str = "CS1:test",
) -> StudyProgress:
    completed_set = frozenset(completed)
    incomplete = tuple(tid for tid in topic_ids if tid not in completed_set)
    remaining = incomplete
    ratio = (len(completed) / len(topic_ids)) if topic_ids else 0.0
    position = CurriculumPosition(
        curriculum_identity=curriculum_identity,
        current_topic_id=current_topic_id,
        current_topic_index=(
            topic_ids.index(current_topic_id)
            if current_topic_id in topic_ids
            else None
        ),
        topic_count=len(topic_ids),
        completed_count=len(completed),
        remaining_count=len(remaining),
        coverage_ratio=ratio,
        journey_stage="in_progress",
        syllabus_complete=not remaining,
    )
    return StudyProgress(
        curriculum_identity=curriculum_identity,
        topic_ids=topic_ids,
        completed_topic_ids=completed,
        incomplete_topic_ids=incomplete,
        current_topic_id=current_topic_id,
        coverage_ratio=ratio,
        journey_stage=position.journey_stage,
        syllabus_complete=position.syllabus_complete,
        completed_objective_ids=(),
        remaining_objective_ids=(),
        position=position,
        projection=ProgressProjection(
            remaining_topic_ids=incomplete,
            next_topic_id=current_topic_id,
            estimated_topics_remaining=len(incomplete),
            twin_present=False,
        ),
    )


def _row(
    topic_id: str,
    state: TopicLearningState,
    *,
    section_id: str = "S1",
    section_title: str = "Section 1",
    title: str | None = None,
) -> TopicCurriculumState:
    return TopicCurriculumState(
        topic_id=topic_id,
        topic_code=topic_id,
        title=title or f"Title {topic_id}",
        section_id=section_id,
        section_title=section_title,
        state=state,
        last_practised_at=(
            FIXED if state is not TopicLearningState.NOT_STARTED else None
        ),
    )


def _mixed_snapshot() -> CurriculumLearningSnapshot:
    return CurriculumLearningSnapshot(
        user_id=1,
        subject_code="CS1",
        curriculum_identity="CS1:test",
        topics=(
            _row(TOPIC_MASTERED, TopicLearningState.MASTERED),
            _row(TOPIC_COMPLETE_DEVELOPING, TopicLearningState.DEVELOPING),
            _row(TOPIC_DEVELOPING, TopicLearningState.DEVELOPING),
            _row(TOPIC_NOT_YET_ASSESSED, TopicLearningState.NOT_YET_ASSESSED),
            _row(TOPIC_NOT_STARTED, TopicLearningState.NOT_STARTED),
        ),
    )


def _mixed_progress() -> StudyProgress:
    topic_ids = (
        TOPIC_MASTERED,
        TOPIC_COMPLETE_DEVELOPING,
        TOPIC_DEVELOPING,
        TOPIC_NOT_YET_ASSESSED,
        TOPIC_NOT_STARTED,
    )
    return _progress(
        topic_ids=topic_ids,
        completed=(TOPIC_MASTERED, TOPIC_COMPLETE_DEVELOPING),
        current_topic_id=TOPIC_DEVELOPING,
    )


class _FakeAssembler:
    def __init__(self, snapshot: CurriculumLearningSnapshot) -> None:
        self._snapshot = snapshot
        self.calls = 0

    def assemble(
        self, *, user_id: int, subject_code: str
    ) -> CurriculumLearningSnapshot:
        self.calls += 1
        return self._snapshot


class _FakeProgress:
    def __init__(self, progress: StudyProgress) -> None:
        self._progress = progress
        self.calls = 0

    def get_study_progress(self, *, user_id: int, subject_code: str) -> StudyProgress:
        self.calls += 1
        return self._progress


def _build_mixed_page(**kwargs):
    snapshot = _mixed_snapshot()
    progress = _mixed_progress()
    why = {
        TOPIC_MASTERED: "Title CS1-A-T01 relies heavily on earlier probability.",
    }
    svc = StudentStudyCurriculumPresentationService(
        assembler=_FakeAssembler(snapshot),
        study_progress=_FakeProgress(progress),
        why_lookup=lambda _code: why,
    )
    return svc.build(user_id=1, subject_code="CS1", subject_label="CS1", **kwargs)


def _render_study(app, page) -> str:
    with app.test_request_context("/student/study"):
        return render_template("student/study.html", study=page)


def test_study_page_projects_all_four_learning_states():
    page = _build_mixed_page()
    states = [topic.state for section in page.sections for topic in section.topics]
    assert TopicLearningState.MASTERED in states
    assert TopicLearningState.DEVELOPING in states
    assert TopicLearningState.NOT_YET_ASSESSED in states
    assert TopicLearningState.NOT_STARTED in states
    assert page.sections[0].title == "Section 1"
    quiet = [
        topic
        for section in page.sections
        for topic in section.topics
        if topic.is_quiet
    ]
    assert [topic.topic_id for topic in quiet] == [TOPIC_NOT_STARTED]


def test_coverage_uses_study_progress_not_four_state_counts():
    page = _build_mixed_page()
    progress = _mixed_progress()
    assert page.covered_count == len(progress.completed_topic_ids) == 2
    assert page.topic_count == len(progress.topic_ids) == 5
    assert page.coverage_ratio == progress.coverage_ratio
    assert page.coverage_label == "2 of 5 topics covered"
    honest_percent = int(
        round(max(0.0, min(1.0, float(progress.coverage_ratio or 0.0))) * 100)
    )
    assert honest_percent == 40
    mastered = sum(
        1
        for section in page.sections
        for topic in section.topics
        if topic.state == TopicLearningState.MASTERED
    )
    started = sum(
        1
        for section in page.sections
        for topic in section.topics
        if not topic.is_quiet
    )
    assert page.covered_count != mastered
    assert page.covered_count != started


def test_study_template_renders_four_states_and_coverage(app, ctx):
    page = _build_mixed_page()
    html = _render_study(app, page)
    assert "Not started" in html
    assert "Not yet assessed" in html
    assert "Developing" in html
    assert "Mastered" in html
    assert "2 of 5 topics covered" in html
    assert 'data-learning-state="mastered"' in html
    assert 'data-learning-state="developing"' in html
    assert 'data-learning-state="not_yet_assessed"' in html
    assert 'data-learning-state="not_started"' in html
    assert "ds-os-study__topic--quiet" in html
    assert "Why this topic matters" in html
    assert "Title CS1-A-T01 relies heavily on earlier probability." in html
    assert "—" not in html


def test_topics_are_not_actionable_to_start_a_session(app, ctx):
    page = _build_mixed_page()
    html = _render_study(app, page)
    assert "student.start_session" not in html
    assert "/student/start-session" not in html
    assert 'action="' not in html.lower() or "start_session" not in html
    assert "Start Today's Session" not in html
    assert "Begin Session" not in html
    for topic_id in (
        TOPIC_MASTERED,
        TOPIC_DEVELOPING,
        TOPIC_NOT_YET_ASSESSED,
        TOPIC_NOT_STARTED,
        TOPIC_COMPLETE_DEVELOPING,
    ):
        assert f'data-study-topic="{topic_id}"' in html
    assert "<details" in html
    assert 'href="/session/' not in html


def test_continue_link_uses_home_resume_href_not_new_decision(app, ctx):
    home = HomePageViewModel(
        session_id="open-sess",
        session_control="resume",
    )
    with app.test_request_context("/student/study"):
        href = home_resume_continue_href(home)
        assert href is not None
        assert "open-sess" in href
        assert href.startswith("/session/")
        start_home = HomePageViewModel(
            session_id="",
            session_control="start",
        )
        assert home_resume_continue_href(start_home) is None
        page = _build_mixed_page(continue_href=href)
        html = render_template("student/study.html", study=page)
    assert 'data-study-continue="true"' in html
    assert 'data-session-resume="true"' in html
    assert href in html
    assert "student.start_session" not in html
    assert "url_for('student.start_session')" not in html


def test_study_route_renders_mixed_states(student_client, monkeypatch):
    snapshot = _mixed_snapshot()
    progress = _mixed_progress()
    assembler = _FakeAssembler(snapshot)
    monkeypatch.setattr(
        "app.infrastructure.adapters.study_curriculum.runtime_query."
        "curriculum_learning_state_assembler",
        lambda **_kwargs: assembler,
    )
    monkeypatch.setattr(
        "app.application.educational_runtime_engine.service."
        "EducationalRuntimeEngineService.get_study_progress",
        lambda self, **_kwargs: progress,
    )
    monkeypatch.setattr(
        "app.presentation.student.services.student_study_curriculum_service."
        "_why_from_knowledge_architecture",
        lambda _code: {TOPIC_MASTERED: "Graph rationale for mastered topic."},
    )
    monkeypatch.setattr(
        "app.services.twin_cutover_service.subject_code_for_user",
        lambda _user_id: "CS1",
    )
    monkeypatch.setattr(
        "app.presentation.student.services.student_home_service."
        "home_resume_continue_href",
        lambda _home: "/session/live-sess/overview",
    )
    response = student_client.get("/student/study")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "Study" in html
    assert "Not started" in html
    assert "Not yet assessed" in html
    assert "Developing" in html
    assert "Mastered" in html
    assert "2 of 5 topics covered" in html
    assert 'data-study-curriculum="page"' in html
    assert "/session/live-sess/overview" in html
    assert 'data-session-resume="true"' in html
    assert "student.start_session" not in html
    assert assembler.calls == 1
    assert "Graph rationale for mastered topic." in html


def test_study_modules_do_not_import_content_authoring_paths():
    root = _repo_root()
    paths = [
        root / "app/presentation/student/dto/study_curriculum.py",
        root
        / "app/presentation/student/services/student_study_curriculum_service.py",
        root / "app/templates/student/study.html",
    ]
    offenders: list[str] = []
    for path in paths:
        text = path.read_text(encoding="utf-8")
        if path.suffix == ".html":
            for frag in FORBIDDEN_IMPORT_FRAGMENTS:
                if frag in text:
                    offenders.append(f"{path.name}: {frag}")
            continue
        tree = ast.parse(text, filename=str(path))
        for node in ast.walk(tree):
            modules: list[str] = []
            if isinstance(node, ast.Import):
                modules = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom):
                modules = [node.module or ""]
            for mod in modules:
                lowered = mod.replace("\\", "/")
                for frag in FORBIDDEN_IMPORT_FRAGMENTS:
                    if frag in lowered:
                        offenders.append(f"{path.name}:{mod}")
    assert offenders == []
