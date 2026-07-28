"""Study Session surface adapter — Experience Models → session briefing dicts."""

from __future__ import annotations

from typing import Any

from app.domain.educational_experience_engine.surfaces import StudySessionBriefing

AUTHORITY_EDUCATIONAL_INTELLIGENCE = "educational_intelligence"


def map_session_briefing(briefing: StudySessionBriefing) -> dict[str, Any]:
    """Map StudySessionBriefing to runtime session start context."""
    return {
        "decision_id": briefing.decision_id,
        "experience_id": briefing.experience_id,
        "title": briefing.briefing_title,
        "briefing_title": briefing.briefing_title,
        "summary": briefing.briefing_summary,
        "educational_why": briefing.educational_why,
        "why_studying": briefing.educational_why,
        "curriculum_target": briefing.curriculum_target,
        "curriculum_area": briefing.curriculum_area,
        "estimated_minutes": briefing.estimated_minutes,
        "estimated_effort_label": briefing.estimated_effort_label,
        "expected_outcome": briefing.expected_outcome,
        "learning_objective": briefing.expected_outcome,
        "urgency": briefing.urgency,
        "prerequisite_note": briefing.prerequisite_note,
        "motivational_line": briefing.motivational_line,
        "session_steps": list(briefing.session_steps),
        "success_signal": briefing.success_signal,
        "authority": AUTHORITY_EDUCATIONAL_INTELLIGENCE,
        "experience_version": briefing.experience_version,
        "source_authority": AUTHORITY_EDUCATIONAL_INTELLIGENCE,
    }
