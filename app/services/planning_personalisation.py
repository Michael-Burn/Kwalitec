"""Bounded planning personalisation from Personal Learning Profile (EP-004.3).

Consumes profile attributes as **evidence only**. Plan construction authority
remains ``PlanningService`` / the EP-003.3 quality + adaptive planner path.

Constitutional rules:
- Never change educational slot priority order
  (review → recovery/weak → progression).
- Never invent missions, mastery, readiness scores, or recommendations.
- Ignore unavailable / unsupported / low-confidence attributes (fail-open).
- Every applied adaptation must be explainable and traceable.
"""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)

PERSONALISATION_SCHEMA_VERSION = "ep004.3/v1"

MIN_CONFIDENCE = 0.3
MIN_SAMPLE = 3
MIN_RECOMMENDED_MINUTES = 20

# Educational ladder ranks — personalisation must not violate ascending order.
_SLOT_EDU_RANK = {
    "review": 0,
    "recovery": 1,
    "weak": 1,
    "progression": 2,
}

ATTR_PREFERRED_SESSION_DURATION = "preferred_study_session_duration"
ATTR_CONSISTENCY_TREND = "consistency_trend"
ATTR_RECOVERY_EFFECTIVENESS = "recovery_effectiveness"
ATTR_REVISION_ADHERENCE = "revision_adherence"
ATTR_PLANNING_COMPLETION_RATE = "planning_completion_rate"
ATTR_PREFERRED_STUDY_WINDOWS = "preferred_study_windows"
ATTR_RECOMMENDATION_RESPONSIVENESS = "recommendation_responsiveness"

_PERSONALISATION_MIRROR_KEYS = (
    "personalisation_applied",
    "personalisation_factors",
    "personalisation_schema_version",
    "personalisation_profile_id",
    "session_sizing_guidance",
    "why_this_plan",
    "supporting_evidence",
    "observed_facts",
    "change_reasoning",
    "suggested_next_action",
    "next_action",
    "explanation_summary",
    "recommended_workload",
    "today_missions_slots",
    "revision_priorities",
)


def apply_profile_personalisation(
    surface: dict[str, Any],
    profile_view: dict[str, Any] | None,
) -> dict[str, Any]:
    """Apply bounded, explainable planning personalisation using profile evidence.

    Fail-open: ``None`` / empty / malformed profile leaves the plan unchanged
    aside from neutral personalisation markers.

    Args:
        surface: Schema-enriched plan or dashboard mission surface.
        profile_view: Consumer view from Personal Learning Profile Port.

    Returns:
        Surface with optional personalisation fields and bounded adaptations.
    """
    if not isinstance(surface, dict):
        return surface

    out = dict(surface)
    if out.get("honest_refusal"):
        out.setdefault("personalisation_applied", False)
        out.setdefault("personalisation_factors", [])
        out.setdefault(
            "personalisation_schema_version", PERSONALISATION_SCHEMA_VERSION
        )
        return out

    out.setdefault("personalisation_applied", False)
    out.setdefault("personalisation_factors", [])
    out.setdefault(
        "personalisation_schema_version", PERSONALISATION_SCHEMA_VERSION
    )
    out.setdefault("personalisation_profile_id", None)

    if not isinstance(profile_view, dict) or not profile_view.get("attributes"):
        return out

    attributes = profile_view.get("attributes") or {}
    if not isinstance(attributes, dict):
        return out

    factors: list[dict[str, Any]] = []
    slots = _slots_of(out)
    daily_plan = out.get("daily_plan")
    daily_plan = daily_plan if isinstance(daily_plan, dict) else {}
    workload = _workload_of(out, daily_plan)
    revision_priorities = _revision_priorities_of(out, daily_plan)

    # P1 — session duration (declared preference only).
    duration_factor = _adapt_session_duration(workload, attributes)
    if duration_factor is not None:
        factors.append(duration_factor)
        guidance = str(duration_factor.get("detail") or "")
        if guidance:
            out["session_sizing_guidance"] = guidance

    # P2 — workload pacing (completion + consistency habit summaries).
    factors.extend(_adapt_workload_pacing(workload, attributes))

    # Apply workload minutes to slots after duration/pacing adjustments.
    if factors and slots:
        slots = _rebalance_slot_minutes(slots, workload)
        _write_slots(out, daily_plan, slots)

    # P3 — recovery sequencing (minute emphasis within fixed slot order).
    recovery_factors, slots = _adapt_recovery_sequencing(slots, attributes)
    factors.extend(recovery_factors)

    # P4 — revision timing (review minute emphasis + next-action framing).
    revision_factors, slots, next_note = _adapt_revision_timing(
        slots, attributes, out
    )
    factors.extend(revision_factors)

    # P5 — equivalent slot selection among revision-pool alternatives.
    equiv_factors, slots, revision_priorities = _adapt_equivalent_slot_selection(
        slots, revision_priorities, attributes
    )
    factors.extend(equiv_factors)

    # Preferred study windows remain unsupported — explicit no-op.
    windows = attributes.get(ATTR_PREFERRED_STUDY_WINDOWS)
    if isinstance(windows, dict) and str(windows.get("status") or "") == "unsupported":
        pass

    # Recommendation responsiveness is a tip-preference journal — unused here
    # (Planning must not absorb Recommendation authority via accept/dismiss).
    _ = attributes.get(ATTR_RECOMMENDATION_RESPONSIVENESS)

    if not _educational_order_preserved(slots):
        logger.warning(
            "planning_personalisation_aborted_order_violation user_id=%s",
            profile_view.get("student_id"),
        )
        out["personalisation_applied"] = False
        out["personalisation_factors"] = []
        return surface if isinstance(surface, dict) else out

    _write_slots(out, daily_plan, slots)
    _write_workload(out, daily_plan, workload)
    _write_revision_priorities(out, daily_plan, revision_priorities)

    if next_note:
        action = str(out.get("suggested_next_action") or out.get("next_action") or "")
        if next_note not in action:
            updated = f"{action} {next_note}".strip() if action else next_note
            out["suggested_next_action"] = updated
            out["next_action"] = updated

    out["personalisation_applied"] = bool(factors)
    out["personalisation_factors"] = factors
    out["personalisation_schema_version"] = PERSONALISATION_SCHEMA_VERSION
    profile_id = str(profile_view.get("profile_id") or "").strip() or None
    out["personalisation_profile_id"] = profile_id if factors else None

    if factors:
        _attach_personalisation_explanation(out, factors)

    if daily_plan:
        nested = dict(out.get("daily_plan") or daily_plan)
        for key in _PERSONALISATION_MIRROR_KEYS:
            if key in out:
                nested[key] = out[key]
        if "today_missions_slots" in out:
            nested["today_missions"] = list(out.get("today_missions_slots") or [])
        explain = dict(nested.get("explainability") or {})
        explain["personalisation_applied"] = bool(factors)
        explain["personalisation_schema_version"] = PERSONALISATION_SCHEMA_VERSION
        nested["explainability"] = explain
        out["daily_plan"] = nested

    explainability = dict(out.get("explainability") or {})
    explainability["personalisation_applied"] = bool(factors)
    explainability["personalisation_schema_version"] = PERSONALISATION_SCHEMA_VERSION
    if factors:
        explainability["quality_contract"] = "ep003.3+ep004.3"
    out["explainability"] = explainability
    return out


def _attr(attributes: dict[str, Any], key: str) -> dict[str, Any] | None:
    raw = attributes.get(key)
    if not isinstance(raw, dict):
        return None
    status = str(raw.get("status") or "").strip().lower()
    kind = str(raw.get("kind") or "").strip().lower()
    if status in {"unavailable", "unsupported"} or kind == "unsupported":
        return None
    if status != "available":
        return None
    try:
        confidence = float(raw.get("confidence") or 0.0)
    except (TypeError, ValueError):
        return None
    try:
        sample = int(raw.get("sample_size") or 0)
    except (TypeError, ValueError):
        sample = 0
    if confidence < MIN_CONFIDENCE or sample < MIN_SAMPLE:
        if key != ATTR_PREFERRED_SESSION_DURATION:
            return None
        if confidence < 1.0 or sample < 1:
            return None
    return raw


def _adapt_session_duration(
    workload: dict[str, Any],
    attributes: dict[str, Any],
) -> dict[str, Any] | None:
    duration = _attr(attributes, ATTR_PREFERRED_SESSION_DURATION)
    if duration is None:
        return None
    value = duration.get("value") if isinstance(duration.get("value"), dict) else {}
    minutes = value.get("declared_session_minutes")
    try:
        preferred = int(minutes) if minutes is not None else 0
    except (TypeError, ValueError):
        preferred = 0
    if preferred <= 0:
        return None

    try:
        available = int(workload.get("available_study_minutes") or 0)
    except (TypeError, ValueError):
        available = 0
    try:
        current = int(workload.get("recommended_minutes") or 0)
    except (TypeError, ValueError):
        current = 0

    target = preferred
    if available > 0:
        target = min(preferred, available)
    target = max(MIN_RECOMMENDED_MINUTES, target) if target > 0 else target
    if target <= 0 or target == current:
        # Still annotate guidance even when minutes already match.
        guidance = (
            f"Aim for about {preferred} minutes — your declared preferred "
            f"session length."
        )
        if target == current and current > 0:
            workload["session_duration_informed"] = True
            rationale = str(workload.get("rationale") or "").strip()
            if guidance not in rationale:
                workload["rationale"] = f"{rationale} {guidance}".strip()
            return _factor(
                ATTR_PREFERRED_SESSION_DURATION,
                duration,
                effect="session_duration_guidance",
                detail=guidance,
            )
        return None

    workload["recommended_minutes"] = target
    workload["session_duration_informed"] = True
    guidance = (
        f"Aim for about {preferred} minutes — your declared preferred "
        f"session length."
    )
    rationale = str(workload.get("rationale") or "").strip()
    note = f" Personalised session length toward {target} minutes."
    if note.strip() not in rationale:
        workload["rationale"] = f"{rationale}{note}".strip()
    return _factor(
        ATTR_PREFERRED_SESSION_DURATION,
        duration,
        effect="session_duration_alignment",
        detail=guidance,
    )


def _adapt_workload_pacing(
    workload: dict[str, Any],
    attributes: dict[str, Any],
) -> list[dict[str, Any]]:
    factors: list[dict[str, Any]] = []
    try:
        recommended = int(workload.get("recommended_minutes") or 0)
    except (TypeError, ValueError):
        recommended = 0
    if recommended <= MIN_RECOMMENDED_MINUTES:
        return factors

    planning = _attr(attributes, ATTR_PLANNING_COMPLETION_RATE)
    if planning is not None:
        value = planning.get("value") if isinstance(planning.get("value"), dict) else {}
        rate = _float(value.get("completion_rate"))
        if rate is not None and rate < 0.4:
            reduced = max(MIN_RECOMMENDED_MINUTES, int(recommended * 0.9))
            if reduced < recommended:
                workload["recommended_minutes"] = reduced
                workload["pacing_informed"] = True
                rationale = str(workload.get("rationale") or "").strip()
                note = (
                    " Lower plan-completion behaviour prefers a slightly lighter "
                    "pace so today stays completable."
                )
                if note.strip() not in rationale:
                    workload["rationale"] = f"{rationale}{note}".strip()
                factors.append(
                    _factor(
                        ATTR_PLANNING_COMPLETION_RATE,
                        planning,
                        effect="pace_reduce_when_completion_low",
                        detail=(
                            "Lower plan-completion behaviour prefers a lighter "
                            "daily workload."
                        ),
                    )
                )
                recommended = reduced

    consistency = _attr(attributes, ATTR_CONSISTENCY_TREND)
    if consistency is not None:
        value = (
            consistency.get("value")
            if isinstance(consistency.get("value"), dict)
            else {}
        )
        direction = str(value.get("direction") or "").strip().lower()
        if direction == "declining" and recommended > MIN_RECOMMENDED_MINUTES:
            reduced = max(MIN_RECOMMENDED_MINUTES, int(recommended * 0.9))
            if reduced < recommended:
                workload["recommended_minutes"] = reduced
                workload["pacing_informed"] = True
                rationale = str(workload.get("rationale") or "").strip()
                note = (
                    " Declining consistency habit signal prefers a slightly "
                    "lighter pace."
                )
                if note.strip() not in rationale:
                    workload["rationale"] = f"{rationale}{note}".strip()
                factors.append(
                    _factor(
                        ATTR_CONSISTENCY_TREND,
                        consistency,
                        effect="pace_reduce_when_consistency_declining",
                        detail=(
                            "Declining consistency habit signal prefers a lighter "
                            "daily workload."
                        ),
                    )
                )
    return factors


def _adapt_recovery_sequencing(
    slots: list[dict[str, Any]],
    attributes: dict[str, Any],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    factors: list[dict[str, Any]] = []
    recovery = _attr(attributes, ATTR_RECOVERY_EFFECTIVENESS)
    if recovery is None or not slots:
        return factors, slots

    value = recovery.get("value") if isinstance(recovery.get("value"), dict) else {}
    rate = _float(value.get("follow_through_rate"))
    if rate is None:
        return factors, slots

    repair_idx = _first_slot_index(slots, {"recovery", "weak"})
    progression_idx = _first_slot_index(slots, {"progression"})
    if repair_idx is None:
        return factors, slots

    slots = [dict(s) for s in slots]
    repair = slots[repair_idx]
    repair_mins = _int(repair.get("allocated_minutes"), default=0)

    if rate >= 0.5 and progression_idx is not None:
        progression = slots[progression_idx]
        prog_mins = _int(progression.get("allocated_minutes"), default=0)
        transfer = min(5, max(0, prog_mins - 5))
        if transfer > 0:
            progression["allocated_minutes"] = prog_mins - transfer
            repair["allocated_minutes"] = repair_mins + transfer
            reason = str(repair.get("reason") or "").strip()
            note = " Recovery follow-through supports emphasising repair today."
            if note.strip() not in reason:
                repair["reason"] = f"{reason}{note}".strip()
            factors.append(
                _factor(
                    ATTR_RECOVERY_EFFECTIVENESS,
                    recovery,
                    effect="recovery_emphasise_follow_through",
                    detail=(
                        "Prior recovery follow-through supports emphasising "
                        "repair minutes within today's authorised slot order."
                    ),
                )
            )
    elif rate < 0.3 and repair_mins > 10:
        lighten = min(5, repair_mins - 10)
        if lighten > 0:
            repair["allocated_minutes"] = repair_mins - lighten
            if progression_idx is not None:
                progression = slots[progression_idx]
                progression["allocated_minutes"] = (
                    _int(progression.get("allocated_minutes"), default=0) + lighten
                )
            reason = str(repair.get("reason") or "").strip()
            note = " Lighter repair pressure while rebuilding follow-through."
            if note.strip() not in reason:
                repair["reason"] = f"{reason}{note}".strip()
            factors.append(
                _factor(
                    ATTR_RECOVERY_EFFECTIVENESS,
                    recovery,
                    effect="recovery_lighten_low_follow_through",
                    detail=(
                        "Lower recovery follow-through prefers lighter repair "
                        "pressure within today's authorised slot order."
                    ),
                )
            )
    return factors, slots


def _adapt_revision_timing(
    slots: list[dict[str, Any]],
    attributes: dict[str, Any],
    surface: dict[str, Any],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], str | None]:
    factors: list[dict[str, Any]] = []
    next_note: str | None = None
    revision = _attr(attributes, ATTR_REVISION_ADHERENCE)
    if revision is None or not slots:
        return factors, slots, None

    value = revision.get("value") if isinstance(revision.get("value"), dict) else {}
    rate = _float(value.get("adherence_rate"))
    if rate is None:
        return factors, slots, None

    review_idx = _first_slot_index(slots, {"review"})
    if review_idx is None:
        return factors, slots, None

    slots = [dict(s) for s in slots]
    review = slots[review_idx]
    review_mins = _int(review.get("allocated_minutes"), default=0)
    progression_idx = _first_slot_index(slots, {"progression"})

    if rate >= 0.6:
        if progression_idx is not None:
            progression = slots[progression_idx]
            prog_mins = _int(progression.get("allocated_minutes"), default=0)
            transfer = min(5, max(0, prog_mins - 5))
            if transfer > 0:
                progression["allocated_minutes"] = prog_mins - transfer
                review["allocated_minutes"] = review_mins + transfer
        topic = str(review.get("topic_name") or "").strip()
        next_note = (
            f"Start with review{f' ({topic})' if topic else ''} first — "
            "your revision adherence supports protecting spaced repetition."
        )
        # Reinforce primary action only when review is already first educationally.
        if review_idx == 0:
            action = str(
                surface.get("suggested_next_action") or surface.get("next_action") or ""
            )
            if topic and f"Start with {topic}" not in action:
                surface["suggested_next_action"] = f"Start with {topic} (review)"
                surface["next_action"] = surface["suggested_next_action"]
        factors.append(
            _factor(
                ATTR_REVISION_ADHERENCE,
                revision,
                effect="revision_boost_adherence",
                detail=(
                    "Observed revision adherence supports protecting review "
                    "timing within today's authorised priorities."
                ),
            )
        )
    elif rate < 0.3:
        topic = str(review.get("topic_name") or "").strip()
        next_note = (
            "Complete today's review block before deferring — protecting "
            "revision timing."
        )
        if topic:
            next_note = (
                f"Complete review of {topic} before deferring — protecting "
                "revision timing."
            )
        factors.append(
            _factor(
                ATTR_REVISION_ADHERENCE,
                revision,
                effect="revision_protect_when_deferred_risk",
                detail=(
                    "Lower revision adherence prefers completing the authorised "
                    "review block before deferring."
                ),
            )
        )
    return factors, slots, next_note


def _adapt_equivalent_slot_selection(
    slots: list[dict[str, Any]],
    revision_priorities: list[dict[str, Any]],
    attributes: dict[str, Any],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    """Prefer an alternative revision-pool topic for weak/recovery when lawful.

    Educational role stays weak/recovery. Only swaps among revision_priorities
    candidates (equivalent repair/revision pool), never invents topics or
    changes slot types / order.
    """
    factors: list[dict[str, Any]] = []
    if len(revision_priorities) < 2 or not slots:
        return factors, slots, revision_priorities

    recovery = _attr(attributes, ATTR_RECOVERY_EFFECTIVENESS)
    if recovery is None:
        return factors, slots, revision_priorities

    value = recovery.get("value") if isinstance(recovery.get("value"), dict) else {}
    rate = _float(value.get("follow_through_rate"))
    # Prefer a slightly lighter alternative only when follow-through is low.
    if rate is None or rate >= 0.3:
        return factors, slots, revision_priorities

    repair_idx = _first_slot_index(slots, {"recovery", "weak"})
    if repair_idx is None:
        return factors, slots, revision_priorities

    slots = [dict(s) for s in slots]
    repair = slots[repair_idx]
    current_id = str(repair.get("topic_id") or "").strip()
    priorities = [dict(p) for p in revision_priorities if isinstance(p, dict)]
    if len(priorities) < 2:
        return factors, slots, revision_priorities

    top = priorities[0]
    alt = priorities[1]
    top_id = str(top.get("topic_id") or "").strip()
    alt_id = str(alt.get("topic_id") or "").strip()
    alt_name = str(alt.get("topic_name") or "").strip()
    if not alt_id or not alt_name:
        return factors, slots, revision_priorities
    if current_id and current_id != top_id:
        # Already not on the top priority — leave educational selection alone.
        return factors, slots, revision_priorities

    repair["topic_id"] = alt_id
    repair["topic_name"] = alt_name
    reason = str(repair.get("reason") or "").strip()
    note = (
        " Equivalent repair topic selected for recoverability "
        "(behavioural follow-through preference)."
    )
    if note.strip() not in reason:
        repair["reason"] = f"{reason}{note}".strip()

    # Keep priorities list educationally honest: move alt ahead of top for display.
    reordered = [alt, top, *priorities[2:]]
    factors.append(
        _factor(
            ATTR_RECOVERY_EFFECTIVENESS,
            recovery,
            effect="equivalent_repair_topic_preference",
            detail=(
                "Lower recovery follow-through prefers an equivalent revision-pool "
                f"topic ({alt_name}) for today's repair slot."
            ),
        )
    )
    return factors, slots, reordered


def _rebalance_slot_minutes(
    slots: list[dict[str, Any]],
    workload: dict[str, Any],
) -> list[dict[str, Any]]:
    """Re-share recommended minutes across slots using existing weights."""
    try:
        total = int(workload.get("recommended_minutes") or 0)
    except (TypeError, ValueError):
        total = 0
    if total <= 0 or not slots:
        return slots

    weights = {
        "review": 35,
        "recovery": 35,
        "weak": 35,
        "progression": 30,
    }
    weight_list = [weights.get(str(s.get("slot") or ""), 30) for s in slots]
    weight_sum = sum(weight_list) or len(slots)
    remaining = total
    out: list[dict[str, Any]] = []
    for index, slot in enumerate(slots):
        row = dict(slot)
        if index == len(slots) - 1:
            mins = max(0, remaining)
        else:
            raw = int(round(total * weight_list[index] / weight_sum))
            mins = max(5, raw) if total >= 15 else max(0, raw)
            mins = min(mins, remaining)
            remaining -= mins
        row["allocated_minutes"] = mins
        out.append(row)
    return out


def _attach_personalisation_explanation(
    surface: dict[str, Any],
    factors: list[dict[str, Any]],
) -> None:
    if not factors:
        return

    evidence = list(surface.get("supporting_evidence") or [])
    for factor in factors:
        line = str(factor.get("student_evidence") or "").strip()
        if line and line not in evidence:
            evidence.append(line)
    surface["supporting_evidence"] = evidence[:8]
    observed = list(surface.get("observed_facts") or [])
    for factor in factors:
        line = str(factor.get("student_evidence") or "").strip()
        if line and line not in observed:
            observed.append(line)
    surface["observed_facts"] = observed[:8]

    why = str(surface.get("why_this_plan") or "").strip()
    note = " Personalised using your observed study habits where evidence allows."
    if note.strip() not in why:
        surface["why_this_plan"] = (why + note).strip()

    change = str(surface.get("change_reasoning") or "").strip()
    change_note = (
        "Plan pacing/structure adjusted from Personal Learning Profile evidence."
    )
    if change_note not in change:
        surface["change_reasoning"] = f"{change} {change_note}".strip()

    summary = str(surface.get("explanation_summary") or "").strip()
    if note.strip() not in summary and surface.get("why_this_plan"):
        surface["explanation_summary"] = (
            f"{surface.get('judgement') or ''}. {surface['why_this_plan']} "
            f"{surface.get('change_reasoning') or ''} "
            f"Next: {surface.get('suggested_next_action') or ''} "
            f"({surface.get('confidence_level') or ''})."
        ).strip()


def _factor(
    attribute_key: str,
    attr: dict[str, Any],
    *,
    effect: str,
    detail: str,
) -> dict[str, Any]:
    confidence = float(attr.get("confidence") or 0.0)
    sample = int(attr.get("sample_size") or 0)
    explanation = str(attr.get("explanation") or "").strip()
    student_evidence = f"Personalisation evidence ({attribute_key}): {detail}"
    return {
        "attribute_key": attribute_key,
        "claim_boundary": str(attr.get("claim_boundary") or ""),
        "confidence": confidence,
        "detail": detail,
        "effect": effect,
        "kind": str(attr.get("kind") or ""),
        "profile_explanation": explanation,
        "sample_size": sample,
        "student_evidence": student_evidence,
    }


def _slots_of(surface: dict[str, Any]) -> list[dict[str, Any]]:
    daily_plan = surface.get("daily_plan")
    raw = surface.get("today_missions_slots")
    if not raw and isinstance(daily_plan, dict):
        raw = daily_plan.get("today_missions")
    if not isinstance(raw, list):
        # Daily plan payload used directly (no surface wrapper).
        raw = surface.get("today_missions")
    if not isinstance(raw, list):
        return []
    return [dict(item) for item in raw if isinstance(item, dict)]


def _workload_of(
    surface: dict[str, Any],
    daily_plan: dict[str, Any],
) -> dict[str, Any]:
    workload = surface.get("recommended_workload")
    if not isinstance(workload, dict):
        workload = daily_plan.get("recommended_workload")
    if not isinstance(workload, dict):
        return {}
    return dict(workload)


def _revision_priorities_of(
    surface: dict[str, Any],
    daily_plan: dict[str, Any],
) -> list[dict[str, Any]]:
    raw = surface.get("revision_priorities")
    if not isinstance(raw, list):
        raw = daily_plan.get("revision_priorities")
    if not isinstance(raw, list):
        return []
    return [dict(item) for item in raw if isinstance(item, dict)]


def _write_slots(
    surface: dict[str, Any],
    daily_plan: dict[str, Any],
    slots: list[dict[str, Any]],
) -> None:
    surface["today_missions_slots"] = slots
    if "today_missions" in surface or not daily_plan:
        surface["today_missions"] = slots
    if daily_plan:
        nested = dict(surface.get("daily_plan") or daily_plan)
        nested["today_missions"] = slots
        surface["daily_plan"] = nested


def _write_workload(
    surface: dict[str, Any],
    daily_plan: dict[str, Any],
    workload: dict[str, Any],
) -> None:
    surface["recommended_workload"] = workload
    if daily_plan:
        nested = dict(surface.get("daily_plan") or daily_plan)
        nested["recommended_workload"] = workload
        surface["daily_plan"] = nested


def _write_revision_priorities(
    surface: dict[str, Any],
    daily_plan: dict[str, Any],
    priorities: list[dict[str, Any]],
) -> None:
    surface["revision_priorities"] = priorities
    if daily_plan:
        nested = dict(surface.get("daily_plan") or daily_plan)
        nested["revision_priorities"] = priorities
        surface["daily_plan"] = nested


def _first_slot_index(
    slots: list[dict[str, Any]],
    names: set[str],
) -> int | None:
    for index, slot in enumerate(slots):
        if str(slot.get("slot") or "") in names:
            return index
    return None


def _educational_order_preserved(slots: list[dict[str, Any]]) -> bool:
    ranks = [_SLOT_EDU_RANK.get(str(s.get("slot") or ""), 9) for s in slots]
    return ranks == sorted(ranks)


def _float(value: Any) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _int(value: Any, *, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


__all__ = [
    "ATTR_CONSISTENCY_TREND",
    "ATTR_PLANNING_COMPLETION_RATE",
    "ATTR_PREFERRED_SESSION_DURATION",
    "ATTR_PREFERRED_STUDY_WINDOWS",
    "ATTR_RECOVERY_EFFECTIVENESS",
    "ATTR_REVISION_ADHERENCE",
    "MIN_CONFIDENCE",
    "MIN_SAMPLE",
    "PERSONALISATION_SCHEMA_VERSION",
    "apply_profile_personalisation",
]
