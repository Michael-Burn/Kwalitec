"""SB-001A Baseline routes — one question at a time.

Replaces student-facing Calibration as the educational entry point.
"""

from __future__ import annotations

import logging
from datetime import date

from flask import flash, redirect, render_template, session, url_for
from flask_login import current_user, login_required

from app.application.platform_integration.discovery import (
    PUBLISHED_CATEGORY_CODE,
)
from app.application.student_baseline import (
    BaselineFinalizeCoordinator,
    BaselineFinalizeError,
    BaselineSubjectScope,
    StudentBaselineService,
)
from app.application.student_baseline.enums import (
    CONFIDENCE_LABELS,
    EXAM_HISTORY_LABELS,
    EXPERIENCE_LABELS,
    OBJECTIVE_LABELS,
    POSITION_MODE_LABELS,
    BaselineStatus,
    ConfidenceBand,
    ExamHistory,
    LearningObjective,
    PositionMode,
    PreviousExperience,
)
from app.presentation.consolidation import (
    redirect_to_canonical_home,
    redirect_to_student_home,
)
from app.services import examination_catalogue as catalogue
from app.services.curriculum_engine_service import CurriculumEngineService
from app.services.subject_support_service import SubjectSupportService
from app.services.welcome_service import WelcomeService
from app.student_baseline import student_baseline_bp
from app.student_baseline.forms import (
    ConfidenceForm,
    ConfirmForm,
    ExamHistoryForm,
    ExperienceForm,
    ObjectiveForm,
    PositionForm,
)

logger = logging.getLogger(__name__)

TOTAL_BASELINE_STEPS = 6

STEP_META = {
    1: ("experience", "Have you studied this subject before?"),
    2: ("position", "Where should we begin?"),
    3: ("exam_history", "Have you sat this exam before?"),
    4: ("objective", "What would you like Kwalitec to do?"),
    5: ("confidence", "How confident do you currently feel?"),
    6: ("confirm", "Ready to begin"),
}


def _wizard_data() -> dict:
    return session.get("wizard_data") or {}


def _require_wizard():
    data = _wizard_data()
    if not data.get("exam_category") or not (
        data.get("exam_paper") or data.get("free_text_subject")
    ):
        flash("Please choose your exam first.", "info")
        return redirect(url_for("study_plan.wizard_step", step=1))
    if not data.get("exam_sitting") or not data.get("exam_date"):
        flash("Please set your exam date first.", "info")
        return redirect(url_for("study_plan.wizard_step", step=2))
    if not data.get("weekday_study_minutes"):
        flash("Please set your study availability first.", "info")
        return redirect(url_for("study_plan.wizard_step", step=3))
    return None


def _paper_or_subject(wizard: dict) -> str:
    category = wizard.get("exam_category", "")
    if catalogue.is_free_text_subject(category):
        return wizard.get("free_text_subject", "")
    return wizard.get("exam_paper", "")


def _discover_curriculum_version(category_code: str, paper_code: str) -> str | None:
    if (category_code or "").strip() == PUBLISHED_CATEGORY_CODE:
        return "published"
    if not category_code or not paper_code:
        return None
    engine = CurriculumEngineService()
    versions = engine.list_supported_versions(category_code, paper_code)
    if not versions:
        return None
    version = max(versions)
    if engine.curriculum_exists(category_code, paper_code, version):
        return version
    return None


def _build_scope(wizard: dict) -> BaselineSubjectScope:
    category = wizard["exam_category"]
    paper = _paper_or_subject(wizard)
    exam_name = catalogue.format_exam_name(category, paper)
    exam_date = wizard.get("exam_date")
    if isinstance(exam_date, str):
        exam_date = date.fromisoformat(exam_date)
    version = wizard.get("curriculum_version") or _discover_curriculum_version(
        category, paper
    )
    return BaselineSubjectScope(
        subject_key=StudentBaselineService.subject_key(category, paper),
        category_code=category,
        subject_code=paper,
        curriculum_version=version,
        exam_name=exam_name,
        exam_sitting=wizard.get("exam_sitting"),
        exam_date=exam_date,
        weekday_study_minutes=wizard.get("weekday_study_minutes"),
        weekend_study_minutes=wizard.get("weekend_study_minutes"),
        preferred_session_minutes=wizard.get("preferred_session_minutes"),
        study_preference=wizard.get("study_preference", "Mixed"),
        target_grade=wizard.get("target_grade")
        or (
            catalogue.get_target_choices(category)[0][0]
            if catalogue.get_target_choices(category)
            else "Pass"
        ),
    )


def _topic_choices(scope: BaselineSubjectScope) -> list[tuple[str, str]]:
    from app.application.student_baseline.topics import list_topic_choices

    return list_topic_choices(
        category_code=scope.category_code,
        subject_code=scope.subject_code,
        curriculum_version=scope.curriculum_version,
    )


def _ensure_draft(scope: BaselineSubjectScope):
    return StudentBaselineService.ensure_draft(current_user.id, scope)


def _render_step(step: int, form, *, scope, baseline, extra=None):
    key, question = STEP_META[step]
    ctx = {
        "form": form,
        "step": step,
        "total_steps": TOTAL_BASELINE_STEPS,
        "step_key": key,
        "step_title": question,
        "wizard_question": question,
        "wizard_helper": _helper_for(step),
        "button_text": "Begin learning" if step == 6 else "Continue",
        "scope": scope,
        "baseline": baseline,
        "back_url": _back_url(step),
    }
    if extra:
        ctx.update(extra)
    return render_template(f"student_baseline/step_{key}.html", **ctx)


def _helper_for(step: int) -> str:
    return {
        1: ("A quick check so we meet you where you are — "
            "not at chapter one by default."),
        2: "Choose a starting point on the official syllabus. No percentages needed.",
        3: "",
        4: "This guides how we open your plan — you can change direction later.",
        5: "Self-assessment only. We do not diagnose from this answer.",
        6: "Confirm once. Then we initialise your study profile and open Home.",
    }[step]


def _back_url(step: int) -> str | None:
    if step <= 1:
        return url_for("study_plan.wizard_step", step=3)
    return url_for("student_baseline.step", step=step - 1)


@student_baseline_bp.get("/")
@login_required
def start():
    """Entry: resume summary or first Baseline question."""
    blocked = _require_wizard()
    if blocked is not None:
        return blocked

    wizard = _wizard_data()
    # Apply calm deferred defaults for preference / target without asking.
    wizard.setdefault("study_preference", "Mixed")
    if not wizard.get("target_grade"):
        choices = catalogue.get_target_choices(wizard.get("exam_category", ""))
        wizard["target_grade"] = choices[0][0] if choices else "Pass"
    session["wizard_data"] = wizard
    session.modified = True

    scope = _build_scope(wizard)
    support = SubjectSupportService.resolve(
        scope.category_code,
        scope.subject_code,
        free_text_subject=catalogue.is_free_text_subject(scope.category_code),
    )
    if not support.allows_plan_creation and scope.curriculum_version != "published":
        from app.application.platform_integration.enrolment_bridge import (
            FounderStudentEnrolmentBridge,
        )

        if not FounderStudentEnrolmentBridge().should_use_bridge(
            category_code=scope.category_code, subject_code=scope.subject_code
        ):
            flash(support.explanation, "warning")
            return redirect(url_for("study_plan.wizard_step", step=1))

    complete = StudentBaselineService.get_complete(
        current_user.id, scope.subject_key
    )
    if complete is not None:
        return render_template(
            "student_baseline/resume.html",
            resume=StudentBaselineService.resume_view(complete),
            scope=scope,
            labels=_resume_labels(complete),
        )

    return redirect(url_for("student_baseline.step", step=1))


def _resume_labels(row) -> dict:
    labels = {}
    if row.experience:
        try:
            labels["experience"] = EXPERIENCE_LABELS[
                PreviousExperience(row.experience)
            ]
        except ValueError:
            labels["experience"] = row.experience
    if row.position_mode:
        try:
            labels["position"] = POSITION_MODE_LABELS[
                PositionMode(row.position_mode)
            ]
        except ValueError:
            labels["position"] = row.position_mode
    if row.learning_objective:
        try:
            labels["objective"] = OBJECTIVE_LABELS[
                LearningObjective(row.learning_objective)
            ]
        except ValueError:
            labels["objective"] = row.learning_objective
    if row.confidence:
        try:
            labels["confidence"] = CONFIDENCE_LABELS[
                ConfidenceBand(row.confidence)
            ]
        except ValueError:
            labels["confidence"] = row.confidence
    if row.exam_history:
        try:
            labels["exam_history"] = EXAM_HISTORY_LABELS[
                ExamHistory(row.exam_history)
            ]
        except ValueError:
            labels["exam_history"] = row.exam_history
    return labels


@student_baseline_bp.get("/step/<int:step>")
@login_required
def step(step: int):
    blocked = _require_wizard()
    if blocked is not None:
        return blocked
    if step < 1 or step > TOTAL_BASELINE_STEPS:
        return redirect(url_for("student_baseline.step", step=1))

    wizard = _wizard_data()
    scope = _build_scope(wizard)
    baseline = _ensure_draft(scope)

    if step == 1:
        form = ExperienceForm()
        if baseline.experience:
            form.experience.data = baseline.experience
        return _render_step(1, form, scope=scope, baseline=baseline)

    if step == 2:
        form = PositionForm()
        form.curriculum_topic_code.choices = [("", "Select a topic…")] + _topic_choices(
            scope
        )
        if baseline.position_mode:
            form.position_mode.data = baseline.position_mode
        if baseline.curriculum_topic_code:
            form.curriculum_topic_code.data = baseline.curriculum_topic_code
        return _render_step(2, form, scope=scope, baseline=baseline)

    if step == 3:
        form = ExamHistoryForm()
        if baseline.exam_history:
            form.exam_history.data = baseline.exam_history
        if baseline.highest_mark:
            form.highest_mark.data = baseline.highest_mark
        return _render_step(3, form, scope=scope, baseline=baseline)

    if step == 4:
        form = ObjectiveForm()
        if baseline.learning_objective:
            form.learning_objective.data = baseline.learning_objective
        return _render_step(4, form, scope=scope, baseline=baseline)

    if step == 5:
        form = ConfidenceForm()
        if baseline.confidence:
            form.confidence.data = baseline.confidence
        return _render_step(5, form, scope=scope, baseline=baseline)

    # Confirm
    decls = StudentBaselineService.declarations_from_row(baseline)
    if decls is None:
        flash("Please finish the earlier questions first.", "info")
        return redirect(url_for("student_baseline.step", step=1))
    form = ConfirmForm()
    return _render_step(
        6,
        form,
        scope=scope,
        baseline=baseline,
        extra={"summary": _resume_labels(baseline), "decls": decls},
    )


@student_baseline_bp.post("/step/<int:step>")
@login_required
def step_post(step: int):
    blocked = _require_wizard()
    if blocked is not None:
        return blocked
    if step < 1 or step > TOTAL_BASELINE_STEPS:
        return redirect(url_for("student_baseline.step", step=1))

    wizard = _wizard_data()
    scope = _build_scope(wizard)
    baseline = _ensure_draft(scope)

    if step == 1:
        form = ExperienceForm()
        if form.validate_on_submit():
            StudentBaselineService.save_answer(
                baseline.id,
                current_user.id,
                experience=form.experience.data,
            )
            return redirect(url_for("student_baseline.step", step=2))
        return _render_step(1, form, scope=scope, baseline=baseline)

    if step == 2:
        form = PositionForm()
        form.curriculum_topic_code.choices = [("", "Select a topic…")] + _topic_choices(
            scope
        )
        if form.validate_on_submit():
            mode = form.position_mode.data
            topic = form.curriculum_topic_code.data or None
            topic_options = [
                value for value, _label in form.curriculum_topic_code.choices if value
            ]
            if mode == PositionMode.CONTINUE_TOPIC.value and not topic_options:
                flash(
                    "A syllabus topic list is not available for this subject yet. "
                    "Choose “Start from the beginning”, or go back and pick another "
                    "exam if you expected a chapter list.",
                    "warning",
                )
                return _render_step(2, form, scope=scope, baseline=baseline)
            if mode == PositionMode.CONTINUE_TOPIC.value and not topic:
                flash("Please choose a topic to continue from.", "warning")
                return _render_step(2, form, scope=scope, baseline=baseline)
            StudentBaselineService.save_answer(
                baseline.id,
                current_user.id,
                position_mode=mode,
                curriculum_topic_code=topic
                if mode == PositionMode.CONTINUE_TOPIC.value
                else None,
                clear_topic=mode == PositionMode.START_BEGINNING.value,
            )
            return redirect(url_for("student_baseline.step", step=3))
        return _render_step(2, form, scope=scope, baseline=baseline)

    if step == 3:
        form = ExamHistoryForm()
        if form.validate_on_submit():
            StudentBaselineService.save_answer(
                baseline.id,
                current_user.id,
                exam_history=form.exam_history.data,
                highest_mark=form.highest_mark.data or "",
            )
            return redirect(url_for("student_baseline.step", step=4))
        return _render_step(3, form, scope=scope, baseline=baseline)

    if step == 4:
        form = ObjectiveForm()
        if form.validate_on_submit():
            StudentBaselineService.save_answer(
                baseline.id,
                current_user.id,
                learning_objective=form.learning_objective.data,
            )
            return redirect(url_for("student_baseline.step", step=5))
        return _render_step(4, form, scope=scope, baseline=baseline)

    if step == 5:
        form = ConfidenceForm()
        if form.validate_on_submit():
            StudentBaselineService.save_answer(
                baseline.id,
                current_user.id,
                confidence=form.confidence.data,
            )
            return redirect(url_for("student_baseline.step", step=6))
        return _render_step(5, form, scope=scope, baseline=baseline)

    # Finalize
    form = ConfirmForm()
    if not form.validate_on_submit():
        decls = StudentBaselineService.declarations_from_row(baseline)
        return _render_step(
            6,
            form,
            scope=scope,
            baseline=baseline,
            extra={"summary": _resume_labels(baseline), "decls": decls},
        )

    # Refresh baseline from DB
    baseline = StudentBaselineService.get_by_id(baseline.id, user_id=current_user.id)
    assert baseline is not None
    try:
        result = BaselineFinalizeCoordinator().finalize(
            user_id=current_user.id,
            baseline=baseline,
            wizard=wizard,
            scope=scope,
        )
    except BaselineFinalizeError as exc:
        flash(exc.message, "warning")
        return redirect(url_for("student_baseline.step", step=6))
    except Exception:
        logger.exception("Baseline finalize failed user=%s", current_user.id)
        flash(
            "We could not finish initialising just now. Your answers are saved — "
            "please try again.",
            "warning",
        )
        return redirect(url_for("student_baseline.step", step=6))

    session.pop("wizard_data", None)
    WelcomeService.mark_eligible(current_user.id)
    flash(result.message, "success")
    # Stay in Student Experience — dual-access Founders must not land on Console.
    return redirect_to_student_home()


@student_baseline_bp.post("/restart")
@login_required
def restart():
    """Student voluntary Baseline restart — history preserved."""
    blocked = _require_wizard()
    if blocked is not None:
        # Allow restart from home when subject known via query/session
        wizard = _wizard_data()
        if not wizard:
            flash("Open your subject enrolment path to restart Baseline.", "info")
            return redirect_to_canonical_home()

    wizard = _wizard_data()
    if not wizard.get("exam_category"):
        # Fall back: restart most recent complete for user if single subject
        rows = [
            r
            for r in StudentBaselineService.list_for_user(current_user.id)
            if r.status == BaselineStatus.COMPLETE.value
        ]
        if len(rows) == 1:
            draft = StudentBaselineService.restart_for_student(
                current_user.id, rows[0].subject_key
            )
            flash("Baseline restarted. Take a moment to update where you are.", "info")
            # Seed minimal wizard for continue
            session["wizard_data"] = {
                "exam_category": draft.category_code,
                "exam_paper": draft.subject_code,
                "subject_key": draft.subject_key,
            }
            session.modified = True
            return redirect(url_for("student_baseline.step", step=1))
        flash("Choose your exam to restart Baseline.", "info")
        return redirect(url_for("study_plan.wizard_step", step=1))

    scope = _build_scope(wizard)
    try:
        StudentBaselineService.restart_for_student(
            current_user.id, scope.subject_key
        )
    except ValueError:
        flash("No completed Baseline to restart.", "info")
        return redirect(url_for("student_baseline.start"))
    flash("Baseline restarted. Study history is unchanged.", "info")
    return redirect(url_for("student_baseline.step", step=1))


@student_baseline_bp.get("/for-plan/<int:study_plan_id>")
@login_required
def for_plan(study_plan_id: int):
    """Legacy Calibration entry compatibility — route into Baseline."""
    from app.extensions import db
    from app.models.study_plan import StudyPlan

    plan = db.session.get(StudyPlan, study_plan_id)
    if plan is None or plan.user_id != current_user.id:
        flash("Study plan not found.", "warning")
        return redirect(url_for("study_plan.index"))

    # Reconstruct wizard anchors from the plan for Baseline continuity.
    parts = (plan.exam_name or "").split(" ", 1)
    category = parts[0] if parts else ""
    paper = parts[1] if len(parts) == 2 else ""
    subject_key = StudentBaselineService.subject_key(category, paper)
    complete = StudentBaselineService.get_complete(current_user.id, subject_key)
    if complete is not None:
        return render_template(
            "student_baseline/resume.html",
            resume=StudentBaselineService.resume_view(complete),
            scope=None,
            labels=_resume_labels(complete),
            from_plan=True,
        )

    session["wizard_data"] = {
        "exam_category": category,
        "exam_paper": paper,
        "subject_key": subject_key,
        "exam_sitting": plan.exam_sitting,
        "exam_date": plan.exam_date.isoformat()
        if plan.exam_date
        else None,
        "weekday_study_minutes": plan.weekday_study_minutes,
        "weekend_study_minutes": plan.weekend_study_minutes,
        "preferred_session_minutes": plan.preferred_session_minutes,
        "study_preference": plan.study_preference,
        "target_grade": plan.target_grade,
        "curriculum_version": plan.curriculum_version,
        "existing_study_plan_id": plan.id,
    }
    session.modified = True
    return redirect(url_for("student_baseline.start"))
