"""Coach surface adapter — Experience Models → coach grounding payloads."""

from __future__ import annotations

from typing import Any

from app.domain.educational_experience_engine.surfaces import CoachConversationContext

AUTHORITY_EDUCATIONAL_INTELLIGENCE = "educational_intelligence"


def map_coach_context(coach: CoachConversationContext) -> dict[str, Any]:
    """Map CoachConversationContext for Intelligent Tutor / Coach consumers."""
    return {
        "decision_id": coach.decision_id,
        "experience_id": coach.experience_id,
        "focus_title": coach.focus_title,
        "coach_opening": coach.coach_opening,
        "educational_why": coach.educational_why,
        "curriculum_target": coach.curriculum_target,
        "curriculum_area": coach.curriculum_area,
        "estimated_minutes": coach.estimated_minutes,
        "expected_outcome": coach.expected_outcome,
        "urgency": coach.urgency,
        "prerequisite_note": coach.prerequisite_note,
        "talking_points": list(coach.talking_points),
        "suggested_prompts": list(coach.suggested_prompts),
        "authority": AUTHORITY_EDUCATIONAL_INTELLIGENCE,
        "experience_version": coach.experience_version,
        "source_authority": AUTHORITY_EDUCATIONAL_INTELLIGENCE,
    }
