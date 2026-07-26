"""Integration tests — Experience → Session Completion → Runtime A → SQL."""

from __future__ import annotations

import pytest

from app.application.config.v2_flags import resolve_v2_feature_flags
from app.application.student_experience.exceptions import StudentExperienceError
from app.infrastructure.adapters.educational_runtime_bridge import (
    AUTHORITY_STUDY_SESSION_SERVICE,
    EVIDENCE_REJECTED,
    INVALID_STATE,
    SESSION_COMPLETION_BRIDGE_SUCCESS,
    SessionCompletionAdapter,
)
from app.infrastructure.adapters.mission.experience_adapter import (
    ExperienceMissionAdapter,
)
from app.infrastructure.adapters.student_experience.composition import (
    StudentExperienceComposition,
    build_production_experience,
)
from app.infrastructure.adapters.student_experience.defaults import (
    seeded_demo_mission,
)
from app.infrastructure.events.registry import EventRegistry
from app.models.learning import StudyAttempt
from app.models.mission import Mission
from app.services.study_session_service import StudySessionService
from tests.conftest import _make_mission, _make_study_plan, _make_subject, _make_user


@pytest.fixture
def learner(ctx, db):
    user = _make_user()
    subject = _make_subject(user.id)
    plan = _make_study_plan(user.id)
    mission = _make_mission(user.id, subject.id, study_plan_id=plan.id)
    return user, subject, plan, mission


def test_adapter_completes_sql_in_progress_mission(learner):
    user, _subject, _plan, mission = learner
    StudySessionService.start_session(mission.id, user.id)
    events = EventRegistry()
    adapter = SessionCompletionAdapter(events=events)
    result = adapter.complete_session(str(user.id), session_id=str(mission.id))
    assert result.ok is True
    assert result.value is not None
    assert result.value["mission_id"] == str(mission.id)
    assert result.value["session_id"] == str(mission.id)
    assert result.value["topic_title"] == mission.title
    assert result.value["status"] == "completed"
    assert result.value["educational_complete"] is True
    assert result.value["authority"] == AUTHORITY_STUDY_SESSION_SERVICE
    refreshed = Mission.query.get(mission.id)
    assert refreshed is not None
    assert refreshed.status == "Completed"
    assert refreshed.id == mission.id
    assert any(
        e.event_type == SESSION_COMPLETION_BRIDGE_SUCCESS
        for e in events.published()
    )


def test_adapter_practice_outcome_evidence_before_completion(learner):
    user, _subject, _plan, mission = learner
    StudySessionService.start_session(mission.id, user.id)
    result = SessionCompletionAdapter().complete_session(
        str(user.id),
        session_id=str(mission.id),
        outcome={
            "questions_attempted": 10,
            "questions_correct": 7,
            "duration_minutes": 20,
        },
    )
    assert result.ok is True
    assert result.value["evidence_accepted"] is True
    assert result.value["educational_complete"] is True
    refreshed = Mission.query.get(mission.id)
    assert refreshed.status == "Completed"
    attempt = (
        StudyAttempt.query.filter_by(user_id=user.id, mission_id=mission.id)
        .order_by(StudyAttempt.id.desc())
        .first()
    )
    assert attempt is not None
    assert attempt.questions_attempted == 10
    assert attempt.questions_correct == 7


def test_adapter_does_not_complete_pending(learner):
    user, _subject, _plan, mission = learner
    assert mission.status == "Pending"
    result = SessionCompletionAdapter().complete_session(
        str(user.id), session_id=str(mission.id)
    )
    assert result.ok is False
    assert result.error_code == INVALID_STATE
    assert Mission.query.get(mission.id).status == "Pending"


def test_evidence_failure_leaves_session_in_progress(learner):
    """Failed evidence commits must leave the SQL session active."""
    user, _subject, _plan, mission = learner
    StudySessionService.start_session(mission.id, user.id)

    class _FailingLearning:
        @staticmethod
        def create_study_attempt(**kwargs):
            raise RuntimeError("evidence commit failed")

    adapter = SessionCompletionAdapter(learning_service=_FailingLearning)
    result = adapter.complete_session(
        str(user.id),
        session_id=str(mission.id),
        outcome={"questions_attempted": 4, "questions_correct": 3},
    )
    assert result.ok is False
    assert result.error_code == EVIDENCE_REJECTED
    refreshed = Mission.query.get(mission.id)
    assert refreshed is not None
    assert refreshed.status == "In Progress"
    assert (
        StudyAttempt.query.filter_by(user_id=user.id, mission_id=mission.id).count()
        == 0
    )


def test_invalid_practice_leaves_session_in_progress(learner):
    user, _subject, _plan, mission = learner
    StudySessionService.start_session(mission.id, user.id)
    result = SessionCompletionAdapter().complete_session(
        str(user.id),
        session_id=str(mission.id),
        outcome={"questions_attempted": 2, "questions_correct": 9},
    )
    assert result.ok is False
    assert result.error_code == INVALID_STATE
    assert Mission.query.get(mission.id).status == "In Progress"


def test_experience_adapter_uses_completion_bridge(learner):
    user, _subject, _plan, mission = learner
    StudySessionService.start_session(mission.id, user.id)
    experience = ExperienceMissionAdapter(
        session_completion=SessionCompletionAdapter()
    )
    completed = experience.complete_session(
        str(user.id), session_id=str(mission.id)
    )
    assert completed["mission_id"] == str(mission.id)
    assert completed["authority"] == AUTHORITY_STUDY_SESSION_SERVICE
    assert completed["status"] == "completed"
    assert completed["topic_title"] != "Core methods"
    assert Mission.query.get(mission.id).status == "Completed"


def test_experience_bridge_no_demo_fallback_on_failure(ctx, db):
    user = _make_user()
    experience = ExperienceMissionAdapter(
        session_completion=SessionCompletionAdapter(), auto_provision=True
    )
    with pytest.raises(StudentExperienceError) as exc:
        experience.complete_session(str(user.id), session_id="999999")
    assert "NOT_FOUND" in str(exc.value) or "FORBIDDEN" in str(exc.value)
    demo = seeded_demo_mission(str(user.id))
    assert demo["todays_session"]["mission_id"] == "m1"


def test_composition_flag_off_preserves_opaque_complete(ctx, db):
    flags = resolve_v2_feature_flags(environ={})
    assert flags.ENABLE_SESSION_COMPLETION_BRIDGE is False
    composition = StudentExperienceComposition(seed_demo_learners=True)
    assert composition._session_completion is None
    composition.seed_learner("42", demo=True)
    started = composition.mission.start_session("42")
    completed = composition.mission.complete_session(
        "42", session_id=str(started["session_id"])
    )
    assert completed.get("completed_at")
    assert completed.get("session_id") == started["session_id"]
    # Opaque path does not touch SQL Mission rows for learner "42".
    assert Mission.query.filter_by(user_id=42).count() == 0


def test_composition_flag_on_wires_completion_bridge(learner):
    user, _subject, _plan, mission = learner
    StudySessionService.start_session(mission.id, user.id)
    flags = resolve_v2_feature_flags(
        environ={"KWALITEC_SESSION_COMPLETION_BRIDGE": "1"}
    )
    assert flags.ENABLE_SESSION_COMPLETION_BRIDGE is True
    assert flags.SEED_DEMO_LEARNERS is False
    composition, _service = build_production_experience(flags=flags)
    assert composition._session_completion is not None
    completed = composition.mission.complete_session(
        str(user.id), session_id=str(mission.id)
    )
    assert completed["mission_id"] == str(mission.id)
    assert completed["authority"] == AUTHORITY_STUDY_SESSION_SERVICE
    assert Mission.query.get(mission.id).status == "Completed"
    demo = seeded_demo_mission(str(user.id))
    assert completed["mission_id"] != demo["todays_session"]["mission_id"]


def test_umbrella_flag_enables_completion_bridge(learner):
    user, _subject, _plan, mission = learner
    StudySessionService.start_session(mission.id, user.id)
    flags = resolve_v2_feature_flags(
        environ={"KWALITEC_EDUCATIONAL_RUNTIME_BRIDGE": "1"}
    )
    assert flags.ENABLE_SESSION_COMPLETION_BRIDGE is True
    composition, _ = build_production_experience(flags=flags)
    assert composition._session_completion is not None
    completed = composition.mission.complete_session(
        str(user.id), session_id=str(mission.id)
    )
    assert completed["mission_id"] == str(mission.id)
    assert Mission.query.get(mission.id).status == "Completed"


def test_start_with_completion_bridge_does_not_auto_complete(learner):
    """Learning loop must not complete SQL mission immediately after start."""
    user, _subject, _plan, mission = learner
    flags = resolve_v2_feature_flags(
        environ={
            "KWALITEC_MISSION_START_BRIDGE": "1",
            "KWALITEC_SESSION_COMPLETION_BRIDGE": "1",
        }
    )
    composition, _ = build_production_experience(flags=flags)
    started = composition.mission.start_session(
        str(user.id), mission_id=str(mission.id)
    )
    assert started["mission_id"] == str(mission.id)
    refreshed = Mission.query.get(mission.id)
    assert refreshed is not None
    assert refreshed.status == "In Progress"


def test_behavioural_parity_with_legacy_finish(learner):
    """Bridged completion preserves identities vs StudySessionService.finish."""
    user, _subject, _plan, mission = learner
    StudySessionService.start_session(mission.id, user.id)

    # Legacy path on a clone mission for parity of status transition.
    legacy_mission = _make_mission(
        user.id, mission.subject_id, study_plan_id=mission.study_plan_id
    )
    StudySessionService.start_session(legacy_mission.id, user.id)
    legacy = StudySessionService.finish_session(
        mission_id=legacy_mission.id,
        user_id=user.id,
        completion_status="yes",
        notes="No practice questions recorded today.",
    )
    assert legacy.mission.status == "Completed"
    assert legacy.mission_completed is True

    bridged = SessionCompletionAdapter().complete_session(
        str(user.id), session_id=str(mission.id)
    )
    assert bridged.ok is True
    assert bridged.value is not None
    assert bridged.value["mission_id"] == str(mission.id)
    assert bridged.value["topic_title"] == mission.title
    sql = Mission.query.get(mission.id)
    assert sql is not None
    assert sql.status == legacy.mission.status
    assert sql.user_id == user.id
    assert sql.title == mission.title
