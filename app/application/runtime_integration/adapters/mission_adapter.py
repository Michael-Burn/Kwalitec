"""Daily Mission surface adapter — Experience Models → mission brief dicts."""

from __future__ import annotations

from typing import Any

from app.domain.educational_experience_engine.surfaces import DailyMissionExperience

AUTHORITY_EDUCATIONAL_INTELLIGENCE = "educational_intelligence"


def map_daily_mission(mission: DailyMissionExperience) -> dict[str, Any]:
    """Map DailyMissionExperience to runtime mission framing fields."""
    return {
        "decision_id": mission.decision_id,
        "experience_id": mission.experience_id,
        "title": mission.mission_title,
        "mission_title": mission.mission_title,
        "summary": mission.mission_summary,
        "why_this_mission": mission.why_this_mission,
        "reason_for_selection": mission.why_this_mission,
        "educational_purpose": mission.expected_outcome,
        "curriculum_target": mission.curriculum_target,
        "curriculum_area": mission.curriculum_area,
        "estimated_minutes": mission.estimated_minutes,
        "estimated_effort_label": mission.estimated_effort_label,
        "expected_outcome": mission.expected_outcome,
        "urgency": mission.urgency,
        "prerequisite_note": mission.prerequisite_note,
        "motivational_line": mission.motivational_line,
        "task_steps": list(mission.task_steps),
        "authority": AUTHORITY_EDUCATIONAL_INTELLIGENCE,
        "experience_version": mission.experience_version,
        "source_authority": AUTHORITY_EDUCATIONAL_INTELLIGENCE,
    }
