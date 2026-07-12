"""Tests for Study Plan → Student Calibration Integration (Capability 3.8.1).

Covers: first Study Plan launches Calibration; skip behaves honestly; Birth
Twin persisted; Dashboard loads afterwards; no duplicated Birth Twin;
framework independence of Application coordinator. No educational redesign.
"""

from __future__ import annotations

import ast
from datetime import date, timedelta
from pathlib import Path

import pytest

from app.application.calibration import (
    AlphaCalibrationDeclarations,
    CalibrationLaunchBlocked,
    CalibrationLaunchBlockReason,
    CalibrationLaunchContext,
    CoreReadingCompleted,
    PersistedCalibrationBirth,
    PreviouslyStudied,
    StudyObjective,
    StudyPlanCalibrationCoordinator,
)
from app.application.config import (
    EducationalIntelligenceFeatureFlags,
    build_twin_provider,
)
from app.application.twin import TwinAbsent, TwinProvider
from app.application.twin_repository import (
    TwinPersistenceFailure,
    TwinPersistenceFailureReason,
    get_shared_twin_repository,
    reset_shared_twin_repository,
)
from app.domain.twin import DigitalTwin
from app.services.study_plan_service import StudyPlanService

APP_ROOT = Path(__file__).resolve().parents[2] / "app" / "application"
INTEGRATION_SOURCE = (
    APP_ROOT / "calibration" / "study_plan_integration.py"
)
SHARED_SOURCE = APP_ROOT / "twin_repository" / "shared.py"

FORBIDDEN_ROOT_MODULES = frozenset(
    {
        "flask",
        "flask_login",
        "flask_sqlalchemy",
        "flask_wtf",
        "wtforms",
        "sqlalchemy",
    }
)

FORBIDDEN_PREFIXES = (
    "app.auth",
    "app.dashboard",
    "app.mission",
    "app.analytics",
    "app.models",
    "app.services",
    "app.calibration",
    "app.study_plan",
)

FORBIDDEN_EDUCATIONAL_IMPORTS = (
    "app.domain.readiness",
    "app.domain.recommendation",
    "app.domain.mission",
    "app.domain.decision",
    "app.domain.learning_events",
    "app.application.orchestration",
    "app.application.dashboard",
)

FORBIDDEN_LOGIC_TOKENS = (
    "average(",
    "hybrid",
    "re_rank",
    "rerank",
    "priority_score",
    "pass_probability",
    "OverallPosture.MID",
    "OverallPosture.HIGH",
    "WarrantPosture.MEDIUM",
    "WarrantPosture.HIGH",
    "nominate_candidates",
    "_judge_factor",
    "ReadinessAggregation",
    "DecisionEngine",
    "RecommendationEngine",
    "MissionIntelligence",
    "EducationalOrchestrator",
    "DashboardAssembler",
)


def _future_exam_date() -> date:
    return date.today() + timedelta(days=180)


def _launch(**overrides: object) -> CalibrationLaunchContext:
    defaults: dict[str, object] = {
        "study_plan_id": 1,
        "authorised_student_identity": "42",
        "curriculum_id": "7",
        "current_exam": "CS1",
        "sitting_label": "April 2027",
        "sitting_date": _future_exam_date(),
        "declared_study_capacity": 8.5,
    }
    defaults.update(overrides)
    return CalibrationLaunchContext(**defaults)  # type: ignore[arg-type]


def _returning_declarations(**overrides: object) -> AlphaCalibrationDeclarations:
    defaults: dict[str, object] = {
        "previously_studied": PreviouslyStudied.PREVIOUSLY_STUDIED,
        "core_reading_completed": CoreReadingCompleted.WHOLE_PAPER,
        "study_objective": StudyObjective.REVISION,
        "previous_attempts_count": 1,
        "declared_completed_sections": ("CS1-A",),
        "declaration_confirmation": True,
    }
    defaults.update(overrides)
    return AlphaCalibrationDeclarations(**defaults)  # type: ignore[arg-type]


@pytest.fixture(autouse=True)
def _clean_shared_repository():
    reset_shared_twin_repository()
    yield
    reset_shared_twin_repository()


class TestLaunchContext:
    def test_builds_launch_from_study_plan_facts(self) -> None:
        coordinator = StudyPlanCalibrationCoordinator()
        launch = coordinator.build_launch_context(
            study_plan_id=9,
            authorised_student_identity="42",
            curriculum_id=7,
            current_exam="CS1",
            sitting_label="April 2027",
            sitting_date=_future_exam_date(),
            weekday_study_minutes=60,
            weekend_study_minutes=90,
        )
        assert isinstance(launch, CalibrationLaunchContext)
        assert launch.curriculum_id == "7"
        assert launch.declared_study_capacity == pytest.approx((60 * 5 + 90 * 2) / 60.0)

    def test_missing_study_plan_blocks_launch(self) -> None:
        blocked = StudyPlanCalibrationCoordinator().build_launch_context(
            study_plan_id=None,
            authorised_student_identity="42",
            curriculum_id=7,
        )
        assert isinstance(blocked, CalibrationLaunchBlocked)
        assert blocked.reason is CalibrationLaunchBlockReason.MISSING_STUDY_PLAN

    def test_missing_curriculum_blocks_birth(self) -> None:
        blocked = StudyPlanCalibrationCoordinator().build_launch_context(
            study_plan_id=1,
            authorised_student_identity="42",
            curriculum_id=None,
        )
        assert isinstance(blocked, CalibrationLaunchBlocked)
        assert blocked.reason is CalibrationLaunchBlockReason.MISSING_CURRICULUM


class TestBirthPersistence:
    def test_complete_persists_birth_twin(self, ctx) -> None:
        coordinator = StudyPlanCalibrationCoordinator()
        launch = _launch()
        result = coordinator.complete(launch, _returning_declarations())
        assert isinstance(result, PersistedCalibrationBirth)
        assert isinstance(result.twin, DigitalTwin)
        assert result.twin.identity.student_id == "42"
        assert result.twin.identity.curriculum_id == "7"

        loaded = coordinator.repository.retrieve_current_twin(result.scope)
        assert loaded == result.twin

    def test_beginner_skip_persists_empty_history_twin(self, ctx) -> None:
        coordinator = StudyPlanCalibrationCoordinator()
        result = coordinator.complete_beginner_skip(_launch())
        assert isinstance(result, PersistedCalibrationBirth)
        assert result.metadata.beginner_or_history_posture.value == "empty_history"
        # Empty belief domains — never Mid theatre from skip.
        assert result.twin.knowledge == result.twin.knowledge.__class__.create()
        assert result.twin.performance == result.twin.performance.__class__.create()

    def test_abandon_without_twin_does_not_persist(self, ctx) -> None:
        coordinator = StudyPlanCalibrationCoordinator()
        launch = _launch()
        skipped = coordinator.abandon_without_twin(launch)
        assert skipped.study_plan_id == launch.study_plan_id
        assert not coordinator.twin_already_exists(launch)

    def test_no_duplicated_birth_twin(self, ctx) -> None:
        coordinator = StudyPlanCalibrationCoordinator()
        launch = _launch()
        first = coordinator.complete(launch, _returning_declarations())
        assert isinstance(first, PersistedCalibrationBirth)
        second = coordinator.complete(launch, _returning_declarations())
        assert isinstance(second, TwinPersistenceFailure)
        assert second.reason is TwinPersistenceFailureReason.DUPLICATE
        assert coordinator.repository.retrieve_current_twin(first.scope) == first.twin


class TestDashboardAfterCalibration:
    def test_dashboard_provider_retrieves_persisted_birth_twin(self, ctx) -> None:
        """Dashboard TwinProvider path loads the Birth Twin from shared store."""
        from app.application.twin import TwinRetrievalContext

        coordinator = StudyPlanCalibrationCoordinator()
        launch = _launch(authorised_student_identity="99", curriculum_id="7")
        birth = coordinator.complete(launch, _returning_declarations())
        assert isinstance(birth, PersistedCalibrationBirth)

        provider = TwinProvider(repository=get_shared_twin_repository())
        retrieved = provider.retrieve(
            "99",
            context=TwinRetrievalContext(curriculum_id="7"),
        )
        assert isinstance(retrieved, DigitalTwin)
        assert retrieved == birth.twin
        assert retrieved.identity.student_id == "99"

    def test_build_twin_provider_uses_shared_repository_when_orchestrator_on(
        self,
        ctx,
    ) -> None:
        flags = EducationalIntelligenceFeatureFlags(
            ENABLE_EDUCATIONAL_ORCHESTRATOR=True,
            ENABLE_EI_RECOMMENDATIONS=True,
        )
        provider = build_twin_provider(
            flags=flags,
            environ={"KWALITEC_EI_INTERNAL_ALPHA": "1"},
        )
        assert provider.repository is get_shared_twin_repository()
        # Empty store → honest absence (no fabricated Mid Twin).
        result = provider.retrieve("99")
        assert isinstance(result, TwinAbsent)


class TestStudyPlanRouteLaunchesCalibration:
    def test_first_study_plan_redirects_to_calibration(
        self, client, ctx, user
    ) -> None:
        client.post(
            "/auth/login",
            data={"email": "test@kwalitec.example", "password": "password123"},
            follow_redirects=True,
        )
        future = _future_exam_date().isoformat()
        with client.session_transaction() as sess:
            sess["wizard_data"] = {
                "exam_category": "IFoA",
                "exam_paper": "CS1",
                "exam_sitting": "April 2027",
                "exam_date": future,
                "current_position": "not_started",
                "weekday_study_minutes": 60,
                "weekend_study_minutes": 90,
                "preferred_session_minutes": 60,
                "study_preference": "Mixed",
                "target_grade": "Pass",
            }

        resp = client.post(
            "/study-plan/review",
            data={"confirm": "yes"},
            follow_redirects=False,
        )
        assert resp.status_code == 302
        location = resp.headers["Location"]
        assert "/calibration/after-plan/" in location

        plan = StudyPlanService.get_user_active_plan(user.id)
        assert plan is not None
        assert f"/calibration/after-plan/{plan.id}" in location

    def test_calibration_skip_beginner_redirects_to_dashboard(
        self, client, ctx, user
    ) -> None:
        reset_shared_twin_repository()
        client.post(
            "/auth/login",
            data={"email": "test@kwalitec.example", "password": "password123"},
            follow_redirects=True,
        )
        plan = StudyPlanService.create_study_plan(
            user_id=user.id,
            exam_name="IFoA CS1",
            exam_sitting="April 2027",
            exam_date=_future_exam_date(),
            weekday_study_minutes=60,
            weekend_study_minutes=90,
            current_stage="I haven't started",
            study_preference="Mixed",
            target_grade="Pass",
            preferred_session_minutes=60,
            curriculum_version="2026",
        )
        assert plan.curriculum_id is not None

        resp = client.post(
            f"/calibration/after-plan/{plan.id}",
            data={"skip_beginner": "I'm starting from scratch — skip detail"},
            follow_redirects=False,
        )
        assert resp.status_code == 302
        assert "/dashboard" in resp.headers["Location"]

        coordinator = StudyPlanCalibrationCoordinator()
        launch = coordinator.build_launch_context(
            study_plan_id=plan.id,
            authorised_student_identity=str(user.id),
            curriculum_id=plan.curriculum_id,
            current_exam="CS1",
            sitting_label=plan.exam_sitting,
            sitting_date=plan.exam_date,
        )
        assert not isinstance(launch, CalibrationLaunchBlocked)
        assert coordinator.twin_already_exists(launch)

    def test_calibration_abandon_does_not_invent_twin(
        self, client, ctx, user
    ) -> None:
        reset_shared_twin_repository()
        client.post(
            "/auth/login",
            data={"email": "test@kwalitec.example", "password": "password123"},
            follow_redirects=True,
        )
        plan = StudyPlanService.create_study_plan(
            user_id=user.id,
            exam_name="IFoA CS1",
            exam_sitting="April 2027",
            exam_date=_future_exam_date(),
            weekday_study_minutes=60,
            weekend_study_minutes=90,
            current_stage="I haven't started",
            study_preference="Mixed",
            target_grade="Pass",
            preferred_session_minutes=60,
            curriculum_version="2026",
        )

        resp = client.post(
            f"/calibration/after-plan/{plan.id}",
            data={"abandon": "Continue without declaring history"},
            follow_redirects=False,
        )
        assert resp.status_code == 302
        assert "/dashboard" in resp.headers["Location"]

        coordinator = StudyPlanCalibrationCoordinator()
        launch = coordinator.build_launch_context(
            study_plan_id=plan.id,
            authorised_student_identity=str(user.id),
            curriculum_id=plan.curriculum_id,
            current_exam="CS1",
            sitting_label=plan.exam_sitting,
            sitting_date=plan.exam_date,
        )
        assert not isinstance(launch, CalibrationLaunchBlocked)
        assert not coordinator.twin_already_exists(launch)

    def test_calibration_complete_persists_and_dashboard_reachable(
        self, client, ctx, user, monkeypatch
    ) -> None:
        reset_shared_twin_repository()
        monkeypatch.setenv("KWALITEC_EI_INTERNAL_ALPHA", "1")
        client.post(
            "/auth/login",
            data={"email": "test@kwalitec.example", "password": "password123"},
            follow_redirects=True,
        )
        plan = StudyPlanService.create_study_plan(
            user_id=user.id,
            exam_name="IFoA CS1",
            exam_sitting="April 2027",
            exam_date=_future_exam_date(),
            weekday_study_minutes=60,
            weekend_study_minutes=90,
            current_stage="I haven't started",
            study_preference="Mixed",
            target_grade="Pass",
            preferred_session_minutes=60,
            curriculum_version="2026",
        )

        resp = client.post(
            f"/calibration/after-plan/{plan.id}",
            data={
                "previously_studied": "previously_studied",
                "core_reading_completed": "whole_paper",
                "previous_attempts_count": "1",
                "study_objective": "revision",
                "confirm": "yes",
            },
            follow_redirects=False,
        )
        assert resp.status_code == 302
        assert "/dashboard" in resp.headers["Location"]

        dash = client.get("/dashboard/", follow_redirects=True)
        assert dash.status_code == 200

        coordinator = StudyPlanCalibrationCoordinator()
        launch = coordinator.build_launch_context(
            study_plan_id=plan.id,
            authorised_student_identity=str(user.id),
            curriculum_id=plan.curriculum_id,
            current_exam="CS1",
            sitting_label=plan.exam_sitting,
            sitting_date=plan.exam_date,
        )
        assert not isinstance(launch, CalibrationLaunchBlocked)
        assert coordinator.twin_already_exists(launch)

        # Second submit must not duplicate Birth Twin.
        again = client.post(
            f"/calibration/after-plan/{plan.id}",
            data={
                "previously_studied": "previously_studied",
                "core_reading_completed": "whole_paper",
                "previous_attempts_count": "1",
                "study_objective": "revision",
                "confirm": "yes",
            },
            follow_redirects=False,
        )
        assert again.status_code == 302
        assert "/dashboard" in again.headers["Location"]


class TestFrameworkIndependence:
    def test_application_integration_has_no_flask_or_orm_imports(self) -> None:
        for path in (INTEGRATION_SOURCE, SHARED_SOURCE):
            tree = ast.parse(path.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        root = alias.name.split(".", 1)[0]
                        assert root not in FORBIDDEN_ROOT_MODULES, path.name
                elif isinstance(node, ast.ImportFrom) and node.module:
                    module = node.module
                    root = module.split(".", 1)[0]
                    assert root not in FORBIDDEN_ROOT_MODULES, path.name
                    for prefix in FORBIDDEN_PREFIXES:
                        assert not module.startswith(prefix), (
                            f"{path.name} imports {module}"
                        )
                    for forbidden in FORBIDDEN_EDUCATIONAL_IMPORTS:
                        assert not module.startswith(forbidden), (
                            f"{path.name} imports {module}"
                        )

    def test_integration_source_has_no_educational_reasoning_tokens(self) -> None:
        src = INTEGRATION_SOURCE.read_text(encoding="utf-8")
        for token in FORBIDDEN_LOGIC_TOKENS:
            assert token not in src, f"forbidden token {token!r}"

    def test_reuses_existing_persister_and_builder(self) -> None:
        src = INTEGRATION_SOURCE.read_text(encoding="utf-8")
        assert "CalibrationBirthPersister" in src
        assert "StudentCalibrationContract" in src
        assert "persist_birth" in src
        # Must not reinvent Twin authorship.
        assert "DigitalTwin.create" not in src
        assert "class StudentCalibrationBuilder" not in src
