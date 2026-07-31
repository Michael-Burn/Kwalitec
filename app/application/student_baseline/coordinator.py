"""SB-001A finalize coordinator — Twin birth then Runtime A / C entry.

Reuses StudyPlanCalibrationCoordinator contract assembly, BaselineTwinBirth,
StudyPlanService, and FounderStudentEnrolmentBridge.enrol without redesigning
Runtime C / SCI / StudyPlan generation.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Any

from app.application.calibration.birth_persistence import PersistedCalibrationBirth
from app.application.calibration.contract import (
    BeginnerOrHistoryPosture,
    CoreReadingCompleted,
    CoreReadingDeclaration,
    CurriculumExamScope,
    IntendedSitting,
    PreviousAttemptsDeclaration,
    PreviouslyStudied,
    StudentCalibrationContract,
)
from app.application.calibration.study_plan_integration import (
    AlphaCalibrationDeclarations,
)
from app.application.educational_runtime_engine.coexistence import (
    RuntimeAuthority,
)
from app.application.platform_integration.enrolment_bridge import (
    FounderStudentEnrolmentBridge,
)
from app.application.platform_integration.exceptions import (
    BridgeEnrolmentBlocked,
    PublishedSubjectNotDiscoverable,
)
from app.application.student_baseline.birth import BaselineTwinBirth
from app.application.student_baseline.declarations import (
    BaselineDeclarations,
    BaselineSubjectScope,
)
from app.application.student_baseline.enums import BaselineStatus, LearningObjective
from app.application.student_baseline.mapper import (
    build_plan_fields,
    to_alpha_declarations,
)
from app.application.student_baseline.service import StudentBaselineService
from app.application.twin_repository.types import (
    TwinPersistenceFailure,
    TwinScope,
)
from app.models.student_baseline import StudentBaseline
from app.services.curriculum_engine_service import CurriculumEngineService
from app.services.study_plan_service import StudyPlanService


@dataclass(frozen=True)
class BaselineFinalizeResult:
    """Outcome of Baseline finalize for presentation redirects."""

    baseline_id: int
    runtime_authority: str
    study_plan_id: int | None
    enrolment_id: str | None
    twin_snapshot_id: str | None
    twin_persisted: bool
    message: str
    redirect_target: str = "student_home"


class BaselineFinalizeError(Exception):
    """Honest finalize failure — no Mid theatre invented."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class BaselineFinalizeCoordinator:
    """Baseline complete → Twin birth → Study Plan or Runtime C enrol."""

    def __init__(
        self,
        *,
        birth: BaselineTwinBirth | None = None,
        bridge: FounderStudentEnrolmentBridge | None = None,
    ) -> None:
        self._birth = birth or BaselineTwinBirth()
        self._bridge = bridge or FounderStudentEnrolmentBridge()

    def finalize(
        self,
        *,
        user_id: int,
        baseline: StudentBaseline,
        wizard: dict[str, Any],
        scope: BaselineSubjectScope,
    ) -> BaselineFinalizeResult:
        """Commit Baseline → Twin → runtime entry.

        Raises:
            BaselineFinalizeError: Missing declarations or enrol blocked.
        """
        if baseline.status != BaselineStatus.DRAFT.value:
            raise BaselineFinalizeError("Baseline is not an open draft")

        declarations = StudentBaselineService.declarations_from_row(baseline)
        if declarations is None:
            raise BaselineFinalizeError(
                "Please finish every Baseline question before continuing."
            )

        curriculum_id = self._resolve_curriculum_id(scope, wizard)
        ordered_codes = self._ordered_topic_codes(
            scope.category_code,
            scope.subject_code,
            scope.curriculum_version,
        )
        plan_fields = build_plan_fields(
            declarations, ordered_topic_codes=ordered_codes
        )
        alpha = to_alpha_declarations(
            declarations,
            completed_section_ids=plan_fields.completed_curriculum_topics,
        )

        # Twin before runtime entry (Part 5).
        twin_result = self._birth_twin(
            user_id=user_id,
            curriculum_id=curriculum_id,
            scope=scope,
            alpha=alpha,
            declarations=declarations,
            wizard=wizard,
        )
        twin_snapshot_id: str | None = None
        twin_persisted = False
        if isinstance(twin_result, PersistedCalibrationBirth):
            twin_snapshot_id = twin_result.snapshot_id
            twin_persisted = True
        elif isinstance(twin_result, TwinPersistenceFailure):
            # Honest continue — Baseline still completes; twin may be absent.
            twin_persisted = False

        use_bridge = self._bridge.should_use_bridge(
            category_code=scope.category_code,
            subject_code=scope.subject_code,
        )

        existing_plan_id = wizard.get("existing_study_plan_id")
        if existing_plan_id and not use_bridge:
            return self._finalize_existing_plan(
                user_id=user_id,
                baseline=baseline,
                twin_snapshot_id=twin_snapshot_id,
                twin_persisted=twin_persisted,
                study_plan_id=int(existing_plan_id),
                plan_fields=plan_fields,
                declarations=declarations,
            )

        if use_bridge:
            return self._finalize_via_bridge(
                user_id=user_id,
                baseline=baseline,
                scope=scope,
                wizard=wizard,
                twin_snapshot_id=twin_snapshot_id,
                twin_persisted=twin_persisted,
                plan_fields=plan_fields,
                declarations=declarations,
            )

        return self._finalize_runtime_a(
            user_id=user_id,
            baseline=baseline,
            scope=scope,
            wizard=wizard,
            twin_snapshot_id=twin_snapshot_id,
            twin_persisted=twin_persisted,
            plan_fields=plan_fields,
        )

    def _finalize_runtime_a(
        self,
        *,
        user_id: int,
        baseline: StudentBaseline,
        scope: BaselineSubjectScope,
        wizard: dict[str, Any],
        twin_snapshot_id: str | None,
        twin_persisted: bool,
        plan_fields,
    ) -> BaselineFinalizeResult:
        exam_date = scope.exam_date
        if exam_date is None and wizard.get("exam_date"):
            raw = wizard["exam_date"]
            exam_date = date.fromisoformat(raw) if isinstance(raw, str) else raw

        study_plan = StudyPlanService.create_study_plan(
            user_id=user_id,
            exam_name=scope.exam_name or wizard.get("exam_name") or "",
            exam_sitting=scope.exam_sitting
            or wizard.get("exam_sitting")
            or "",
            exam_date=exam_date,
            weekday_study_minutes=int(
                scope.weekday_study_minutes
                or wizard.get("weekday_study_minutes")
                or 60
            ),
            weekend_study_minutes=int(
                scope.weekend_study_minutes
                or wizard.get("weekend_study_minutes")
                or 60
            ),
            current_stage=plan_fields.current_stage,
            study_preference=scope.study_preference
            or wizard.get("study_preference")
            or "Mixed",
            target_grade=scope.target_grade
            or wizard.get("target_grade")
            or "Pass",
            preferred_session_minutes=int(
                scope.preferred_session_minutes
                or wizard.get("preferred_session_minutes")
                or 60
            ),
            curriculum_version=scope.curriculum_version,
            curriculum_topic_code=plan_fields.curriculum_topic_code,
            completed_curriculum_topics=plan_fields.completed_curriculum_topics,
        )

        if plan_fields.completed_curriculum_topics:
            StudyPlanService.sync_declared_completed_topics(
                study_plan.id,
                user_id,
                plan_fields.completed_curriculum_topics,
            )

        StudentBaselineService.mark_complete(
            baseline,
            twin_snapshot_id=twin_snapshot_id,
            study_plan_id=study_plan.id,
            runtime_authority=RuntimeAuthority.JSON_BUNDLED.value,
        )

        msg = (
            "Your Baseline is recorded. We've initialised your study profile "
            "from where you are today."
            if twin_persisted
            else (
                "Your Baseline is recorded and your study plan is ready. "
                "We could not save a Twin snapshot just now — continuing honestly."
            )
        )
        return BaselineFinalizeResult(
            baseline_id=baseline.id,
            runtime_authority=RuntimeAuthority.JSON_BUNDLED.value,
            study_plan_id=study_plan.id,
            enrolment_id=None,
            twin_snapshot_id=twin_snapshot_id,
            twin_persisted=twin_persisted,
            message=msg,
        )

    def _finalize_existing_plan(
        self,
        *,
        user_id: int,
        baseline: StudentBaseline,
        twin_snapshot_id: str | None,
        twin_persisted: bool,
        study_plan_id: int,
        plan_fields,
        declarations: BaselineDeclarations,
    ) -> BaselineFinalizeResult:
        """Attach Baseline + Twin to an already-created Study Plan (legacy path)."""
        if plan_fields.completed_curriculum_topics:
            StudyPlanService.sync_declared_completed_topics(
                study_plan_id,
                user_id,
                plan_fields.completed_curriculum_topics,
            )
        plan = StudyPlanService.get_user_active_plan(user_id)
        if plan is not None and plan.id == study_plan_id:
            plan.current_stage = plan_fields.current_stage
            plan.curriculum_topic_code = plan_fields.curriculum_topic_code
            from app.extensions import db

            db.session.commit()

        StudentBaselineService.mark_complete(
            baseline,
            twin_snapshot_id=twin_snapshot_id,
            study_plan_id=study_plan_id,
            runtime_authority=RuntimeAuthority.JSON_BUNDLED.value,
        )
        _ = declarations
        return BaselineFinalizeResult(
            baseline_id=baseline.id,
            runtime_authority=RuntimeAuthority.JSON_BUNDLED.value,
            study_plan_id=study_plan_id,
            enrolment_id=None,
            twin_snapshot_id=twin_snapshot_id,
            twin_persisted=twin_persisted,
            message=(
                "Your Baseline is recorded. We've updated your study profile "
                "from where you are today."
            ),
        )

    def _finalize_via_bridge(
        self,
        *,
        user_id: int,
        baseline: StudentBaseline,
        scope: BaselineSubjectScope,
        wizard: dict[str, Any],
        twin_snapshot_id: str | None,
        twin_persisted: bool,
        plan_fields,
        declarations: BaselineDeclarations,
    ) -> BaselineFinalizeResult:
        exam_date = scope.exam_date
        if exam_date is None and wizard.get("exam_date"):
            raw = wizard["exam_date"]
            exam_date = date.fromisoformat(raw) if isinstance(raw, str) else raw

        # Runtime A kwargs used only if routing selects JSON path.
        runtime_a_kwargs = {
            "exam_name": scope.exam_name or "",
            "exam_sitting": scope.exam_sitting or wizard.get("exam_sitting") or "",
            "exam_date": exam_date,
            "weekday_study_minutes": int(
                scope.weekday_study_minutes
                or wizard.get("weekday_study_minutes")
                or 60
            ),
            "weekend_study_minutes": int(
                scope.weekend_study_minutes
                or wizard.get("weekend_study_minutes")
                or 60
            ),
            "current_stage": plan_fields.current_stage,
            "study_preference": scope.study_preference
            or wizard.get("study_preference")
            or "Mixed",
            "target_grade": scope.target_grade
            or wizard.get("target_grade")
            or "Pass",
            "preferred_session_minutes": int(
                scope.preferred_session_minutes
                or wizard.get("preferred_session_minutes")
                or 60
            ),
            "curriculum_version": scope.curriculum_version,
            "curriculum_topic_code": plan_fields.curriculum_topic_code,
            "completed_curriculum_topics": plan_fields.completed_curriculum_topics,
        }

        try:
            result = self._bridge.enrol(
                user_id=user_id,
                category_code=scope.category_code,
                subject_code=scope.subject_code,
                exam_date=exam_date,
                runtime_a_kwargs=runtime_a_kwargs,
            )
        except (BridgeEnrolmentBlocked, PublishedSubjectNotDiscoverable) as exc:
            raise BaselineFinalizeError(str(exc)) from exc

        # Baseline declarations are available for correlation; engine unchanged.
        _ = declarations

        StudentBaselineService.mark_complete(
            baseline,
            twin_snapshot_id=twin_snapshot_id,
            study_plan_id=result.study_plan_id,
            enrolment_id=result.enrolment_id,
            runtime_authority=result.runtime_authority.value,
        )

        return BaselineFinalizeResult(
            baseline_id=baseline.id,
            runtime_authority=result.runtime_authority.value,
            study_plan_id=result.study_plan_id,
            enrolment_id=result.enrolment_id,
            twin_snapshot_id=twin_snapshot_id,
            twin_persisted=twin_persisted,
            message=result.message,
            redirect_target="student_home",
        )

    def _birth_twin(
        self,
        *,
        user_id: int,
        curriculum_id: str,
        scope: BaselineSubjectScope,
        alpha: AlphaCalibrationDeclarations,
        declarations: BaselineDeclarations,
        wizard: dict[str, Any],
    ) -> PersistedCalibrationBirth | TwinPersistenceFailure | None:
        if not curriculum_id:
            return None

        sitting_date = scope.exam_date
        if sitting_date is None and wizard.get("exam_date"):
            raw = wizard["exam_date"]
            sitting_date = (
                date.fromisoformat(raw) if isinstance(raw, str) else raw
            )

        previously = alpha.previously_studied
        if isinstance(previously, str):
            previously = PreviouslyStudied(previously)
        posture = (
            BeginnerOrHistoryPosture.EMPTY_HISTORY
            if previously is PreviouslyStudied.FIRST_TIME
            else BeginnerOrHistoryPosture.HISTORY_PRESENT
        )
        attempts = (
            PreviousAttemptsDeclaration.create_none()
            if alpha.previous_attempts_count <= 0
            else PreviousAttemptsDeclaration.create(
                count=alpha.previous_attempts_count
            )
        )
        core = CoreReadingDeclaration.create(CoreReadingCompleted.NONE)
        intended = IntendedSitting.create(
            sitting_date=sitting_date if isinstance(sitting_date, date) else None,
            sitting_label=scope.exam_sitting
            or wizard.get("exam_sitting")
            or scope.subject_code,
        )
        capacity = None
        wd = scope.weekday_study_minutes or wizard.get("weekday_study_minutes")
        we = scope.weekend_study_minutes or wizard.get("weekend_study_minutes")
        if wd is not None and we is not None:
            capacity = (5 * float(wd) + 2 * float(we)) / 60.0

        # Restart objective forces empty history posture for Twin honesty.
        if declarations.learning_objective is LearningObjective.RESTART:
            previously = PreviouslyStudied.FIRST_TIME
            posture = BeginnerOrHistoryPosture.EMPTY_HISTORY
            sections: tuple[str, ...] = ()
        else:
            sections = (
                ()
                if posture is BeginnerOrHistoryPosture.EMPTY_HISTORY
                else tuple(alpha.declared_completed_sections)
            )

        contract = StudentCalibrationContract.create(
            authorised_student_identity=str(user_id),
            curriculum_exam_scope=CurriculumExamScope.create(
                curriculum_id,
                current_exam=scope.subject_code,
            ),
            declaration_confirmation=True,
            previously_studied=previously,
            core_reading_completed=core,
            previous_attempts=attempts,
            study_objective=alpha.study_objective,
            intended_sitting=intended,
            beginner_or_history_posture=posture,
            declared_completed_sections=sections,
            declared_study_capacity=capacity,
            optional_notes=(
                f"sb001a:{declarations.learning_objective.value}:"
                f"{declarations.confidence.value}"
            ),
        )
        twin_scope = TwinScope.create(
            str(user_id),
            sitting_id=None,
            curriculum_id=curriculum_id,
        )
        return self._birth.persist(contract, declarations, scope=twin_scope)

    @staticmethod
    def _resolve_curriculum_id(
        scope: BaselineSubjectScope, wizard: dict[str, Any]
    ) -> str:
        version = scope.curriculum_version or wizard.get("curriculum_version")
        if version:
            return str(version)
        return scope.subject_code or scope.subject_key

    @staticmethod
    def _ordered_topic_codes(
        category_code: str,
        subject_code: str,
        curriculum_version: str | None,
    ) -> list[str]:
        if not curriculum_version or curriculum_version == "published":
            return []
        if not category_code or not subject_code:
            return []
        try:
            engine = CurriculumEngineService()
            if not engine.curriculum_exists(
                category_code, subject_code, curriculum_version
            ):
                return []
            curriculum = engine.load_auto(
                category_code, subject_code, curriculum_version
            )
            topics = CurriculumEngineService.get_topics_flat(curriculum)
            return [t.code for t in topics]
        except Exception:
            return []
