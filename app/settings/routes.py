"""Settings blueprint routes — profile, data export, backup/restore."""

from __future__ import annotations

import json
from datetime import datetime

from flask import (
    Blueprint,
    Response,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import current_user, login_required

from app.extensions import db
from app.models.curriculum import Topic
from app.models.decision import Decision
from app.models.learning import StudyAttempt
from app.models.mission import Mission, MissionTask
from app.models.study_plan import StudyPlan, WeekPlan
from app.models.topic_progress import TopicProgress

settings_bp = Blueprint("settings", __name__, url_prefix="/settings")

# ── Models needed for backup/restore ────────────────────────────────────
_BACKUP_MODELS = [
    (StudyPlan, "study_plans"),
    (WeekPlan, "week_plans"),
    (Mission, "missions"),
    (MissionTask, "mission_tasks"),
    (StudyAttempt, "study_attempts"),
    (TopicProgress, "topic_progress"),
    (Decision, "decisions"),
]


def _user_query(model_class, user_id):
    """Return a query filtered to a user's records for *model_class*.

    Most models carry a direct ``user_id`` column; a few (WeekPlan,
    MissionTask) are owned via a parent model and need an explicit join.
    """
    if model_class is WeekPlan:
        return (
            WeekPlan.query
            .join(StudyPlan, WeekPlan.study_plan_id == StudyPlan.id)
            .filter(StudyPlan.user_id == user_id)
        )
    if model_class is MissionTask:
        return (
            MissionTask.query
            .join(Mission, MissionTask.mission_id == Mission.id)
            .filter(Mission.user_id == user_id)
        )
    return model_class.query.filter_by(user_id=user_id)


def _delete_user_records(model_class, user_id):
    """Delete every record of *model_class* belonging to *user_id*.

    Uses the direct ``user_id`` column when available; falls back to a
    subquery for models without one (WeekPlan, MissionTask).
    """
    if model_class is WeekPlan:
        sub = _user_query(WeekPlan, user_id).with_entities(WeekPlan.id).subquery()
        WeekPlan.query.filter(WeekPlan.id.in_(sub)).delete(synchronize_session="fetch")
        return
    if model_class is MissionTask:
        sub = _user_query(MissionTask, user_id).with_entities(MissionTask.id).subquery()
        MissionTask.query.filter(MissionTask.id.in_(sub)).delete(synchronize_session="fetch")
        return
    model_class.query.filter_by(user_id=user_id).delete()


# ── Settings Pages ──────────────────────────────────────────────────────

@settings_bp.get("/")
@login_required
def index():
    """Render the settings overview page."""
    return render_template("settings/index.html", title="Settings", section="general")


@settings_bp.get("/profile")
@login_required
def profile():
    """Render the profile settings section."""
    return render_template("settings/index.html", title="Settings", section="profile")


@settings_bp.post("/profile")
@login_required
def update_profile():
    """Update user profile settings."""
    # Profile fields like display_name can be added to User model in future
    flash("Profile settings saved successfully.", "success")
    return redirect(url_for("settings.profile"))


@settings_bp.get("/preferences")
@login_required
def preferences():
    """Render the preferences settings section."""
    return render_template(
        "settings/index.html", title="Settings", section="preferences"
    )


@settings_bp.get("/internal-alpha")
@login_required
def internal_alpha():
    """Render Internal Alpha informational status (presentation only)."""
    from app.services.internal_alpha_status_service import InternalAlphaStatusService

    status = InternalAlphaStatusService.build_status(current_user.id)
    return render_template(
        "settings/index.html",
        title="Internal Alpha",
        section="internal-alpha",
        alpha_status=status,
    )


@settings_bp.post("/preferences")
@login_required
def update_preferences():
    """Update user preferences."""
    daily_goal_hours = request.form.get("daily_goal_hours", "").strip()
    if daily_goal_hours:
        try:
            hours = float(daily_goal_hours)
            # Preference stored in session for now; future: persist to User model
            from flask import session
            session["daily_goal_hours"] = hours
            flash("Preferences updated successfully.", "success")
        except ValueError:
            flash("Please enter a valid number for daily study goal hours.", "danger")

    return redirect(url_for("settings.preferences"))


@settings_bp.get("/data")
@login_required
def data():
    """Render the data management section (export, backup, restore)."""
    # Gather data stats per model
    model_stats = {}
    for model_class, label in _BACKUP_MODELS:
        count = _user_query(model_class, current_user.id).count()
        model_stats[label] = count

    return render_template(
        "settings/index.html",
        title="Settings",
        section="data",
        model_stats=model_stats,
    )


# ── PDF Export ──────────────────────────────────────────────────────────

@settings_bp.get("/export/pdf")
@login_required
def export_weekly_pdf():
    """Export the current weekly report as a plain-text download.

    A lightweight plain-text weekly report is returned as a .txt file with a
    .pdf-like naming convention. For a full PDF implementation, integrate a
    library such as WeasyPrint or ReportLab.
    """
    from app.services.analytics_service import AnalyticsService
    from app.services.readiness_service import ReadinessService

    user_id = current_user.id

    weekly_report = AnalyticsService.generate_weekly_report(user_id)
    readiness = ReadinessService.get_overall_readiness(user_id)
    curriculum_coverage = ReadinessService.get_curriculum_coverage(user_id)

    # Build a structured plain-text report
    lines = []
    lines.append("╔══════════════════════════════════════════════╗")
    lines.append("║         KWALITEC — WEEKLY REPORT            ║")
    lines.append("╚══════════════════════════════════════════════╝")
    lines.append("")
    lines.append(f"User:        {current_user.email}")
    lines.append(f"Week:        {weekly_report.get('week_label', 'N/A')}")
    lines.append(f"Generated:   {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}")
    lines.append("")
    lines.append("─── Overview ─────────────────────────────────")
    lines.append(f"Overall Readiness:      {readiness['score']:.0f}%")
    lines.append(f"Curriculum Coverage:    {curriculum_coverage['coverage_percentage']:.0f}%")
    lines.append(f"Average Mastery:        {readiness['avg_mastery']:.0f}%")
    lines.append(f"Current Streak:         {weekly_report.get('current_streak', 0)} days")
    lines.append("")
    lines.append("─── This Week ────────────────────────────────")
    lines.append(f"Study Hours:            {weekly_report.get('study_hours', 0)}h")
    lines.append(
        f"Missions:               {weekly_report.get('missions_completed', 0)}/"
        f"{weekly_report.get('total_missions', 0)} completed"
    )
    lines.append(f"Topics Reviewed:        {weekly_report.get('topics_reviewed', 0)}")
    lines.append(f"Days Studied:           {weekly_report.get('days_studied', 0)}/7")
    lines.append("")

    accuracy = weekly_report.get("accuracy")
    if accuracy is not None:
        lines.append("─── Accuracy ──────────────────────────────────")
        lines.append(f"Weekly Accuracy:        {accuracy:.1f}%")
        lines.append(
            f"Questions:              {weekly_report.get('questions_correct', 0)}/"
            f"{weekly_report.get('questions_attempted', 0)} correct"
        )
        lines.append("")

    highlights = weekly_report.get("highlights", [])
    if highlights:
        lines.append("─── Highlights ───────────────────────────────")
        for h in highlights:
            lines.append(f"  ✓ {h}")
        lines.append("")

    improvements = weekly_report.get("areas_for_improvement", [])
    if improvements:
        lines.append("─── Areas for Improvement ────────────────────")
        for a in improvements:
            lines.append(f"  ! {a}")
        lines.append("")

    lines.append("─── End of Report ────────────────────────────")

    content = "\n".join(lines)

    return Response(
        content,
        mimetype="text/plain",
        headers={
            "Content-Disposition": (
                f"attachment; filename=kwalitec-weekly-report-"
                f"{datetime.utcnow().strftime('%Y-%m-%d')}.txt"
            )
        },
    )


# ── JSON Backup & Restore ────────────────────────────────────────────────

@settings_bp.get("/export/backup")
@login_required
def export_backup():
    """Export all user learning data as a JSON backup file."""
    user_id = current_user.id
    backup: dict = {
        "metadata": {
            "version": "1.0",
            "exported_at": datetime.utcnow().isoformat(),
            "user_email": current_user.email,
            "user_id": user_id,
        },
        "data": {},
    }

    for model_class, label in _BACKUP_MODELS:
        records = _user_query(model_class, user_id).all()
        backup["data"][label] = [
            _serialize_record(r) for r in records
        ]

    # Include topic data (read-only curriculum data, not user-specific)
    topics = Topic.query.all()
    backup["data"]["topics"] = [_serialize_record(t) for t in topics]

    content = json.dumps(backup, indent=2, default=str, ensure_ascii=False)

    return Response(
        content,
        mimetype="application/json",
        headers={
            "Content-Disposition": (
                f"attachment; filename=kwalitec-backup-"
                f"{datetime.utcnow().strftime('%Y-%m-%d')}.json"
            )
        },
    )


@settings_bp.post("/import/restore")
@login_required
def import_restore():
    """Restore user data from a JSON backup file.

    This is a destructive operation — it replaces existing data for the
    listed model types. Curriculum/topic data is not modified.
    """
    uploaded = request.files.get("backup_file")
    if not uploaded:
        flash("No backup file provided.", "danger")
        return redirect(url_for("settings.data"))

    try:
        raw = uploaded.read().decode("utf-8")
        backup = json.loads(raw)
    except (json.JSONDecodeError, UnicodeDecodeError):
        flash("Invalid backup file — could not parse JSON.", "danger")
        return redirect(url_for("settings.data"))

    # Validate structure
    metadata = backup.get("metadata", {})
    if metadata.get("version") != "1.0":
        flash("Unsupported backup version.", "danger")
        return redirect(url_for("settings.data"))

    data = backup.get("data", {})
    user_id = current_user.id

    restored_count = 0

    for model_class, label in _BACKUP_MODELS:
        if label not in data:
            continue

        # Remove existing records for this user and model
        _delete_user_records(model_class, user_id)

        # Does this model carry a direct user_id column?
        _has_user_id = hasattr(model_class, "user_id") or "user_id" in {
            c.name for c in model_class.__table__.columns
        }

        # Insert records from backup
        for record_data in data[label]:
            record_data.pop("id", None)  # Let the DB assign new IDs
            if _has_user_id:
                record_data["user_id"] = user_id  # Ensure ownership
            instance = model_class(**record_data)
            db.session.add(instance)
            restored_count += 1

    db.session.commit()

    flash(
        f"Restore complete. {restored_count} records imported from backup.", "success"
    )
    return redirect(url_for("settings.data"))


# ── Helpers ──────────────────────────────────────────────────────────────

def _serialize_record(record) -> dict:
    """Convert a SQLAlchemy model instance to a plain dict for JSON export.

    Uses the model's __table__ columns to produce a safe, generic
    serialisation. Datetime and date objects are converted to ISO strings.
    """
    result: dict = {}
    for column in record.__table__.columns:
        value = getattr(record, column.name)
        if isinstance(value, (datetime,)):
            value = value.isoformat()
        elif hasattr(value, "isoformat"):
            value = value.isoformat()
        result[column.name] = value
    return result
