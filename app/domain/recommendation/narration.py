"""Structural narration tags keyed by Decision reason-code family.

No free-text LLM authority. Truth before polish; tensions preserved.
"""

from __future__ import annotations

from app.domain.decision.action_types import ActionFamily, ActionIntent
from app.domain.decision.decision import Decision, DecisionWarrantPosture
from app.domain.decision.reason_codes import ReasonCodeFamily, ReasonCodeId
from app.domain.recommendation.warrant import (
    THIN_WARRANT_CONFIDENCE_POSTURES,
    RecommendationConfidencePosture,
)

# Family → structural narration tags (not marketing slogans).
NARRATION_TAGS_BY_FAMILY: dict[ReasonCodeFamily, tuple[str, ...]] = {
    ReasonCodeFamily.CURRICULUM_WEIGHT: ("official_syllabus_weight",),
    ReasonCodeFamily.KNOWLEDGE_GAP: ("coverage_or_mastery_gap",),
    ReasonCodeFamily.RETENTION_RISK: ("retention_risk", "revise_not_study"),
    ReasonCodeFamily.ASSESSMENT_WARRANT_GAP: (
        "assessment_warrant_thin",
        "performance_tag_honesty",
    ),
    ReasonCodeFamily.TIME_GOAL_PRESSURE: ("sitting_time_pressure",),
    ReasonCodeFamily.FEASIBILITY_DEMOTION: (
        "feasibility_demotion_visible",
        "need_still_attributable",
    ),
    ReasonCodeFamily.COLD_START_LOW_WARRANT: (
        "warrant_honesty",
        "diagnostic_clarity",
        "no_mid_preparedness_theatre",
    ),
    ReasonCodeFamily.FACTOR_DISAGREEMENT: (
        "factor_tension_preserved",
        "no_bland_mid_collapse",
    ),
    ReasonCodeFamily.HISTORY_ANTI_THRASH: (
        "prior_preference_respected",
        "dismiss_not_mastery",
    ),
    ReasonCodeFamily.CONFIDENCE_RISK_FRAMING: (
        "confidence_risk_framing_only",
        "confidence_not_mastery",
    ),
}


def suggestion_presentation_tags(
    decision: Decision,
    confidence: RecommendationConfidencePosture,
) -> tuple[str, ...]:
    """Structural presentation tags for the actionable suggestion surface."""
    tags: list[str] = []
    family = decision.selected.family
    intent = decision.selected.intent

    tags.append(f"action_family/{family.value}")
    tags.append(f"intent/{intent.value}")

    if family == ActionFamily.DIAGNOSTIC or intent == ActionIntent.EVIDENCE_CREATING:
        tags.append("diagnostic_framing")
        tags.append("evidence_creating")
    if family == ActionFamily.REVISE:
        tags.append("revise_not_study")
    if family == ActionFamily.STUDY:
        tags.append("study_not_revise")
    if family == ActionFamily.REST_PROTECT_INTENSITY:
        tags.append("rest_protect_not_failure")
        tags.append("sustainability_honesty")
    if family == ActionFamily.ASSESS:
        tags.append("assess_warrant_building")

    if confidence in THIN_WARRANT_CONFIDENCE_POSTURES:
        tags.append("thin_warrant_honesty")
        tags.append("no_mid_high_preparedness_claim")
    if confidence == RecommendationConfidencePosture.COLD_START:
        tags.append("cold_start_communication")
        tags.append("curiosity_clarity")
    if confidence == RecommendationConfidencePosture.NOT_YET_KNOWABLE:
        tags.append("not_yet_knowable_first_class")

    if decision.warrant_posture in {
        DecisionWarrantPosture.COLD_START,
        DecisionWarrantPosture.NOT_YET_KNOWABLE,
        DecisionWarrantPosture.INHERITED_LOW,
    }:
        tags.append("inherit_decision_warrant")

    code_ids = {r.code_id for r in decision.reason_codes}
    if ReasonCodeId.KNOWS_NOW_MAY_NOT_RETAIN in code_ids:
        tags.append("knowledge_vs_memory_tension")
    if ReasonCodeId.BEHAVIOUR_STRONG_PERFORMANCE_THIN in code_ids:
        tags.append("behaviour_vs_performance_tension")
        tags.append("streaks_not_learning_value")
    if ReasonCodeId.CONFIDENCE_NOT_MASTERY in code_ids:
        tags.append("confidence_risk_framing_only")

    # Deduplicate preserving order.
    seen: set[str] = set()
    unique: list[str] = []
    for tag in tags:
        if tag not in seen:
            seen.add(tag)
            unique.append(tag)
    return tuple(unique)


def urgency_duration_tags(decision: Decision) -> tuple[str, ...]:
    """Decision-derived feasibility / urgency presentation — not a priority score."""
    tags: list[str] = []
    for ack in decision.constraint_acknowledgements:
        tags.append(f"constraint/{ack.constraint_class.value}")
        for note in ack.note_tags:
            tags.append(note)
    selected = decision.selected_candidate
    tags.append(f"feasibility/{selected.feasibility.value}")
    code_ids = {r.code_id for r in decision.reason_codes}
    if ReasonCodeId.SITTING_TIME_PRESSURE in code_ids:
        tags.append("sitting_time_pressure")
    if ReasonCodeId.SESSION_TIME_DEMOTION in code_ids:
        tags.append("session_time_demotion_visible")
    if ReasonCodeId.INTENSITY_PROTECTION in code_ids:
        tags.append("intensity_protection_visible")
    if ReasonCodeId.BEHAVIOUR_SUSTAINABILITY in code_ids:
        tags.append("behaviour_sustainability_visible")
    # No engagement urgency theatre.
    tags.append("no_engagement_urgency_theatre")
    seen: set[str] = set()
    unique: list[str] = []
    for tag in tags:
        if tag not in seen:
            seen.add(tag)
            unique.append(tag)
    return tuple(unique)


def family_narration_tags(family: ReasonCodeFamily) -> tuple[str, ...]:
    """Return structural narration tags for a Decision reason-code family."""
    return NARRATION_TAGS_BY_FAMILY.get(family, ())
