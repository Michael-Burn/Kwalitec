"""Student-selected Study sessions: reached gate, provenance, isolation."""

from __future__ import annotations

import ast
from datetime import UTC, date, datetime, timedelta
from pathlib import Path

import pytest

from app.application.config.v2_flags import resolve_v2_feature_flags
from app.application.educational_experience import EducationalExperienceService
from app.application.educational_runtime_engine.service import (
    EducationalRuntimeEngineService,
)
from app.application.learning_session.dto.candidate_observation import (
    CandidateObservation,
    RuntimeEvidenceType,
)
from app.application.learning_session.runtime import LearningSessionRuntime
from app.application.learning_session.session_origin import (
    SESSION_ORIGIN_STUDENT_SELECTED,
    STUDENT_SELECTED_WHY,
)
from app.application.platform_integration.discovery import PUBLISHED_CATEGORY_CODE
from app.application.platform_integration.enrolment_bridge import (
    FounderStudentEnrolmentBridge,
)
from app.application.student_runtime import (
    OpenSessionReplacementRequired,
    StudentRuntimeCoordinator,
    TopicNotReached,
)
from app.application.student_twin.session_evidence_consumer import (
    SessionTwinEvidenceConsumer,
)
from app.application.student_twin.twin_engine import StudentTwinEngine
from app.domain.educational_runtime_engine.events import EducationalEventType
from app.domain.educational_runtime_engine.state import MissionStatus
from app.infrastructure.adapters.learner_progress.query_adapter import (
    QualifyingStudyDayQueryAdapter,
)
from app.infrastructure.adapters.learning_session.persistence import (
    LearningSessionPersistenceAdapter,
)
from app.infrastructure.adapters.learning_session.runtime_engine import (
    LearningSessionRuntimeEngine,
)
from app.infrastructure.adapters.student_twin.daily_loop_persistence import (
    DailyLoopTwinPersistence,
)
from app.infrastructure.session.runtime_adapter import SessionRuntimeAdapter
from app.infrastructure.session.store import SessionDocumentStore
from app.models.educational_runtime_engine import (
    RuntimeEducationalEvent,
    RuntimeMissionInstance,
)
from app.models.user import User
from tests.application.platform_integration.helpers import (
    bridge_flags,
    make_user,
    publish_subject,
)

FIXED = datetime(2026, 9, 6, 10, 0, tzinfo=UTC)
ROOT = Path(__file__).resolve().parents[3]


def _flags_on(**extra: str):
    env = {"SR_SESSION_PRIMARY": "1", **extra}
    return resolve_v2_feature_flags(environ=env)


def _enrol_runtime_c(user: User, subject: str) -> None:
    bridge = FounderStudentEnrolmentBridge(flags=bridge_flags())
    result = bridge.enrol(
        user_id=user.id,
        category_code=PUBLISHED_CATEGORY_CODE,
        subject_code=subject,
        exam_date=date.today() + timedelta(days=120),
    )
    assert result.runtime_authority == "published_curriculum"


def _coordinator(store: SessionDocumentStore | None = None, **kwargs):
    store = store or SessionDocumentStore()
    persistence = LearningSessionPersistenceAdapter(store=store)
    overview = SessionRuntimeAdapter(store=store, auto_provision=False)
    return (
        StudentRuntimeCoordinator(
            persistence=persistence,
            session_overview_writer=overview,
            flags=_flags_on(),
            **kwargs,
        ),
        persistence,
        overview,
        store,
    )


def _progress_topics(user_id: int, subject: str):
    engine = EducationalRuntimeEngineService()
    progress = engine.get_study_progress(user_id=user_id, subject_code=subject)
    current = progress.current_topic_id
    unreached = next(
        (
            tid
            for tid in progress.topic_ids
            if tid != current and tid not in progress.completed_topic_ids
        ),
        None,
    )
    return progress, current, unreached


def _complete_with_educational_evidence(
    *,
    persistence: LearningSessionPersistenceAdapter,
    user_id: int,
    session_id: str,
    topic_id: str,
    monkeypatch,
):
    monkeypatch.setenv("SR_EVIDENCE_GATE", "1")
    monkeypatch.setenv("SR_SESSION_COMPLETION_PRODUCT", "1")
    monkeypatch.setenv("SR_TWIN_DAILY_LOOP", "1")
    twin_store = DailyLoopTwinPersistence(store=persistence.store)
    consumer = SessionTwinEvidenceConsumer(
        engine=StudentTwinEngine(clock=lambda: FIXED, id_factory=lambda: "sel01"),
        store=twin_store,
        clock=lambda: FIXED,
        id_factory=lambda: "sel01",
        flag_resolver=resolve_v2_feature_flags,
    )
    engine = LearningSessionRuntimeEngine(
        runtime=LearningSessionRuntime(),
        persistence=persistence,
        mission_completer=EducationalRuntimeEngineService(),
        twin_consumer=consumer,
    )
    obs = CandidateObservation.create(
        observation_id="obs-sel-correct",
        type_id=RuntimeEvidenceType.PRACTICE_CORRECT,
        student_id=str(user_id),
        session_id=session_id,
        topic_id=topic_id,
        mission_instance_id="",
        recorded_at=FIXED,
    )
    persistence.append_candidate(session_id=session_id, observation=obs.to_opaque())
    result = engine.complete_session_opaque(
        str(user_id),
        session_id=session_id,
        finish_verdict="yes",
    )
    return result, twin_store


def test_unreached_topic_cannot_be_selected_server_side(ctx):
    subject = publish_subject("SEL1", title="Unreached Gate")
    user = make_user("sel-unreached@example.com")
    _enrol_runtime_c(user, subject)
    EducationalExperienceService().load_for_user(user.id)
    progress, _current, unreached = _progress_topics(user.id, subject)
    assert unreached is not None
    assert unreached not in progress.completed_topic_ids
    assert unreached != progress.current_topic_id

    coordinator, _, _, _ = _coordinator()
    with pytest.raises(TopicNotReached):
        coordinator.start_student_selected_session(
            user_id=user.id,
            topic_id=unreached,
            subject_code=subject,
        )


def test_reached_topic_launches_playable_session_with_student_selected_origin(ctx):
    subject = publish_subject("SEL2", title="Reached Launch")
    user = make_user("sel-reached@example.com")
    _enrol_runtime_c(user, subject)
    EducationalExperienceService().load_for_user(user.id)
    _progress, current, _unreached = _progress_topics(user.id, subject)
    assert current

    coordinator, persistence, overview_writer, _store = _coordinator()
    binding = coordinator.start_student_selected_session(
        user_id=user.id,
        topic_id=current,
        subject_code=subject,
    )
    assert binding.session_id.startswith("lsr-")
    assert binding.topic_id == current
    assert binding.mission_instance_id == ""
    assert binding.session_origin == SESSION_ORIGIN_STUDENT_SELECTED
    assert binding.phase == "active"

    record = persistence.load(session_id=binding.session_id)
    assert record is not None
    assert record.get("session_origin") == SESSION_ORIGIN_STUDENT_SELECTED
    assert not str(record.get("mission_instance_id") or "").strip()
    handle = persistence.load_handle(session_id=binding.session_id)
    assert handle is not None
    assert handle.phase.value == "active"

    overview = overview_writer.get_session_overview(
        str(user.id), session_id=binding.session_id
    )
    assert overview is not None
    assert overview.get("session_origin") == SESSION_ORIGIN_STUDENT_SELECTED
    assert overview.get("why_studying") == STUDENT_SELECTED_WHY
    assert "Today's Mission" not in str(overview.get("why_studying") or "")


def test_completing_generates_twin_evidence_through_normal_path(ctx, monkeypatch):
    subject = publish_subject("SEL3", title="Twin Evidence")
    user = make_user("sel-twin@example.com")
    _enrol_runtime_c(user, subject)
    EducationalExperienceService().load_for_user(user.id)
    _progress, current, _unreached = _progress_topics(user.id, subject)

    coordinator, persistence, _, _store = _coordinator()
    binding = coordinator.start_student_selected_session(
        user_id=user.id,
        topic_id=current,
        subject_code=subject,
    )
    result, twin_store = _complete_with_educational_evidence(
        persistence=persistence,
        user_id=user.id,
        session_id=binding.session_id,
        topic_id=current,
        monkeypatch=monkeypatch,
    )
    assert result is not None
    assert result["status"] == "completed"
    assert result["twin_updated"] is True
    package = persistence.load_evidence_package(session_id=binding.session_id)
    assert package is not None
    assert (package.get("validation") or {}).get("may_update_twin") is True
    saved = twin_store.load_twin(learner_id=str(user.id), subject_code=subject)
    assert saved is not None


def test_completing_does_not_advance_sequential_pointer(ctx, monkeypatch):
    subject = publish_subject("SEL4", title="No Pointer Advance")
    user = make_user("sel-pointer@example.com")
    _enrol_runtime_c(user, subject)
    EducationalExperienceService().load_for_user(user.id)
    before, current, _unreached = _progress_topics(user.id, subject)
    events_before = RuntimeEducationalEvent.query.filter_by(
        user_id=user.id,
        event_type=EducationalEventType.TOPIC_COMPLETED.value,
    ).count()

    coordinator, persistence, _, _store = _coordinator()
    binding = coordinator.start_student_selected_session(
        user_id=user.id,
        topic_id=current,
        subject_code=subject,
    )
    result, _twin = _complete_with_educational_evidence(
        persistence=persistence,
        user_id=user.id,
        session_id=binding.session_id,
        topic_id=current,
        monkeypatch=monkeypatch,
    )
    assert result["status"] == "completed"
    assert result.get("progress_advanced") is False
    assert result.get("mission_completed") is False

    after = EducationalRuntimeEngineService().get_study_progress(
        user_id=user.id, subject_code=subject
    )
    assert after.current_topic_id == before.current_topic_id
    assert after.completed_topic_ids == before.completed_topic_ids
    events_after = RuntimeEducationalEvent.query.filter_by(
        user_id=user.id,
        event_type=EducationalEventType.TOPIC_COMPLETED.value,
    ).count()
    assert events_after == events_before


def test_completing_does_not_satisfy_todays_mission_even_same_topic(
    ctx, monkeypatch
):
    subject = publish_subject("SEL5", title="Mission Isolation")
    user = make_user("sel-mission@example.com")
    _enrol_runtime_c(user, subject)
    snap = EducationalExperienceService().load_for_user(user.id)
    assert snap is not None and snap.mission is not None
    today_mid = snap.mission.mission_instance_id
    today_mission = EducationalRuntimeEngineService().get_mission_instance(
        user_id=user.id,
        mission_instance_id=today_mid,
    )
    assert today_mission is not None
    today_topic = today_mission.topic_id
    assert today_topic

    coordinator, persistence, _, _store = _coordinator()
    binding = coordinator.start_student_selected_session(
        user_id=user.id,
        topic_id=today_topic,
        subject_code=subject,
    )
    assert binding.topic_id == today_topic
    assert binding.mission_instance_id != today_mid
    assert not binding.mission_instance_id

    result, _twin = _complete_with_educational_evidence(
        persistence=persistence,
        user_id=user.id,
        session_id=binding.session_id,
        topic_id=today_topic,
        monkeypatch=monkeypatch,
    )
    assert result["status"] == "completed"
    assert result.get("mission_completed") is False

    mission = EducationalRuntimeEngineService().get_mission_instance(
        user_id=user.id,
        mission_instance_id=today_mid,
    )
    assert mission is not None
    assert mission.status != MissionStatus.COMPLETED.value
    row = RuntimeMissionInstance.query.filter_by(
        mission_instance_id=today_mid
    ).first()
    assert row is not None
    assert row.status != MissionStatus.COMPLETED.value


def test_qualifying_student_selected_session_counts_toward_streak(
    ctx, monkeypatch
):
    subject = publish_subject("SEL6", title="Streak Pickup")
    user = make_user("sel-streak@example.com")
    _enrol_runtime_c(user, subject)
    EducationalExperienceService().load_for_user(user.id)
    _progress, current, _unreached = _progress_topics(user.id, subject)

    coordinator, persistence, _, _store = _coordinator()
    binding = coordinator.start_student_selected_session(
        user_id=user.id,
        topic_id=current,
        subject_code=subject,
    )
    result, _twin = _complete_with_educational_evidence(
        persistence=persistence,
        user_id=user.id,
        session_id=binding.session_id,
        topic_id=current,
        monkeypatch=monkeypatch,
    )
    assert result["status"] == "completed"
    assert result["twin_updated"] is True

    query = QualifyingStudyDayQueryAdapter(
        index=persistence.qualifying_study_day_index
    )
    stats = query.streak_stats(user_id=user.id, as_of=date.today())
    assert stats.current_streak_days >= 1
    assert date.today() in stats.qualifying_dates


def test_flask_post_rejects_unreached_topic(ctx, app, monkeypatch):
    monkeypatch.setenv("SR_SESSION_PRIMARY", "1")
    subject = publish_subject("SEL7", title="Post Gate")
    user = make_user("sel-post@example.com")
    _enrol_runtime_c(user, subject)
    EducationalExperienceService().load_for_user(user.id)
    _progress, _current, unreached = _progress_topics(user.id, subject)
    assert unreached is not None

    client = app.test_client()
    with client.session_transaction() as sess:
        sess["_user_id"] = str(user.id)
        sess["_fresh"] = True
    response = client.post(
        "/student/study/start",
        data={"topic_id": unreached, "subject_code": subject},
        follow_redirects=True,
    )
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "Available once you reach it in your learning path." in html
    assert "/session/" not in response.request.path


def _session_id_from_location(location: str) -> str:
    parts = [part for part in location.split("/") if part]
    if "session" not in parts:
        raise AssertionError(f"no session path in {location}")
    return parts[parts.index("session") + 1]


def _login(client, user: User) -> None:
    with client.session_transaction() as sess:
        sess["_user_id"] = str(user.id)
        sess["_fresh"] = True


def _app_runtime(app):
    from app.presentation.session.factory import (
        get_session_experience_composition,
        init_session_experience,
    )

    init_session_experience(app)
    composition = get_session_experience_composition()
    assert composition is not None
    persistence = LearningSessionPersistenceAdapter(store=composition.store)
    coordinator = StudentRuntimeCoordinator(
        persistence=persistence,
        session_overview_writer=composition.runtime,
        flags=_flags_on(),
    )
    return coordinator, persistence


def _start_unfinished_mission(coordinator, user: User):
    snap = EducationalExperienceService().load_for_user(user.id)
    assert snap is not None and snap.mission is not None
    binding = coordinator.accept_and_start_session(
        user_id=user.id,
        mission_instance_id=snap.mission.mission_instance_id,
        topic_title=snap.mission.topic_title,
        estimated_minutes=30,
    )
    return binding, snap


def test_resume_keeps_student_selected_orientation_copy(ctx, app, monkeypatch):
    """Unfinished student-selected sitting still shows honest why-copy on resume.

    find_open_session does not copy session_origin onto SessionBindingResult.
    Resume must still render the stored sitting's orientation, not sequential
    Mission copy, via the same Study start / Session overview path a student
    hits after leaving an unfinished sitting.
    """
    monkeypatch.setenv("SR_SESSION_PRIMARY", "1")
    subject = publish_subject("SEL8", title="Resume Origin")
    user = make_user("sel-resume@example.com")
    _enrol_runtime_c(user, subject)
    EducationalExperienceService().load_for_user(user.id)
    _progress, current, _unreached = _progress_topics(user.id, subject)
    assert current

    from app.presentation.session.factory import init_session_experience

    with app.app_context():
        init_session_experience(app)

    client = app.test_client()
    with client.session_transaction() as sess:
        sess["_user_id"] = str(user.id)
        sess["_fresh"] = True

    started = client.post(
        "/student/study/start",
        data={"topic_id": current, "subject_code": subject},
        follow_redirects=False,
    )
    assert started.status_code in (302, 303)
    start_location = started.headers.get("Location", "")
    assert "/session/" in start_location
    session_id = _session_id_from_location(start_location)
    assert session_id.startswith("lsr-")

    client.get("/student/")

    resumed = client.post(
        "/student/study/start",
        data={"topic_id": current, "subject_code": subject},
        follow_redirects=False,
    )
    assert resumed.status_code in (302, 303)
    resume_location = resumed.headers.get("Location", "")
    assert "/session/" in resume_location
    assert _session_id_from_location(resume_location) == session_id

    overview = client.get(
        f"/session/{session_id}/overview",
        follow_redirects=True,
    )
    assert overview.status_code == 200
    html = overview.get_data(as_text=True)
    assert STUDENT_SELECTED_WHY in html
    assert "Today's Mission focuses on" not in html


def test_no_unfinished_session_starts_immediately_without_confirmation(
    ctx, app, monkeypatch
):
    monkeypatch.setenv("SR_SESSION_PRIMARY", "1")
    subject = publish_subject("SEL9", title="Clean Start")
    user = make_user("sel-clean@example.com")
    _enrol_runtime_c(user, subject)
    EducationalExperienceService().load_for_user(user.id)
    _progress, current, _unreached = _progress_topics(user.id, subject)
    assert current

    with app.app_context():
        coordinator, persistence = _app_runtime(app)
        assert coordinator.find_open_session(str(user.id)) is None

    client = app.test_client()
    _login(client, user)
    study_page = client.get("/student/study")
    assert study_page.status_code == 200
    study_html = study_page.get_data(as_text=True)
    assert "You have an unfinished session." not in study_html
    assert "data-study-replace-confirm" not in study_html

    response = client.post(
        "/student/study/start",
        data={"topic_id": current, "subject_code": subject},
        follow_redirects=False,
    )
    assert response.status_code in (302, 303)
    location = response.headers.get("Location", "")
    assert "/session/" in location
    html = response.get_data(as_text=True)
    assert "You have an unfinished session." not in html
    assert "data-study-replace-confirm" not in html

    with app.app_context():
        opened = persistence.find_open(student_id=str(user.id))
        assert opened is not None
        assert opened["session_id"] == _session_id_from_location(location)
        assert opened.get("session_origin") == SESSION_ORIGIN_STUDENT_SELECTED


def test_unfinished_session_requires_confirmation_before_pointer_replaced(
    ctx, app, monkeypatch
):
    monkeypatch.setenv("SR_SESSION_PRIMARY", "1")
    subject = publish_subject("SEL10", title="Confirm Guard")
    user = make_user("sel-confirm@example.com")
    _enrol_runtime_c(user, subject)
    EducationalExperienceService().load_for_user(user.id)
    _progress, current, _unreached = _progress_topics(user.id, subject)
    assert current

    with app.app_context():
        coordinator, persistence = _app_runtime(app)
        mission_binding, _snap = _start_unfinished_mission(coordinator, user)
        with pytest.raises(OpenSessionReplacementRequired) as raised:
            coordinator.start_student_selected_session(
                user_id=user.id,
                topic_id=current,
                subject_code=subject,
            )
        assert raised.value.session_id == mission_binding.session_id
        still = coordinator.find_open_session(str(user.id))
        assert still is not None
        assert still.session_id == mission_binding.session_id

    client = app.test_client()
    _login(client, user)
    response = client.post(
        "/student/study/start",
        data={"topic_id": current, "subject_code": subject},
        follow_redirects=False,
    )
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert 'data-study-replace-confirm="true"' in html
    assert "You have an unfinished session." in html
    assert "replace your current resume point" in html
    assert "It won't be deleted" in html
    assert "you won't be able to resume it from here" in html
    assert "Go back" in html
    assert "Start this session" in html
    assert "lose" not in html.lower()
    assert "abandoned" not in html.lower()
    assert "/session/" not in (response.headers.get("Location") or "")

    with app.app_context():
        still_open = persistence.find_open(student_id=str(user.id))
        assert still_open is not None
        assert still_open["session_id"] == mission_binding.session_id


def test_declining_replace_confirmation_leaves_unfinished_pointer_untouched(
    ctx, app, monkeypatch
):
    monkeypatch.setenv("SR_SESSION_PRIMARY", "1")
    subject = publish_subject("SEL11", title="Decline Guard")
    user = make_user("sel-decline@example.com")
    _enrol_runtime_c(user, subject)
    EducationalExperienceService().load_for_user(user.id)
    _progress, current, _unreached = _progress_topics(user.id, subject)
    assert current

    with app.app_context():
        coordinator, persistence = _app_runtime(app)
        mission_binding, _snap = _start_unfinished_mission(coordinator, user)

    client = app.test_client()
    _login(client, user)
    blocked = client.post(
        "/student/study/start",
        data={"topic_id": current, "subject_code": subject},
        follow_redirects=False,
    )
    assert blocked.status_code == 200
    html = blocked.get_data(as_text=True)
    assert 'data-study-replace-back="true"' in html
    assert 'href="/student/study"' in html or "href=\"/student/study\"" in html

    back = client.get("/student/study")
    assert back.status_code == 200
    back_html = back.get_data(as_text=True)
    assert "data-study-replace-confirm" not in back_html

    with app.app_context():
        still = persistence.find_open(student_id=str(user.id))
        assert still is not None
        assert still["session_id"] == mission_binding.session_id
        assert still.get("session_origin") != SESSION_ORIGIN_STUDENT_SELECTED


def test_confirming_replace_starts_student_selected_with_isolation_intact(
    ctx, app, monkeypatch
):
    monkeypatch.setenv("SR_SESSION_PRIMARY", "1")
    subject = publish_subject("SEL12", title="Confirm Proceed")
    user = make_user("sel-proceed@example.com")
    _enrol_runtime_c(user, subject)
    snap = EducationalExperienceService().load_for_user(user.id)
    assert snap is not None and snap.mission is not None
    today_mid = snap.mission.mission_instance_id
    _progress, current, _unreached = _progress_topics(user.id, subject)
    assert current

    with app.app_context():
        coordinator, persistence = _app_runtime(app)
        mission_binding, _snap = _start_unfinished_mission(coordinator, user)

    client = app.test_client()
    _login(client, user)
    confirmed = client.post(
        "/student/study/start",
        data={
            "topic_id": current,
            "subject_code": subject,
            "confirm_replace": "1",
        },
        follow_redirects=False,
    )
    assert confirmed.status_code in (302, 303)
    location = confirmed.headers.get("Location", "")
    assert "/session/" in location
    new_id = _session_id_from_location(location)
    assert new_id != mission_binding.session_id

    with app.app_context():
        record = persistence.load(session_id=new_id)
        assert record is not None
        assert record.get("session_origin") == SESSION_ORIGIN_STUDENT_SELECTED
        assert not str(record.get("mission_instance_id") or "").strip()
        opened = persistence.find_open(student_id=str(user.id))
        assert opened is not None
        assert opened["session_id"] == new_id
        mission = EducationalRuntimeEngineService().get_mission_instance(
            user_id=user.id,
            mission_instance_id=today_mid,
        )
        assert mission is not None
        assert mission.status != MissionStatus.COMPLETED.value

    overview = client.get(
        f"/session/{new_id}/overview",
        follow_redirects=True,
    )
    assert overview.status_code == 200
    html = overview.get_data(as_text=True)
    assert STUDENT_SELECTED_WHY in html
    assert "Today's Mission focuses on" not in html


def test_student_selected_path_does_not_import_decision_engine():
    path = (
        ROOT
        / "app"
        / "application"
        / "student_runtime"
        / "coordinator.py"
    )
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    imported: list[str] = []
    for node in ast.walk(tree):
        modules: list[str] = []
        if isinstance(node, ast.Import):
            modules = [alias.name for alias in node.names]
        elif isinstance(node, ast.ImportFrom):
            modules = [node.module or ""]
        imported.extend(modules)
    blob = " ".join(imported)
    assert "adaptive_decision" not in blob
    assert "SittingDecisionOrchestrator" not in blob
    origin_path = (
        ROOT / "app" / "application" / "learning_session" / "session_origin.py"
    )
    origin_tree = ast.parse(
        origin_path.read_text(encoding="utf-8"), filename=str(origin_path)
    )
    origin_mods: list[str] = []
    for node in ast.walk(origin_tree):
        if isinstance(node, ast.Import):
            origin_mods.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            origin_mods.append(node.module or "")
    origin_blob = " ".join(origin_mods)
    assert "educational_packages" not in origin_blob
    assert "educational_authoring" not in origin_blob
    assert "curriculum.data" not in origin_blob
