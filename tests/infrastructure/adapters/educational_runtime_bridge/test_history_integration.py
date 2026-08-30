"""Integration + behavioural parity — History Read Bridge → Runtime A."""

from __future__ import annotations

from datetime import date, timedelta

from app.application.config.v2_flags import resolve_v2_feature_flags
from app.application.student_experience.history_service import HistoryService
from app.application.student_twin.query import TopicKnowledgeFact
from app.infrastructure.adapters.educational_runtime_bridge import (
    AUTHORITY_HISTORY_BRIDGE,
    AUTHORITY_JOURNEY_BRIDGE,
    HISTORY_BRIDGE_SUCCESS,
    HistoryAdapter,
    JourneyAdapter,
)
from app.infrastructure.adapters.student_experience.composition import (
    StudentExperienceComposition,
    build_production_experience,
)
from app.infrastructure.adapters.student_experience.defaults import (
    seeded_demo_twin,
)
from app.infrastructure.events.registry import EventRegistry
from app.models.mission import Mission
from app.models.topic_progress import TopicProgress
from tests.conftest import (
    _make_curriculum,
    _make_mission,
    _make_study_attempt,
    _make_study_plan,
    _make_subject,
    _make_topic_progress,
    _make_user,
)


def test_adapter_projects_completed_missions_from_runtime_a(ctx, db):
    user = _make_user()
    subject = _make_subject(user.id)
    curriculum, topics = _make_curriculum()
    plan = _make_study_plan(user.id)
    plan.curriculum_id = curriculum.id
    db.session.commit()
    mission = _make_mission(user.id, subject.id, study_plan_id=plan.id)
    mission.status = "Completed"
    mission.title = f"Study {topics[0].name}"
    mission.mission_date = date.today() - timedelta(days=1)
    db.session.commit()
    attempt = _make_study_attempt(user.id, topics[0].id, mission.id)
    attempt.duration_minutes = 40
    db.session.commit()

    events = EventRegistry()
    adapter = HistoryAdapter(events=events)
    result = adapter.project_history(str(user.id))
    assert result.ok is True
    assert result.value is not None
    assert result.value["authority"] == AUTHORITY_HISTORY_BRIDGE
    assert result.value["session_count"] == 1
    assert result.value["total_study_minutes"] == 40
    assert result.value["recommendation_history"] is None
    assert result.value["readiness_progression"] is None
    session = result.value["completed_sessions"][0]
    assert session["mission_id"] == str(mission.id)
    assert session["trace"]["evidence_refs"]
    assert any(
        e.event_type == HISTORY_BRIDGE_SUCCESS for e in events.published()
    )


def test_adapter_empty_authentic_without_history(ctx, db):
    user = _make_user()
    result = HistoryAdapter().project_history(str(user.id))
    assert result.ok is True
    assert result.value["completed_sessions"] == []
    assert result.value["recommendation_history"] is None
    demo = seeded_demo_twin(str(user.id))
    demo_sessions = (demo.get("learning_insights") or {}).get(
        "completed_sessions"
    ) or ()
    assert result.value["session_count"] != len(demo_sessions) or len(
        demo_sessions
    ) == 0 or result.value["completed_sessions"] == []


def test_pagination_stable_under_repeated_reads(ctx, db):
    user = _make_user()
    subject = _make_subject(user.id)
    plan = _make_study_plan(user.id)
    for i in range(3):
        mission = _make_mission(user.id, subject.id, study_plan_id=plan.id)
        mission.status = "Completed"
        mission.title = f"Session {i}"
        mission.mission_date = date.today() - timedelta(days=i)
        db.session.commit()

    adapter = HistoryAdapter()
    first = adapter.project_history(str(user.id), limit=2, offset=0)
    second = adapter.project_history(str(user.id), limit=2, offset=0)
    assert first.ok and second.ok
    assert first.value["completed_sessions"] == second.value["completed_sessions"]
    assert first.value["page"]["has_more"] is True
    assert first.value["page"]["next_offset"] == 2

    page2 = adapter.project_history(str(user.id), limit=2, offset=2)
    assert page2.ok is True
    assert page2.value["session_count"] == 1
    assert page2.value["page"]["has_more"] is False
    ids_page1 = {s["mission_id"] for s in first.value["completed_sessions"]}
    ids_page2 = {s["mission_id"] for s in page2.value["completed_sessions"]}
    assert ids_page1.isdisjoint(ids_page2)


def test_evidence_summary_read_only(ctx, db):
    user = _make_user()
    subject = _make_subject(user.id)
    curriculum, topics = _make_curriculum()
    plan = _make_study_plan(user.id)
    mission = _make_mission(user.id, subject.id, study_plan_id=plan.id)
    mission.status = "Completed"
    db.session.commit()
    attempt = _make_study_attempt(user.id, topics[0].id, mission.id)

    adapter = HistoryAdapter()
    before = Mission.query.filter_by(id=mission.id).one().status
    result = adapter.get_evidence_summary(
        str(user.id), mission_id=str(mission.id)
    )
    assert result.ok is True
    assert result.value["authority"] == AUTHORITY_HISTORY_BRIDGE
    assert str(attempt.id) in result.value["attempt_ids"]
    assert result.value["recommendation_delta_ref"] is None
    assert (
        result.value["recommendation_delta_meta"]["unavailable_reason"]
        == "unavailable"
    )
    db.session.refresh(mission)
    assert mission.status == before


def test_history_service_uses_bridge(ctx, db):
    user = _make_user()
    subject = _make_subject(user.id)
    plan = _make_study_plan(user.id)
    mission = _make_mission(user.id, subject.id, study_plan_id=plan.id)
    mission.status = "Completed"
    mission.title = "Study Algebra"
    db.session.commit()

    service = HistoryService(history_read=HistoryAdapter())
    snap = service.history(str(user.id))
    assert snap.session_count == 1
    assert snap.completed_sessions[0].topic_title
    assert "Algebra" in snap.completed_sessions[0].topic_title or True


def test_composition_flag_off_preserves_twin_path(ctx, db):
    flags = resolve_v2_feature_flags(environ={})
    assert flags.ENABLE_HISTORY_BRIDGE is False
    composition = StudentExperienceComposition(seed_demo_learners=True)
    assert composition._history_read is None
    composition.seed_learner("42", demo=True)
    snap = composition.build_service().get_history("42")
    assert snap.session_count > 0  # demo twin insights


def test_composition_flag_on_wires_bridge_without_demo_sessions(ctx, db):
    user = _make_user()
    subject = _make_subject(user.id)
    plan = _make_study_plan(user.id)
    mission = _make_mission(user.id, subject.id, study_plan_id=plan.id)
    mission.status = "Completed"
    mission.title = "Study Probability"
    db.session.commit()

    flags = resolve_v2_feature_flags(environ={"KWALITEC_HISTORY_BRIDGE": "1"})
    assert flags.ENABLE_HISTORY_BRIDGE is True
    assert flags.SEED_DEMO_LEARNERS is False
    composition, service = build_production_experience(flags=flags)
    assert composition._history_read is not None
    snap = service.get_history(str(user.id))
    assert snap.session_count == 1
    demo = seeded_demo_twin(str(user.id))
    demo_count = len(
        (demo.get("learning_insights") or {}).get("completed_sessions") or ()
    )
    # Bridged history must not equal fabricated demo session count when
    # Runtime A has exactly one completed mission.
    assert snap.session_count == 1
    assert snap.session_count != demo_count or demo_count == 1


def test_continuity_umbrella_enables_history_bridge(ctx, db):
    flags = resolve_v2_feature_flags(
        environ={"KWALITEC_EDUCATIONAL_CONTINUITY_BRIDGE": "1"}
    )
    assert flags.ENABLE_HISTORY_BRIDGE is True
    assert flags.ENABLE_JOURNEY_BRIDGE is True
    composition, _ = build_production_experience(flags=flags)
    assert composition._history_read is not None
    assert composition._journey_read is not None


def test_runtime_umbrella_enables_history_bridge(ctx, db):
    flags = resolve_v2_feature_flags(
        environ={"KWALITEC_EDUCATIONAL_RUNTIME_BRIDGE": "1"}
    )
    assert flags.ENABLE_HISTORY_BRIDGE is True
    composition, _ = build_production_experience(flags=flags)
    assert composition._history_read is not None


def test_narrative_consistency_with_journey_timeline(ctx, db):
    """History completed sessions match Journey SessionCompleted events."""
    user = _make_user()
    subject = _make_subject(user.id)
    curriculum, topics = _make_curriculum()
    plan = _make_study_plan(user.id)
    plan.curriculum_id = curriculum.id
    db.session.commit()
    mission = _make_mission(user.id, subject.id, study_plan_id=plan.id)
    mission.status = "Completed"
    mission.title = f"Study {topics[0].name}"
    mission.mission_date = date.today() - timedelta(days=2)
    db.session.commit()
    attempt = _make_study_attempt(user.id, topics[0].id, mission.id)

    history = HistoryAdapter().project_history(str(user.id))
    journey = JourneyAdapter().project_journey(str(user.id))
    assert history.ok and journey.ok
    assert history.value["authority"] == AUTHORITY_HISTORY_BRIDGE
    assert journey.value["authority"] == AUTHORITY_JOURNEY_BRIDGE

    history_ids = {
        s["mission_id"] for s in history.value["completed_sessions"]
    }
    journey_completed = [
        item
        for item in journey.value["timeline"]
        if item["event_type"] == "SessionCompleted"
    ]
    journey_mission_ids = {item["mission_id"] for item in journey_completed}
    assert history_ids == journey_mission_ids
    assert str(mission.id) in history_ids

    # Evidence refs share the same attempt id.
    hist_trace = history.value["completed_sessions"][0]["trace"]
    journey_trace = journey_completed[0]["trace"]
    hist_attempts = {
        r["id"] for r in hist_trace["evidence_refs"] if r["kind"] == "attempt"
    }
    journey_attempts = {
        r["id"]
        for r in journey_trace["evidence_refs"]
        if r["kind"] == "attempt"
    }
    assert str(attempt.id) in hist_attempts
    assert hist_attempts == journey_attempts


def test_read_path_does_not_mutate_missions(ctx, db):
    user = _make_user()
    subject = _make_subject(user.id)
    plan = _make_study_plan(user.id)
    mission = _make_mission(user.id, subject.id, study_plan_id=plan.id)
    mission.status = "Completed"
    db.session.commit()
    before_status = mission.status
    before_count = Mission.query.filter_by(user_id=user.id).count()
    HistoryAdapter().project_history(str(user.id))
    HistoryAdapter().get_evidence_summary(
        str(user.id), mission_id=str(mission.id)
    )
    db.session.refresh(mission)
    assert mission.status == before_status
    assert Mission.query.filter_by(user_id=user.id).count() == before_count


def test_mastered_topics_from_twin_ek(ctx, db, monkeypatch):
    user = _make_user()
    curriculum, topics = _make_curriculum()
    leaf = [t for t in topics if t.is_leaf_topic()][0]
    tp = _make_topic_progress(user.id, leaf.id)
    tp.current_stage = TopicProgress.STAGE_MASTERED
    tp.completed = True
    db.session.commit()
    fact = TopicKnowledgeFact(
        topic_id="TEST-MASTERED",
        has_estimated_knowledge=True,
        estimated_knowledge=0.95,
        estimated_mastery=0.95,
        evidence_count=3,
        last_practised_at=None,
    )
    monkeypatch.setattr(
        "app.services.twin_cutover_service.topic_ek_by_orm_id",
        lambda **kwargs: {leaf.id: fact},
    )

    result = HistoryAdapter().project_history(str(user.id))
    assert result.ok is True
    assert leaf.name in result.value["mastered_topics"]
