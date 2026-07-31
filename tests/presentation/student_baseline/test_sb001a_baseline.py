"""SB-001A presentation — Baseline flow, calibration redirects, finalize."""

from __future__ import annotations

from datetime import date, timedelta

import pytest

from app.application.student_baseline import (
    BaselineFinalizeCoordinator,
    BaselineSubjectScope,
    StudentBaselineService,
)
from app.application.student_baseline.enums import (
    ConfidenceBand,
    ExamHistory,
    LearningObjective,
    PositionMode,
    PreviousExperience,
)
from app.extensions import db
from app.models.study_plan import StudyPlan


@pytest.fixture
def logged_in(client, ctx):
    from tests.conftest import _make_user

    user = _make_user()
    client.post(
        "/auth/login",
        data={"email": user.email, "password": "password123"},
        follow_redirects=True,
    )
    return client, user


def _wizard_session(client):
    with client.session_transaction() as sess:
        sess["wizard_data"] = {
            "exam_category": "IFoA",
            "exam_paper": "CS1",
            "exam_sitting": "April 2027",
            "exam_date": (date.today() + timedelta(days=200)).isoformat(),
            "weekday_study_minutes": 60,
            "weekend_study_minutes": 90,
            "preferred_session_minutes": 60,
            "study_preference": "Mixed",
            "target_grade": "Pass",
            "curriculum_version": "2026",
        }


class TestBaselineRoutes:
    def test_availability_redirects_to_baseline(self, logged_in):
        client, _user = logged_in
        _wizard_session(client)
        # Clear minutes so we post availability
        with client.session_transaction() as sess:
            sess["wizard_data"].pop("weekday_study_minutes", None)
            sess["wizard_data"].pop("weekend_study_minutes", None)
        resp = client.post(
            "/study-plan/wizard/3",
            data={
                "weekday_study_minutes": 60,
                "weekend_study_minutes": 90,
                "preferred_session_minutes": 60,
            },
            follow_redirects=False,
        )
        assert resp.status_code == 302
        assert "/baseline" in resp.headers["Location"]

    def test_wizard_step4_goes_to_baseline(self, logged_in):
        client, _user = logged_in
        _wizard_session(client)
        resp = client.get("/study-plan/wizard/4", follow_redirects=False)
        assert resp.status_code == 302
        assert "/baseline" in resp.headers["Location"]

    def test_progressive_experience_step(self, logged_in):
        client, _user = logged_in
        _wizard_session(client)
        resp = client.get("/baseline/step/1")
        assert resp.status_code == 200
        assert b"Brand new" in resp.data
        assert b"Baseline 1 of 6" in resp.data

        resp = client.post(
            "/baseline/step/1",
            data={"experience": PreviousExperience.BRAND_NEW.value},
            follow_redirects=False,
        )
        assert resp.status_code == 302
        assert "/baseline/step/2" in resp.headers["Location"]

    def test_calibration_redirects_to_baseline(self, logged_in):
        client, user = logged_in
        plan = StudyPlan(
            user_id=user.id,
            exam_name="IFoA CS1",
            exam_sitting="April 2027",
            exam_date=date.today() + timedelta(days=200),
            weekday_study_minutes=60,
            weekend_study_minutes=90,
            current_stage="I haven't started",
            study_preference="Mixed",
            target_grade="Pass",
            preferred_session_minutes=60,
            curriculum_version="2026",
            active=True,
        )
        db.session.add(plan)
        db.session.commit()

        resp = client.get(
            f"/calibration/after-plan/{plan.id}", follow_redirects=False
        )
        assert resp.status_code == 302
        assert "/baseline/" in resp.headers["Location"]

    def test_resume_when_baseline_complete(self, logged_in):
        client, user = logged_in
        _wizard_session(client)
        scope = BaselineSubjectScope(
            subject_key="IFoA:CS1",
            category_code="IFoA",
            subject_code="CS1",
            curriculum_version="2026",
        )
        draft = StudentBaselineService.ensure_draft(user.id, scope)
        StudentBaselineService.save_answer(
            draft.id,
            user.id,
            experience=PreviousExperience.STARTED.value,
            position_mode=PositionMode.START_BEGINNING.value,
            exam_history=ExamHistory.FIRST_SITTING.value,
            learning_objective=LearningObjective.CONTINUE.value,
            confidence=ConfidenceBand.MODERATE.value,
        )
        StudentBaselineService.mark_complete(draft, twin_snapshot_id="t1")
        resp = client.get("/baseline/")
        assert resp.status_code == 200
        assert b"already set" in resp.data.lower() or b"Restart Baseline" in resp.data


class TestBaselineFinalizeRuntimeA:
    def test_brand_new_creates_plan_and_baseline(self, ctx, logged_in):
        _client, user = logged_in
        scope = BaselineSubjectScope(
            subject_key="IFoA:CS1",
            category_code="IFoA",
            subject_code="CS1",
            curriculum_version="2026",
            exam_name="IFoA CS1",
            exam_sitting="April 2027",
            exam_date=date.today() + timedelta(days=200),
            weekday_study_minutes=60,
            weekend_study_minutes=90,
            preferred_session_minutes=60,
            study_preference="Mixed",
            target_grade="Pass",
        )
        draft = StudentBaselineService.ensure_draft(user.id, scope)
        StudentBaselineService.save_answer(
            draft.id,
            user.id,
            experience=PreviousExperience.BRAND_NEW.value,
            position_mode=PositionMode.START_BEGINNING.value,
            exam_history=ExamHistory.FIRST_SITTING.value,
            learning_objective=LearningObjective.RECOMMEND.value,
            confidence=ConfidenceBand.VERY_LOW.value,
        )
        draft = StudentBaselineService.get_by_id(draft.id)
        result = BaselineFinalizeCoordinator().finalize(
            user_id=user.id,
            baseline=draft,
            wizard={
                "exam_category": "IFoA",
                "exam_paper": "CS1",
                "exam_sitting": "April 2027",
                "exam_date": scope.exam_date.isoformat(),
                "weekday_study_minutes": 60,
                "weekend_study_minutes": 90,
                "preferred_session_minutes": 60,
                "study_preference": "Mixed",
                "target_grade": "Pass",
                "curriculum_version": "2026",
            },
            scope=scope,
        )
        assert result.study_plan_id is not None
        plan = db.session.get(StudyPlan, result.study_plan_id)
        assert plan is not None
        stage = (plan.current_stage or "").lower()
        assert "haven't started" in stage or plan.current_stage
        complete = StudentBaselineService.get_complete(user.id, "IFoA:CS1")
        assert complete is not None
        assert complete.status == "complete"
        assert complete.confidence == ConfidenceBand.VERY_LOW.value

    def test_continue_topic_sets_topic_code(self, ctx, logged_in):
        _client, user = logged_in
        from app.services.curriculum_engine_service import CurriculumEngineService

        engine = CurriculumEngineService()
        codes: list[str] = []
        if engine.curriculum_exists("IFoA", "CS1", "2026"):
            curriculum = engine.load_auto("IFoA", "CS1", "2026")
            topics = CurriculumEngineService.get_topics_flat(curriculum)
            codes = [t.code for t in topics]
        if len(codes) < 2:
            pytest.skip("CS1 curriculum topics unavailable")

        topic = codes[1]
        scope = BaselineSubjectScope(
            subject_key="IFoA:CS1",
            category_code="IFoA",
            subject_code="CS1",
            curriculum_version="2026",
            exam_name="IFoA CS1",
            exam_sitting="April 2027",
            exam_date=date.today() + timedelta(days=200),
            weekday_study_minutes=60,
            weekend_study_minutes=90,
            preferred_session_minutes=60,
            study_preference="Mixed",
            target_grade="Pass",
        )
        draft = StudentBaselineService.ensure_draft(user.id, scope)
        StudentBaselineService.save_answer(
            draft.id,
            user.id,
            experience=PreviousExperience.ABOUT_HALFWAY.value,
            position_mode=PositionMode.CONTINUE_TOPIC.value,
            curriculum_topic_code=topic,
            exam_history=ExamHistory.PREVIOUSLY_ATTEMPTED.value,
            learning_objective=LearningObjective.CONTINUE.value,
            confidence=ConfidenceBand.HIGH.value,
        )
        draft = StudentBaselineService.get_by_id(draft.id)
        result = BaselineFinalizeCoordinator().finalize(
            user_id=user.id,
            baseline=draft,
            wizard={
                "exam_sitting": "April 2027",
                "exam_date": scope.exam_date.isoformat(),
                "weekday_study_minutes": 60,
                "weekend_study_minutes": 90,
                "curriculum_version": "2026",
            },
            scope=scope,
        )
        plan = db.session.get(StudyPlan, result.study_plan_id)
        assert plan.curriculum_topic_code == topic


class TestRuntimeCBridgeOrdering:
    def test_bridge_enrol_after_baseline_ready(
        self, ctx, logged_in, monkeypatch
    ):
        """Thin bridge: enrol not invoked until finalize with complete decls."""
        _client, user = logged_in
        calls: list[str] = []

        class FakeBridge:
            def should_use_bridge(self, *, category_code, subject_code):
                return True

            def enrol(self, **kwargs):
                calls.append("enrol")
                from app.application.educational_runtime_engine.coexistence import (
                    RuntimeAuthority,
                )
                from app.application.platform_integration.dto import (
                    EnrolmentBridgeResult,
                    RoutingDecision,
                )

                decision = RoutingDecision(
                    subject_code=kwargs.get("subject_code") or "X",
                    category_code=kwargs.get("category_code") or "PUBLISHED",
                    runtime_authority=RuntimeAuthority.PUBLISHED_CURRICULUM,
                    reason="test",
                    published_package_id=1,
                    curriculum_identity="pub:1",
                    discovery_enabled=True,
                    enrolment_enabled=True,
                    flags_snapshot={},
                )
                return EnrolmentBridgeResult(
                    runtime_authority=RuntimeAuthority.PUBLISHED_CURRICULUM,
                    routing=decision,
                    audit_id="audit-1",
                    enrolment_id="enrol-1",
                    curriculum_identity="pub:1",
                    study_plan_id=None,
                    redirect_target="student_home",
                    message="enrolled",
                )

        # Twin birth: allow failure/success without real curriculum id issues
        from app.application.student_baseline import coordinator as coord_mod

        monkeypatch.setattr(
            coord_mod.BaselineFinalizeCoordinator,
            "_birth_twin",
            lambda self, **kwargs: None,
        )

        scope = BaselineSubjectScope(
            subject_key="PUBLISHED:DEMO",
            category_code="PUBLISHED",
            subject_code="DEMO",
            curriculum_version="published",
            exam_name="PUBLISHED DEMO",
            exam_sitting="April 2027",
            exam_date=date.today() + timedelta(days=200),
            weekday_study_minutes=60,
            weekend_study_minutes=90,
            preferred_session_minutes=60,
            study_preference="Mixed",
            target_grade="Pass",
        )
        draft = StudentBaselineService.ensure_draft(user.id, scope)
        StudentBaselineService.save_answer(
            draft.id,
            user.id,
            experience=PreviousExperience.BRAND_NEW.value,
            position_mode=PositionMode.START_BEGINNING.value,
            exam_history=ExamHistory.FIRST_SITTING.value,
            learning_objective=LearningObjective.RECOMMEND.value,
            confidence=ConfidenceBand.MODERATE.value,
        )
        draft = StudentBaselineService.get_by_id(draft.id)
        assert not calls
        result = BaselineFinalizeCoordinator(bridge=FakeBridge()).finalize(
            user_id=user.id,
            baseline=draft,
            wizard={"exam_date": scope.exam_date.isoformat()},
            scope=scope,
        )
        assert calls == ["enrol"]
        assert result.enrolment_id == "enrol-1"
        assert StudentBaselineService.get_complete(user.id, "PUBLISHED:DEMO")
