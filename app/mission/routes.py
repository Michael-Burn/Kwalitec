"""Mission blueprint routes."""

from __future__ import annotations

import logging

from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.mission.forms import PracticeOutcomeCaptureForm
from app.models.mission import Mission
from app.models.topic_progress import TopicProgress
from app.services.curriculum_engine_service import (
    CurriculumEngineService,
)
from app.services.curriculum_service import CurriculumService
from app.services.educational_explainability_service import (
    EducationalExplainabilityService,
)
from app.services.mission_service import MissionService
from app.services.readiness_service import ReadinessService
from app.services.study_plan_service import StudyPlanService
from app.services.study_session_service import (
    COMPLETION_YES,
    PRACTICE_OUTCOME_SUCCESS_MESSAGE,
    StudySessionService,
)
from app.services.study_tips_service import StudyTipsService

logger = logging.getLogger(__name__)

mission_bp = Blueprint("mission", __name__, url_prefix="/missions")


def _resolve_topic_for_mission(user_id: int, mission: Mission):
    """Best-effort topic linked to a mission for progress updates.

    Prefers a topic whose official title or natural study label appears in the
    mission title, then falls back to the next incomplete curriculum topic for
    the mission's study plan (or the active plan when unbound).
    """
    from app.services.planning_service import PlanningService

    plan = None
    if mission.study_plan_id is not None:
        plan = StudyPlanService.get_plan(mission.study_plan_id, user_id=user_id)
    if plan is None:
        plan = StudyPlanService.get_user_active_plan(user_id)
    if not plan or not plan.curriculum:
        return None

    curriculum = plan.curriculum
    title = mission.title or ""
    for topic in CurriculumService.get_ordered_topics(curriculum):
        if not topic.name:
            continue
        if topic.name in title:
            return topic
        label = PlanningService._topic_study_label(topic)
        if label and label in title:
            return topic

    from app.services.learning_lifecycle_service import LearningLifecycleService

    # Revision Mode has no Current Learning Topic — do not invent Topic 1.
    if LearningLifecycleService.is_revision(user_id, study_plan=plan):
        return None

    return CurriculumService.get_next_incomplete_topic(user_id, curriculum)


def _apply_mission_topic_progress(user_id: int, topic) -> None:
    """Persist syllabus progress so dashboard readiness updates after completion.

    Also advances the active plan's ``curriculum_topic_code`` past the
    completed topic so refresh/heal cannot demote progress on the first
    syllabus leaf (e.g. CS1 ``1.1``).

    In Revision Mode (syllabus complete), Study Progress coverage is not
    advanced — revision consolidates completed material and must not restart
    Topic 1 or invent new coverage.
    """
    if topic is None:
        return

    from app.extensions import db
    from app.services.learning_lifecycle_service import LearningLifecycleService

    if LearningLifecycleService.is_revision(user_id):
        progress = CurriculumService.get_or_create_topic_progress(
            user_id=user_id,
            topic_id=topic.id,
        )
        # Consolidation signal only — never un-complete or invent mastery.
        progress.revision_count = int(progress.revision_count or 0) + 1
        progress.mark_reviewed()
        db.session.commit()
        return

    progress = CurriculumService.get_or_create_topic_progress(
        user_id=user_id,
        topic_id=topic.id,
    )
    # EIP-001 / EIP-002 / EL-001 / IA-004: Mission Completion may update Study
    # Progress only. Never Estimated Mastery/Knowledge, never Educational
    # Evidence of understanding, never student-felt confidence (Art. V; EL-004).
    progress.completed = True
    progress.current_stage = TopicProgress.STAGE_COMPLETED
    progress.mark_reviewed()

    # Advance the following incomplete topic into Learning when present.
    if topic.curriculum:
        nxt = CurriculumService.get_next_incomplete_topic(user_id, topic.curriculum)
        if nxt is not None:
            next_progress = CurriculumService.get_or_create_topic_progress(
                user_id=user_id,
                topic_id=nxt.id,
            )
            if not next_progress.completed:
                next_progress.current_stage = TopicProgress.STAGE_LEARNING

    active_plan = StudyPlanService.get_user_active_plan(user_id)
    if active_plan is not None:
        StudyPlanService.reconcile_current_topic_pointer(active_plan)

    db.session.commit()


@mission_bp.get("/")
@login_required
def missions():
    """Daily mission page with full context."""
    user_id = current_user.id

    # Active study plan first — today's mission must belong to it (IA-001).
    active_study_plan = StudyPlanService.get_user_active_plan(user_id)

    # Ensure a plan-scoped mission exists before launch/display.
    if active_study_plan is not None:
        from app.services.planning_service import PlanningService

        PlanningService.generate_today_mission(user_id)

    missions_list = Mission.query.filter_by(user_id=user_id).order_by(
        Mission.mission_date.desc()
    ).all()

    today_mission = MissionService.get_today_mission(
        user_id,
        study_plan_id=active_study_plan.id if active_study_plan else None,
    )

    # Curriculum summary (coverage / readiness widgets only — not mission topic)
    curriculum_summary = None
    readiness_summary = None
    coverage_narrative = None
    if active_study_plan:
        try:
            curriculum_summary = CurriculumEngineService().build_student_curriculum(
                active_study_plan
            )
            if curriculum_summary is not None:
                readiness_summary = ReadinessService.calculate_readiness(
                    curriculum_summary
                )
                if readiness_summary is not None:
                    coverage_narrative = (
                        EducationalExplainabilityService.explain_coverage_readiness(
                            readiness_percentage=readiness_summary.readiness_percentage,
                            explanation=readiness_summary.explanation,
                        )
                    )
        except Exception:
            logger.warning(
                "Could not build curriculum summary for user %s",
                user_id,
                exc_info=True,
            )

    mission_narrative = None
    session_context = None
    from app.services.learning_lifecycle_service import (
        LearningLifecycle,
        LearningLifecycleService,
    )

    lifecycle = LearningLifecycleService.resolve(
        user_id, study_plan=active_study_plan
    )
    is_revision = lifecycle.stage == LearningLifecycle.REVISION

    if today_mission is not None:
        syllabus_pct = None
        completed_topics = None
        total_topics = None
        if curriculum_summary is not None:
            completed_topics = getattr(curriculum_summary, "completed_topics", None)
            total_topics = getattr(curriculum_summary, "total_topics", None)
        if readiness_summary is not None:
            syllabus_pct = readiness_summary.readiness_percentage * 100
        mission_narrative = EducationalExplainabilityService.build_mission_narrative(
            mission_title=today_mission.title,
            mission_status=today_mission.status,
            exam_name=active_study_plan.exam_name if active_study_plan else None,
            completed_topics=completed_topics,
            total_topics=total_topics,
            syllabus_coverage_pct=syllabus_pct,
            is_revision=is_revision,
        )
        session_context = StudySessionService.build_session_context(
            today_mission,
            active_study_plan,
            why_studying=(
                mission_narrative.reason_for_selection if mission_narrative else None
            ),
            learning_objective=(
                mission_narrative.educational_purpose if mission_narrative else None
            ),
        )

    return render_template(
        "mission/index.html",
        title="Today's Study Session",
        missions=missions_list,
        today_mission=today_mission,
        active_study_plan=active_study_plan,
        curriculum_summary=curriculum_summary,
        readiness_summary=readiness_summary,
        coverage_narrative=coverage_narrative,
        mission_narrative=mission_narrative,
        session_context=session_context,
        study_tip=StudyTipsService.tip_for_day(),
        is_revision=is_revision,
        lifecycle=lifecycle,
    )


def _session_context_for_mission(user_id: int, mission: Mission):
    """Build narrative + Study Session context for a mission-owned page."""
    plan = None
    if mission.study_plan_id is not None:
        plan = StudyPlanService.get_plan(mission.study_plan_id, user_id=user_id)
    if plan is None:
        plan = StudyPlanService.get_user_active_plan(user_id)

    mission_narrative = EducationalExplainabilityService.build_mission_narrative(
        mission_title=mission.title,
        mission_status=mission.status,
        exam_name=plan.exam_name if plan else None,
    )
    session_context = StudySessionService.build_session_context(
        mission,
        plan,
        why_studying=mission_narrative.reason_for_selection,
        learning_objective=mission_narrative.educational_purpose,
    )
    return plan, mission_narrative, session_context


@mission_bp.post("/<int:mission_id>/session/start")
@login_required
def start_study_session(mission_id: int):
    """LXP-002: Start today's Study Session from Today's Mission."""
    try:
        mission = StudySessionService.start_session(mission_id, current_user.id)
    except ValueError as e:
        flash(str(e), "warning")
        return redirect(url_for("mission.missions"))

    return redirect(url_for("mission.study_session", mission_id=mission.id))


@mission_bp.get("/<int:mission_id>/session")
@login_required
def study_session(mission_id: int):
    """LXP-002: Dedicated Study Session screen."""
    try:
        mission = StudySessionService.get_owned_mission(mission_id, current_user.id)
    except ValueError:
        flash("You can only open your own study sessions.", "danger")
        return redirect(url_for("mission.missions"))

    if mission.status == "Completed":
        return redirect(
            url_for(
                "mission.study_session_recorded",
                mission_id=mission.id,
                practice="1",
            )
        )

    if mission.status == "Pending":
        # Opening the session screen is an intentional start.
        try:
            mission = StudySessionService.start_session(mission.id, current_user.id)
        except ValueError as e:
            flash(str(e), "warning")
            return redirect(url_for("mission.missions"))

    _plan, mission_narrative, session_context = _session_context_for_mission(
        current_user.id, mission
    )

    return render_template(
        "mission/session.html",
        title="Study Session",
        mission=mission,
        mission_narrative=mission_narrative,
        session_context=session_context,
    )


@mission_bp.route("/<int:mission_id>/session/finish", methods=["GET", "POST"])
@login_required
def finish_study_session(mission_id: int):
    """LXP-003: Practice Outcome Capture after Finish Study Session."""
    try:
        mission = StudySessionService.get_owned_mission(mission_id, current_user.id)
    except ValueError:
        flash("You can only finish your own study sessions.", "danger")
        return redirect(url_for("mission.missions"))

    if mission.status == "Completed":
        return redirect(
            url_for(
                "mission.study_session_recorded",
                mission_id=mission.id,
                practice="1",
            )
        )

    form = PracticeOutcomeCaptureForm()
    _plan, mission_narrative, session_context = _session_context_for_mission(
        current_user.id, mission
    )

    if request.method == "POST" and request.form.get("skip_practice") == "1":
        topic = _resolve_topic_for_mission(current_user.id, mission)
        topic_id = topic.id if topic is not None else None
        try:
            StudySessionService.finish_session(
                mission_id=mission.id,
                user_id=current_user.id,
                completion_status=COMPLETION_YES,
                notes="No practice questions recorded today.",
                topic_id=topic_id,
            )
        except ValueError as e:
            flash(str(e), "warning")
            return redirect(url_for("mission.missions"))

        flash("Today's study session has been recorded.", "success")
        return redirect(
            url_for(
                "mission.study_session_recorded",
                mission_id=mission.id,
                practice="0",
            )
        )

    if form.validate_on_submit():
        topic = _resolve_topic_for_mission(current_user.id, mission)
        topic_id = topic.id if topic is not None else None

        try:
            result = StudySessionService.record_practice_outcome(
                mission_id=mission.id,
                user_id=current_user.id,
                questions_attempted=form.questions_attempted.data,
                questions_correct=form.questions_correct.data,
                duration_minutes=form.duration_minutes.data,
                notes=form.notes.data,
                topic_id=topic_id,
            )
        except ValueError as e:
            flash(str(e), "warning")
            return redirect(url_for("mission.missions"))

        flash(PRACTICE_OUTCOME_SUCCESS_MESSAGE, "success")
        return redirect(
            url_for(
                "mission.study_session_recorded",
                mission_id=result.mission.id,
                practice="1",
                evidence="1" if result.authorised_evidence else "0",
            )
        )

    return render_template(
        "mission/session_practice_outcome.html",
        title="Practice Outcome Capture",
        mission=mission,
        form=form,
        mission_narrative=mission_narrative,
        session_context=session_context,
    )


@mission_bp.get("/<int:mission_id>/session/recorded")
@login_required
def study_session_recorded(mission_id: int):
    """LXP-004 Study Session Feedback after Practice Outcome Capture."""
    try:
        mission = StudySessionService.get_owned_mission(mission_id, current_user.id)
    except ValueError:
        flash("You can only view your own study sessions.", "danger")
        return redirect(url_for("mission.missions"))

    study_progress_updated = request.args.get("progress") == "1"
    _plan, mission_narrative, session_context = _session_context_for_mission(
        current_user.id, mission
    )
    session_feedback = StudySessionService.build_session_feedback(
        mission.id,
        current_user.id,
        topic_title=session_context.topic_title,
        study_progress_updated=study_progress_updated,
    )

    return render_template(
        "mission/session_recorded.html",
        title="Study Session Feedback",
        mission=mission,
        mission_narrative=mission_narrative,
        session_context=session_context,
        session_feedback=session_feedback,
        practice_success_message=PRACTICE_OUTCOME_SUCCESS_MESSAGE,
    )


@mission_bp.post("/tasks/<int:task_id>/toggle")
@login_required
def toggle_task(task_id: int) -> dict:
    """Toggle the completion status of a task.

    Expects JSON with optional 'completed' field (defaults to True).

    Returns:
        JSON response with updated task data and mission completion status.
    """
    try:
        data = request.get_json() or {}
        completed = data.get("completed", True)

        task = MissionService.mark_task_complete(task_id, current_user.id, completed)
        mission = task.mission

        # Check if all tasks are now complete
        all_complete = all(t.completed for t in mission.tasks)

        return jsonify({
            "success": True,
            "task": {
                "id": task.id,
                "title": task.title,
                "completed": task.completed,
            },
            "mission": {
                "id": mission.id,
                "all_tasks_complete": all_complete,
            }
        })
    except ValueError as e:
        logger.warning("Task toggle failed: %s", e)
        return jsonify({"success": False, "error": str(e)}), 400
    except Exception as e:
        logger.error("Task toggle error: %s", e, exc_info=True)
        return jsonify({"success": False, "error": str(e)}), 500


def _wants_json_response() -> bool:
    """True when a legacy client expects a JSON navigation payload."""
    if request.is_json:
        return True
    accept = request.accept_mimetypes
    if accept.best == "application/json":
        return True
    content_type = (request.content_type or "").lower()
    return content_type.startswith("application/json")


def _authoritative_closure_redirect(mission: Mission):
    """PTP-002: Send the student to the single Version 1 closure path.

    Open missions → Practice Outcome Capture (session/finish).
    Completed missions → Study Session Feedback (session/recorded).
    Never writes educational state from legacy entry points.
    """
    if mission.status == "Pending":
        try:
            mission = StudySessionService.start_session(mission.id, current_user.id)
        except ValueError:
            pass

    if mission.status == "Completed":
        return url_for(
            "mission.study_session_recorded",
            mission_id=mission.id,
            practice="1",
        )
    return url_for("mission.finish_study_session", mission_id=mission.id)


@mission_bp.post("/<int:mission_id>/complete")
@login_required
def complete_mission(mission_id: int):
    """PTP-002 legacy compatibility — delegate to Study Session closure.

    Does not mark the mission complete, create a StudyAttempt, or update
    Study Progress. The authoritative student path is:

        Study Session → Practice Outcome Capture → Study Session Feedback
    """
    try:
        mission = StudySessionService.get_owned_mission(mission_id, current_user.id)
    except ValueError as e:
        logger.warning("Legacy complete delegated failed: %s", e)
        if _wants_json_response():
            return jsonify({"success": False, "error": str(e)}), 400
        flash(str(e), "warning")
        return redirect(url_for("mission.missions"))

    target = _authoritative_closure_redirect(mission)
    if _wants_json_response():
        return jsonify({
            "success": True,
            "delegated": True,
            "message": (
                "Today's study is recorded through the Study Session path."
            ),
            "redirect_url": target,
            "mission": {
                "id": mission.id,
                "status": mission.status,
                "completion_percentage": mission.get_completion_percentage(),
            },
        })
    return redirect(target)


@mission_bp.get("/review/<int:mission_id>")
@login_required
def review_mission(mission_id: int):
    """PTP-002 legacy compatibility — Reflect on Your Learning redirects.

    The competing reflection form is no longer a student journey. Practice
    Outcome Capture and Study Session Feedback own the record / close day.
    """
    try:
        mission = StudySessionService.get_owned_mission(mission_id, current_user.id)
    except ValueError:
        flash("You can only review your own study sessions.", "danger")
        return redirect(url_for("mission.missions"))

    return redirect(_authoritative_closure_redirect(mission))


@mission_bp.post("/review/<int:mission_id>")
@login_required
def submit_review(mission_id: int):
    """PTP-002 legacy compatibility — never write a second educational record.

    POST bodies to the retired Reflect on Your Learning form are ignored for
    state mutation and redirected to the authoritative Study Session path.
    """
    try:
        mission = StudySessionService.get_owned_mission(mission_id, current_user.id)
    except ValueError:
        flash("You can only review your own study sessions.", "danger")
        return redirect(url_for("mission.missions"))

    flash(
        "Practice results and session feedback are recorded through the "
        "Study Session path after you finish studying.",
        "info",
    )
    return redirect(_authoritative_closure_redirect(mission))
