"""Student Calibration routes — Study Plan → Calibration → Dashboard.

Presentation owns auth, HTTP, forms, and redirects. Twin birth is owned by
Application ``StudyPlanCalibrationCoordinator`` (Builder → Persister →
Repository). Never invokes Readiness / Decision / Recommendation / Mission /
EducationalOrchestrator / DashboardAssembler directly.
"""

from __future__ import annotations

import logging

from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from app.application.calibration import (
    AlphaCalibrationDeclarations,
    CalibrationLaunchBlocked,
    CalibrationLaunchBlockReason,
    CalibrationValidationError,
    CoreReadingCompleted,
    PersistedCalibrationBirth,
    PreviouslyStudied,
    StudyObjective,
    StudyPlanCalibrationCoordinator,
)
from app.application.twin_repository import (
    TwinPersistenceFailure,
    TwinPersistenceFailureReason,
)
from app.calibration import calibration_bp
from app.calibration.forms import AlphaCalibrationForm
from app.models.study_plan import StudyPlan
from app.services.curriculum_engine_service import CurriculumEngineService
from app.services.study_plan_service import StudyPlanService

logger = logging.getLogger(__name__)


def _coordinator() -> StudyPlanCalibrationCoordinator:
    return StudyPlanCalibrationCoordinator()


def _load_owned_plan(study_plan_id: int) -> StudyPlan | None:
    from app.extensions import db

    plan = db.session.get(StudyPlan, study_plan_id)
    if plan is None or plan.user_id != current_user.id:
        return None
    return plan


def _current_exam_from_plan(plan: StudyPlan) -> str | None:
    parts = (plan.exam_name or "").split(" ", 1)
    if len(parts) == 2 and parts[1].strip():
        return parts[1].strip()
    return plan.exam_name or None


def _launch_from_plan(plan: StudyPlan):
    return _coordinator().build_launch_context(
        study_plan_id=plan.id,
        authorised_student_identity=str(current_user.id),
        curriculum_id=plan.curriculum_id,
        current_exam=_current_exam_from_plan(plan),
        sitting_label=plan.exam_sitting,
        sitting_date=plan.exam_date,
        weekday_study_minutes=plan.weekday_study_minutes,
        weekend_study_minutes=plan.weekend_study_minutes,
    )


def _section_choices(plan: StudyPlan) -> list[tuple[str, str]]:
    """Canonical curriculum section/topic ids for declared coverage — V1/V2 safe."""
    if not plan.curriculum_version:
        return []
    parts = (plan.exam_name or "").split(" ", 1)
    if len(parts) != 2:
        return []
    organisation, paper = parts[0], parts[1]
    engine = CurriculumEngineService()
    if not engine.curriculum_exists(organisation, paper, plan.curriculum_version):
        return []
    try:
        curriculum = engine.load_auto(organisation, paper, plan.curriculum_version)
        topics = CurriculumEngineService.get_topics_flat(curriculum)
        return [(t.code, f"{t.code} — {t.title}") for t in topics]
    except Exception:
        logger.exception(
            "Failed to load curriculum sections for calibration plan=%s", plan.id
        )
        return []


@calibration_bp.get("/after-plan/<int:study_plan_id>")
@login_required
def start(study_plan_id: int):
    """Launch Calibration immediately after Study Plan creation."""
    plan = _load_owned_plan(study_plan_id)
    if plan is None:
        flash("Study plan not found.", "warning")
        return redirect(url_for("study_plan.index"))

    launch = _launch_from_plan(plan)
    if isinstance(launch, CalibrationLaunchBlocked):
        if launch.reason is CalibrationLaunchBlockReason.MISSING_CURRICULUM:
            flash(
                "Your study plan was created. We cannot record educational "
                "history without an official syllabus for this exam — "
                "continuing without a calibrated starting profile.",
                "info",
            )
            return redirect(url_for("dashboard.index"))
        flash(
            "Calibration needs a successfully created study plan first.",
            "info",
        )
        return redirect(url_for("study_plan.wizard_step", step=1))

    if _coordinator().twin_already_exists(launch):
        flash(
            "Your study profile already includes declared history for this plan.",
            "info",
        )
        return redirect(url_for("dashboard.index"))

    form = AlphaCalibrationForm()
    form.completed_sections.choices = _section_choices(plan)
    return render_template(
        "calibration/alpha.html",
        form=form,
        study_plan=plan,
        launch=launch,
        title="Educational history",
    )


@calibration_bp.post("/after-plan/<int:study_plan_id>")
@login_required
def submit(study_plan_id: int):
    """Confirm Calibration declarations, beginner skip, or honest abandon."""
    plan = _load_owned_plan(study_plan_id)
    if plan is None:
        flash("Study plan not found.", "warning")
        return redirect(url_for("study_plan.index"))

    launch = _launch_from_plan(plan)
    if isinstance(launch, CalibrationLaunchBlocked):
        flash(
            "Calibration cannot complete without curriculum scope.",
            "info",
        )
        return redirect(url_for("dashboard.index"))

    form = AlphaCalibrationForm()
    form.completed_sections.choices = _section_choices(plan)

    # Explicit beginner skip — empty-history Birth Twin, never Mid theatre.
    if form.skip_beginner.data:
        return _finish_beginner_skip(launch)

    # Abandon without declaration — Study Plan kept; no Twin invented.
    if form.abandon.data:
        _coordinator().abandon_without_twin(launch)
        flash(
            "Study plan created. We have not recorded educational history yet — "
            "guidance will start honestly from a fresh beginning.",
            "info",
        )
        return redirect(url_for("dashboard.index"))

    if not form.validate_on_submit():
        return render_template(
            "calibration/alpha.html",
            form=form,
            study_plan=plan,
            launch=launch,
            title="Educational history",
        )

    if form.confirm.data != "yes":
        flash("Please confirm your declarations to continue.", "warning")
        return render_template(
            "calibration/alpha.html",
            form=form,
            study_plan=plan,
            launch=launch,
            title="Educational history",
        )

    attempts = form.previous_attempts_count.data
    if attempts is None:
        attempts = 0

    declarations = AlphaCalibrationDeclarations(
        previously_studied=form.previously_studied.data,
        core_reading_completed=form.core_reading_completed.data or "none",
        study_objective=form.study_objective.data or StudyObjective.FIRST_SIT.value,
        previous_attempts_count=int(attempts),
        declared_completed_sections=tuple(form.completed_sections.data or ()),
        declaration_confirmation=True,
    )

    # First-time students must not carry attempt / section theatre.
    if declarations.previously_studied == PreviouslyStudied.FIRST_TIME.value or (
        declarations.previously_studied is PreviouslyStudied.FIRST_TIME
    ):
        declarations = AlphaCalibrationDeclarations(
            previously_studied=PreviouslyStudied.FIRST_TIME,
            core_reading_completed=CoreReadingCompleted.NONE
            if form.core_reading_completed.data == "none"
            else form.core_reading_completed.data,
            study_objective=form.study_objective.data or StudyObjective.FIRST_SIT.value,
            previous_attempts_count=0,
            declared_completed_sections=(),
            declaration_confirmation=True,
        )

    return _persist_and_redirect(launch, declarations)


def _finish_beginner_skip(launch):
    try:
        result = _coordinator().complete_beginner_skip(launch)
    except CalibrationValidationError as exc:
        logger.warning("Beginner skip calibration validation failed: %s", exc)
        flash(
            "We could not record a beginner starting profile. "
            "Your study plan is ready — continuing honestly.",
            "warning",
        )
        return redirect(url_for("dashboard.index"))

    if isinstance(result, TwinPersistenceFailure):
        return _handle_persist_failure(result, launch.study_plan_id)

    flash(
        "Study plan created. Starting from scratch — we'll refine guidance "
        "as you study.",
        "success",
    )
    return redirect(url_for("dashboard.index"))


def _persist_and_redirect(launch, declarations: AlphaCalibrationDeclarations):
    try:
        result = _coordinator().complete(launch, declarations)
    except CalibrationValidationError as exc:
        logger.warning("Calibration validation failed: %s", exc)
        flash(
            "Please check your answers — some declarations don't fit together "
            "yet. Nothing was recorded as mastery.",
            "warning",
        )
        return redirect(
            url_for("calibration.start", study_plan_id=launch.study_plan_id)
        )

    if isinstance(result, TwinPersistenceFailure):
        return _handle_persist_failure(result, launch.study_plan_id)

    assert isinstance(result, PersistedCalibrationBirth)
    flash(
        "Study plan created. We've recorded what you declared about your "
        "educational history — not measured mastery. Here's your dashboard.",
        "success",
    )
    return redirect(url_for("dashboard.index"))


def _handle_persist_failure(
    failure: TwinPersistenceFailure, study_plan_id: int
):
    if failure.reason is TwinPersistenceFailureReason.DUPLICATE:
        flash(
            "Your study profile already exists for this plan. "
            "Continuing to the dashboard.",
            "info",
        )
        return redirect(url_for("dashboard.index"))

    logger.warning(
        "Calibration birth persist failed for plan=%s reason=%s detail=%s",
        study_plan_id,
        failure.reason.value,
        failure.detail,
    )
    flash(
        "Your study plan was created, but we could not save your declared "
        "history right now. Continuing honestly without inventing readiness.",
        "warning",
    )
    return redirect(url_for("dashboard.index"))


@calibration_bp.get("/resume")
@login_required
def resume():
    """Resume Calibration for the active Study Plan when Twin is still absent."""
    plan = StudyPlanService.get_user_active_plan(current_user.id)
    if plan is None:
        flash("Create a study plan first — then we can record your history.", "info")
        return redirect(url_for("study_plan.wizard_step", step=1))
    return redirect(url_for("calibration.start", study_plan_id=plan.id))
