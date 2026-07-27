"""Recommendation quality contract (EP-003.1 / EP-004.2).

Applies Product Constitution, P-001.2 Explainability Standard, and P-001.3
Recommendation Quality Standard to Runtime A recommendation rows produced by
``RecommendationService``.

Ownership:
- Ranking / selection / schema attachment remain RecommendationService authority
  (this module is called only from that service).
- EP-004.2: optional Personal Learning Profile consumer view may inform bounded
  tie-break personalisation after Decision Framework ranking — profile never
  owns ladder class selection.
- Consumes Planning mission surface for plan-coherence *labelling* only —
  never invents missions or readiness scores.
- Does not duplicate PlanningService or ReadinessService educational maths.
"""

from __future__ import annotations

import logging
from datetime import UTC, datetime
from typing import Any

logger = logging.getLogger(__name__)

EXPLANATION_SCHEMA_VERSION = "p001.2/v1"
EXPLANATION_LEVEL_DEFAULT = "level_2"

CONFIDENCE_HIGH = "High confidence"
CONFIDENCE_MODERATE = "Moderate confidence"
CONFIDENCE_LOW = "Low confidence / Suggested"
CONFIDENCE_CANNOT_ESTIMATE = "Cannot yet be estimated"

CATEGORY_REVIEW = "Review"
CATEGORY_WEAK_TOPIC = "Weak Topic"
CATEGORY_NEW_TOPIC = "New Topic"
CATEGORY_MOCK_EXAM = "Mock Exam"
CATEGORY_REST = "Rest"
CATEGORY_REVISION = "Revision"
CATEGORY_EXAM_TECHNIQUE = "Exam Technique"
CATEGORY_DEFERRED = "Deferred"
CATEGORY_STUDY_FOCUS = "Study Focus"
CATEGORY_STUDY_RISK = "Study Risk"
CATEGORY_STUDY_STRENGTH = "Study Strength"

PRIORITY_CRITICAL = "Critical"
PRIORITY_HIGH = "High"
PRIORITY_MEDIUM = "Medium"
PRIORITY_LOW = "Low"

PRIORITY_ORDER = {
    PRIORITY_CRITICAL: 0,
    PRIORITY_HIGH: 1,
    PRIORITY_MEDIUM: 2,
    PRIORITY_LOW: 3,
}

# P-001.3 Decision Framework §3 priority ladder (lower = higher priority).
LADDER_SAFETY = 1
LADDER_AUTHORISED_TODAY = 2
LADDER_BLOCKING_DEFICIT = 3
LADDER_EXAM_CRITICAL = 4
LADDER_WEAK_TOPIC = 5
LADDER_NEW_LEARNING = 6
LADDER_ROUTINE_REVISION = 7
LADDER_WORKLOAD = 8
LADDER_MOTIVATION = 9
LADDER_DEFERRED = 99

SCHEMA_REQUIRED_KEYS = (
    "title",
    "reason",
    "expected_benefit",
    "next_action",
    "confidence_level",
    "supporting_evidence",
    "why_recommended",
    "suggested_next_action",
    "review_point",
    "decision_ladder_rank",
    "plan_coherence",
    "explanation_schema_version",
    "explanation_level",
)


def has_complete_explanation_schema(row: dict[str, Any] | None) -> bool:
    """True when a recommendation row carries the mandatory explanation schema."""
    if not isinstance(row, dict):
        return False
    if row.get("honest_refusal"):
        return all(
            str(row.get(key) or "").strip()
            for key in (
                "title",
                "reason",
                "confidence_level",
                "why_recommended",
                "suggested_next_action",
            )
        )
    required = (
        "title",
        "reason",
        "expected_benefit",
        "confidence_level",
        "why_recommended",
        "suggested_next_action",
        "supporting_evidence",
        "explanation_schema_version",
    )
    for key in required:
        value = row.get(key)
        if value is None:
            return False
        if isinstance(value, list | tuple) and len(value) == 0:
            return False
        if isinstance(value, str) and not value.strip():
            return False
    return True


def apply_quality_contract(
    user_id: int,
    recommendations: list[dict[str, Any]],
    *,
    limit: int = 5,
    profile_view: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    """Rank, gate, and enrich recommendations to the P-001.2 / P-001.3 contract.

    EP-004.2: optional ``profile_view`` supplies Personal Learning Profile
    evidence for bounded tie-break personalisation after Decision Framework
    ranking. Profile never owns ladder class selection.

    Fail-open: plan-coherence lookup failures do not drop candidates.
    """
    authorised_focus = _resolve_authorised_today_focus(user_id)
    evidence_density = _estimate_evidence_density(user_id)

    enriched: list[dict[str, Any]] = []
    for raw in recommendations:
        if not isinstance(raw, dict):
            continue
        row = dict(raw)
        row = _assign_ladder_rank(row)
        row = _apply_plan_coherence(row, authorised_focus)
        row = _apply_confidence(row, evidence_density)
        row = _attach_explanation_schema(row)
        if _passes_hard_gates(row, evidence_density):
            enriched.append(row)

    enriched.sort(
        key=lambda r: (
            int(r.get("decision_ladder_rank") or LADDER_DEFERRED),
            PRIORITY_ORDER.get(str(r.get("priority") or ""), 99),
            str(r.get("title") or ""),
        )
    )

    seen_titles: set[str] = set()
    unique: list[dict[str, Any]] = []
    for rec in enriched:
        title = str(rec.get("title") or "")
        if title and title not in seen_titles:
            seen_titles.add(title)
            unique.append(rec)

    if not unique:
        if evidence_density == "thin" or not recommendations:
            return [_honest_refusal_row(authorised_focus)][: max(1, int(limit))]
        return []

    # EP-004.2: bounded personalisation after Decision Framework ordering.
    # Fail-open — missing profile leaves unique[:limit] behaviour intact.
    try:
        from app.services.recommendation_personalisation import (
            apply_profile_personalisation,
            stamp_profile_id,
        )

        personalised = apply_profile_personalisation(
            unique,
            profile_view,
            limit=limit,
        )
        return stamp_profile_id(personalised, profile_view)
    except Exception:  # noqa: BLE001 — personalisation must never break tips
        logger.debug(
            "recommendation_personalisation_failed user_id=%s",
            user_id,
            exc_info=True,
        )
        return unique[: max(1, int(limit))]


def _resolve_authorised_today_focus(user_id: int) -> str | None:
    """Read Today's Mission title for coherence labelling — never invents plans."""
    try:
        from app.services.planning_service import PlanningService

        surface = PlanningService.get_dashboard_mission_surface(user_id)
        if not isinstance(surface, dict):
            return None
        mission = surface.get("today_mission")
        if mission is None:
            return None
        title = getattr(mission, "title", None)
        if title is None and isinstance(mission, dict):
            title = mission.get("title")
        text = str(title or "").strip()
        return text or None
    except Exception:  # noqa: BLE001 — fail-open coherence
        logger.debug(
            "recommendation_quality_mission_lookup_failed user_id=%s",
            user_id,
            exc_info=True,
        )
        return None


def _estimate_evidence_density(user_id: int) -> str:
    """Coarse evidence density from Readiness signals (consume, do not recalculate)."""
    try:
        from app.services.readiness_service import ReadinessService

        readiness = ReadinessService.get_overall_readiness(user_id)
        total = int(readiness.get("total_topics") or 0)
        started = int(readiness.get("topics_started") or 0)
        if total <= 0 or started <= 0:
            return "thin"
        coverage = float(readiness.get("coverage_pct") or 0.0)
        if started >= 3 and coverage >= 20.0:
            return "dense"
        if started >= 1:
            return "moderate"
        return "thin"
    except Exception:  # noqa: BLE001 — fail-open to moderate
        logger.debug(
            "recommendation_quality_evidence_density_failed user_id=%s",
            user_id,
            exc_info=True,
        )
        return "moderate"


def _assign_ladder_rank(row: dict[str, Any]) -> dict[str, Any]:
    if row.get("decision_ladder_rank") is not None:
        try:
            row["decision_ladder_rank"] = int(row["decision_ladder_rank"])
            return row
        except (TypeError, ValueError):
            pass

    category = str(row.get("category") or "")
    priority = str(row.get("priority") or "")

    if category == CATEGORY_DEFERRED or row.get("honest_refusal"):
        rank = LADDER_DEFERRED
    elif category == CATEGORY_STUDY_FOCUS:
        rank = LADDER_AUTHORISED_TODAY
    elif category == CATEGORY_REST and priority == PRIORITY_CRITICAL:
        rank = LADDER_SAFETY
    elif category == CATEGORY_REST:
        rank = LADDER_WORKLOAD
    elif category == CATEGORY_REVIEW and priority == PRIORITY_CRITICAL:
        rank = LADDER_BLOCKING_DEFICIT
    elif category == CATEGORY_REVIEW:
        rank = LADDER_ROUTINE_REVISION
    elif category == CATEGORY_WEAK_TOPIC and priority == PRIORITY_CRITICAL:
        rank = LADDER_BLOCKING_DEFICIT
    elif category == CATEGORY_WEAK_TOPIC:
        rank = LADDER_WEAK_TOPIC
    elif category in {CATEGORY_MOCK_EXAM, CATEGORY_EXAM_TECHNIQUE}:
        rank = LADDER_EXAM_CRITICAL
    elif category == CATEGORY_REVISION and priority in {
        PRIORITY_CRITICAL,
        PRIORITY_HIGH,
    }:
        rank = LADDER_EXAM_CRITICAL
    elif category == CATEGORY_REVISION:
        rank = LADDER_ROUTINE_REVISION
    elif category == CATEGORY_NEW_TOPIC:
        rank = LADDER_NEW_LEARNING
    elif category == CATEGORY_STUDY_RISK:
        rank = LADDER_BLOCKING_DEFICIT
    elif category == CATEGORY_STUDY_STRENGTH:
        rank = LADDER_MOTIVATION
    else:
        rank = LADDER_ROUTINE_REVISION

    row["decision_ladder_rank"] = rank
    return row


def _apply_plan_coherence(
    row: dict[str, Any],
    authorised_focus: str | None,
) -> dict[str, Any]:
    """Label advice that competes with Today's Mission (G3 / Q9)."""
    category = str(row.get("category") or "")
    title = str(row.get("title") or "")
    focus = (authorised_focus or "").strip()

    if row.get("honest_refusal"):
        row["plan_coherence"] = "deferred"
        row["plan_coherence_label"] = "No recommendation yet"
        return row

    if not focus:
        row["plan_coherence"] = "no_active_mission"
        row["plan_coherence_label"] = "No active Today’s Mission to align with"
        return row

    focus_l = focus.lower()
    title_l = title.lower()
    aligns = focus_l in title_l or title_l in focus_l

    if category in {CATEGORY_STUDY_FOCUS, CATEGORY_NEW_TOPIC} and aligns:
        row["plan_coherence"] = "aligned"
        row["plan_coherence_label"] = f"Aligned with Today’s Mission: {focus}"
        row["decision_ladder_rank"] = min(
            int(row.get("decision_ladder_rank") or LADDER_AUTHORISED_TODAY),
            LADDER_AUTHORISED_TODAY,
        )
        return row

    if category in {
        CATEGORY_WEAK_TOPIC,
        CATEGORY_REVIEW,
        CATEGORY_MOCK_EXAM,
        CATEGORY_REVISION,
        CATEGORY_EXAM_TECHNIQUE,
        CATEGORY_STUDY_RISK,
    }:
        row["plan_coherence"] = "advisory"
        row["plan_coherence_label"] = (
            f"Advisory — does not replace Today’s Mission ({focus})"
        )
        reason = str(row.get("reason") or "").strip()
        advice_note = (
            f" This is optional coaching and does not replace Today’s Mission "
            f"({focus})."
        )
        if advice_note.strip() not in reason:
            row["reason"] = (reason + advice_note).strip()
        return row

    if category == CATEGORY_REST:
        row["plan_coherence"] = "wellbeing"
        row["plan_coherence_label"] = (
            f"Wellbeing adjustment alongside Today’s Mission ({focus})"
        )
        return row

    row["plan_coherence"] = "contextual"
    row["plan_coherence_label"] = f"Context for Today’s Mission: {focus}"
    return row


def _apply_confidence(
    row: dict[str, Any],
    evidence_density: str,
) -> dict[str, Any]:
    existing = str(row.get("confidence_level") or "").strip()
    if existing:
        return row

    if row.get("honest_refusal"):
        row["confidence_level"] = CONFIDENCE_CANNOT_ESTIMATE
        return row

    category = str(row.get("category") or "")
    priority = str(row.get("priority") or "")

    if evidence_density == "thin":
        row["confidence_level"] = CONFIDENCE_LOW
    elif category in {CATEGORY_REST, CATEGORY_REVIEW} and priority == PRIORITY_CRITICAL:
        row["confidence_level"] = (
            CONFIDENCE_HIGH if evidence_density == "dense" else CONFIDENCE_MODERATE
        )
    elif evidence_density == "dense" and priority in {
        PRIORITY_CRITICAL,
        PRIORITY_HIGH,
    }:
        row["confidence_level"] = CONFIDENCE_HIGH
    elif evidence_density == "dense":
        row["confidence_level"] = CONFIDENCE_MODERATE
    else:
        row["confidence_level"] = CONFIDENCE_MODERATE
    return row


def _default_next_action(row: dict[str, Any]) -> str:
    category = str(row.get("category") or "")
    title = str(row.get("title") or "this recommendation")
    mapping = {
        CATEGORY_REVIEW: (
            "Open Today’s Study Session or schedule a short review session."
        ),
        CATEGORY_WEAK_TOPIC: (
            "Continue Today’s Study Session first; optionally practise "
            "weaker topics later."
        ),
        CATEGORY_NEW_TOPIC: (
            "Open Today’s Study Session to continue your Current Learning Topic."
        ),
        CATEGORY_MOCK_EXAM: (
            "Plan a mock or exam-style section when you next have a free block."
        ),
        CATEGORY_REST: (
            "Choose a lighter session or a rest day, then return tomorrow."
        ),
        CATEGORY_REVISION: (
            "Shift spare study blocks toward consolidation and revision."
        ),
        CATEGORY_EXAM_TECHNIQUE: (
            "Add a short timing or technique drill to an upcoming session."
        ),
        CATEGORY_STUDY_FOCUS: f"Start or resume: {title}.",
        CATEGORY_STUDY_RISK: (
            "Address this risk after confirming Today’s Mission is on track."
        ),
        CATEGORY_STUDY_STRENGTH: (
            "Keep momentum on this strength without abandoning today’s plan."
        ),
        CATEGORY_DEFERRED: (
            "Complete a short study session so guidance can be personalised."
        ),
    }
    return mapping.get(category, f"Take the next clear step: {title}.")


def _supporting_evidence(row: dict[str, Any]) -> list[str]:
    existing = row.get("supporting_evidence") or row.get("observed_facts")
    if isinstance(existing, list | tuple):
        points = [str(p).strip() for p in existing if str(p).strip()]
        if points:
            return points[:4]

    reason = str(row.get("reason") or "").strip()
    if reason:
        first = reason.split(".")[0].strip()
        return [first + ("." if first and not first.endswith(".") else "")]
    title = str(row.get("title") or "").strip()
    return [f"Generated from your current study signals for: {title}."]


def _attach_explanation_schema(row: dict[str, Any]) -> dict[str, Any]:
    title = str(row.get("title") or "").strip()
    reason = str(row.get("reason") or "").strip()
    benefit = str(row.get("expected_benefit") or "").strip()
    next_action = str(
        row.get("next_action") or row.get("suggested_next_action") or ""
    ).strip()
    if not next_action:
        next_action = _default_next_action(row)

    evidence = _supporting_evidence(row)
    confidence = str(row.get("confidence_level") or CONFIDENCE_LOW).strip()
    review_point = str(row.get("review_point") or "").strip() or (
        "Reassess after your next study session or plan refresh."
    )

    row["why_recommended"] = reason or title
    row["supporting_evidence"] = evidence
    row["observed_facts"] = list(
        row.get("observed_facts") or evidence
    )
    if "estimates" not in row:
        row["estimates"] = []
    row["expected_benefit"] = benefit or (
        "Improve the highest-value lawful next step for your exam preparation."
    )
    row["next_action"] = next_action
    row["suggested_next_action"] = next_action
    row["confidence_level"] = confidence
    row["review_point"] = review_point
    row["educational_advice"] = str(
        row.get("educational_advice") or f"Suggested: {title}."
    )
    row["explanation_schema_version"] = EXPLANATION_SCHEMA_VERSION
    row["explanation_level"] = str(
        row.get("explanation_level") or EXPLANATION_LEVEL_DEFAULT
    )
    row["explanation_schema_complete"] = True
    return row


def _passes_hard_gates(row: dict[str, Any], evidence_density: str) -> bool:
    """Apply P-001.3 G1–G6 for primary eligibility."""
    if row.get("honest_refusal"):
        return True

    title = str(row.get("title") or "").strip()
    reason = str(row.get("reason") or "").strip()
    if not title or not reason:
        return False  # G1 / G4

    if evidence_density == "thin" and str(row.get("category") or "") in {
        CATEGORY_MOCK_EXAM,
        CATEGORY_EXAM_TECHNIQUE,
        CATEGORY_STUDY_STRENGTH,
    }:
        return False  # G6 — refuse fabricated certainty tips on thin history

    if not has_complete_explanation_schema(row):
        return False  # G4

    return True


def _honest_refusal_row(authorised_focus: str | None) -> dict[str, Any]:
    # Truncate microseconds so repeated calls within the same second (e.g.
    # dual-run comparisons) produce a stable generated_at value.
    now = datetime.now(UTC).replace(microsecond=0).isoformat()
    focus_note = (
        f" Keep following Today’s Mission ({authorised_focus}) meanwhile."
        if authorised_focus
        else " Start or continue a short study session to build evidence."
    )
    reason = (
        "There is not yet enough personal study evidence for a confident "
        "primary tip."
        + focus_note
    )
    next_action = (
        f"Continue Today’s Mission: {authorised_focus}."
        if authorised_focus
        else "Complete a short study session so guidance can be personalised."
    )
    row = {
        "title": "No recommendation yet",
        "category": CATEGORY_DEFERRED,
        "priority": PRIORITY_LOW,
        "reason": reason,
        "expected_benefit": (
            "Avoid fabricated certainty; build enough evidence for useful guidance."
        ),
        "generated_at": now,
        "honest_refusal": True,
        "decision_ladder_rank": LADDER_DEFERRED,
        "confidence_level": CONFIDENCE_CANNOT_ESTIMATE,
        "source_authority": "legacy",
    }
    row = _apply_plan_coherence(row, authorised_focus)
    row["next_action"] = next_action
    row["suggested_next_action"] = next_action
    row["why_recommended"] = reason
    row["supporting_evidence"] = [
        "Insufficient personal study history for a confident primary tip.",
    ]
    row["observed_facts"] = list(row["supporting_evidence"])
    row["estimates"] = []
    row["educational_advice"] = reason
    row["review_point"] = "Reassess after your next completed session."
    row["explanation_schema_version"] = EXPLANATION_SCHEMA_VERSION
    row["explanation_level"] = EXPLANATION_LEVEL_DEFAULT
    row["explanation_schema_complete"] = True
    return row
