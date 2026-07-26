"""Planning quality contract (EP-003.3) + personalisation hook (EP-004.3).

Applies Product Constitution and P-001.2 Explainability Standard to Runtime A
planning surfaces produced by ``PlanningService``.

Ownership:
- Plan construction / mission persistence / schema attachment remain
  PlanningService authority (this module is called only from that service).
- Consumes ReadinessService ``get_overall_readiness`` for readiness-informed
  *labelling and workload notes* only — never recalculates readiness scores.
- Consumes RecommendationService tip titles for recommendation-alignment
  *labelling* only — never ranks or invents recommendations.
- EP-004.3: optional Personal Learning Profile view supplies evidence for
  bounded pacing / duration / recovery / revision adaptations after the
  quality schema is attached — profile never owns plan slots or missions.
- Does not duplicate ReadinessService or RecommendationService educational maths.
"""

from __future__ import annotations

import logging
import threading
from typing import Any

logger = logging.getLogger(__name__)

EXPLANATION_SCHEMA_VERSION = "p001.2/v1"
EXPLANATION_LEVEL_DEFAULT = "level_2"

CONFIDENCE_HIGH = "High confidence"
CONFIDENCE_MODERATE = "Moderate confidence"
CONFIDENCE_LOW = "Low confidence / Suggested"
CONFIDENCE_CANNOT_ESTIMATE = "Cannot yet be estimated"

COHERENCE_ALIGNED = "aligned"
COHERENCE_ADVISORY = "advisory"
COHERENCE_RECOVERY = "recovery"
COHERENCE_EMPTY = "empty"
COHERENCE_UNAVAILABLE = "unavailable"

SCHEMA_REQUIRED_KEYS = (
    "judgement",
    "why_this_plan",
    "supporting_evidence",
    "confidence_level",
    "expected_benefit",
    "suggested_next_action",
    "review_point",
    "plan_drivers",
    "explanation_schema_version",
    "explanation_level",
)

_quality_depth = threading.local()


def _enter_quality() -> int:
    depth = int(getattr(_quality_depth, "depth", 0) or 0)
    _quality_depth.depth = depth + 1
    return depth + 1


def _exit_quality() -> None:
    depth = int(getattr(_quality_depth, "depth", 0) or 0)
    _quality_depth.depth = max(0, depth - 1)


def quality_reentrancy_depth() -> int:
    """Current planning-quality stack depth (tests / reentrancy guards)."""
    return int(getattr(_quality_depth, "depth", 0) or 0)


def has_complete_plan_explanation_schema(
    surface: dict[str, Any] | None,
) -> bool:
    """True when a plan / mission surface carries the mandatory explanation schema."""
    if not isinstance(surface, dict):
        return False
    if surface.get("honest_refusal"):
        return all(
            str(surface.get(key) or "").strip()
            for key in (
                "judgement",
                "why_this_plan",
                "confidence_level",
                "suggested_next_action",
            )
        )
    for key in (
        "judgement",
        "why_this_plan",
        "confidence_level",
        "suggested_next_action",
        "supporting_evidence",
        "explanation_schema_version",
    ):
        value = surface.get(key)
        if value is None:
            return False
        if isinstance(value, list | tuple) and len(value) == 0:
            return False
        if isinstance(value, str) and not value.strip():
            return False
    drivers = surface.get("plan_drivers")
    if not isinstance(drivers, list) or len(drivers) == 0:
        return False
    return bool(surface.get("explanation_schema_complete"))


def apply_planning_quality_contract(
    user_id: int,
    surface: dict[str, Any],
    profile_view: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Enrich a dashboard mission / plan surface to the P-001.2 contract.

    Fail-open: readiness / recommendation lookup failures degrade labels only.
    Never invents missions or recalculates readiness / recommendation ranking.

    EP-004.3: optional ``profile_view`` supplies Personal Learning Profile
    evidence for bounded personalisation after the quality schema is attached.
    """
    if not isinstance(surface, dict):
        return surface

    depth = _enter_quality()
    try:
        out = dict(surface)
        daily_plan = out.get("daily_plan")
        daily_plan = daily_plan if isinstance(daily_plan, dict) else {}
        slots = _coerce_slots(out, daily_plan)

        if not slots and not out.get("today_mission") and not daily_plan:
            return _honest_refusal_surface(
                out,
                reason="No active study plan or today's mission is available yet.",
            )

        readiness = _resolve_overall_readiness(user_id) if depth <= 1 else {}
        rec_titles = (
            _resolve_recommendation_titles(user_id) if depth <= 1 else ()
        )

        drivers = _plan_drivers(out, daily_plan, slots, readiness)
        out["plan_drivers"] = drivers

        readiness_alignment = _readiness_alignment(readiness, slots)
        recommendation_alignment = _recommendation_alignment(slots, rec_titles)
        plan_coherence = _plan_coherence(
            daily_plan, slots, readiness_alignment, recommendation_alignment
        )
        out["readiness_alignment"] = readiness_alignment
        out["recommendation_alignment"] = recommendation_alignment
        out["plan_coherence"] = plan_coherence

        out = _maybe_adjust_workload_for_readiness(out, daily_plan, readiness)

        student_confidence = _student_confidence(out, daily_plan, readiness, slots)
        out["confidence_level"] = student_confidence

        evidence = _supporting_evidence(
            out, daily_plan, slots, readiness, rec_titles
        )
        out["supporting_evidence"] = evidence
        out["observed_facts"] = list(evidence)

        primary_action = _primary_next_action(out, slots)
        out["suggested_next_action"] = primary_action
        out["next_action"] = primary_action

        change_reason = _change_reasoning(daily_plan, slots, readiness)
        out["change_reasoning"] = change_reason

        why = _why_this_plan(
            slots,
            readiness_alignment=readiness_alignment,
            recommendation_alignment=recommendation_alignment,
            plan_coherence=plan_coherence,
            confidence=student_confidence,
        )
        expected_benefit = (
            "Give you a balanced, completable study day with clear priorities."
        )
        review_point = (
            "Refresh after completing today's mission or after a missed day."
        )

        primary_title = _primary_focus_title(out, slots)
        judgement = (
            f"Today's plan: {primary_title}"
            if primary_title
            else "Today's plan: focus on your authorised mission"
        )

        out["judgement"] = judgement
        out["why_this_plan"] = why
        out["expected_benefit"] = expected_benefit
        out["review_point"] = review_point
        out["explanation_summary"] = _explanation_summary(
            judgement=judgement,
            why=why,
            confidence=student_confidence,
            next_action=primary_action,
            change_reason=change_reason,
        )
        out["explanation_schema_version"] = EXPLANATION_SCHEMA_VERSION
        out["explanation_level"] = EXPLANATION_LEVEL_DEFAULT
        out["explanation_schema_complete"] = True
        out["honest_refusal"] = False

        explainability = dict(out.get("explainability") or {})
        explainability.update(
            {
                "quality_contract": "ep003.3",
                "explanation_schema_version": EXPLANATION_SCHEMA_VERSION,
                "confidence_student_label": student_confidence,
                "primary_next_action": primary_action,
                "change_reasoning": change_reason,
                "readiness_alignment": readiness_alignment,
                "recommendation_alignment": recommendation_alignment,
                "plan_coherence": plan_coherence,
            }
        )
        out["explainability"] = explainability

        # Mirror schema onto nested daily_plan when present (cutover payload).
        if daily_plan:
            nested = dict(daily_plan)
            for key in (
                "judgement",
                "why_this_plan",
                "supporting_evidence",
                "confidence_level",
                "expected_benefit",
                "suggested_next_action",
                "next_action",
                "review_point",
                "plan_drivers",
                "change_reasoning",
                "explanation_summary",
                "explanation_schema_version",
                "explanation_level",
                "explanation_schema_complete",
                "honest_refusal",
                "readiness_alignment",
                "recommendation_alignment",
                "plan_coherence",
            ):
                if key in out:
                    nested[key] = out[key]
            nested_explain = dict(nested.get("explainability") or {})
            nested_explain.update(explainability)
            nested["explainability"] = nested_explain
            out["daily_plan"] = nested

        return _maybe_apply_personalisation(out, profile_view)
    finally:
        _exit_quality()


def apply_planning_quality_to_daily_plan(
    user_id: int,
    payload: dict[str, Any],
    profile_view: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Enrich a Twin daily study plan dict via surface mapping."""
    if not isinstance(payload, dict):
        return payload

    surface = {
        "today_mission": None,
        "source_authority": "daily_study_plan",
        "daily_plan": payload,
        "today_missions_slots": list(payload.get("today_missions") or []),
        "recommended_workload": dict(payload.get("recommended_workload") or {}),
        "topic_ordering": list(payload.get("topic_ordering") or []),
        "revision_priorities": list(payload.get("revision_priorities") or []),
        "limitations_codes": list(payload.get("limitations_codes") or []),
        "explainability": dict(payload.get("explainability") or {}),
        "plan_date": payload.get("plan_date"),
        "availability": payload.get("availability"),
    }
    enriched = apply_planning_quality_contract(
        user_id, surface, profile_view=profile_view
    )
    out = dict(payload)
    for key in (
        "judgement",
        "why_this_plan",
        "supporting_evidence",
        "observed_facts",
        "expected_benefit",
        "suggested_next_action",
        "next_action",
        "review_point",
        "change_reasoning",
        "explanation_summary",
        "explanation_schema_version",
        "explanation_level",
        "explanation_schema_complete",
        "honest_refusal",
        "confidence_level",
        "plan_drivers",
        "readiness_alignment",
        "recommendation_alignment",
        "plan_coherence",
        "personalisation_applied",
        "personalisation_factors",
        "personalisation_schema_version",
        "personalisation_profile_id",
        "session_sizing_guidance",
        "today_missions",
        "revision_priorities",
    ):
        if key in enriched:
            out[key] = enriched[key]

    if isinstance(enriched.get("recommended_workload"), dict):
        out["recommended_workload"] = dict(enriched["recommended_workload"])

    if isinstance(enriched.get("today_missions_slots"), list):
        out["today_missions"] = list(enriched["today_missions_slots"])

    explainability = dict(out.get("explainability") or {})
    explainability.update(dict(enriched.get("explainability") or {}))
    out["explainability"] = explainability
    return out


def _maybe_apply_personalisation(
    surface: dict[str, Any],
    profile_view: dict[str, Any] | None,
) -> dict[str, Any]:
    """EP-004.3: bounded personalisation after quality schema (fail-open)."""
    try:
        from app.services.planning_personalisation import apply_profile_personalisation

        return apply_profile_personalisation(surface, profile_view)
    except Exception:  # noqa: BLE001 — personalisation must never break planning
        logger.debug(
            "planning_personalisation_failed",
            exc_info=True,
        )
        surface.setdefault("personalisation_applied", False)
        surface.setdefault("personalisation_factors", [])
        return surface


def _coerce_slots(
    surface: dict[str, Any],
    daily_plan: dict[str, Any],
) -> list[dict[str, Any]]:
    raw = surface.get("today_missions_slots") or daily_plan.get("today_missions") or []
    if not isinstance(raw, list):
        return []
    return [dict(item) for item in raw if isinstance(item, dict)]


def _resolve_overall_readiness(user_id: int) -> dict[str, Any]:
    """Consume bare readiness composite — never dashboard surface (recursion)."""
    try:
        from app.services.readiness_service import ReadinessService

        readiness = ReadinessService.get_overall_readiness(user_id)
        return readiness if isinstance(readiness, dict) else {}
    except Exception:  # noqa: BLE001 — fail-open
        logger.debug(
            "planning_quality_readiness_lookup_failed user_id=%s",
            user_id,
            exc_info=True,
        )
        return {}


def _resolve_recommendation_titles(user_id: int) -> tuple[str, ...]:
    """Consume recommendation titles for alignment labels — never re-rank."""
    try:
        from app.services.recommendation_service import RecommendationService

        rows = RecommendationService.generate_recommendations(user_id, limit=3)
        titles: list[str] = []
        for row in rows or []:
            if not isinstance(row, dict):
                continue
            title = str(row.get("title") or "").strip()
            if title:
                titles.append(title)
        return tuple(titles)
    except Exception:  # noqa: BLE001 — fail-open
        logger.debug(
            "planning_quality_recommendation_lookup_failed user_id=%s",
            user_id,
            exc_info=True,
        )
        return ()


def _score_value(readiness: dict[str, Any]) -> float | None:
    raw = readiness.get("score")
    if raw is None:
        return None
    try:
        return float(raw)
    except (TypeError, ValueError):
        return None


def _plan_drivers(
    surface: dict[str, Any],
    daily_plan: dict[str, Any],
    slots: list[dict[str, Any]],
    readiness: dict[str, Any],
) -> list[dict[str, Any]]:
    drivers: list[dict[str, Any]] = []
    for slot in slots:
        slot_name = str(slot.get("slot") or "focus").strip() or "focus"
        topic = str(slot.get("topic_name") or slot.get("topic_id") or "").strip()
        reason = str(slot.get("reason") or "").strip()
        drivers.append(
            {
                "driver_id": f"slot_{slot_name}",
                "label": topic or slot_name.replace("_", " ").title(),
                "influence": (
                    "primary"
                    if slot_name in {"review", "recovery", "weak"}
                    else "supporting"
                ),
                "value": slot.get("allocated_minutes"),
                "source": "planning.today_missions",
                "rationale": reason or f"Authorised {slot_name} focus for today.",
            }
        )

    workload = surface.get("recommended_workload") or daily_plan.get(
        "recommended_workload"
    )
    if isinstance(workload, dict) and workload.get("recommended_minutes") is not None:
        drivers.append(
            {
                "driver_id": "recommended_workload",
                "label": "Recommended study minutes",
                "influence": "supporting",
                "value": workload.get("recommended_minutes"),
                "source": "planning.recommended_workload",
                "rationale": str(
                    workload.get("rationale") or "Planner workload guardrail."
                ),
            }
        )

    score = _score_value(readiness)
    if score is not None:
        drivers.append(
            {
                "driver_id": "readiness_signal",
                "label": "Estimated readiness",
                "influence": "supporting",
                "value": score,
                "source": "readiness.get_overall_readiness",
                "rationale": (
                    f"Readiness composite about {int(round(score))}% informs "
                    "workload caution — Planning does not recalculate readiness."
                ),
            }
        )

    explain = daily_plan.get("explainability") or surface.get("explainability") or {}
    if isinstance(explain, dict) and explain.get("recovery_mode"):
        missed = explain.get("mission_missed_count") or 0
        drivers.append(
            {
                "driver_id": "adaptive_recovery",
                "label": "Adaptive recovery",
                "influence": "primary",
                "value": missed,
                "source": "planning.mission_missed_count",
                "rationale": (
                    f"Missed session signal ({missed}) favours recovery over "
                    "new progression today."
                ),
            }
        )

    if not drivers:
        drivers.append(
            {
                "driver_id": "legacy_mission",
                "label": "Today's Mission",
                "influence": "primary",
                "value": None,
                "source": "planning.generate_today_mission",
                "rationale": "Legacy mission path — syllabus sequence for today.",
            }
        )
    return drivers


def _readiness_alignment(
    readiness: dict[str, Any],
    slots: list[dict[str, Any]],
) -> str:
    score = _score_value(readiness)
    if score is None and not readiness:
        return COHERENCE_UNAVAILABLE
    if not slots:
        return COHERENCE_EMPTY
    slot_names = {str(s.get("slot") or "") for s in slots}
    if score is not None and score < 45 and (
        "recovery" in slot_names or "weak" in slot_names or "review" in slot_names
    ):
        return COHERENCE_ALIGNED
    if score is not None and score >= 70 and "progression" in slot_names:
        return COHERENCE_ALIGNED
    if (
        score is not None
        and score < 45
        and "progression" in slot_names
        and len(slots) == 1
    ):
        return COHERENCE_ADVISORY
    return COHERENCE_ALIGNED if slots else COHERENCE_EMPTY


def _recommendation_alignment(
    slots: list[dict[str, Any]],
    rec_titles: tuple[str, ...],
) -> str:
    if not slots:
        return COHERENCE_EMPTY
    if not rec_titles:
        # Still recommendation-aware via Decision Framework slot order.
        order = [str(s.get("slot") or "") for s in slots]
        rank = {"review": 0, "recovery": 1, "weak": 1, "progression": 2}
        ranks = [rank.get(s, 9) for s in order]
        return COHERENCE_ALIGNED if ranks == sorted(ranks) else COHERENCE_ADVISORY

    haystack = " ".join(t.lower() for t in rec_titles)
    for slot in slots:
        topic = str(slot.get("topic_name") or "").strip().lower()
        if topic and topic in haystack:
            return COHERENCE_ALIGNED
    return COHERENCE_ADVISORY


def _plan_coherence(
    daily_plan: dict[str, Any],
    slots: list[dict[str, Any]],
    readiness_alignment: str,
    recommendation_alignment: str,
) -> str:
    explain = daily_plan.get("explainability") if isinstance(daily_plan, dict) else {}
    if isinstance(explain, dict) and explain.get("recovery_mode"):
        return COHERENCE_RECOVERY
    if readiness_alignment == COHERENCE_UNAVAILABLE and not slots:
        return COHERENCE_UNAVAILABLE
    if (
        readiness_alignment == COHERENCE_ALIGNED
        and recommendation_alignment == COHERENCE_ALIGNED
    ):
        return COHERENCE_ALIGNED
    if not slots:
        return COHERENCE_EMPTY
    return COHERENCE_ADVISORY


def _maybe_adjust_workload_for_readiness(
    surface: dict[str, Any],
    daily_plan: dict[str, Any],
    readiness: dict[str, Any],
) -> dict[str, Any]:
    """Annotate workload when readiness is low — never invents a new plan."""
    score = _score_value(readiness)
    workload = surface.get("recommended_workload")
    if not isinstance(workload, dict):
        workload = dict(daily_plan.get("recommended_workload") or {})
    else:
        workload = dict(workload)
    if not workload or score is None:
        surface["recommended_workload"] = workload
        return surface

    try:
        recommended = int(workload.get("recommended_minutes") or 0)
    except (TypeError, ValueError):
        recommended = 0

    rationale = str(workload.get("rationale") or "").strip()
    if score < 40 and recommended > 25:
        reduced = max(20, int(recommended * 0.9))
        if reduced < recommended:
            note = (
                f" Readiness about {int(round(score))}% — keep today's load "
                "slightly lighter so the plan stays completable."
            )
            if note.strip() not in rationale:
                rationale = f"{rationale}{note}".strip()
            workload["recommended_minutes"] = reduced
            workload["rationale"] = rationale
            workload["readiness_informed"] = True
    surface["recommended_workload"] = workload
    return surface


def _student_confidence(
    surface: dict[str, Any],
    daily_plan: dict[str, Any],
    readiness: dict[str, Any],
    slots: list[dict[str, Any]],
) -> str:
    availability = surface.get("availability") or daily_plan.get("availability")
    if availability and str(availability) != "available":
        return CONFIDENCE_CANNOT_ESTIMATE
    if not slots and not surface.get("today_mission"):
        return CONFIDENCE_CANNOT_ESTIMATE

    score = _score_value(readiness)
    started = int(readiness.get("topics_started") or 0) if readiness else 0
    explain = daily_plan.get("explainability") or surface.get("explainability") or {}
    evidence_attempts = 0
    if isinstance(explain, dict):
        try:
            evidence_attempts = int(explain.get("evidence_attempt_count") or 0)
        except (TypeError, ValueError):
            evidence_attempts = 0

    if started <= 0 and evidence_attempts <= 0 and (score is None or score <= 0):
        return CONFIDENCE_LOW
    if isinstance(explain, dict) and explain.get("recovery_mode"):
        return CONFIDENCE_MODERATE
    if score is not None and score >= 65 and evidence_attempts >= 5:
        return CONFIDENCE_HIGH
    if score is not None and score >= 45:
        return CONFIDENCE_MODERATE
    return CONFIDENCE_LOW


def _supporting_evidence(
    surface: dict[str, Any],
    daily_plan: dict[str, Any],
    slots: list[dict[str, Any]],
    readiness: dict[str, Any],
    rec_titles: tuple[str, ...],
) -> list[str]:
    evidence: list[str] = []
    for slot in slots[:3]:
        topic = str(slot.get("topic_name") or "").strip()
        reason = str(slot.get("reason") or "").strip()
        if topic and reason:
            evidence.append(f"{topic}: {reason}")
        elif topic:
            evidence.append(f"Planned focus: {topic}")
        elif reason:
            evidence.append(reason)

    workload = surface.get("recommended_workload") or daily_plan.get(
        "recommended_workload"
    )
    if isinstance(workload, dict) and workload.get("recommended_minutes") is not None:
        evidence.append(
            f"Recommended study time: {workload.get('recommended_minutes')} minutes"
        )

    score = _score_value(readiness)
    if score is not None:
        evidence.append(f"Estimated readiness signal: about {int(round(score))}%")

    if rec_titles:
        evidence.append(f"Related study tip: {rec_titles[0]}")

    mission = surface.get("today_mission")
    if mission is not None and not evidence:
        title = getattr(mission, "title", None)
        if title is None and isinstance(mission, dict):
            title = mission.get("title")
        if title:
            evidence.append(f"Today's Mission: {title}")

    if not evidence:
        evidence.append("Active study plan guides today's authorised focus.")
    return evidence[:6]


def _primary_next_action(
    surface: dict[str, Any],
    slots: list[dict[str, Any]],
) -> str:
    if slots:
        topic = str(slots[0].get("topic_name") or "").strip()
        slot = str(slots[0].get("slot") or "focus").strip()
        if topic:
            return f"Start with {topic} ({slot})"
        return f"Start today's {slot} focus"
    mission = surface.get("today_mission")
    if mission is not None:
        title = getattr(mission, "title", None)
        if title is None and isinstance(mission, dict):
            title = mission.get("title")
        if title:
            return f"Continue: {title}"
    return "Open Today's Mission and complete the next study block"


def _primary_focus_title(
    surface: dict[str, Any],
    slots: list[dict[str, Any]],
) -> str:
    if slots:
        topic = str(slots[0].get("topic_name") or "").strip()
        if topic:
            return topic
    mission = surface.get("today_mission")
    if mission is not None:
        title = getattr(mission, "title", None)
        if title is None and isinstance(mission, dict):
            title = mission.get("title")
        text = str(title or "").strip()
        if text:
            return text
    return ""


def _change_reasoning(
    daily_plan: dict[str, Any],
    slots: list[dict[str, Any]],
    readiness: dict[str, Any],
) -> str:
    explain = daily_plan.get("explainability") or {}
    if isinstance(explain, dict) and explain.get("recovery_mode"):
        missed = explain.get("mission_missed_count") or 0
        return (
            f"Plan adjusted for recovery after {missed} missed session(s) — "
            "prioritising consolidation over new progression."
        )
    slot_names = [str(s.get("slot") or "") for s in slots]
    if "review" in slot_names:
        return "Includes due review to protect spaced repetition."
    if "weak" in slot_names or "recovery" in slot_names:
        return "Prioritises a weaker topic for readiness gain per study hour."
    score = _score_value(readiness)
    if score is not None and score < 45:
        return "Readiness signal is cautious — plan favours completable priorities."
    return "Plan follows authorised syllabus progression for today."


def _why_this_plan(
    slots: list[dict[str, Any]],
    *,
    readiness_alignment: str,
    recommendation_alignment: str,
    plan_coherence: str,
    confidence: str,
) -> str:
    if not slots:
        return (
            "This plan follows your active study sequence for today "
            f"({confidence})."
        )
    parts = [
        f"Priorities: {', '.join(str(s.get('slot') or 'focus') for s in slots)}."
    ]
    if plan_coherence == COHERENCE_RECOVERY:
        parts.append("Recovery mode keeps the day balanced after missed sessions.")
    elif readiness_alignment == COHERENCE_ALIGNED:
        parts.append("Priorities align with your current readiness signal.")
    if recommendation_alignment == COHERENCE_ALIGNED:
        parts.append("Focus order matches recommendation-aware study priorities.")
    elif recommendation_alignment == COHERENCE_ADVISORY:
        parts.append(
            "Study tips remain advisory — Today's Mission stays the plan authority."
        )
    parts.append(f"Confidence: {confidence}.")
    return " ".join(parts)


def _explanation_summary(
    *,
    judgement: str,
    why: str,
    confidence: str,
    next_action: str,
    change_reason: str,
) -> str:
    return (
        f"{judgement}. {why} {change_reason} "
        f"Next: {next_action} ({confidence})."
    )


def _honest_refusal_surface(
    surface: dict[str, Any],
    *,
    reason: str,
) -> dict[str, Any]:
    out = dict(surface)
    judgement = "No study plan ready yet"
    why = reason
    action = "Create or activate a study plan, then return to Today's Mission"
    out.update(
        {
            "judgement": judgement,
            "why_this_plan": why,
            "supporting_evidence": [reason],
            "observed_facts": [reason],
            "confidence_level": CONFIDENCE_CANNOT_ESTIMATE,
            "expected_benefit": (
                "Avoid inventing a study day without an authorised plan."
            ),
            "suggested_next_action": action,
            "next_action": action,
            "review_point": "Revisit after activating a study plan.",
            "plan_drivers": [
                {
                    "driver_id": "no_plan",
                    "label": "No authorised plan",
                    "influence": "blocking",
                    "value": None,
                    "source": "planning",
                    "rationale": reason,
                }
            ],
            "change_reasoning": "Cannot build an adaptive day without an active plan.",
            "explanation_summary": f"{judgement}. {why} Next: {action}.",
            "explanation_schema_version": EXPLANATION_SCHEMA_VERSION,
            "explanation_level": EXPLANATION_LEVEL_DEFAULT,
            "explanation_schema_complete": True,
            "honest_refusal": True,
            "readiness_alignment": COHERENCE_UNAVAILABLE,
            "recommendation_alignment": COHERENCE_UNAVAILABLE,
            "plan_coherence": COHERENCE_UNAVAILABLE,
        }
    )
    explainability = dict(out.get("explainability") or {})
    explainability.update(
        {
            "quality_contract": "ep003.3",
            "honest_refusal": True,
            "explanation_schema_version": EXPLANATION_SCHEMA_VERSION,
        }
    )
    out["explainability"] = explainability
    return out


__all__ = [
    "COHERENCE_ADVISORY",
    "COHERENCE_ALIGNED",
    "COHERENCE_EMPTY",
    "COHERENCE_RECOVERY",
    "COHERENCE_UNAVAILABLE",
    "CONFIDENCE_CANNOT_ESTIMATE",
    "CONFIDENCE_HIGH",
    "CONFIDENCE_LOW",
    "CONFIDENCE_MODERATE",
    "EXPLANATION_LEVEL_DEFAULT",
    "EXPLANATION_SCHEMA_VERSION",
    "SCHEMA_REQUIRED_KEYS",
    "apply_planning_quality_contract",
    "apply_planning_quality_to_daily_plan",
    "has_complete_plan_explanation_schema",
    "quality_reentrancy_depth",
]
