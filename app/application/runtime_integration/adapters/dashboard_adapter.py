"""Dashboard surface adapter — Experience Models → recommendation card dicts."""

from __future__ import annotations

from typing import Any

from app.application.educational_experience_engine.dto import SurfaceBundle
from app.domain.educational_experience_engine.surfaces import DashboardPriorityCard

AUTHORITY_EDUCATIONAL_INTELLIGENCE = "educational_intelligence"


def map_dashboard_card(card: DashboardPriorityCard) -> dict[str, Any]:
    """Map a DashboardPriorityCard to a template-friendly dict."""
    return {
        "decision_id": card.decision_id,
        "experience_id": card.experience_id,
        "title": card.card_title,
        "summary": card.card_summary,
        "reason": card.why_label,
        "why_recommended": card.why_label,
        "curriculum_target": card.curriculum_target,
        "curriculum_area": card.curriculum_area,
        "effort_label": card.effort_label,
        "expected_benefit": card.expected_outcome,
        "expected_outcome": card.expected_outcome,
        "urgency": card.urgency,
        "rank_position": card.rank_position,
        "priority": card.priority,
        "cta_label": card.cta_label,
        "category": "Educational Intelligence",
        "authority": AUTHORITY_EDUCATIONAL_INTELLIGENCE,
        "experience_version": card.experience_version,
        "source_authority": AUTHORITY_EDUCATIONAL_INTELLIGENCE,
    }


def map_dashboard_recommendation(bundle: SurfaceBundle) -> dict[str, Any]:
    """Primary dashboard/home recommendation dict from a SurfaceBundle."""
    card = map_dashboard_card(bundle.dashboard_card)
    experience = bundle.experience
    card["estimated_minutes"] = experience.estimated_effort.minutes
    card["topic_title"] = card["title"]
    card["recommendation_label"] = card["title"]
    card["rationale"] = card["summary"]
    card["suggested_next_action"] = (
        experience.next_steps[0] if experience.next_steps else card["cta_label"]
    )
    card["next_action"] = card["suggested_next_action"]
    card["supporting_evidence"] = [
        f"Curriculum target: {experience.trace.curriculum_target}",
        f"Decision type: {experience.trace.decision_type}",
    ]
    card["confidence_level"] = "high"
    card["explanation"] = {
        "summary": card["summary"],
        "why_recommended": card["why_recommended"],
        "authority": AUTHORITY_EDUCATIONAL_INTELLIGENCE,
        "expected_benefit": card["expected_outcome"],
        "suggested_next_action": card["suggested_next_action"],
    }
    card["alternatives"] = []
    card["mission_aligned"] = False
    card["fallback_used"] = False
    card["next_action_authority"] = True
    return card
