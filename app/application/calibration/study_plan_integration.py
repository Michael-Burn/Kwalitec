"""Study Plan → Student Calibration product Integration (Capability 3.8.1).

Coordinates the lawful product flow after Study Plan success:

    Study Plan created
        → launch Calibration
        → student confirms declarations (or explicit beginner skip)
        → StudentCalibrationBuilder (via CalibrationBirthPersister)
        → TwinRepository
        → handoff to Dashboard

Reuses Builder, Persister, and Repository exactly as implemented.
Never redesigns those components. Never reasons educationally. Never
invokes Readiness / Decision / Recommendation / Mission / Orchestrator /
or dashboard assembly. Never imports Flask / ORM / SQL.

See CAPABILITY_3_6_3_STUDENT_CALIBRATION_PRODUCT_FLOW.md and
APPLICATION_LAYER_ARCHITECTURE.md.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from enum import StrEnum
from typing import Any

from app.application.calibration.birth_persistence import (
    CalibrationBirthPersister,
    PersistedCalibrationBirth,
)
from app.application.calibration.contract import (
    BeginnerOrHistoryPosture,
    CoreReadingCompleted,
    CoreReadingDeclaration,
    CurriculumExamScope,
    IntendedSitting,
    PreviousAttemptsDeclaration,
    PreviouslyStudied,
    StudentCalibrationContract,
    StudyObjective,
)
from app.application.twin_repository.shared import get_shared_twin_repository
from app.application.twin_repository.twin_repository import TwinRepository
from app.application.twin_repository.types import (
    TwinPersistenceFailure,
    TwinScope,
)


class CalibrationLaunchBlockReason(StrEnum):
    """Honest reasons Calibration birth cannot start for a plan."""

    MISSING_STUDY_PLAN = "missing_study_plan"
    MISSING_CURRICULUM = "missing_curriculum"
    MISSING_STUDENT = "missing_student"


@dataclass(frozen=True)
class CalibrationLaunchContext:
    """Authorised product facts for Calibration after Study Plan success.

    Sitting / capacity / syllabus anchors only — never educational judgements.
    """

    study_plan_id: int
    authorised_student_identity: str
    curriculum_id: str
    current_exam: str | None
    sitting_label: str | None
    sitting_date: date | None
    declared_study_capacity: float | None = None


@dataclass(frozen=True)
class CalibrationLaunchBlocked:
    """Honest signal that Calibration birth cannot launch."""

    reason: CalibrationLaunchBlockReason
    detail: str | None = None
    study_plan_id: int | None = None


@dataclass(frozen=True)
class CalibrationSkippedWithoutTwin:
    """Student left Calibration without Twin birth — no Mid invention.

    Study Plan remains successfully created. Dashboard must treat Twin as
    absent until an explicit Calibration (or beginner skip birth) completes.
    """

    study_plan_id: int
    authorised_student_identity: str


@dataclass(frozen=True)
class AlphaCalibrationDeclarations:
    """Closed Alpha Calibration answers — structural declarations only."""

    previously_studied: PreviouslyStudied | str
    core_reading_completed: CoreReadingCompleted | str
    study_objective: StudyObjective | str
    previous_attempts_count: int = 0
    declared_completed_sections: tuple[str, ...] = ()
    declaration_confirmation: bool = True


class StudyPlanCalibrationCoordinator:
    """Application use-case: Study Plan success → Calibration birth → handoff.

    Owns sequencing and Contract assembly from closed declarations.
    Builder creates. Persister + Repository store. This class only wires.
    """

    def __init__(
        self,
        *,
        persister: CalibrationBirthPersister | None = None,
        repository: TwinRepository | None = None,
    ) -> None:
        self._repository = (
            repository if repository is not None else get_shared_twin_repository()
        )
        self._persister = (
            persister
            if persister is not None
            else CalibrationBirthPersister(repository=self._repository)
        )

    @property
    def repository(self) -> TwinRepository:
        """Shared TwinRepository used for Birth persist (and later retrieve)."""
        return self._repository

    @property
    def persister(self) -> CalibrationBirthPersister:
        """Injected or default CalibrationBirthPersister."""
        return self._persister

    def build_launch_context(
        self,
        *,
        study_plan_id: int | None,
        authorised_student_identity: str | None,
        curriculum_id: int | str | None,
        current_exam: str | None = None,
        sitting_label: str | None = None,
        sitting_date: date | None = None,
        weekday_study_minutes: int | None = None,
        weekend_study_minutes: int | None = None,
    ) -> CalibrationLaunchContext | CalibrationLaunchBlocked:
        """Derive Calibration launch facts from an authorised Study Plan.

        Missing Study Plan or curriculum identity blocks birth honestly.
        Does not invent Mid readiness or a Twin.
        """
        if study_plan_id is None:
            return CalibrationLaunchBlocked(
                reason=CalibrationLaunchBlockReason.MISSING_STUDY_PLAN,
                detail="Calibration requires a successfully created Study Plan",
            )

        student = _nonblank(authorised_student_identity)
        if student is None:
            return CalibrationLaunchBlocked(
                reason=CalibrationLaunchBlockReason.MISSING_STUDENT,
                detail="authorised student identity is required",
                study_plan_id=study_plan_id,
            )

        curriculum = _curriculum_id_str(curriculum_id)
        if curriculum is None:
            return CalibrationLaunchBlocked(
                reason=CalibrationLaunchBlockReason.MISSING_CURRICULUM,
                detail=(
                    "Calibration cannot birth a Twin without curriculum / "
                    "syllabus scope"
                ),
                study_plan_id=study_plan_id,
            )

        capacity = _weekly_hours_from_minutes(
            weekday_study_minutes, weekend_study_minutes
        )
        exam = _optional_nonblank(current_exam)
        label = _optional_nonblank(sitting_label)

        return CalibrationLaunchContext(
            study_plan_id=int(study_plan_id),
            authorised_student_identity=student,
            curriculum_id=curriculum,
            current_exam=exam,
            sitting_label=label,
            sitting_date=sitting_date if isinstance(sitting_date, date) else None,
            declared_study_capacity=capacity,
        )

    def build_contract(
        self,
        launch: CalibrationLaunchContext,
        declarations: AlphaCalibrationDeclarations,
    ) -> StudentCalibrationContract:
        """Assemble immutable Contract from launch anchors + closed declarations.

        Structural mapping only — Builder validates educational coherence.
        """
        previously = declarations.previously_studied
        if isinstance(previously, str):
            previously = PreviouslyStudied(previously)

        posture = (
            BeginnerOrHistoryPosture.EMPTY_HISTORY
            if previously is PreviouslyStudied.FIRST_TIME
            else BeginnerOrHistoryPosture.HISTORY_PRESENT
        )

        core = declarations.core_reading_completed
        if isinstance(core, str):
            core = CoreReadingCompleted(core)
        core_decl = CoreReadingDeclaration.create(core)

        attempts = (
            PreviousAttemptsDeclaration.create_none()
            if declarations.previous_attempts_count <= 0
            else PreviousAttemptsDeclaration.create(
                count=declarations.previous_attempts_count
            )
        )

        sections = (
            ()
            if posture is BeginnerOrHistoryPosture.EMPTY_HISTORY
            else tuple(declarations.declared_completed_sections)
        )

        return StudentCalibrationContract.create(
            authorised_student_identity=launch.authorised_student_identity,
            curriculum_exam_scope=CurriculumExamScope.create(
                launch.curriculum_id,
                current_exam=launch.current_exam,
            ),
            declaration_confirmation=bool(declarations.declaration_confirmation),
            previously_studied=previously,
            core_reading_completed=core_decl,
            previous_attempts=attempts,
            study_objective=declarations.study_objective,
            intended_sitting=self._intended_sitting(launch),
            beginner_or_history_posture=posture,
            declared_completed_sections=sections,
            declared_study_capacity=launch.declared_study_capacity,
        )

    def build_beginner_skip_contract(
        self,
        launch: CalibrationLaunchContext,
    ) -> StudentCalibrationContract:
        """Explicit beginner / empty-history Contract for lawful skip birth.

        Never invents Mid readiness or returning-student theatre.
        """
        return self.build_contract(
            launch,
            AlphaCalibrationDeclarations(
                previously_studied=PreviouslyStudied.FIRST_TIME,
                core_reading_completed=CoreReadingCompleted.NONE,
                study_objective=StudyObjective.FIRST_SIT,
                previous_attempts_count=0,
                declared_completed_sections=(),
                declaration_confirmation=True,
            ),
        )

    def complete(
        self,
        launch: CalibrationLaunchContext,
        declarations: AlphaCalibrationDeclarations,
    ) -> PersistedCalibrationBirth | TwinPersistenceFailure:
        """Build Contract, birth Twin, persist via CalibrationBirthPersister.

        Persist scope matches TwinProvider dashboard retrieval
        (student + curriculum; sitting label lives on Twin Identity / Goals).
        """
        contract = self.build_contract(launch, declarations)
        return self._persist(launch, contract)

    def complete_beginner_skip(
        self,
        launch: CalibrationLaunchContext,
    ) -> PersistedCalibrationBirth | TwinPersistenceFailure:
        """Persist explicit empty-history Birth Twin for beginner skip."""
        contract = self.build_beginner_skip_contract(launch)
        return self._persist(launch, contract)

    def abandon_without_twin(
        self,
        launch: CalibrationLaunchContext,
    ) -> CalibrationSkippedWithoutTwin:
        """Record honest abandon — Study Plan kept; no Twin invented."""
        return CalibrationSkippedWithoutTwin(
            study_plan_id=launch.study_plan_id,
            authorised_student_identity=launch.authorised_student_identity,
        )

    def twin_already_exists(self, launch: CalibrationLaunchContext) -> bool:
        """True when a Birth Twin already exists for the dashboard retrieve scope."""
        scope = self._dashboard_scope(launch)
        current = self._repository.retrieve_current_twin(scope)
        return not isinstance(current, TwinPersistenceFailure)

    def _persist(
        self,
        launch: CalibrationLaunchContext,
        contract: StudentCalibrationContract,
    ) -> PersistedCalibrationBirth | TwinPersistenceFailure:
        scope = self._dashboard_scope(launch)
        return self._persister.persist_birth(contract, scope=scope)

    def _dashboard_scope(self, launch: CalibrationLaunchContext) -> TwinScope:
        """Scope TwinProvider uses on dashboard (sitting_id unset)."""
        return TwinScope.create(
            launch.authorised_student_identity,
            sitting_id=None,
            curriculum_id=launch.curriculum_id,
        )

    def _intended_sitting(self, launch: CalibrationLaunchContext) -> IntendedSitting:
        if launch.sitting_date is not None or launch.sitting_label is not None:
            return IntendedSitting.create(
                sitting_date=launch.sitting_date,
                sitting_label=launch.sitting_label,
            )
        # Builder requires at least one sitting anchor; use curriculum exam label.
        label = launch.current_exam or f"plan-{launch.study_plan_id}"
        return IntendedSitting.create(sitting_label=label)


def _nonblank(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    normalized = value.strip()
    return normalized or None


def _optional_nonblank(value: str | None) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str):
        return None
    normalized = value.strip()
    return normalized or None


def _curriculum_id_str(curriculum_id: int | str | None) -> str | None:
    if curriculum_id is None:
        return None
    if isinstance(curriculum_id, bool):
        return None
    if isinstance(curriculum_id, int):
        if curriculum_id <= 0:
            return None
        return str(curriculum_id)
    if isinstance(curriculum_id, str):
        normalized = curriculum_id.strip()
        return normalized or None
    return None


def _weekly_hours_from_minutes(
    weekday_study_minutes: int | None,
    weekend_study_minutes: int | None,
) -> float | None:
    if weekday_study_minutes is None and weekend_study_minutes is None:
        return None
    weekday = int(weekday_study_minutes or 0)
    weekend = int(weekend_study_minutes or 0)
    if weekday < 0 or weekend < 0:
        return None
    minutes = weekday * 5 + weekend * 2
    return minutes / 60.0


__all__ = [
    "AlphaCalibrationDeclarations",
    "CalibrationLaunchBlockReason",
    "CalibrationLaunchBlocked",
    "CalibrationLaunchContext",
    "CalibrationSkippedWithoutTwin",
    "StudyPlanCalibrationCoordinator",
]
