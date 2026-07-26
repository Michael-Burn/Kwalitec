"""Readiness quality contract (EP-003.2).

Applies Product Constitution and P-001.2 Explainability Standard to Runtime A
readiness surfaces produced by ``ReadinessService``.

Ownership:
- Evaluation / score / drivers / schema attachment remain ReadinessService
  authority (this module is called only from that service).
- Consumes Planning mission surface for next-action *labelling* only —
  never invents missions or recommendations.
- Does not duplicate RecommendationService selection or PlanningService maths.
"""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)

EXPLANATION_SCHEMA_VERSION = "p001.2/v1"
EXPLANATION_LEVEL_DEFAULT = "level_2"

CONFIDENCE_HIGH = "High confidence"
CONFIDENCE_MODERATE = "Moderate confidence"
CONFIDENCE_LOW = "Low confidence / Suggested"
CONFIDENCE_CANNOT_ESTIMATE = "Cannot yet be estimated"

_INTERNAL_CONFIDENCE_MAP = {
    "very_low": CONFIDENCE_CANNOT_ESTIMATE,
    "low": CONFIDENCE_LOW,
    "medium": CONFIDENCE_MODERATE,
    "high": CONFIDENCE_HIGH,
}

SCHEMA_REQUIRED_KEYS = (
    "judgement",
    "why_this_estimate",
    "supporting_evidence",
    "confidence_level",
    "expected_benefit",
    "suggested_next_action",
    "review_point",
    "readiness_drivers",
    "explanation_schema_version",
    "explanation_level",
)


def has_complete_readiness_explanation_schema(
    surface: dict[str, Any] | None,
) -> bool:
    """True when a readiness surface carries the mandatory explanation schema."""
    if not isinstance(surface, dict):
        return False
    if surface.get("honest_refusal"):
        return all(
            str(surface.get(key) or "").strip()
            for key in (
                "judgement",
                "why_this_estimate",
                "confidence_level",
                "suggested_next_action",
            )
        )
    for key in (
        "judgement",
        "why_this_estimate",
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
    drivers = surface.get("readiness_drivers")
    if not isinstance(drivers, list) or len(drivers) == 0:
        return False
    return bool(surface.get("explanation_schema_complete"))


def apply_readiness_quality_contract(
    user_id: int,
    surface: dict[str, Any],
    *,
    previous_score: float | None = None,
) -> dict[str, Any]:
    """Enrich a dashboard readiness surface to the P-001.2 contract.

    Fail-open: mission lookup failures degrade next-action copy only.
    Never recalculates the readiness score.
    """
    if not isinstance(surface, dict):
        return surface

    out = dict(surface)
    readiness = out.get("readiness")
    readiness = readiness if isinstance(readiness, dict) else {}

    can_estimate, refusal_reason = _estimate_eligibility(readiness, out)
    if not can_estimate:
        return _honest_refusal_surface(out, readiness, refusal_reason)

    drivers = _ensure_explicit_drivers(out, readiness)
    out["readiness_drivers"] = drivers

    student_confidence = _student_confidence_label(out, readiness, drivers)
    out["confidence_level"] = student_confidence

    evidence = _supporting_evidence(out, readiness, drivers)
    out["supporting_evidence"] = evidence
    out["observed_facts"] = list(evidence)

    primary_action = _primary_next_action(user_id, out)
    out["suggested_next_action"] = primary_action
    out["next_action"] = primary_action

    change_reason = _change_reasoning(
        readiness,
        drivers,
        previous_score=previous_score,
        prior_change=out.get("change_reasoning"),
    )
    out["change_reasoning"] = change_reason

    why = _why_this_estimate(readiness, drivers, student_confidence)
    expected_benefit = (
        "Help you judge study preparation honestly and choose the next "
        "useful study step."
    )
    # PX-002A copy standard: "Session" is the approved term.
    review_point = "Reassess after your next completed session or plan refresh."

    score = _score_value(readiness)
    judgement = (
        f"Estimated readiness: about {int(round(score))}%"
        if score is not None
        else "Estimated readiness: provisional"
    )

    out["judgement"] = judgement
    out["why_this_estimate"] = why
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
            "quality_contract": "ep003.2",
            "explanation_schema_version": EXPLANATION_SCHEMA_VERSION,
            "confidence_student_label": student_confidence,
            "primary_next_action": primary_action,
            "change_reasoning": change_reason,
        }
    )
    out["explainability"] = explainability
    return out


def apply_readiness_quality_to_assessment(
    user_id: int,
    assessment: dict[str, Any],
    *,
    previous_score: float | None = None,
) -> dict[str, Any]:
    """Enrich a Twin readiness intelligence assessment dict via surface mapping."""
    if not isinstance(assessment, dict):
        return assessment

    score = assessment.get("readiness_score")
    surface = {
        "readiness": {
            "score": score,
            "coverage_pct": None,
            "avg_mastery": None,
            "review_discipline": None,
            "total_topics": 1 if score is not None else 0,
            "topics_started": 1 if score is not None else 0,
            "topics_mastered": 0,
        },
        "weakest_topics": [
            _area_as_topic(a) for a in (assessment.get("weakest_areas") or [])
        ],
        "strongest_topics": [
            _area_as_topic(a) for a in (assessment.get("strongest_areas") or [])
        ],
        "source_authority": "readiness_intelligence",
        "confidence_level": assessment.get("confidence_level") or "",
        "limitations_codes": list(assessment.get("limitations_codes") or []),
        "readiness_drivers": list(assessment.get("readiness_drivers") or []),
        "recommended_next_actions": list(
            assessment.get("recommended_next_actions") or []
        ),
        "explainability": dict(assessment.get("explainability") or {}),
    }

    # Prefer component values from drivers when present.
    for driver in surface["readiness_drivers"]:
        if not isinstance(driver, dict):
            continue
        driver_id = str(driver.get("driver_id") or "")
        value = driver.get("value")
        try:
            numeric = float(value) if value is not None else None
        except (TypeError, ValueError):
            numeric = None
        if numeric is None:
            continue
        if driver_id == "curriculum_coverage":
            surface["readiness"]["coverage_pct"] = numeric
        elif driver_id == "knowledge_strength":
            surface["readiness"]["avg_mastery"] = numeric
        elif driver_id == "mission_discipline":
            surface["readiness"]["review_discipline"] = numeric

    enriched = apply_readiness_quality_contract(
        user_id,
        surface,
        previous_score=previous_score,
    )

    out = dict(assessment)
    for key in (
        "judgement",
        "why_this_estimate",
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
        "readiness_drivers",
    ):
        if key in enriched:
            out[key] = enriched[key]

    explainability = dict(out.get("explainability") or {})
    explainability.update(dict(enriched.get("explainability") or {}))
    out["explainability"] = explainability
    return out


def _area_as_topic(area: Any) -> dict[str, Any]:
    if not isinstance(area, dict):
        return {}
    return {
        "topic_id": area.get("topic_id"),
        "topic_name": area.get("topic_name"),
        "mastery_score": area.get("mastery_score"),
        "reason": area.get("reason"),
    }


def _score_value(readiness: dict[str, Any]) -> float | None:
    raw = readiness.get("score")
    if raw is None:
        return None
    try:
        return float(raw)
    except (TypeError, ValueError):
        return None


def _estimate_eligibility(
    readiness: dict[str, Any],
    surface: dict[str, Any],
) -> tuple[bool, str]:
    total = int(readiness.get("total_topics") or 0)
    started = int(readiness.get("topics_started") or 0)
    score = _score_value(readiness)
    has_drivers = bool(surface.get("readiness_drivers"))

    if total > 0 and started <= 0 and (score is None or score <= 0):
        return False, (
            "No topics started yet — coverage and practice history are empty."
        )
    if score is None and not has_drivers:
        if total <= 0:
            return False, "No syllabus topics are available for an estimate yet."
        return False, "Readiness assessment did not supply a score."
    # Score present (including Twin projection without legacy topic counts).
    if score is not None or has_drivers:
        return True, ""
    return False, "No syllabus topics are available for an estimate yet."


def _honest_refusal_surface(
    surface: dict[str, Any],
    readiness: dict[str, Any],
    reason: str,
) -> dict[str, Any]:
    out = dict(surface)
    next_action = (
        "Complete a short study session on your Current Learning Topic "
        "so readiness can be estimated."
    )
    drivers = [
        {
            "driver_id": "evidence_density",
            "label": "Evidence density",
            "influence": "risk_elevating",
            "value": 0,
            "source": "runtime_a.readiness_quality",
            "rationale": reason,
        }
    ]
    out.update(
        {
            "readiness_drivers": drivers,
            "confidence_level": CONFIDENCE_CANNOT_ESTIMATE,
            "judgement": "Estimated readiness: cannot yet be estimated",
            "why_this_estimate": reason,
            "supporting_evidence": [reason],
            "observed_facts": [reason],
            "expected_benefit": (
                "Avoid fabricated certainty until enough study evidence exists."
            ),
            "suggested_next_action": next_action,
            "next_action": next_action,
            "review_point": "Reassess after your next completed session.",
            "change_reasoning": (
                "No prior estimate to compare — evidence is still insufficient."
            ),
            "explanation_summary": (
                f"{reason} Suggested next step: {next_action}"
            ),
            "explanation_schema_version": EXPLANATION_SCHEMA_VERSION,
            "explanation_level": EXPLANATION_LEVEL_DEFAULT,
            "explanation_schema_complete": True,
            "honest_refusal": True,
        }
    )
    explainability = dict(out.get("explainability") or {})
    explainability.update(
        {
            "quality_contract": "ep003.2",
            "status": "cannot_estimate",
            "explanation_schema_version": EXPLANATION_SCHEMA_VERSION,
        }
    )
    out["explainability"] = explainability
    # Preserve readiness dict for collectors / templates.
    out["readiness"] = readiness if readiness else out.get("readiness") or {}
    return out


def _ensure_explicit_drivers(
    surface: dict[str, Any],
    readiness: dict[str, Any],
) -> list[dict[str, Any]]:
    existing = surface.get("readiness_drivers")
    if isinstance(existing, list) and existing:
        normalised: list[dict[str, Any]] = []
        for row in existing:
            if isinstance(row, dict) and str(row.get("driver_id") or "").strip():
                normalised.append(dict(row))
        if normalised:
            return normalised

    drivers: list[dict[str, Any]] = []
    coverage = readiness.get("coverage_pct")
    mastery = readiness.get("avg_mastery")
    review = readiness.get("review_discipline")

    drivers.append(
        _component_driver(
            driver_id="curriculum_coverage",
            label="Curriculum coverage",
            value=coverage,
            weight_note="50% of estimated readiness",
            rationale_prefix="Syllabus leaves started",
        )
    )
    drivers.append(
        _component_driver(
            driver_id="knowledge_strength",
            label="Knowledge strength",
            value=mastery,
            weight_note="30% of estimated readiness",
            rationale_prefix="Average Estimated Knowledge on started topics",
        )
    )
    drivers.append(
        _component_driver(
            driver_id="mission_discipline",
            label="Review discipline",
            value=review,
            weight_note="20% of estimated readiness",
            rationale_prefix="Recent review / mission completion",
        )
    )

    started = int(readiness.get("topics_started") or 0)
    total = int(readiness.get("total_topics") or 0)
    drivers.append(
        {
            "driver_id": "evidence_density",
            "label": "Evidence density",
            "influence": (
                "supportive"
                if started >= max(3, total // 4)
                else ("mixed" if started >= 1 else "risk_elevating")
            ),
            "value": started,
            "source": "runtime_a.get_overall_readiness",
            "rationale": (
                f"{started} of {total} syllabus topics started "
                "(practice history density)."
            ),
        }
    )
    return drivers


def _component_driver(
    *,
    driver_id: str,
    label: str,
    value: Any,
    weight_note: str,
    rationale_prefix: str,
) -> dict[str, Any]:
    try:
        numeric = float(value) if value is not None else None
    except (TypeError, ValueError):
        numeric = None
    influence = "unknown"
    if numeric is not None:
        if numeric >= 70.0:
            influence = "supportive"
        elif numeric >= 40.0:
            influence = "mixed"
        else:
            influence = "risk_elevating"
    rationale = (
        f"{rationale_prefix} (~{int(round(numeric))}%). {weight_note}."
        if numeric is not None
        else f"{rationale_prefix} unavailable. {weight_note}."
    )
    return {
        "driver_id": driver_id,
        "label": label,
        "influence": influence,
        "value": numeric,
        "source": "runtime_a.get_overall_readiness",
        "rationale": rationale,
    }


def _student_confidence_label(
    surface: dict[str, Any],
    readiness: dict[str, Any],
    drivers: list[dict[str, Any]],
) -> str:
    existing = str(surface.get("confidence_level") or "").strip()
    if existing in {
        CONFIDENCE_HIGH,
        CONFIDENCE_MODERATE,
        CONFIDENCE_LOW,
        CONFIDENCE_CANNOT_ESTIMATE,
    }:
        return existing

    mapped = _INTERNAL_CONFIDENCE_MAP.get(existing.lower())
    if mapped:
        return mapped

    started = int(readiness.get("topics_started") or 0)
    total = int(readiness.get("total_topics") or 0)
    coverage = float(readiness.get("coverage_pct") or 0.0)
    risk_drivers = sum(
        1 for d in drivers if str(d.get("influence") or "") == "risk_elevating"
    )

    if started <= 0 or total <= 0:
        return CONFIDENCE_CANNOT_ESTIMATE
    if started < 3 or coverage < 15.0:
        return CONFIDENCE_LOW
    if started >= max(5, total // 3) and coverage >= 35.0 and risk_drivers <= 1:
        return CONFIDENCE_HIGH
    return CONFIDENCE_MODERATE


def _supporting_evidence(
    surface: dict[str, Any],
    readiness: dict[str, Any],
    drivers: list[dict[str, Any]],
) -> list[str]:
    existing = surface.get("supporting_evidence") or surface.get("observed_facts")
    if isinstance(existing, list | tuple):
        points = [str(p).strip() for p in existing if str(p).strip()]
        if points:
            return points[:5]

    points: list[str] = []
    started = int(readiness.get("topics_started") or 0)
    total = int(readiness.get("total_topics") or 0)
    if total > 0:
        points.append(f"{started} of {total} syllabus topics started.")

    for key, label in (
        ("coverage_pct", "Syllabus coverage"),
        ("avg_mastery", "Average Estimated Knowledge"),
        ("review_discipline", "Review discipline"),
    ):
        raw = readiness.get(key)
        try:
            if raw is not None:
                points.append(f"{label} ~{int(round(float(raw)))}%.")
        except (TypeError, ValueError):
            continue

    weak = surface.get("weakest_topics") or []
    if isinstance(weak, list) and weak:
        first = weak[0] if isinstance(weak[0], dict) else {}
        name = str(
            first.get("topic_name") or first.get("name") or first.get("title") or ""
        ).strip()
        if name:
            points.append(f"Lower Estimated Knowledge area: {name}.")

    for driver in drivers[:2]:
        rationale = str(driver.get("rationale") or "").strip()
        label = str(driver.get("label") or "").strip()
        if rationale:
            points.append(rationale)
        elif label:
            points.append(label)

    # Deduplicate while preserving order.
    seen: set[str] = set()
    unique: list[str] = []
    for point in points:
        if point not in seen:
            seen.add(point)
            unique.append(point)
    return unique[:5] or [
        "Estimated readiness uses syllabus coverage, Estimated Knowledge, "
        "and review habits."
    ]


def _primary_next_action(user_id: int, surface: dict[str, Any]) -> str:
    actions = surface.get("recommended_next_actions") or []
    if isinstance(actions, list):
        for action in actions:
            if isinstance(action, str) and action.strip():
                return action.strip()
            if not isinstance(action, dict):
                continue
            for key in ("title", "action", "text", "label"):
                value = action.get(key)
                if value is not None and str(value).strip():
                    return str(value).strip()

    focus = _resolve_authorised_today_focus(user_id)
    if focus:
        return f"Continue Today’s Mission: {focus}."

    weak = surface.get("weakest_topics") or []
    if isinstance(weak, list) and weak:
        first = weak[0] if isinstance(weak[0], dict) else {}
        name = str(
            first.get("topic_name") or first.get("name") or first.get("title") or ""
        ).strip()
        if name:
            return (
                f"After Today’s Mission, practise {name} to repair a weaker area."
            )

    # PX-002A copy standard: "Session" is the approved term ("study session"
    # is a rejected synonym — see app/presentation/product_language.py).
    return "Open Today’s Session and complete the next planned study block."


def _resolve_authorised_today_focus(user_id: int) -> str | None:
    """Read Today's Mission title for next-action labelling — never invents plans."""
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
    except Exception:  # noqa: BLE001 — fail-open next action
        logger.debug(
            "readiness_quality_mission_lookup_failed user_id=%s",
            user_id,
            exc_info=True,
        )
        return None


def _change_reasoning(
    readiness: dict[str, Any],
    drivers: list[dict[str, Any]],
    *,
    previous_score: float | None,
    prior_change: Any,
) -> str:
    if isinstance(prior_change, str) and prior_change.strip():
        return prior_change.strip()

    score = _score_value(readiness)
    if previous_score is not None and score is not None:
        delta = score - float(previous_score)
        if abs(delta) < 0.5:
            direction = "unchanged"
        elif delta > 0:
            direction = f"up about {int(round(abs(delta)))} points"
        else:
            direction = f"down about {int(round(abs(delta)))} points"
    else:
        direction = None

    supportive = [
        str(d.get("label") or d.get("driver_id") or "").strip()
        for d in drivers
        if str(d.get("influence") or "") == "supportive"
    ]
    risks = [
        str(d.get("label") or d.get("driver_id") or "").strip()
        for d in drivers
        if str(d.get("influence") or "") == "risk_elevating"
    ]
    supportive = [s for s in supportive if s][:2]
    risks = [r for r in risks if r][:2]

    parts: list[str] = []
    if direction == "unchanged":
        parts.append("Estimated readiness is broadly unchanged since the last view.")
    elif direction:
        parts.append(f"Estimated readiness moved {direction} since the last view.")
    else:
        parts.append(
            "Score change vs a prior session is not available yet — "
            "current drivers explain this estimate."
        )

    if supportive:
        parts.append(f"Supportive drivers: {', '.join(supportive)}.")
    if risks:
        parts.append(f"Holding the estimate back: {', '.join(risks)}.")
    if not supportive and not risks:
        parts.append(
            "Coverage, Estimated Knowledge, and review habits jointly shape "
            "this estimate."
        )
    return " ".join(parts)


def _why_this_estimate(
    readiness: dict[str, Any],
    drivers: list[dict[str, Any]],
    confidence: str,
) -> str:
    coverage = readiness.get("coverage_pct")
    mastery = readiness.get("avg_mastery")
    review = readiness.get("review_discipline")
    try:
        parts = []
        if coverage is not None:
            parts.append(f"syllabus coverage (~{int(round(float(coverage)))}%)")
        if mastery is not None:
            parts.append(
                f"average Estimated Knowledge (~{int(round(float(mastery)))}%)"
            )
        if review is not None:
            parts.append(f"review habits (~{int(round(float(review)))}%)")
        if parts:
            basis = ", ".join(parts)
            return (
                f"This estimate combines {basis}. "
                f"Confidence: {confidence}."
            )
    except (TypeError, ValueError):
        pass

    top = [
        str(d.get("label") or "").strip()
        for d in drivers[:3]
        if str(d.get("label") or "").strip()
    ]
    if top:
        return (
            f"This estimate is driven by {', '.join(top)}. "
            f"Confidence: {confidence}."
        )
    return (
        "This is a provisional study-preparation judgement from authorised "
        f"readiness signals. Confidence: {confidence}."
    )


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
        f"Suggested next step: {next_action} ({confidence})."
    )


__all__ = [
    "CONFIDENCE_CANNOT_ESTIMATE",
    "CONFIDENCE_HIGH",
    "CONFIDENCE_LOW",
    "CONFIDENCE_MODERATE",
    "EXPLANATION_LEVEL_DEFAULT",
    "EXPLANATION_SCHEMA_VERSION",
    "SCHEMA_REQUIRED_KEYS",
    "apply_readiness_quality_contract",
    "apply_readiness_quality_to_assessment",
    "has_complete_readiness_explanation_schema",
]
