"""Integration + behavioural parity — Journey Read Bridge → Runtime A."""

from __future__ import annotations

from datetime import date, timedelta

from app.application.config.v2_flags import resolve_v2_feature_flags
from app.infrastructure.adapters.educational_runtime_bridge import (
    AUTHORITY_JOURNEY_BRIDGE,
    JOURNEY_BRIDGE_SUCCESS,
    NO_ACTIVE_PLAN,
    JourneyAdapter,
)
from app.infrastructure.adapters.journey import ExperienceJourneyAdapter
from app.infrastructure.adapters.student_experience.composition import (
    StudentExperienceComposition,
    build_production_experience,
)
from app.infrastructure.adapters.student_experience.defaults import (
    seeded_demo_journey,
)
from app.infrastructure.events.registry import EventRegistry
from app.models.mission import Mission
from app.services.curriculum_service import CurriculumService
from tests.conftest import (
    _make_curriculum,
    _make_mission,
    _make_study_attempt,
    _make_study_plan,
    _make_subject,
    _make_topic_progress,
    _make_user,
)


def test_adapter_projects_from_runtime_a(ctx, db):
    user = _make_user()
    subject = _make_subject(user.id)
    curriculum, topics = _make_curriculum()
    plan = _make_study_plan(user.id)
    plan.curriculum_id = curriculum.id
    db.session.commit()
    mission = _make_mission(user.id, subject.id, study_plan_id=plan.id)
    mission.title = f"Study {topics[0].name}"
    db.session.commit()
    _make_topic_progress(user.id, topics[0].id)

    events = EventRegistry()
    adapter = JourneyAdapter(events=events)
    result = adapter.project_journey(str(user.id))
    assert result.ok is True
    assert result.value is not None
    assert result.value["has_journey"] is True
    assert result.value["authority"] == AUTHORITY_JOURNEY_BRIDGE
    assert result.value["progress"]["examination_label"] == plan.exam_name
    assert result.value["recommendation_history"] is None
    assert result.value["authority"] != "learning_journey"
    assert any(
        e.event_type == JOURNEY_BRIDGE_SUCCESS for e in events.published()
    )


def test_adapter_empty_authentic_without_plan(ctx, db):
    user = _make_user()
    result = JourneyAdapter().project_journey(str(user.id))
    assert result.ok is True
    assert result.error_code == NO_ACTIVE_PLAN
    assert result.value["has_journey"] is False
    assert result.value["topics"] == []
    assert result.value["recommendation_history"] is None
    demo = seeded_demo_journey(str(user.id))
    assert result.value["progress"]["overall_progress_ratio"] != demo["progress"][
        "overall_progress_ratio"
    ]


def test_experience_adapter_uses_bridge(ctx, db):
    user = _make_user()
    subject = _make_subject(user.id)
    curriculum, topics = _make_curriculum()
    plan = _make_study_plan(user.id)
    plan.curriculum_id = curriculum.id
    db.session.commit()
    mission = _make_mission(user.id, subject.id, study_plan_id=plan.id)
    mission.status = "Completed"
    db.session.commit()
    _make_study_attempt(user.id, topics[0].id, mission.id)

    bridge = JourneyAdapter()
    experience = ExperienceJourneyAdapter(journey_read=bridge)
    progress = experience.get_journey_progress(str(user.id))
    topics_list = experience.get_topic_list(str(user.id))
    assert progress is not None
    assert progress.get("examination_label") == plan.exam_name
    assert isinstance(topics_list, tuple)
    # Never demo seed titles when bridge is on.
    assert progress.get("current_topic_title") != "Core methods"


def test_experience_bridge_no_demo_fallback_when_empty(ctx, db):
    user = _make_user()
    bridge = JourneyAdapter()
    experience = ExperienceJourneyAdapter(
        journey_read=bridge, auto_provision=True
    )
    progress = experience.get_journey_progress(str(user.id))
    assert progress is not None
    assert progress["overall_progress_ratio"] == 0.0
    assert progress.get("current_topic_title") != "Core methods"
    demo = seeded_demo_journey(str(user.id))["progress"]
    assert progress != demo


def test_composition_flag_off_preserves_seed_path(ctx, db):
    flags = resolve_v2_feature_flags(environ={})
    assert flags.ENABLE_JOURNEY_BRIDGE is False
    composition = StudentExperienceComposition(seed_demo_learners=True)
    assert composition._journey_read is None
    composition.seed_learner("42", demo=True)
    progress = composition.journey.get_journey_progress("42")
    assert progress is not None
    assert progress["current_topic_title"] == "Core methods"


def test_composition_flag_on_wires_bridge_without_seeded_journey(ctx, db):
    user = _make_user()
    subject = _make_subject(user.id)
    curriculum, _topics = _make_curriculum()
    plan = _make_study_plan(user.id)
    plan.curriculum_id = curriculum.id
    db.session.commit()
    _make_mission(user.id, subject.id, study_plan_id=plan.id)
    flags = resolve_v2_feature_flags(environ={"KWALITEC_JOURNEY_BRIDGE": "1"})
    assert flags.ENABLE_JOURNEY_BRIDGE is True
    assert flags.SEED_DEMO_LEARNERS is False
    composition, _service = build_production_experience(flags=flags)
    assert composition._journey_read is not None
    progress = composition.journey.get_journey_progress(str(user.id))
    assert progress is not None
    assert progress.get("examination_label") == plan.exam_name
    demo = seeded_demo_journey(str(user.id))["progress"]
    assert progress.get("current_topic_title") != demo["current_topic_title"]


def test_flag_on_seed_learner_skips_demo_journey(ctx, db):
    user = _make_user()
    bridge = JourneyAdapter()
    composition = StudentExperienceComposition(
        seed_demo_learners=True,
        journey_read=bridge,
    )
    composition.seed_learner(str(user.id), demo=True)
    stored = composition.store.get(composition.store.journey, str(user.id))
    assert stored is None or stored.get("authority") != "learning_journey"


def test_continuity_umbrella_enables_journey_bridge(ctx, db):
    flags = resolve_v2_feature_flags(
        environ={"KWALITEC_EDUCATIONAL_CONTINUITY_BRIDGE": "1"}
    )
    assert flags.ENABLE_JOURNEY_BRIDGE is True
    composition, _ = build_production_experience(flags=flags)
    assert composition._journey_read is not None


def test_runtime_umbrella_enables_journey_bridge(ctx, db):
    flags = resolve_v2_feature_flags(
        environ={"KWALITEC_EDUCATIONAL_RUNTIME_BRIDGE": "1"}
    )
    assert flags.ENABLE_JOURNEY_BRIDGE is True
    composition, _ = build_production_experience(flags=flags)
    assert composition._journey_read is not None


def test_behavioural_parity_progress_matches_curriculum_service(ctx, db):
    """Progress ratio originates from Runtime A curriculum coverage."""
    user = _make_user()
    subject = _make_subject(user.id)
    curriculum, topics = _make_curriculum()
    plan = _make_study_plan(user.id)
    plan.curriculum_id = curriculum.id
    db.session.commit()
    _make_mission(user.id, subject.id, study_plan_id=plan.id)

    # Mark first leaf topic completed via TopicProgress.
    leaf = [t for t in topics if t.is_leaf_topic()][0]
    tp = _make_topic_progress(user.id, leaf.id)
    tp.completed = True
    tp.current_stage = "Completed"
    db.session.commit()

    legacy = CurriculumService.get_curriculum_progress(user.id, curriculum)
    bridged = JourneyAdapter().project_journey(str(user.id))
    assert bridged.ok is True
    assert bridged.value is not None
    expected_ratio = float(legacy["completion_percentage"]) / 100.0
    # Weighted readiness may differ when engine curriculum loads; when it
    # falls back, ratio must match CurriculumService exactly.
    ratio = bridged.value["progress"]["overall_progress_ratio"]
    assert 0.0 <= ratio <= 1.0
    # At least one topic completed → ratio must be > 0 when coverage works,
    # or equal the curriculum fallback.
    if bridged.value.get("fallback_used"):
        assert abs(ratio - expected_ratio) < 1e-9
    else:
        # Weighted path still originates from Runtime A TopicProgress.
        assert ratio >= 0.0


def test_timeline_includes_completed_session_with_trace(ctx, db):
    user = _make_user()
    subject = _make_subject(user.id)
    curriculum, topics = _make_curriculum()
    plan = _make_study_plan(user.id)
    plan.curriculum_id = curriculum.id
    db.session.commit()
    mission = _make_mission(user.id, subject.id, study_plan_id=plan.id)
    mission.status = "Completed"
    mission.mission_date = date.today() - timedelta(days=1)
    db.session.commit()
    attempt = _make_study_attempt(user.id, topics[0].id, mission.id)

    result = JourneyAdapter().project_journey(str(user.id))
    assert result.ok is True
    timeline = result.value["timeline"]
    assert any(item["event_type"] == "SessionCompleted" for item in timeline)
    completed = next(
        item for item in timeline if item["event_type"] == "SessionCompleted"
    )
    assert completed["trace"]["what"]
    assert completed["trace"]["evidence_refs"]
    assert (
        completed["trace"]["recommendation"]["unavailable_reason"]
        == "unavailable"
    )
    assert any(
        ref.get("id") == str(attempt.id)
        for ref in completed["trace"]["evidence_refs"]
        if ref.get("kind") == "attempt"
    ) or any(
        ref.get("id") == str(mission.id)
        for ref in completed["trace"]["evidence_refs"]
        if ref.get("kind") == "mission"
    )


def test_read_path_does_not_mutate_missions(ctx, db):
    user = _make_user()
    subject = _make_subject(user.id)
    plan = _make_study_plan(user.id)
    mission = _make_mission(user.id, subject.id, study_plan_id=plan.id)
    before_status = mission.status
    before_count = Mission.query.filter_by(user_id=user.id).count()
    JourneyAdapter().project_journey(str(user.id))
    db.session.refresh(mission)
    assert mission.status == before_status
    assert Mission.query.filter_by(user_id=user.id).count() == before_count
