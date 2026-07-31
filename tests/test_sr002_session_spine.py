"""SR-002 — Student Runtime Session Spine Binding (SR-001A Phase P1).

Unit / integration / regression / acceptance coverage for:
Home Primary → Start/Resume Study Session → LearningSessionRuntime → /session/*
Mission Accepted ≡ session start; Deferred preserved; flag rollback.
"""

from __future__ import annotations

from datetime import date, timedelta
from unittest.mock import patch

import pytest

from app.application.config.v2_flags import resolve_v2_feature_flags
from app.application.educational_experience import EducationalExperienceService
from app.application.educational_runtime_engine.service import (
    EducationalRuntimeEngineService,
)
from app.application.platform_integration.discovery import PUBLISHED_CATEGORY_CODE
from app.application.platform_integration.enrolment_bridge import (
    FounderStudentEnrolmentBridge,
)
from app.application.student_runtime import (
    SessionSpineUnavailable,
    StudentRuntimeCoordinator,
)
from app.domain.educational_runtime_engine.events import EducationalEventType
from app.domain.educational_runtime_engine.state import MissionStatus
from app.infrastructure.adapters.learning_session.persistence import (
    LearningSessionPersistenceAdapter,
)
from app.infrastructure.session.store import SessionDocumentStore
from app.models.user import User
from app.presentation.student.educational_view_models import (
    page_from_educational_experience,
)
from app.presentation.student.services.student_home_service import StudentHomeService
from tests.application.platform_integration.helpers import (
    bridge_flags,
    make_user,
    publish_subject,
)


def _flags_on(**extra: str):
    env = {"SR_SESSION_PRIMARY": "1", **extra}
    return resolve_v2_feature_flags(environ=env)


def _flags_off(**extra: str):
    env = {"SR_SESSION_PRIMARY": "0", **extra}
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


def _login(client, user: User) -> None:
    with client.session_transaction() as sess:
        sess["_user_id"] = str(user.id)
        sess["_fresh"] = True


def _coordinator(store: SessionDocumentStore | None = None, **kwargs):
    persistence = LearningSessionPersistenceAdapter(
        store=store or SessionDocumentStore()
    )
    return StudentRuntimeCoordinator(
        persistence=persistence,
        flags=_flags_on(),
        **kwargs,
    ), persistence


# ---------------------------------------------------------------------------
# Unit
# ---------------------------------------------------------------------------


class TestFeatureFlagMatrix:
    def test_session_primary_defaults_off(self):
        flags = resolve_v2_feature_flags(environ={})
        assert flags.SR_SESSION_PRIMARY is False
        assert flags.SR_PILOT_MARK_COMPLETE is False

    def test_session_primary_env_on(self):
        flags = resolve_v2_feature_flags(environ={"SR_SESSION_PRIMARY": "1"})
        assert flags.SR_SESSION_PRIMARY is True

    def test_pilot_mark_complete_independent(self):
        flags = resolve_v2_feature_flags(
            environ={"SR_SESSION_PRIMARY": "1", "SR_PILOT_MARK_COMPLETE": "true"}
        )
        assert flags.SR_SESSION_PRIMARY is True
        assert flags.SR_PILOT_MARK_COMPLETE is True


class TestMissionAcceptSemantics:
    def test_accept_mission_creates_lsr_session(self, ctx):
        subject = publish_subject("SR2U1", title="Spine Unit")
        user = make_user("sr002-unit-accept@example.com")
        _enrol_runtime_c(user, subject)
        snap = EducationalExperienceService().load_for_user(user.id)
        assert snap is not None and snap.mission is not None

        store = SessionDocumentStore()
        coordinator, persistence = _coordinator(store)
        binding = coordinator.accept_and_start_session(
            user_id=user.id,
            mission_instance_id=snap.mission.mission_instance_id,
            topic_title=snap.mission.topic_title,
            estimated_minutes=30,
        )
        assert binding.session_id.startswith("lsr-")
        assert binding.resumed is False
        assert binding.phase == "active"
        assert binding.authority == "learning_session_runtime"

        mission = EducationalRuntimeEngineService().get_mission_instance(
            user_id=user.id,
            mission_instance_id=snap.mission.mission_instance_id,
        )
        assert mission is not None
        assert mission.status == MissionStatus.ACCEPTED.value

        handle = persistence.load_handle(session_id=binding.session_id)
        assert handle is not None
        assert handle.phase.value == "active"

    def test_accept_is_idempotent_resume(self, ctx):
        subject = publish_subject("SR2U2", title="Spine Resume")
        user = make_user("sr002-unit-resume@example.com")
        _enrol_runtime_c(user, subject)
        snap = EducationalExperienceService().load_for_user(user.id)
        mid = snap.mission.mission_instance_id

        coordinator, _ = _coordinator()
        first = coordinator.accept_and_start_session(
            user_id=user.id, mission_instance_id=mid, topic_title="T"
        )
        second = coordinator.accept_and_start_session(
            user_id=user.id, mission_instance_id=mid, topic_title="T"
        )
        assert first.session_id == second.session_id
        assert second.resumed is True

    def test_flag_off_blocks_spine(self, ctx):
        subject = publish_subject("SR2U3", title="Spine Blocked")
        user = make_user("sr002-unit-flagoff@example.com")
        _enrol_runtime_c(user, subject)
        snap = EducationalExperienceService().load_for_user(user.id)
        coordinator = StudentRuntimeCoordinator(
            persistence=LearningSessionPersistenceAdapter(),
            flags=_flags_off(),
        )
        with pytest.raises(SessionSpineUnavailable):
            coordinator.accept_and_start_session(
                user_id=user.id,
                mission_instance_id=snap.mission.mission_instance_id,
            )

    def test_defer_mission_preserves_ile004(self, ctx):
        subject = publish_subject("SR2U4", title="Spine Defer")
        user = make_user("sr002-unit-defer@example.com")
        _enrol_runtime_c(user, subject)
        snap = EducationalExperienceService().load_for_user(user.id)
        mid = snap.mission.mission_instance_id

        coordinator, _ = _coordinator()
        coordinator.defer_mission(
            user_id=user.id, mission_instance_id=mid, reason_code="not_today"
        )
        mission = EducationalRuntimeEngineService().get_mission_instance(
            user_id=user.id, mission_instance_id=mid
        )
        assert mission is not None
        assert mission.status == MissionStatus.DEFERRED.value

        # Deferred student can still accept later.
        binding = coordinator.accept_and_start_session(
            user_id=user.id, mission_instance_id=mid, topic_title="T"
        )
        assert binding.session_id
        mission = EducationalRuntimeEngineService().get_mission_instance(
            user_id=user.id, mission_instance_id=mid
        )
        assert mission.status == MissionStatus.ACCEPTED.value

    def test_accept_does_not_emit_topic_completed(self, ctx):
        subject = publish_subject("SR2U5", title="No Topic Advance")
        user = make_user("sr002-unit-no-topic@example.com")
        _enrol_runtime_c(user, subject)
        snap = EducationalExperienceService().load_for_user(user.id)
        before = EducationalRuntimeEngineService().get_journey(
            user_id=user.id, subject_code=subject
        )
        before_coverage = before.progress.coverage_ratio if before else 0.0

        coordinator, _ = _coordinator()
        coordinator.accept_and_start_session(
            user_id=user.id,
            mission_instance_id=snap.mission.mission_instance_id,
            topic_title="T",
        )
        after = EducationalRuntimeEngineService().get_journey(
            user_id=user.id, subject_code=subject
        )
        assert after is not None
        assert after.progress.coverage_ratio == before_coverage


# ---------------------------------------------------------------------------
# Integration
# ---------------------------------------------------------------------------


class TestHomeToSessionIntegration:
    def test_home_primary_start_study_session_when_flag_on(self, ctx, app):
        subject = publish_subject("SR2I1", title="Home Start")
        user = make_user("sr002-int-home@example.com")
        _enrol_runtime_c(user, subject)
        snap = EducationalExperienceService().load_for_user(user.id)
        assert snap is not None

        with patch(
            "app.application.config.v2_flags.resolve_v2_feature_flags",
            return_value=_flags_on(),
        ):
            page = page_from_educational_experience(snap, surface="home")
        assert page.home is not None
        assert page.home.can_start_session is True
        assert page.home.session_control == "start"
        assert page.home.session_control != "complete_runtime_c"
        assert "Start Today's Session" in page.home.primary_cta_label

        with app.test_request_context("/student/"):
            home_page = StudentHomeService().build_home(page)
        assert home_page.mission is not None
        assert home_page.mission.primary_kind == "start_form"
        assert "Start Today's Session" in home_page.mission.primary_label

    def test_coordinator_provisions_session_overview(self, ctx):
        from app.infrastructure.session.runtime_adapter import SessionRuntimeAdapter

        subject = publish_subject("SR2I2", title="Overview Bind")
        user = make_user("sr002-int-overview@example.com")
        _enrol_runtime_c(user, subject)
        snap = EducationalExperienceService().load_for_user(user.id)

        store = SessionDocumentStore()
        runtime_adapter = SessionRuntimeAdapter(store=store, auto_provision=False)
        coordinator = StudentRuntimeCoordinator(
            persistence=LearningSessionPersistenceAdapter(store=store),
            session_overview_writer=runtime_adapter,
            flags=_flags_on(),
        )
        binding = coordinator.accept_and_start_session(
            user_id=user.id,
            mission_instance_id=snap.mission.mission_instance_id,
            topic_title=snap.mission.topic_title or "Topic",
            estimated_minutes=25,
        )
        overview = runtime_adapter.get_session_overview(
            str(user.id), session_id=binding.session_id
        )
        assert overview is not None
        assert overview["session_id"] == binding.session_id
        assert overview["authority"] == "learning_session_runtime"
        assert overview.get("mission_id") == snap.mission.mission_instance_id

    def test_http_start_lands_on_session(self, ctx, client, app):
        subject = publish_subject("SR2I3", title="HTTP Start")
        user = make_user("sr002-int-http@example.com")
        _enrol_runtime_c(user, subject)
        snap = EducationalExperienceService().load_for_user(user.id)
        mid = snap.mission.mission_instance_id
        _login(client, user)

        with patch(
            "app.application.config.v2_flags.resolve_v2_feature_flags",
            return_value=_flags_on(),
        ):
            from app.presentation.session.factory import init_session_experience

            with app.app_context():
                init_session_experience(app)

            home = client.get("/student/")
            assert home.status_code == 200
            body = home.get_data(as_text=True)
            assert (
                "Start Today's Session" in body
                or "Start Today&#39;s Session" in body
                or "Start Study Session" in body
                or 'data-session-control="start"' in body
            )
            assert 'data-session-control="complete_runtime_c"' not in body

            response = client.post(
                "/student/session/start",
                data={
                    "mission_id": mid,
                    "session_id": "",
                    "record_commitment": "0",
                },
                follow_redirects=False,
            )
            assert response.status_code in (302, 303)
            location = response.headers.get("Location", "")
            assert "/session/" in location


# ---------------------------------------------------------------------------
# Regression
# ---------------------------------------------------------------------------


class TestRollbackAndRegression:
    def test_flag_off_restores_mark_complete_primary(self, ctx, app):
        subject = publish_subject("SR2R1", title="Rollback")
        user = make_user("sr002-reg-rollback@example.com")
        _enrol_runtime_c(user, subject)
        snap = EducationalExperienceService().load_for_user(user.id)

        with patch(
            "app.application.config.v2_flags.resolve_v2_feature_flags",
            return_value=_flags_off(),
        ):
            page = page_from_educational_experience(snap, surface="home")
        assert page.home.session_control == "complete_runtime_c"
        assert page.home.can_start_session is False
        assert "Confirm today's Mission" in page.home.primary_cta_label

        with app.test_request_context("/student/"):
            home_page = StudentHomeService().build_home(page)
        assert home_page.mission.primary_kind == "complete_runtime_c"

    def test_complete_route_blocked_when_session_primary_on(self, ctx, client):
        subject = publish_subject("SR2R2", title="Block Complete")
        user = make_user("sr002-reg-block@example.com")
        _enrol_runtime_c(user, subject)
        snap = EducationalExperienceService().load_for_user(user.id)
        _login(client, user)

        with patch(
            "app.application.config.v2_flags.resolve_v2_feature_flags",
            return_value=_flags_on(),
        ):
            response = client.post(
                "/student/mission/complete",
                data={"mission_id": snap.mission.mission_instance_id},
                follow_redirects=True,
            )
        assert response.status_code == 200
        body = response.get_data(as_text=True)
        assert (
            "Start Today's Session" in body
            or "Start Study Session" in body
            or "Session" in body
        )
        mission = EducationalRuntimeEngineService().get_mission_instance(
            user_id=user.id,
            mission_instance_id=snap.mission.mission_instance_id,
        )
        assert mission.status != MissionStatus.COMPLETED.value

    def test_mission_accepted_event_type_exists(self):
        assert EducationalEventType.MISSION_ACCEPTED.value == "mission_accepted"
        assert EducationalEventType.MISSION_DEFERRED.value == "mission_deferred"


# ---------------------------------------------------------------------------
# Acceptance
# ---------------------------------------------------------------------------


class TestAcceptanceGSession:
    def test_published_student_reaches_session_from_home_primary(
        self, ctx, client, app
    ):
        """G-Session precursor: Home Primary → /session/* via LSR."""
        subject = publish_subject("SR2A1", title="G-Session")
        user = make_user("sr002-acc-gsession@example.com")
        _enrol_runtime_c(user, subject)
        snap = EducationalExperienceService().load_for_user(user.id)
        mid = snap.mission.mission_instance_id
        _login(client, user)

        with patch(
            "app.application.config.v2_flags.resolve_v2_feature_flags",
            return_value=_flags_on(),
        ):
            from app.presentation.session.factory import init_session_experience

            with app.app_context():
                init_session_experience(app)

            start = client.post(
                "/student/session/start",
                data={
                    "mission_id": mid,
                    "session_id": "",
                    "record_commitment": "0",
                },
                follow_redirects=False,
            )
            assert start.status_code in (302, 303)
            location = start.headers["Location"]
            assert "/session/" in location

            session_page = client.get(location, follow_redirects=True)
            assert session_page.status_code == 200

            # Resume CTA after accept
            home = client.get("/student/")
            assert home.status_code == 200
            body = home.get_data(as_text=True)
            assert (
                "Continue" in body
                or "Start Today's Session" in body
                or "Resume Study Session" in body
                or "Start Study Session" in body
                or "/session/" in body
            )
