"""Recommendation → Experience opaque DTO mapping (translator only).

Projections may consume Evidence / Mission / Progress / Learning State /
Curriculum via Runtime A services. This module never mutates educational state.

EP-006.2: preserve authored Meaningful Explanation Schema (MES) keys so
Student Home / Coach can pass them through without re-narration.
"""

from __future__ import annotations

from typing import Any

from app.infrastructure.adapters.educational_runtime_bridge.contracts import (
    AUTHORITY_RECOMMENDATION_BRIDGE,
)

# Experience Home reads title/topic_title/summary; Bridge contract also names
# recommendation_label. Project both from the same Runtime A fields.

# MES keys authored by RecommendationService — pass through when present.
_MES_PASS_THROUGH_KEYS: tuple[str, ...] = (
    "why_recommended",
    "supporting_evidence",
    "confidence_level",
    "suggested_next_action",
    "next_action",
    "review_point",
    "expected_benefit",
    "decision_ladder_rank",
    "plan_coherence",
    "plan_coherence_label",
    "change_reasoning",
    "observed_facts",
    "estimates",
    "educational_advice",
    "explanation_schema_version",
    "explanation_level",
    "explanation_schema_complete",
    "honest_refusal",
    "personalisation_applied",
    "personalisation_factors",
    "confidence_basis",
)


def map_recommendation_to_projection(
    *,
    student_id: str,
    mission: Any | None = None,
    primary: dict[str, Any] | None = None,
    alternatives: list[dict[str, Any]] | None = None,
    topic_code: str | None = None,
    estimated_minutes: int | None = None,
    decision_id: str | None = None,
    fallback_used: bool = False,
) -> dict[str, Any] | None:
    """Translate Runtime A recommendation (+ optional mission) to opaque DTO.

    When a mission exists, the primary label/topic is aligned to the mission
    title (Foundational Trust dual-“next” rule). RecommendationService narrative
    supplies explanation / alternatives without contradicting the mission topic.
    """
    alt_source = list(alternatives or [])
    mission_id: str | None = None
    mission_title = ""
    if mission is not None:
        mission_id = str(getattr(mission, "id", "") or "")
        mission_title = str(getattr(mission, "title", "") or "").strip()

    if mission is not None and mission_title:
        label = mission_title
        topic_title = mission_title
        mission_aligned = True
        summary = _narrative_summary(primary) or f"Today's mission: {mission_title}"
        category = str((primary or {}).get("category") or "Mission")
        priority = str((primary or {}).get("priority") or "High")
        expected_benefit = str((primary or {}).get("expected_benefit") or "")
        # Prefer RecommendationService rows as alternatives when present;
        # do not re-rank or invent.
        mapped_alts = [_map_alternative(a) for a in alt_source]
        if primary and not mapped_alts:
            # Primary was narrative-only under mission alignment — keep empty.
            mapped_alts = []
    elif primary:
        label = str(primary.get("title") or "").strip()
        topic_title = label
        mission_aligned = False
        summary = _narrative_summary(primary)
        category = str(primary.get("category") or "")
        priority = str(primary.get("priority") or "")
        expected_benefit = str(primary.get("expected_benefit") or "")
        mapped_alts = [_map_alternative(a) for a in alt_source]
    else:
        return None

    if not label:
        return None

    sid = student_id.strip()
    resolved_decision_id = (decision_id or "").strip() or _stable_decision_id(
        sid, mission_id=mission_id, label=label
    )
    explanation = _mes_explanation(
        primary=primary,
        summary=summary,
        category=category,
        priority=priority,
        expected_benefit=expected_benefit,
    )

    projection: dict[str, Any] = {
        "student_id": sid,
        "decision_id": resolved_decision_id,
        "recommendation_label": label,
        "title": label,
        "topic_code": (topic_code or "").strip(),
        "topic_title": topic_title,
        "summary": summary,
        "rationale": summary,
        "estimated_minutes": estimated_minutes,
        "expected_benefit_delta": None,
        "expected_readiness_improvement": None,
        "mission_id": mission_id,
        "explanation": explanation,
        "alternatives": mapped_alts,
        "authority": AUTHORITY_RECOMMENDATION_BRIDGE,
        "next_action_authority": True,
        "mission_aligned": mission_aligned,
        "fallback_used": bool(fallback_used),
        "category": category,
        "priority": priority,
        "expected_benefit": expected_benefit,
    }
    # Also surface MES keys at top level so HomeService / ExplanationService
    # can read them without depending solely on the nested explanation dict.
    if primary:
        for key in _MES_PASS_THROUGH_KEYS:
            if key in primary and key not in projection:
                projection[key] = primary[key]
            elif key in primary and not projection.get(key):
                projection[key] = primary[key]
        # Prefer explicit top-level MES when nested already filled expected_benefit.
        for key in (
            "why_recommended",
            "supporting_evidence",
            "confidence_level",
            "suggested_next_action",
            "next_action",
            "review_point",
            "confidence_basis",
            "plan_coherence",
            "plan_coherence_label",
            "honest_refusal",
        ):
            if key in primary:
                projection[key] = primary[key]
    return projection


def _mes_explanation(
    *,
    primary: dict[str, Any] | None,
    summary: str,
    category: str,
    priority: str,
    expected_benefit: str,
) -> dict[str, Any]:
    """Build explanation dict with authored MES keys preserved."""
    explanation: dict[str, Any] = {
        "summary": summary,
        "authority": AUTHORITY_RECOMMENDATION_BRIDGE,
        "category": category,
        "priority": priority,
        "expected_benefit": expected_benefit,
        "reason": summary,
    }
    if not primary:
        return explanation

    if primary.get("generated_at") is not None:
        explanation["generated_at"] = primary.get("generated_at")

    why = str(primary.get("why_recommended") or "").strip()
    if why:
        explanation["why_recommended"] = why
    evidence = primary.get("supporting_evidence")
    if isinstance(evidence, list):
        explanation["supporting_evidence"] = list(evidence)
        explanation["evidence_points"] = [
            str(item).strip() for item in evidence if str(item).strip()
        ]
    confidence = str(primary.get("confidence_level") or "").strip()
    if confidence:
        explanation["confidence_level"] = confidence
        explanation["confidence"] = confidence
    next_action = str(
        primary.get("suggested_next_action") or primary.get("next_action") or ""
    ).strip()
    if next_action:
        explanation["suggested_next_action"] = next_action
        explanation["next_action"] = str(primary.get("next_action") or next_action)
    review = str(primary.get("review_point") or "").strip()
    if review:
        explanation["review_point"] = review
    basis = str(primary.get("confidence_basis") or "").strip()
    if basis:
        explanation["confidence_basis"] = basis

    for key in _MES_PASS_THROUGH_KEYS:
        if key in explanation:
            continue
        if key in primary and primary[key] is not None:
            explanation[key] = primary[key]
    return explanation


def _narrative_summary(primary: dict[str, Any] | None) -> str:
    if not primary:
        return ""
    # Prefer authored why when reason is a short code-like label; otherwise
    # keep legacy reason/title for mission alignment summaries.
    reason = str(primary.get("reason") or "").strip()
    why = str(primary.get("why_recommended") or "").strip()
    title = str(primary.get("title") or "").strip()
    return reason or why or title


def _map_alternative(rec: dict[str, Any]) -> dict[str, Any]:
    title = str(rec.get("title") or "").strip()
    reason = str(rec.get("reason") or "").strip()
    mapped: dict[str, Any] = {
        "title": title,
        "recommendation_label": title,
        "category": str(rec.get("category") or ""),
        "priority": str(rec.get("priority") or ""),
        "reason": reason,
        "summary": reason,
        "expected_benefit": str(rec.get("expected_benefit") or ""),
    }
    for key in (
        "why_recommended",
        "supporting_evidence",
        "confidence_level",
        "suggested_next_action",
        "next_action",
        "review_point",
        "expected_benefit",
        "plan_coherence",
        "plan_coherence_label",
    ):
        if key in rec and rec[key] is not None:
            mapped[key] = rec[key]
    if not mapped.get("why_recommended") and reason:
        mapped["why_recommended"] = reason
    return mapped


def _stable_decision_id(
    student_id: str, *, mission_id: str | None, label: str
) -> str:
    """Deterministic projection id — not an educational invention."""
    if mission_id:
        return f"rec-mission-{mission_id}"
    safe_label = "".join(c if c.isalnum() else "-" for c in label.lower())[:48]
    return f"rec-{student_id}-{safe_label}".rstrip("-")
