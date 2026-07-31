"""Map SB-001A Baseline declarations onto Calibration Contract vocabulary.

Structural mapping only — never diagnoses mastery or readiness.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.application.calibration.contract import (
    SOURCE_SELF_DECLARED,
    WARRANT_THIN,
    PreviouslyStudied,
    StudyObjective,
)
from app.application.calibration.study_plan_integration import (
    AlphaCalibrationDeclarations,
)
from app.application.student_baseline.declarations import BaselineDeclarations
from app.application.student_baseline.enums import (
    ConfidenceBand,
    ExamHistory,
    LearningObjective,
    PositionMode,
    PreviousExperience,
)


@dataclass(frozen=True)
class StudyPlanBaselineFields:
    """Fields StudyPlanService already understands from Baseline."""

    current_position: str
    current_stage: str
    curriculum_topic_code: str | None
    completed_curriculum_topics: list[str]


_POSITION_LABELS = {
    "not_started": "I haven't started",
    "learning": "Learning new material",
    "completed": "Completed the syllabus once",
    "revising": "Currently revising",
}


def experience_to_position(experience: PreviousExperience) -> str:
    """Map experience band to StudyPlan current_position code."""
    return {
        PreviousExperience.BRAND_NEW: "not_started",
        PreviousExperience.STARTED: "learning",
        PreviousExperience.ABOUT_HALFWAY: "learning",
        PreviousExperience.MOSTLY_COMPLETED: "completed",
        PreviousExperience.REVISION_PHASE: "revising",
    }[experience]


def experience_to_previously_studied(
    experience: PreviousExperience,
) -> PreviouslyStudied:
    """Map experience to Calibration previously_studied token."""
    if experience is PreviousExperience.BRAND_NEW:
        return PreviouslyStudied.FIRST_TIME
    return PreviouslyStudied.PREVIOUSLY_STUDIED


def objective_to_study_objective(
    objective: LearningObjective,
) -> StudyObjective:
    """Map Baseline objective onto existing StudyObjective enum."""
    if objective is LearningObjective.CONTINUE:
        return StudyObjective.FINISH_REMAINING
    return StudyObjective.FIRST_SIT


def attempts_count(exam_history: ExamHistory) -> int:
    """Closed attempt count for Calibration contract assembly."""
    if exam_history is ExamHistory.PREVIOUSLY_ATTEMPTED:
        return 1
    return 0


def build_plan_fields(
    declarations: BaselineDeclarations,
    *,
    ordered_topic_codes: list[str] | None = None,
) -> StudyPlanBaselineFields:
    """Derive StudyPlan stage / topic / completed topics from Baseline."""
    position = experience_to_position(declarations.experience)
    topic: str | None = None
    completed: list[str] = []

    if declarations.learning_objective is LearningObjective.RESTART:
        position = "not_started"
        topic = None
        completed = []
    elif declarations.position_mode is PositionMode.CONTINUE_TOPIC:
        topic = declarations.curriculum_topic_code
        codes = ordered_topic_codes or []
        if topic and codes and topic in codes:
            idx = codes.index(topic)
            completed = list(codes[:idx])
        elif topic:
            completed = []
    elif declarations.position_mode is PositionMode.START_BEGINNING:
        topic = None
        completed = []

    stage = _POSITION_LABELS.get(position, position)
    return StudyPlanBaselineFields(
        current_position=position,
        current_stage=stage,
        curriculum_topic_code=topic,
        completed_curriculum_topics=completed,
    )


def to_alpha_declarations(
    declarations: BaselineDeclarations,
    *,
    completed_section_ids: list[str] | tuple[str, ...] | None = None,
) -> AlphaCalibrationDeclarations:
    """Assemble AlphaCalibrationDeclarations for Twin birth reuse."""
    previously = experience_to_previously_studied(declarations.experience)
    sections: tuple[str, ...] = ()
    if previously is PreviouslyStudied.PREVIOUSLY_STUDIED:
        sections = tuple(completed_section_ids or ())
        if (
            declarations.position_mode is PositionMode.CONTINUE_TOPIC
            and declarations.curriculum_topic_code
            and declarations.curriculum_topic_code not in sections
        ):
            # Declared current topic is exposure, not necessarily completed.
            pass

    return AlphaCalibrationDeclarations(
        previously_studied=previously,
        core_reading_completed="none",
        study_objective=objective_to_study_objective(
            declarations.learning_objective
        ),
        previous_attempts_count=attempts_count(declarations.exam_history),
        declared_completed_sections=sections,
        declaration_confirmation=True,
    )


def baseline_provenance_cargo(declarations: BaselineDeclarations) -> dict:
    """Self-declared Baseline cargo for Twin birth provenance."""
    return {
        "source": SOURCE_SELF_DECLARED,
        "warrant": WARRANT_THIN,
        "baseline_programme": "SB-001A",
        "experience": declarations.experience.value,
        "position_mode": declarations.position_mode.value,
        "curriculum_topic_code": declarations.curriculum_topic_code,
        "exam_history": declarations.exam_history.value,
        "highest_mark": declarations.highest_mark,
        "learning_objective": declarations.learning_objective.value,
        "confidence": declarations.confidence.value,
        "confidence_kind": "self_declared",
    }


def confidence_label(band: ConfidenceBand) -> str:
    """Human label for Founder / resume surfaces."""
    from app.application.student_baseline.enums import CONFIDENCE_LABELS

    return CONFIDENCE_LABELS[band]
