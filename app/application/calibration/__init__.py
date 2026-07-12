"""Application Calibration Integration — Twin-birth prior construction.

Consumes the immutable Student Calibration Contract and emits a calibrated
birth Twin with self_declared provenance. Birth → Persist composition lives
in ``birth_persistence`` (Capability 3.7.5). Study Plan → Calibration product
flow lives in ``study_plan_integration`` (Capability 3.8.1). Builder itself
never persists. Never reasons educationally or imports Flask / ORM /
Educational Intelligence engines.
"""

from __future__ import annotations

from app.application.calibration.birth_persistence import (
    CalibrationBirthPersister,
    PersistedCalibrationBirth,
)
from app.application.calibration.contract import (
    CONTRACT_VERSION_1_0,
    SOURCE_SELF_DECLARED,
    WARRANT_THIN,
    BeginnerOrHistoryPosture,
    CoreReadingCompleted,
    CoreReadingDeclaration,
    CurriculumExamScope,
    DeclaredPosture,
    IntendedSitting,
    PreviousAttemptsDeclaration,
    PreviouslyStudied,
    StudentCalibrationContract,
    StudyObjective,
    derive_declared_posture,
)
from app.application.calibration.result import (
    CalibrationBirthMetadata,
    CalibrationResult,
    KnowledgePriorMarker,
    PerformancePriorMarker,
    PriorProvenance,
)
from app.application.calibration.student_calibration_builder import (
    CalibrationBuildError,
    CalibrationValidationError,
    StudentCalibrationBuilder,
)
from app.application.calibration.study_plan_integration import (
    AlphaCalibrationDeclarations,
    CalibrationLaunchBlocked,
    CalibrationLaunchBlockReason,
    CalibrationLaunchContext,
    CalibrationSkippedWithoutTwin,
    StudyPlanCalibrationCoordinator,
)

__all__ = [
    "CONTRACT_VERSION_1_0",
    "SOURCE_SELF_DECLARED",
    "WARRANT_THIN",
    "AlphaCalibrationDeclarations",
    "BeginnerOrHistoryPosture",
    "CalibrationBirthMetadata",
    "CalibrationBirthPersister",
    "CalibrationBuildError",
    "CalibrationLaunchBlocked",
    "CalibrationLaunchBlockReason",
    "CalibrationLaunchContext",
    "CalibrationResult",
    "CalibrationSkippedWithoutTwin",
    "CalibrationValidationError",
    "CoreReadingCompleted",
    "CoreReadingDeclaration",
    "CurriculumExamScope",
    "DeclaredPosture",
    "IntendedSitting",
    "KnowledgePriorMarker",
    "PerformancePriorMarker",
    "PersistedCalibrationBirth",
    "PreviousAttemptsDeclaration",
    "PreviouslyStudied",
    "PriorProvenance",
    "StudentCalibrationBuilder",
    "StudentCalibrationContract",
    "StudyObjective",
    "StudyPlanCalibrationCoordinator",
    "derive_declared_posture",
]
