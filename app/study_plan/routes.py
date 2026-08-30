"""Study Plan blueprint routes — exam-aware wizard."""

from __future__ import annotations

import logging
from datetime import date

from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required

from app.application.educational_runtime_engine.coexistence import (
    RuntimeAuthority,
)
from app.application.educational_runtime_engine.exceptions import (
    EnrolmentAlreadyExists,
)
from app.application.platform_integration.discovery import (
    PUBLISHED_CATEGORY_CODE,
    PublishedSubjectDiscoveryService,
)
from app.application.platform_integration.enrolment_bridge import (
    FounderStudentEnrolmentBridge,
)
from app.application.platform_integration.exceptions import (
    BridgeEnrolmentBlocked,
    PublishedSubjectNotDiscoverable,
)
from app.application.platform_integration.routing import RuntimeRoutingService
from app.application.platform_integration.subject_catalogue import (
    SubjectCatalogueService,
)
from app.presentation.consolidation import redirect_to_student_home
from app.presentation.student.services.choose_exam_service import ChooseExamService
from app.services import examination_catalogue as catalogue
from app.services.curriculum_engine_service import CurriculumEngineService
from app.services.study_plan_service import StudyPlanService
from app.services.subject_support_service import SubjectSupportService
from app.study_plan.forms import (
    ExamSittingForm,
    StudyAvailabilityForm,
    StudyPlanReviewForm,
    SubjectCatalogueForm,
)

logger = logging.getLogger(__name__)

study_plan_bp = Blueprint("study_plan", __name__, url_prefix="/study-plan")

# PX-002 / SB-001A visible onboarding path:
# Welcome → Choose Exam → Exam Date → Study Availability → Baseline → Home
TOTAL_STEPS = 4

STEP_TITLES = {
    1: "Choose Exam",
    2: "Exam Date",
    3: "Study Availability",
    4: "Baseline",
}


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────


def _position_label(code: str) -> str:
    """Map a current_position code to a human-readable label."""
    return {
        "not_started": "I haven't started",
        "learning": "Learning new material",
        "completed": "Completed the syllabus once",
        "revising": "Currently revising",
    }.get(code, code)


def _build_current_stage(position: str) -> str:
    """Return the human-readable study stage label from a position code.

    Only the study stage itself is returned (e.g. "Learning new material").
    The curriculum topic code is stored separately in curriculum_topic_code.
    """
    return _position_label(position)


def _parse_current_stage(current_stage: str) -> tuple[str, str]:
    """Split a stored current_stage back into (position_code, topic)."""
    if not current_stage:
        return "not_started", ""
    if current_stage.startswith("I haven't started"):
        return "not_started", ""
    if current_stage.startswith("Learning new material"):
        topic = ""
        if ": " in current_stage:
            topic = current_stage.split(": ", 1)[1]
        return "learning", topic
    if current_stage.startswith("Completed the syllabus once"):
        return "completed", ""
    if current_stage.startswith("Currently revising"):
        return "revising", ""
    return "learning", current_stage


# ── Curriculum version discovery ──────────────────────────────────────────
# Versions are discovered from on-disk syllabus JSON via the Curriculum Engine.
# Adding a new paper requires only a V2 JSON file under app/curriculum/data/ —
# no per-paper entries here.


def _discover_curriculum_version(category_code: str, paper_code: str) -> str | None:
    """Return the latest on-disk curriculum version for an examination.

    Discovers versions through ``CurriculumEngineService.list_supported_versions``
    so CS1, CB2, CM1, and future papers stay curriculum-driven without a
    hardcoded paper map.

    Args:
        category_code: Examining body code (e.g. ``"IFoA"``).
        paper_code: Paper code (e.g. ``"CB2"``).

    Returns:
        Latest available version string (e.g. ``"2026"``), or ``None`` when
        no syllabus JSON exists for the pair.
    """
    if not category_code or not paper_code:
        return None

    engine = CurriculumEngineService()
    versions = engine.list_supported_versions(category_code, paper_code)
    if not versions:
        return None

    # Year strings sort lexicographically in chronological order.
    return max(versions)


def _resolve_curriculum_version(
    category_code: str, paper_code: str
) -> str | None | bool:
    """Determine the curriculum version for a given examination.

    Returns:
        * ``str`` — curriculum version to use (e.g. ``"2026"``).
        * ``"published"`` — founder-published subject (Runtime C; no JSON syllabus).
        * ``None`` — no curriculum is associated with this exam; proceed normally.
        * ``False`` — a curriculum was discovered but could not be verified on disk.
    """
    if (category_code or "").strip() == PUBLISHED_CATEGORY_CODE:
        return "published"

    version = _discover_curriculum_version(category_code, paper_code)
    if version is None:
        return None  # No on-disk syllabus — continue without curriculum binding.

    engine = CurriculumEngineService()
    # exists() normalises casing internally.
    if engine.curriculum_exists(category_code, paper_code, version):
        logger.debug(
            "Curriculum %s/%s/%s found — associating with study plan.",
            category_code,
            paper_code,
            version,
        )
        return version

    logger.warning(
        "Discovered curriculum %s/%s/%s was not verifiable on disk.",
        category_code,
        paper_code,
        version,
    )
    flash(
        f"A curriculum for {category_code} {paper_code} (version {version}) "
        f"is not yet available. Please select another examination or try again later.",
        "warning",
    )
    return False


# ─────────────────────────────────────────────────────────────────────────────
# Index
# ─────────────────────────────────────────────────────────────────────────────


@study_plan_bp.get("/")
@login_required
def index():
    """Redirect to the active study plan or wizard if none exists."""
    active_plan = StudyPlanService.get_user_active_plan(current_user.id)
    if active_plan:
        return redirect(url_for("study_plan.view_plan", study_plan_id=active_plan.id))
    return redirect(url_for("study_plan.wizard_step", step=1))


# ─────────────────────────────────────────────────────────────────────────────
# Wizard — GET
# ─────────────────────────────────────────────────────────────────────────────


@study_plan_bp.get("/wizard/<int:step>")
@login_required
def wizard_step(step: int):
    """Handle a specific step of the study plan wizard."""
    if step < 1 or step > TOTAL_STEPS:
        return redirect(url_for("study_plan.wizard_step", step=1))

    if step == 1:
        return _handle_step_1()
    if step == 2:
        return _handle_step_2()
    if step == 3:
        return _handle_step_3()
    if step == 4:
        return redirect(url_for("student_baseline.start"))
    return redirect(url_for("study_plan.wizard_step", step=1))


# ─────────────────────────────────────────────────────────────────────────────
# Wizard — POST
# ─────────────────────────────────────────────────────────────────────────────


@study_plan_bp.post("/wizard/<int:step>")
@login_required
def wizard_step_post(step: int):
    """Handle form submission for a wizard step."""
    if step < 1 or step > TOTAL_STEPS:
        return redirect(url_for("study_plan.wizard_step", step=1))

    if "wizard_data" not in session:
        session["wizard_data"] = {}

    if step == 1:
        return _handle_step_1_post()
    if step == 2:
        return _handle_step_2_post()
    if step == 3:
        return _handle_step_3_post()
    if step == 4:
        return redirect(url_for("student_baseline.start"))
    return redirect(url_for("study_plan.wizard_step", step=1))


# ─────────────────────────────────────────────────────────────────────────────
# Step 1 — Examination category
# ─────────────────────────────────────────────────────────────────────────────


def _discovery() -> PublishedSubjectDiscoveryService:
    """Return the PI-002A discovery service (flag-gated)."""
    return PublishedSubjectDiscoveryService()


def _catalogue() -> SubjectCatalogueService:
    """Return the PX-002 Subject Catalogue projection."""
    return SubjectCatalogueService(discovery=_discovery())


def _resolve_wizard_category(category_code: str):
    """Resolve a wizard category including published subjects."""
    return _discovery().get_category(category_code) or catalogue.get_category(
        category_code
    )


def _wizard_selection_support(wizard_data: dict):
    """Resolve support status for the current wizard selection."""
    category_code = wizard_data.get("exam_category", "")
    free_text = catalogue.is_free_text_subject(category_code)
    if free_text:
        paper = wizard_data.get("free_text_subject", "")
    else:
        paper = wizard_data.get("exam_paper", "")
    return SubjectSupportService.resolve(
        category_code, paper, free_text_subject=free_text
    )


def _require_supported_selection():
    """Redirect to Choose Exam when selection cannot create a real plan."""
    wizard_data = session.get("wizard_data", {})
    category_code = wizard_data.get("exam_category")
    if not category_code:
        flash("Please complete the wizard from the beginning.", "info")
        return redirect(url_for("study_plan.wizard_step", step=1))

    has_paper = bool(
        wizard_data.get("exam_paper") or wizard_data.get("free_text_subject")
    )
    if not has_paper:
        flash("Please choose your exam first.", "info")
        return redirect(url_for("study_plan.wizard_step", step=1))

    support = _wizard_selection_support(wizard_data)
    if not support.allows_plan_creation:
        flash(support.explanation, "warning")
        return redirect(url_for("study_plan.wizard_step", step=1))
    return None


def _apply_deferred_defaults(wizard_data: dict) -> None:
    """Fold Position / Learning Style / Target with calm defaults (PX-001)."""
    wizard_data.setdefault("current_position", "not_started")
    wizard_data.setdefault("current_topic", "")
    wizard_data.setdefault("study_preference", "Mixed")
    if not wizard_data.get("target_grade"):
        category_code = wizard_data.get("exam_category", "")
        choices = catalogue.get_target_choices(category_code) if category_code else []
        wizard_data["target_grade"] = choices[0][0] if choices else "Pass"


def _prepare_catalogue_form(form: SubjectCatalogueForm) -> SubjectCatalogueForm:
    """Bind Ready subject choices; Coming Soon is not selectable."""
    entries = _catalogue().list_entries(include_coming_soon=True)
    form.subject_key.choices = [
        (e.subject_key, e.name) for e in entries if e.selectable
    ]
    return form


# ─────────────────────────────────────────────────────────────────────────────
# Step 1 — Choose Exam (Subject Catalogue)
# ─────────────────────────────────────────────────────────────────────────────


def _choose_exam() -> ChooseExamService:
    """Return the DX-005B Choose Exam discovery projector."""
    return ChooseExamService(catalogue=_catalogue())


def _render_choose_exam(form, *, support_gate=None):
    selected = (form.subject_key.data or "").strip()
    discovery = _choose_exam().build(
        selected_key=selected,
        query=request.args.get("q", ""),
        status_filter=request.args.get("status", "all"),
        sort=request.args.get("sort", "updated"),
        family_filter=request.args.get("family", "all"),
    )
    return render_template(
        "study_plan/wizard_step_1.html",
        form=form,
        step=1,
        total_steps=TOTAL_STEPS,
        step_title=STEP_TITLES[1],
        discovery=discovery,
        support_gate=support_gate,
    )


def _handle_step_1():
    """Display Subject Catalogue for Choose Exam."""
    form = _prepare_catalogue_form(SubjectCatalogueForm())
    wizard_data = session.get("wizard_data", {})
    org = wizard_data.get("exam_category")
    paper = wizard_data.get("exam_paper")
    if org and paper:
        form.subject_key.data = f"{org}:{paper}"
    return _render_choose_exam(form)


def _handle_step_1_post():
    """Process Subject Catalogue selection — Ready only."""
    form = _prepare_catalogue_form(SubjectCatalogueForm())
    catalogue = _catalogue()
    if form.validate_on_submit():
        subject_key = form.subject_key.data
        entry = catalogue.get_entry(subject_key)
        parsed = catalogue.parse_subject_key(subject_key)
        if entry is None or parsed is None or not entry.selectable:
            gate = (
                entry.explanation
                if entry is not None
                else "Please choose a Ready subject to continue."
            )
            # Reuse support gate shape when possible.
            support = None
            if parsed is not None:
                support = SubjectSupportService.resolve(parsed[0], parsed[1])
            if support is not None and not support.allows_plan_creation:
                return _render_choose_exam(form, support_gate=support)
            flash(gate if isinstance(gate, str) else str(gate), "warning")
            return _render_choose_exam(form)

        org, paper = parsed
        session["wizard_data"]["exam_category"] = org
        session["wizard_data"]["exam_paper"] = paper
        session["wizard_data"]["subject_key"] = subject_key
        session["wizard_data"].pop("free_text_subject", None)
        for key in ("exam_sitting", "exam_date", "target_grade"):
            session["wizard_data"].pop(key, None)
        session.modified = True
        return redirect(url_for("study_plan.wizard_step", step=2))
    return _render_choose_exam(form)


# ─────────────────────────────────────────────────────────────────────────────
# Step 2 — Exam Date
# ─────────────────────────────────────────────────────────────────────────────


def _handle_step_2():
    """Display exam sitting/date form."""
    blocked = _require_supported_selection()
    if blocked is not None:
        return blocked

    wizard_data = session.get("wizard_data", {})
    category_code = wizard_data.get("exam_category")
    form = ExamSittingForm()
    sitting_choices = catalogue.get_sitting_choices(category_code)
    form.exam_sitting.choices = sitting_choices
    show_sitting = not catalogue.is_placeholder_sitting_menu(sitting_choices)
    if "exam_sitting" in wizard_data:
        form.exam_sitting.data = wizard_data["exam_sitting"]
    if "exam_date" in wizard_data:
        form.populate_from_exam_date(wizard_data["exam_date"])
    return render_template(
        "study_plan/wizard_step_3.html",
        form=form,
        step=2,
        total_steps=TOTAL_STEPS,
        step_title=STEP_TITLES[2],
        show_sitting=show_sitting,
    )


def _handle_step_2_post():
    """Process exam sitting/date form."""
    blocked = _require_supported_selection()
    if blocked is not None:
        return blocked

    wizard_data = session.get("wizard_data", {})
    category_code = wizard_data.get("exam_category")
    form = ExamSittingForm()
    sitting_choices = catalogue.get_sitting_choices(category_code)
    form.exam_sitting.choices = sitting_choices
    show_sitting = not catalogue.is_placeholder_sitting_menu(sitting_choices)
    if form.validate_on_submit():
        exam_date = form.exam_date
        if show_sitting:
            sitting = form.exam_sitting.data
        else:
            sitting = catalogue.sitting_label_from_exam_date(exam_date)
        session["wizard_data"]["exam_sitting"] = sitting
        if hasattr(exam_date, "isoformat"):
            session["wizard_data"]["exam_date"] = exam_date.isoformat()
        else:
            session["wizard_data"]["exam_date"] = str(exam_date)
        session.modified = True
        return redirect(url_for("study_plan.wizard_step", step=3))
    return render_template(
        "study_plan/wizard_step_3.html",
        form=form,
        step=2,
        total_steps=TOTAL_STEPS,
        step_title=STEP_TITLES[2],
        show_sitting=show_sitting,
    )


# ─────────────────────────────────────────────────────────────────────────────
# Step 3 — Study Availability
# ─────────────────────────────────────────────────────────────────────────────


def _handle_step_3():
    """Display study availability form."""
    blocked = _require_supported_selection()
    if blocked is not None:
        return blocked

    form = StudyAvailabilityForm()
    wizard_data = session.get("wizard_data", {})
    if "weekday_study_minutes" in wizard_data:
        form.weekday_study_minutes.data = wizard_data["weekday_study_minutes"]
    if "weekend_study_minutes" in wizard_data:
        form.weekend_study_minutes.data = wizard_data["weekend_study_minutes"]
    if "preferred_session_minutes" in wizard_data:
        form.preferred_session_minutes.data = wizard_data["preferred_session_minutes"]
    return render_template(
        "study_plan/wizard_step_5.html",
        form=form,
        step=3,
        total_steps=TOTAL_STEPS,
        step_title=STEP_TITLES[3],
    )


def _handle_step_3_post():
    """Process study availability, apply deferred defaults, begin learning."""
    blocked = _require_supported_selection()
    if blocked is not None:
        return blocked

    form = StudyAvailabilityForm()
    if form.validate_on_submit():
        session["wizard_data"]["weekday_study_minutes"] = (
            form.weekday_study_minutes.data
        )
        session["wizard_data"]["weekend_study_minutes"] = (
            form.weekend_study_minutes.data
        )
        session["wizard_data"]["preferred_session_minutes"] = (
            form.preferred_session_minutes.data
        )
        _apply_deferred_defaults(session["wizard_data"])
        session.modified = True
        return redirect(url_for("student_baseline.start"))
    return render_template(
        "study_plan/wizard_step_5.html",
        form=form,
        step=3,
        total_steps=TOTAL_STEPS,
        step_title=STEP_TITLES[3],
    )


# ─────────────────────────────────────────────────────────────────────────────
# Review / Begin Learning
# ─────────────────────────────────────────────────────────────────────────────


@study_plan_bp.get("/review")
@login_required
def review():
    """Begin Learning — SB-001A routes through Baseline before plan creation."""
    wizard_data = session.get("wizard_data", {})

    if not wizard_data or "exam_category" not in wizard_data:
        flash("Please complete the wizard from the beginning.", "info")
        return redirect(url_for("study_plan.wizard_step", step=1))

    _apply_deferred_defaults(wizard_data)
    session["wizard_data"] = wizard_data
    session.modified = True
    return redirect(url_for("student_baseline.start"))


@study_plan_bp.post("/review")
@login_required
def review_post():
    """Legacy POST — refuse hollow subjects; else Baseline owns finalise."""
    # Keep Coming Soon / unsupported refusal at this legacy entry so students
    # never enter Baseline for a subject that cannot create a plan (PTP-001).
    blocked = _require_supported_selection()
    if blocked is not None:
        return blocked
    return redirect(url_for("student_baseline.start"))


# Review create-on-POST removed — SB-001A Baseline finalize owns plan creation.


def _confirm_availability_line(review_data: dict) -> str:
    weekday = review_data.get("weekday_study_minutes")
    weekend = review_data.get("weekend_study_minutes")
    session_len = review_data.get("preferred_session_minutes")
    if weekday is None or weekend is None:
        return ""
    sitting = review_data.get("exam_sitting") or ""
    parts = [f"Weekdays {weekday} mins · Weekend {weekend} mins"]
    if session_len:
        parts.append(f"Sessions {session_len} mins")
    if sitting:
        parts.append(sitting)
    return " · ".join(parts)


def _confirm_defaults_line(wizard_data: dict) -> str:
    """One quiet line for applied defaults the student did not choose."""
    # Position / style / target are deferred defaults (PX-001) — disclose once.
    return "Starting position, learning style, and target applied as defaults."


def _build_review_data(wizard_data: dict) -> dict:
    """Build a structured dict for the review template sections."""
    category_code = wizard_data.get("exam_category", "")
    category = _resolve_wizard_category(category_code)

    # Paper / subject display
    if catalogue.is_free_text_subject(category_code):
        paper_label = wizard_data.get("free_text_subject", "")
    else:
        paper_label = wizard_data.get("exam_paper", "")

    exam_name = (
        catalogue.format_exam_name(category_code, paper_label) if paper_label else ""
    )

    # Exam date + days remaining
    exam_date_str = wizard_data.get("exam_date", "")
    days_remaining = None
    exam_date_display = exam_date_str
    if exam_date_str:
        try:
            exam_date = (
                date.fromisoformat(exam_date_str)
                if isinstance(exam_date_str, str)
                else exam_date_str
            )
            exam_date_display = exam_date.strftime("%B %d, %Y")
            days_remaining = (exam_date - date.today()).days
        except (ValueError, TypeError):
            pass

    # Current position
    position_code = wizard_data.get("current_position", "")
    position_label = _position_label(position_code)
    current_topic = wizard_data.get("current_topic", "")
    completed_curriculum_topics = wizard_data.get("completed_curriculum_topics", [])

    return {
        "category": category,
        "category_code": category_code,
        "paper_label": paper_label,
        "exam_name": exam_name,
        "exam_sitting": wizard_data.get("exam_sitting", ""),
        "exam_date_display": exam_date_display,
        "days_remaining": days_remaining,
        "position_label": position_label,
        "current_topic": current_topic,
        "completed_curriculum_topics": completed_curriculum_topics,
        "weekday_study_minutes": wizard_data.get("weekday_study_minutes", ""),
        "weekend_study_minutes": wizard_data.get("weekend_study_minutes", ""),
        "preferred_session_minutes": wizard_data.get("preferred_session_minutes", ""),
        "study_preference": wizard_data.get("study_preference", ""),
        "target_grade": wizard_data.get("target_grade", ""),
    }


# ─────────────────────────────────────────────────────────────────────────────
# View & list plans
# ─────────────────────────────────────────────────────────────────────────────


@study_plan_bp.get("/<int:study_plan_id>")
@login_required
def view_plan(study_plan_id: int):
    """View a study plan."""
    study_plan = StudyPlanService.get_plan(study_plan_id)

    if not study_plan:
        flash("Study plan not found.", "warning")
        return redirect(url_for("study_plan.index"))

    if study_plan.user_id != current_user.id:
        flash("You can only view your own study plans.", "danger")
        return redirect(url_for("study_plan.index"))

    twin_progress_by_topic = None
    from app.application.student_twin.cutover import (
        phase2_twin_cutover_enabled,
    )
    from app.services.twin_cutover_service import (
        study_plan_progress_display_map,
    )

    if phase2_twin_cutover_enabled():
        topics = (
            list(study_plan.curriculum.topics)
            if study_plan.curriculum and study_plan.curriculum.topics
            else None
        )
        twin_progress_by_topic = study_plan_progress_display_map(
            user_id=current_user.id,
            topic_progress_rows=list(current_user.topic_progress or ()),
            topics=topics,
        )

    return render_template(
        "study_plan/view.html",
        study_plan=study_plan,
        title="Study Plan",
        twin_progress_by_topic=twin_progress_by_topic,
    )


@study_plan_bp.get("/plans/all")
@login_required
def list_plans():
    """List all study plans for the user."""
    plans = StudyPlanService.get_user_plans(current_user.id)
    return render_template("study_plan/list.html", plans=plans, title="Study Plan")


# ─────────────────────────────────────────────────────────────────────────────
# Edit Study Plan
# ─────────────────────────────────────────────────────────────────────────────


@study_plan_bp.get("/<int:study_plan_id>/edit")
@login_required
def edit_plan(study_plan_id: int):
    """Display the edit form for a study plan."""
    study_plan = StudyPlanService.get_plan(study_plan_id)

    if not study_plan:
        flash("Study plan not found.", "warning")
        return redirect(url_for("study_plan.list_plans"))

    if study_plan.user_id != current_user.id:
        flash("You can only edit your own study plans.", "danger")
        return redirect(url_for("study_plan.list_plans"))

    if study_plan.archived:
        flash("Cannot edit an archived study plan.", "warning")
        return redirect(url_for("study_plan.list_plans"))

    from app.study_plan.forms import EditStudyPlanForm

    form = EditStudyPlanForm(obj=study_plan)
    form.populate_from_exam_date(study_plan.exam_date)

    # Load curriculum topics for the checkbox list if applicable
    curriculum_topics = []
    completed_curriculum_topics = []
    curriculum_version = study_plan.curriculum_version

    if curriculum_version:
        parts = study_plan.exam_name.split(" ", 1)
        if len(parts) == 2:
            organisation, paper = parts
            engine = CurriculumEngineService()
            if engine.curriculum_exists(organisation, paper, curriculum_version):
                try:
                    curriculum = engine.load_auto(
                        organisation, paper, curriculum_version
                    )
                    curriculum_topics = CurriculumEngineService.get_topics_flat(
                        curriculum
                    )
                    # Determine which topics are already completed
                    from app.models.topic_progress import TopicProgress

                    completed_progress = TopicProgress.query.filter_by(
                        user_id=current_user.id,
                        completed=True,
                    ).all()
                    completed_topic_ids = {tp.topic_id for tp in completed_progress}
                    from app.models.curriculum import Topic as DBTopic

                    for engine_topic in curriculum_topics:
                        db_topic = DBTopic.query.filter_by(
                            curriculum_id=study_plan.curriculum_id,
                            name=engine_topic.title,
                        ).first()
                        if db_topic and db_topic.id in completed_topic_ids:
                            completed_curriculum_topics.append(engine_topic.code)
                except Exception:
                    logger.exception("Failed to load curriculum for edit form.")

    return render_template(
        "study_plan/edit.html",
        form=form,
        study_plan=study_plan,
        curriculum_topics=curriculum_topics,
        completed_curriculum_topics=completed_curriculum_topics,
    )


@study_plan_bp.post("/<int:study_plan_id>/edit")
@login_required
def edit_plan_post(study_plan_id: int):
    """Handle study plan edit form submission."""
    study_plan = StudyPlanService.get_plan(study_plan_id)

    if not study_plan:
        flash("Study plan not found.", "warning")
        return redirect(url_for("study_plan.list_plans"))

    if study_plan.user_id != current_user.id:
        flash("You can only edit your own study plans.", "danger")
        return redirect(url_for("study_plan.list_plans"))

    if study_plan.archived:
        flash("Cannot edit an archived study plan.", "warning")
        return redirect(url_for("study_plan.list_plans"))

    from app.study_plan.forms import EditStudyPlanForm

    form = EditStudyPlanForm()

    if form.validate_on_submit():
        try:
            # Collect completed curriculum topic codes from the form
            completed_codes = request.form.getlist("curriculum_topic")
            completed_codes = [c.strip() for c in completed_codes if c.strip()]

            # Determine curriculum_topic_code: first topic NOT in completed set
            curriculum_topic_code = study_plan.curriculum_topic_code
            curriculum_version = study_plan.curriculum_version
            if curriculum_version:
                parts = study_plan.exam_name.split(" ", 1)
                if len(parts) == 2:
                    engine = CurriculumEngineService()
                    if engine.curriculum_exists(parts[0], parts[1], curriculum_version):
                        try:
                            cur = engine.load_auto(
                                parts[0], parts[1], curriculum_version
                            )
                            completed_set = set(completed_codes)
                            for topic in CurriculumEngineService.get_topics_flat(cur):
                                if topic.code not in completed_set:
                                    curriculum_topic_code = topic.code
                                    break
                        except Exception:
                            pass

            update_kwargs = {
                "exam_name": form.exam_name.data,
                "exam_sitting": form.exam_sitting.data,
                "exam_date": form.exam_date,
                "weekday_study_minutes": form.weekday_study_minutes.data,
                "weekend_study_minutes": form.weekend_study_minutes.data,
                "current_stage": form.current_stage.data,
                "study_preference": form.study_preference.data,
                "target_grade": form.target_grade.data,
                "preferred_session_minutes": form.preferred_session_minutes.data,
                "curriculum_topic_code": curriculum_topic_code,
                "completed_curriculum_topics": completed_codes,
            }

            StudyPlanService.update_study_plan(
                study_plan_id=study_plan_id,
                user_id=current_user.id,
                **update_kwargs,
            )

            flash("Study plan updated successfully!", "success")
            return redirect(
                url_for("study_plan.view_plan", study_plan_id=study_plan_id)
            )
        except ValueError as e:
            flash(str(e), "danger")

    return render_template(
        "study_plan/edit.html",
        form=form,
        study_plan=study_plan,
        curriculum_topics=[],
        completed_curriculum_topics=[],
    )


# ─────────────────────────────────────────────────────────────────────────────
# Delete Study Plan
# ─────────────────────────────────────────────────────────────────────────────


@study_plan_bp.post("/<int:study_plan_id>/delete")
@login_required
def delete_plan(study_plan_id: int):
    """Delete a study plan after confirmation."""
    from app.models.study_plan import StudyPlan

    study_plan = StudyPlan.query.get(study_plan_id)

    if not study_plan:
        flash("Study plan not found.", "warning")
        return redirect(url_for("study_plan.list_plans"))

    if study_plan.user_id != current_user.id:
        flash("You can only delete your own study plans.", "danger")
        return redirect(url_for("study_plan.list_plans"))

    try:
        StudyPlanService.delete_study_plan(study_plan_id, current_user.id)
        flash(
            "Study plan deleted. Your learning progress and study history "
            "are preserved.",
            "info",
        )
    except ValueError as e:
        flash(str(e), "danger")
    except Exception:
        logger.exception(
            "Study plan delete failed for plan_id=%s user_id=%s",
            study_plan_id,
            current_user.id,
        )
        flash(
            "Could not delete this study plan because related records still "
            "reference it. You can archive it instead.",
            "danger",
        )

    return redirect(url_for("study_plan.list_plans"))


# ─────────────────────────────────────────────────────────────────────────────
# Archive Study Plan
# ─────────────────────────────────────────────────────────────────────────────


@study_plan_bp.post("/<int:study_plan_id>/archive")
@login_required
def archive_plan(study_plan_id: int):
    """Archive a study plan to preserve history but remove from active scheduling."""
    from app.models.study_plan import StudyPlan

    study_plan = StudyPlan.query.get(study_plan_id)

    if not study_plan:
        flash("Study plan not found.", "warning")
        return redirect(url_for("study_plan.list_plans"))

    if study_plan.user_id != current_user.id:
        flash("You can only archive your own study plans.", "danger")
        return redirect(url_for("study_plan.list_plans"))

    try:
        StudyPlanService.archive_study_plan(study_plan_id, current_user.id)
        flash("Study plan archived.", "info")
    except ValueError as e:
        flash(str(e), "danger")

    return redirect(url_for("study_plan.list_plans"))


# ─────────────────────────────────────────────────────────────────────────────
# Set Active Study Plan
# ─────────────────────────────────────────────────────────────────────────────


@study_plan_bp.post("/<int:study_plan_id>/set-active")
@login_required
def set_active_plan(study_plan_id: int):
    """Set a study plan as the active plan (only one active at a time).

    On success, redirects to the dashboard so every student-facing surface
    re-reads ``StudyPlan.active`` and today's mission in the same response
    cycle — no manual refresh or secondary navigation required (IA-002).
    """
    from app.models.study_plan import StudyPlan

    study_plan = StudyPlan.query.get(study_plan_id)

    if not study_plan:
        flash("Study plan not found.", "warning")
        return redirect(url_for("study_plan.list_plans"))

    if study_plan.user_id != current_user.id:
        flash("You can only set your own study plans as active.", "danger")
        return redirect(url_for("study_plan.list_plans"))

    if study_plan.archived:
        flash("Cannot activate an archived study plan.", "warning")
        return redirect(url_for("study_plan.list_plans"))

    try:
        StudyPlanService.set_active_plan(study_plan_id, current_user.id)
        flash(
            f"{study_plan.exam_name} is now your active study plan.",
            "success",
        )
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("study_plan.list_plans"))

    return redirect_to_student_home()
