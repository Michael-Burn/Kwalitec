"""Mission blueprint routes."""

from __future__ import annotations

import logging
from datetime import date

from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.mission.forms import MissionReviewForm, MistakeForm
from app.models.mission import Mission
from app.models.topic_progress import TopicProgress
from app.services.curriculum_engine_service import (
    CurriculumEngineService,
)
from app.services.curriculum_service import CurriculumService
from app.services.learning_service import LearningService
from app.services.mission_service import MissionService
from app.services.readiness_service import ReadinessService
from app.services.study_plan_service import StudyPlanService
from app.services.study_tips_service import StudyTipsService

logger = logging.getLogger(__name__)

mission_bp = Blueprint("mission", __name__, url_prefix="/missions")


def _resolve_topic_for_mission(user_id: int, mission: Mission):
    """Best-effort topic linked to a mission for progress updates.

    Prefers a topic whose official title or natural study label appears in the
    mission title, then falls back to the next incomplete curriculum topic for
    the active plan.
    """
    from app.services.planning_service import PlanningService

    active_plan = StudyPlanService.get_user_active_plan(user_id)
    if not active_plan or not active_plan.curriculum:
        return None

    curriculum = active_plan.curriculum
    title = mission.title or ""
    for topic in CurriculumService.get_ordered_topics(curriculum):
        if not topic.name:
            continue
        if topic.name in title:
            return topic
        label = PlanningService._topic_study_label(topic)
        if label and label in title:
            return topic

    return CurriculumService.get_next_incomplete_topic(user_id, curriculum)


def _apply_mission_topic_progress(user_id: int, topic) -> None:
    """Persist syllabus progress so dashboard readiness updates after completion."""
    if topic is None:
        return

    progress = CurriculumService.get_or_create_topic_progress(
        user_id=user_id,
        topic_id=topic.id,
    )
    progress.completed = True
    progress.confidence = "High"
    progress.current_stage = TopicProgress.STAGE_COMPLETED
    if progress.mastery_score < 70.0:
        progress.mastery_score = 70.0
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

    from app.extensions import db

    db.session.commit()


@mission_bp.get("/")
@login_required
def missions():
    """Daily mission page with full context."""
    user_id = current_user.id

    missions_list = Mission.query.filter_by(user_id=user_id).order_by(
        Mission.mission_date.desc()
    ).all()

    # Today's mission
    today_mission = MissionService.get_today_mission(user_id)

    # Active study plan (for estimated time)
    active_study_plan = StudyPlanService.get_user_active_plan(user_id)

    # Curriculum summary (for today's topic code/title and readiness)
    curriculum_summary = None
    readiness_summary = None
    if active_study_plan:
        try:
            curriculum_summary = CurriculumEngineService().build_student_curriculum(
                active_study_plan
            )
            if curriculum_summary is not None:
                readiness_summary = ReadinessService.calculate_readiness(
                    curriculum_summary
                )
        except Exception:
            logger.warning(
                "Could not build curriculum summary for user %s",
                user_id,
                exc_info=True,
            )

    return render_template(
        "mission/index.html",
        title="Daily Mission",
        missions=missions_list,
        today_mission=today_mission,
        active_study_plan=active_study_plan,
        curriculum_summary=curriculum_summary,
        readiness_summary=readiness_summary,
        study_tip=StudyTipsService.tip_for_day(),
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


@mission_bp.post("/<int:mission_id>/complete")
@login_required
def complete_mission(mission_id: int):
    """Mark a mission complete, persist progress, and refresh dashboard state.

    Completes all tasks, sets mission status to Completed, records a study
    attempt against the linked curriculum topic when available, and updates
    TopicProgress so readiness/progress bars advance after refresh.
    """
    try:
        mission = MissionService.complete_mission(mission_id, current_user.id)
        topic = _resolve_topic_for_mission(current_user.id, mission)
        topic_id = topic.id if topic is not None else None

        LearningService.create_study_attempt(
            user_id=current_user.id,
            mission_id=mission.id,
            topic_id=topic_id,
            study_date=date.today(),
        )
        _apply_mission_topic_progress(current_user.id, topic)

        return jsonify({
            "success": True,
            "mission": {
                "id": mission.id,
                "status": mission.status,
                "completion_percentage": mission.get_completion_percentage(),
            },
            "redirect_url": url_for("dashboard.index"),
        })
    except ValueError as e:
        logger.warning("Mission complete failed: %s", e)
        return jsonify({"success": False, "error": str(e)}), 400
    except Exception as e:
        logger.error("Mission complete error: %s", e, exc_info=True)
        return jsonify({"success": False, "error": str(e)}), 500


@mission_bp.get("/review/<int:mission_id>")
@login_required
def review_mission(mission_id: int):
    """Display mission review form after mission completion.

    Allows student to record how they learned and what they need to improve.
    """
    mission = Mission.query.get_or_404(mission_id)

    # Verify mission belongs to current user
    if mission.user_id != current_user.id:
        flash("You can only review your own missions.", "danger")
        return redirect(url_for("dashboard.index"))

    # Verify all tasks are complete
    if not all(t.completed for t in mission.tasks):
        flash("Complete all tasks before reviewing your mission.", "info")
        return redirect(url_for("dashboard.index"))

    form = MissionReviewForm()
    mistake_form = MistakeForm()

    return render_template(
        "mission/review.html",
        title="Reflect on Your Learning",
        mission=mission,
        form=form,
        mistake_form=mistake_form,
    )


@mission_bp.post("/review/<int:mission_id>")
@login_required
def submit_review(mission_id: int):
    """Handle mission review submission.

    Creates a StudyAttempt and optional Mistake records.
    """
    mission = Mission.query.get_or_404(mission_id)

    # Verify mission belongs to current user
    if mission.user_id != current_user.id:
        flash("You can only review your own missions.", "danger")
        return redirect(url_for("dashboard.index"))

    form = MissionReviewForm()
    if not form.validate_on_submit():
        mistake_form = MistakeForm()
        return render_template(
            "mission/review.html",
            title="Reflect on Your Learning",
            mission=mission,
            form=form,
            mistake_form=mistake_form,
        ), 400

    try:
        topic = _resolve_topic_for_mission(current_user.id, mission)
        topic_id = topic.id if topic is not None else None

        # Create study attempt linked to the curriculum topic when known
        study_attempt = LearningService.create_study_attempt(
            user_id=current_user.id,
            mission_id=mission_id,
            topic_id=topic_id,
            study_date=date.today(),
            duration_minutes=form.duration_minutes.data,
            questions_attempted=form.questions_attempted.data,
            questions_correct=form.questions_correct.data,
            confidence_before=form.confidence_before.data,
            confidence_after=form.confidence_after.data,
            notes=form.notes.data,
        )

        # Handle optional mistakes
        mistakes_data = request.form.getlist("mistake")
        for mistake_index in range(len(mistakes_data)):
            if mistakes_data[mistake_index]:
                mistake_type = request.form.get(f"mistake_type_{mistake_index}")
                description = request.form.get(f"description_{mistake_index}")
                correct_solution = request.form.get(f"correct_solution_{mistake_index}")

                if description:
                    LearningService.record_mistake(
                        study_attempt_id=study_attempt.id,
                        description=description,
                        topic_id=topic_id,
                        mistake_type=mistake_type,
                        correct_solution=correct_solution,
                    )

        # Mark mission as completed and advance syllabus progress
        MissionService.update_mission_status(
            mission_id=mission.id,
            user_id=current_user.id,
            status="Completed",
        )
        _apply_mission_topic_progress(current_user.id, topic)

        flash("Mission review saved. Great work!", "success")
        return redirect(url_for("dashboard.index"))

    except ValueError as e:
        logger.warning("Review submission failed: %s", e)
        form.errors["general"] = [str(e)]
        mistake_form = MistakeForm()
        return render_template(
            "mission/review.html",
            title="Reflect on Your Learning",
            mission=mission,
            form=form,
            mistake_form=mistake_form,
        ), 400
