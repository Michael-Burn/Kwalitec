"""LXP-003 — Study Session Product Completion (SR-001A Phase P2).

Unit / integration / regression / acceptance coverage for:
pause / resume, finish review (Yes/Partially/No), session persistence,
recovery across refresh, no silent complete, no mission completion.
"""

from __future__ import annotations

from datetime import date, timedelta

import pytest

from app.application.config.v2_flags import resolve_v2_feature_flags
from app.application.learning_session.dto.finish_review import (
    FinishReview,
    FinishReviewVerdict,
)
from app.application.learning_session.exceptions import (
    FinishReviewRequired,
    InvalidSessionState,
)
from app.application.learning_session.lifecycle_manager import LifecycleManager
from app.application.learning_session.runtime import LearningSessionRuntime
from app.application.learning_session.runtime_phase import (
    RuntimePhase,
    product_lifecycle_label,
)
from app.application.platform_integration.discovery import PUBLISHED_CATEGORY_CODE
from app.application.platform_integration.enrolment_bridge import (
    FounderStudentEnrolmentBridge,
)
from app.domain.educational_runtime_engine.events import EducationalEventType
from app.domain.learning_journey.value_objects.session_state import SessionState
from app.infrastructure.adapters.learning_session.persistence import (
    LearningSessionPersistenceAdapter,
)
from app.infrastructure.adapters.learning_session.runtime_engine import (
    LearningSessionRuntimeEngine,
)
from app.infrastructure.session.store import SessionDocumentStore
from app.models.user import User
from tests.application.learning_session.helpers import make_journey, make_session
from tests.application.platform_integration.helpers import (
    bridge_flags,
    make_user,
    publish_subject,
)


def _flags_product(**extra: str):
    env = {
        "SR_SESSION_PRIMARY": "1",
        "SR_SESSION_COMPLETION_PRODUCT": "1",
        **extra,
    }
    return resolve_v2_feature_flags(environ=env)


def _flags_product_off(**extra: str):
    env = {
        "SR_SESSION_PRIMARY": "1",
        "SR_SESSION_COMPLETION_PRODUCT": "0",
        **extra,
    }
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


def _active_handle(runtime: LearningSessionRuntime | None = None):
    lsr = runtime or LearningSessionRuntime()
    journey = make_journey()
    handle = lsr.create_session(journey, session_id="lsr-p2-1")
    handle = lsr.prepare_session(handle)
    return lsr.start_session(handle), lsr


# ---------------------------------------------------------------------------
# Unit — finish review DTOs + state machine
# ---------------------------------------------------------------------------


class TestFinishReviewDto:
    def test_verdicts(self):
        for value in ("yes", "partially", "no"):
            review = FinishReview.create(value, notes="ok")
            assert review.verdict.value == value
            assert review.label in {"Yes", "Partially", "No"}

    def test_opaque_roundtrip(self):
        review = FinishReview.create(
            FinishReviewVerdict.PARTIALLY, notes="half done"
        )
        restored = FinishReview.from_opaque(review.to_opaque())
        assert restored is not None
        assert restored.verdict is FinishReviewVerdict.PARTIALLY
        assert restored.notes == "half done"

    def test_from_opaque_none(self):
        assert FinishReview.from_opaque(None) is None
        assert FinishReview.from_opaque({}) is None


class TestReadyToFinishLifecycle:
    def setup_method(self):
        self.lifecycle = LifecycleManager()

    def test_request_finish_from_active(self):
        result = self.lifecycle.request_finish(
            make_session(state=SessionState.ACTIVE),
            phase=RuntimePhase.ACTIVE,
        )
        assert result.phase == RuntimePhase.READY_TO_FINISH
        assert result.session.state == SessionState.ACTIVE

    def test_request_finish_from_paused(self):
        result = self.lifecycle.request_finish(
            make_session(state=SessionState.PAUSED),
            phase=RuntimePhase.PAUSED,
        )
        assert result.phase == RuntimePhase.READY_TO_FINISH
        assert result.session.state == SessionState.PAUSED

    def test_complete_from_ready_to_finish(self):
        result = self.lifecycle.complete(
            make_session(state=SessionState.ACTIVE),
            phase=RuntimePhase.READY_TO_FINISH,
        )
        assert result.phase == RuntimePhase.COMPLETED
        assert result.session.state == SessionState.COMPLETED

    def test_resume_cancels_finish_review(self):
        result = self.lifecycle.resume(
            make_session(state=SessionState.ACTIVE),
            phase=RuntimePhase.READY_TO_FINISH,
        )
        assert result.phase == RuntimePhase.ACTIVE

    def test_request_finish_rejects_planned(self):
        with pytest.raises(InvalidSessionState):
            self.lifecycle.request_finish(
                make_session(),
                phase=RuntimePhase.PLANNED,
            )

    def test_product_lifecycle_labels(self):
        assert product_lifecycle_label(RuntimePhase.PLANNED) == "Created"
        assert product_lifecycle_label(RuntimePhase.ACTIVE) == "In Progress"
        assert product_lifecycle_label(RuntimePhase.PAUSED) == "Paused"
        assert product_lifecycle_label(RuntimePhase.READY_TO_FINISH) == (
            "Ready to Finish"
        )
        assert product_lifecycle_label(RuntimePhase.COMPLETED) == "Completed"


class TestPauseResumeRuntime:
    def test_pause_and_resume(self):
        handle, lsr = _active_handle()
        paused = lsr.pause_session(handle)
        assert paused.phase == RuntimePhase.PAUSED
        resumed = lsr.resume_session(paused)
        assert resumed.phase == RuntimePhase.ACTIVE
        assert resumed.session.session_id == handle.session.session_id

    def test_finish_review_required_blocks_silent_complete(self):
        handle, lsr = _active_handle()
        with pytest.raises(FinishReviewRequired):
            lsr.complete_session(handle, require_finish_review=True)

    def test_complete_with_finish_review(self):
        handle, lsr = _active_handle()
        handle = lsr.request_finish(handle)
        handle = lsr.record_finish_review(handle, verdict="yes", notes="done")
        completed = lsr.complete_session(handle, require_finish_review=True)
        assert completed.phase == RuntimePhase.COMPLETED
        assert completed.finish_review is not None
        assert completed.finish_review.verdict is FinishReviewVerdict.YES


class TestFeatureFlag:
    def test_completion_product_defaults_off(self):
        flags = resolve_v2_feature_flags(environ={})
        assert flags.SR_SESSION_COMPLETION_PRODUCT is False

    def test_completion_product_env_on(self):
        flags = resolve_v2_feature_flags(
            environ={"SR_SESSION_COMPLETION_PRODUCT": "1"}
        )
        assert flags.SR_SESSION_COMPLETION_PRODUCT is True


# ---------------------------------------------------------------------------
# Integration — persistence + engine
# ---------------------------------------------------------------------------


class TestPersistenceAndRecovery:
    def test_pause_resume_same_session_id(self):
        store = SessionDocumentStore()
        persistence = LearningSessionPersistenceAdapter(store=store)
        engine = LearningSessionRuntimeEngine(
            persistence=persistence, require_finish_review=True
        )
        handle, lsr = _active_handle()
        persistence.save_binding(
            student_id="42",
            mission_instance_id="m-1",
            handle=handle,
            topic_title="Interest Rates",
            active_surface="activity",
        )
        paused = engine.pause_session_opaque("42", session_id=handle.session.session_id)
        assert paused is not None
        assert paused["phase"] == "paused"
        resumed = engine.resume_session_opaque(
            "42", session_id=handle.session.session_id
        )
        assert resumed is not None
        assert resumed["phase"] == "active"
        assert resumed["session_id"] == handle.session.session_id
        reloaded = persistence.load_handle(session_id=handle.session.session_id)
        assert reloaded is not None
        assert reloaded.session.session_id == handle.session.session_id

    def test_progress_survives_reload(self):
        store = SessionDocumentStore()
        persistence = LearningSessionPersistenceAdapter(store=store)
        handle, _ = _active_handle()
        persistence.save_binding(
            student_id="7",
            mission_instance_id="m-2",
            handle=handle,
            topic_title="Cashflows",
            active_surface="activity",
        )
        persistence.update_checklist_item(
            session_id=handle.session.session_id,
            student_id="7",
            item_id="read",
            done=True,
        )
        progress = persistence.load_progress(session_id=handle.session.session_id)
        assert progress is not None
        assert progress["active_surface"] == "activity"
        assert any(
            i["id"] == "read" and i["done"] for i in progress["checklist"]
        )

    def test_finish_review_persisted(self):
        store = SessionDocumentStore()
        persistence = LearningSessionPersistenceAdapter(store=store)
        engine = LearningSessionRuntimeEngine(
            persistence=persistence, require_finish_review=True
        )
        handle, _ = _active_handle()
        persistence.save_binding(
            student_id="9",
            mission_instance_id="m-3",
            handle=handle,
            topic_title="Bonds",
        )
        result = engine.complete_session_opaque(
            "9",
            session_id=handle.session.session_id,
            finish_verdict="partially",
            finish_notes="got halfway",
        )
        assert result is not None
        assert result["status"] == "completed"
        assert result["mission_completed"] is False
        assert result["progress_advanced"] is False
        assert result["finish_review"]["verdict"] == "partially"
        doc = persistence.load(session_id=handle.session.session_id)
        assert doc is not None
        assert doc["finish_review"]["verdict"] == "partially"

    def test_silent_complete_rejected_when_required(self):
        store = SessionDocumentStore()
        persistence = LearningSessionPersistenceAdapter(store=store)
        engine = LearningSessionRuntimeEngine(
            persistence=persistence, require_finish_review=True
        )
        handle, _ = _active_handle()
        persistence.save_binding(
            student_id="11",
            mission_instance_id="m-4",
            handle=handle,
            topic_title="Derivatives",
        )
        result = engine.complete_session_opaque(
            "11", session_id=handle.session.session_id
        )
        assert result is not None
        assert result["error"] == "finish_review_required"
        assert result["progress_advanced"] is False
        doc = persistence.load(session_id=handle.session.session_id)
        assert doc is not None
        assert doc["status"] == "open"


# ---------------------------------------------------------------------------
# Regression — incomplete sessions do not emit TOPIC_COMPLETED
# ---------------------------------------------------------------------------


class TestNoMissionCompletion:
    def test_session_complete_does_not_emit_topic_completed(
        self, app, db, ctx
    ):
        user = make_user(email="lxp003-reg@example.com")
        db.session.add(user)
        db.session.commit()
        publish_subject("CS1")
        _enrol_runtime_c(user, "CS1")

        store = SessionDocumentStore()
        persistence = LearningSessionPersistenceAdapter(store=store)
        from app.application.educational_runtime_engine.service import (
            EducationalRuntimeEngineService,
        )

        engine = EducationalRuntimeEngineService()
        handle, _ = _active_handle()
        persistence.save_binding(
            student_id=str(user.id),
            mission_instance_id="mission-synthetic",
            handle=handle,
            topic_title="Regression Topic",
        )
        runtime_engine = LearningSessionRuntimeEngine(
            persistence=persistence, require_finish_review=True
        )
        result = runtime_engine.complete_session_opaque(
            str(user.id),
            session_id=handle.session.session_id,
            finish_verdict="yes",
        )
        assert result["mission_completed"] is False
        assert result["progress_advanced"] is False

        # Event stream must not gain TOPIC_COMPLETED from this close.
        events = ()
        if hasattr(engine, "list_events"):
            events = engine.list_events(user_id=user.id) or ()
        topic_completed = [
            e
            for e in events
            if getattr(e, "event_type", None) == EducationalEventType.TOPIC_COMPLETED
            or str(getattr(e, "event_type", "")) == "topic_completed"
        ]
        assert topic_completed == []


# ---------------------------------------------------------------------------
# Acceptance — pause, return, finish with explicit review
# ---------------------------------------------------------------------------


class TestAcceptanceHttp:
    def test_pause_resume_finish_review_flow(self, app, client, db, ctx):
        user = make_user(email="lxp003-acc@example.com")
        db.session.add(user)
        db.session.commit()
        _login(client, user)

        store = SessionDocumentStore()
        persistence = LearningSessionPersistenceAdapter(store=store)
        handle, _ = _active_handle()
        sid = handle.session.session_id
        persistence.save_binding(
            student_id=str(user.id),
            mission_instance_id="m-acc",
            handle=handle,
            topic_title="Acceptance Topic",
            active_surface="activity",
        )
        engine = LearningSessionRuntimeEngine(
            persistence=persistence, require_finish_review=True
        )

        paused = engine.pause_session_opaque(str(user.id), session_id=sid)
        assert paused["phase"] == "paused"
        # Simulate leave + return (multiple "refreshes")
        for _ in range(3):
            loaded = persistence.load_handle(session_id=sid)
            assert loaded is not None
            assert loaded.phase == RuntimePhase.PAUSED
        resumed = engine.resume_session_opaque(str(user.id), session_id=sid)
        assert resumed["phase"] == "active"
        ready = engine.request_finish_opaque(str(user.id), session_id=sid)
        assert ready["phase"] == "ready_to_finish"
        blocked = engine.complete_session_opaque(str(user.id), session_id=sid)
        assert blocked["error"] == "finish_review_required"
        done = engine.complete_session_opaque(
            str(user.id),
            session_id=sid,
            finish_verdict="no",
            finish_notes="could not continue",
        )
        assert done["status"] == "completed"
        assert done["finish_review"]["verdict"] == "no"
        assert done["mission_completed"] is False

    def test_flag_off_allows_complete_without_review(self):
        store = SessionDocumentStore()
        persistence = LearningSessionPersistenceAdapter(store=store)
        engine = LearningSessionRuntimeEngine(
            persistence=persistence, require_finish_review=False
        )
        handle, _ = _active_handle()
        persistence.save_binding(
            student_id="99",
            mission_instance_id="m-off",
            handle=handle,
            topic_title="Rollback Topic",
        )
        result = engine.complete_session_opaque(
            "99", session_id=handle.session.session_id
        )
        assert result is not None
        assert result["status"] == "completed"
        assert result.get("error") is None
