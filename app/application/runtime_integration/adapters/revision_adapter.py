"""Revision Planner surface adapter — Experience Models → planner entry dicts."""

from __future__ import annotations

from typing import Any

from app.domain.educational_experience_engine.surfaces import RevisionPlannerEntry

AUTHORITY_EDUCATIONAL_INTELLIGENCE = "educational_intelligence"


def map_revision_entry(entry: RevisionPlannerEntry) -> dict[str, Any]:
    """Map RevisionPlannerEntry to runtime revision planner fields."""
    return {
        "decision_id": entry.decision_id,
        "experience_id": entry.experience_id,
        "title": entry.entry_title,
        "entry_title": entry.entry_title,
        "summary": entry.entry_summary,
        "educational_why": entry.educational_why,
        "curriculum_target": entry.curriculum_target,
        "curriculum_area": entry.curriculum_area,
        "estimated_minutes": entry.estimated_minutes,
        "estimated_effort_label": entry.estimated_effort_label,
        "expected_outcome": entry.expected_outcome,
        "urgency": entry.urgency,
        "prerequisite_note": entry.prerequisite_note,
        "revision_steps": list(entry.revision_steps),
        "is_revision_action": entry.is_revision_action,
        "authority": AUTHORITY_EDUCATIONAL_INTELLIGENCE,
        "experience_version": entry.experience_version,
        "source_authority": AUTHORITY_EDUCATIONAL_INTELLIGENCE,
    }
