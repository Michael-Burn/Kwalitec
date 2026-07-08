"""Mission blueprint routes."""

from __future__ import annotations

import logging
from datetime import date

from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.extensions import db
from app.mission.forms import MissionReviewForm, MistakeForm
from app.models.mission import Mission, MissionTask
from app.services.learning_service import LearningService
from app.services.mission_service import MissionService

logger = logging.getLogger(__name__)

mission_bp = Blueprint("mission", __name__, url_prefix="/missions")


@mission_bp.get("/")
@login_required
def missions():
    """List all missions for the current user."""
    missions_list = Mission.query.filter_by(user_id=current_user.id).order_by(
        Mission.mission_date.desc()
    ).all()
    
    return render_template(
        "mission/index.html",
        title="Missions",
        missions=missions_list,
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
        # Create study attempt
        study_attempt = LearningService.create_study_attempt(
            user_id=current_user.id,
            mission_id=mission_id,
            topic_id=None,
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
                        topic_id=None,
                        mistake_type=mistake_type,
                        correct_solution=correct_solution,
                    )
        
        # Mark mission as completed
        MissionService.update_mission_status(
            mission_id=mission.id,
            user_id=current_user.id,
            status="Completed",
        )
        
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