"""Bounded recommendation personalisation from Personal Learning Profile (EP-004.2).

Consumes profile attributes as **evidence only**. Ranking authority remains
``RecommendationService`` / the P-001.3 Decision Framework.

Constitutional rules:
- Never change ladder ranks for safety / authorised Today’s Mission / blocking
  deficit (ranks 1–3).
- Never invent educational warrants from preference or habit summaries.
- Never treat accept/dismiss as mastery or recommendation correctness.
- Ignore unavailable / unsupported / low-confidence attributes (fail-open).
- Every applied adjustment must be explainable and traceable.
"""

from __future__ import annotations

import logging
from typing import Any

from app.services.recommendation_quality import (
    CATEGORY_MOCK_EXAM,
    CATEGORY_NEW_TOPIC,
    CATEGORY_REST,
    CATEGORY_REVIEW,
    CATEGORY_REVISION,
    CATEGORY_STUDY_STRENGTH,
    CATEGORY_WEAK_TOPIC,
    LADDER_AUTHORISED_TODAY,
    LADDER_BLOCKING_DEFICIT,
    LADDER_SAFETY,
    PRIORITY_ORDER,
)

logger = logging.getLogger(__name__)

PERSONALISATION_SCHEMA_VERSION = "ep004.2/v1"

# Sample-sufficiency gate (aligns with profile confidence = sample/10).
MIN_CONFIDENCE = 0.3
MIN_SAMPLE = 3

# Neutral tie-break; lower sorts earlier within the same ladder + priority.
TIE_NEUTRAL = 50
TIE_MIN = 0
TIE_MAX = 99

# Protected ladder ranks — personalisation must not reclassify these.
_PROTECTED_LADDER = frozenset(
    {LADDER_SAFETY, LADDER_AUTHORISED_TODAY, LADDER_BLOCKING_DEFICIT}
)

ATTR_PREFERRED_SESSION_DURATION = "preferred_study_session_duration"
ATTR_CONSISTENCY_TREND = "consistency_trend"
ATTR_RECOVERY_EFFECTIVENESS = "recovery_effectiveness"
ATTR_REVISION_ADHERENCE = "revision_adherence"
ATTR_RECOMMENDATION_RESPONSIVENESS = "recommendation_responsiveness"
ATTR_PLANNING_COMPLETION_RATE = "planning_completion_rate"
ATTR_PREFERRED_STUDY_WINDOWS = "preferred_study_windows"


def apply_profile_personalisation(
    recommendations: list[dict[str, Any]],
    profile_view: dict[str, Any] | None,
    *,
    limit: int = 5,
) -> list[dict[str, Any]]:
    """Apply bounded, explainable personalisation using profile evidence.

    Fail-open: ``None`` / empty / malformed profile leaves recommendations
    unchanged (aside from ensuring a neutral personalisation marker).

    Args:
        recommendations: Schema-enriched rows already ladder-ranked.
        profile_view: Consumer view from Personal Learning Profile Port.
        limit: Maximum rows to return after cadence adjustments.

    Returns:
        Re-sorted, optionally cadence-trimmed recommendation rows.
    """
    if not recommendations:
        return []

    rows = [dict(r) for r in recommendations if isinstance(r, dict)]
    if not rows:
        return []

    if not isinstance(profile_view, dict) or not profile_view.get("attributes"):
        for row in rows:
            row.setdefault("personalisation_applied", False)
            row.setdefault("personalisation_factors", [])
            row.setdefault(
                "personalisation_schema_version", PERSONALISATION_SCHEMA_VERSION
            )
            row.setdefault("personalisation_tie_break", TIE_NEUTRAL)
        return _stable_sort(rows)[: max(1, int(limit))]

    attributes = profile_view.get("attributes") or {}
    if not isinstance(attributes, dict):
        attributes = {}

    for row in rows:
        _personalise_row(row, attributes)

    rows = _apply_cadence(rows, attributes, limit=limit)
    return _stable_sort(rows)[: max(1, int(limit))]


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
        # Declared session duration uses sample_size=1 with confidence 1.0 —
        # allow that preference via explicit exception below.
        if key != ATTR_PREFERRED_SESSION_DURATION:
            return None
        if confidence < 1.0 or sample < 1:
            return None
    return raw


def _personalise_row(row: dict[str, Any], attributes: dict[str, Any]) -> None:
    factors: list[dict[str, Any]] = []
    tie = TIE_NEUTRAL
    category = str(row.get("category") or "")
    ladder = int(row.get("decision_ladder_rank") or 99)
    protected = ladder in _PROTECTED_LADDER or bool(row.get("honest_refusal"))

    # R1 / R2 — recovery strategy preference (tie-break only when not protected).
    recovery = _attr(attributes, ATTR_RECOVERY_EFFECTIVENESS)
    if recovery is not None and not protected:
        value = recovery.get("value") if isinstance(recovery.get("value"), dict) else {}
        rate = _float(value.get("follow_through_rate"))
        if rate is not None:
            if rate >= 0.5 and category in {
                CATEGORY_WEAK_TOPIC,
                CATEGORY_REVIEW,
            }:
                tie -= 8
                factors.append(
                    _factor(
                        ATTR_RECOVERY_EFFECTIVENESS,
                        recovery,
                        effect="prefer_recovery_follow_through",
                        detail=(
                            "Prior recovery follow-through supports keeping "
                            "repair tips visible within this priority band."
                        ),
                    )
                )
            elif rate < 0.3 and category == CATEGORY_WEAK_TOPIC:
                tie += 6
                factors.append(
                    _factor(
                        ATTR_RECOVERY_EFFECTIVENESS,
                        recovery,
                        effect="prefer_lighter_recovery",
                        detail=(
                            "Lower recovery follow-through prefers lighter "
                            "repair pressure within this priority band."
                        ),
                    )
                )

    # R1 — revision adherence preference (tie-break).
    revision = _attr(attributes, ATTR_REVISION_ADHERENCE)
    if revision is not None and not protected:
        value = revision.get("value") if isinstance(revision.get("value"), dict) else {}
        rate = _float(value.get("adherence_rate"))
        if rate is not None and rate >= 0.6 and category in {
            CATEGORY_REVISION,
            CATEGORY_REVIEW,
        }:
            tie -= 10
            factors.append(
                _factor(
                    ATTR_REVISION_ADHERENCE,
                    revision,
                    effect="prefer_revision_adherence",
                    detail=(
                        "Observed revision adherence supports elevating "
                        "revision/review tips within this priority band."
                    ),
                )
            )

    # R1 — consistency trend (habit summary → effort preference, not mastery).
    consistency = _attr(attributes, ATTR_CONSISTENCY_TREND)
    if consistency is not None and not protected:
        value = (
            consistency.get("value")
            if isinstance(consistency.get("value"), dict)
            else {}
        )
        direction = str(value.get("direction") or "").strip().lower()
        if direction == "declining":
            if category == CATEGORY_REST:
                tie -= 7
                factors.append(
                    _factor(
                        ATTR_CONSISTENCY_TREND,
                        consistency,
                        effect="prefer_wellbeing_when_declining",
                        detail=(
                            "Declining consistency habit signal prefers "
                            "wellbeing/rest tips within this priority band."
                        ),
                    )
                )
            elif category == CATEGORY_NEW_TOPIC:
                tie += 5
                factors.append(
                    _factor(
                        ATTR_CONSISTENCY_TREND,
                        consistency,
                        effect="soften_new_learning_when_declining",
                        detail=(
                            "Declining consistency habit signal softens new "
                            "learning pressure within this priority band."
                        ),
                    )
                )

    # Planning completion — proportionality / cadence of heavy tips.
    planning = _attr(attributes, ATTR_PLANNING_COMPLETION_RATE)
    if planning is not None and not protected:
        value = planning.get("value") if isinstance(planning.get("value"), dict) else {}
        rate = _float(value.get("completion_rate"))
        if rate is not None and rate < 0.4 and category == CATEGORY_MOCK_EXAM:
            tie += 8
            factors.append(
                _factor(
                    ATTR_PLANNING_COMPLETION_RATE,
                    planning,
                    effect="defer_heavy_mock_when_completion_low",
                    detail=(
                        "Lower plan-completion behaviour prefers deferring "
                        "mock-exam tips within this priority band."
                    ),
                )
            )

    # R3 — session sizing guidance (annotation only; never invents minutes).
    duration = _attr(attributes, ATTR_PREFERRED_SESSION_DURATION)
    if duration is not None:
        value = duration.get("value") if isinstance(duration.get("value"), dict) else {}
        minutes = value.get("declared_session_minutes")
        try:
            minutes_i = int(minutes) if minutes is not None else 0
        except (TypeError, ValueError):
            minutes_i = 0
        if minutes_i > 0:
            guidance = (
                f"Aim for about {minutes_i} minutes — your declared preferred "
                f"session length."
            )
            row["session_sizing_guidance"] = guidance
            next_action = str(
                row.get("suggested_next_action") or row.get("next_action") or ""
            ).strip()
            if guidance not in next_action:
                updated = f"{next_action} {guidance}".strip()
                row["next_action"] = updated
                row["suggested_next_action"] = updated
            factors.append(
                _factor(
                    ATTR_PREFERRED_SESSION_DURATION,
                    duration,
                    effect="session_sizing_guidance",
                    detail=guidance,
                )
            )

    # Preferred study windows remain unsupported — explicit no-op with trail.
    windows = attributes.get(ATTR_PREFERRED_STUDY_WINDOWS)
    if isinstance(windows, dict) and str(windows.get("status") or "") == "unsupported":
        # Do not invent window-based ordering.
        pass

    # R4 note: responsiveness never promotes accepted categories (Art. V §2).
    # Cadence trimming is applied in _apply_cadence.

    tie = max(TIE_MIN, min(TIE_MAX, tie))
    row["personalisation_tie_break"] = tie
    row["personalisation_applied"] = bool(factors)
    row["personalisation_factors"] = factors
    row["personalisation_schema_version"] = PERSONALISATION_SCHEMA_VERSION
    row["personalisation_profile_id"] = None  # filled by caller if known

    if factors:
        _attach_personalisation_explanation(row, factors)


def _apply_cadence(
    rows: list[dict[str, Any]],
    attributes: dict[str, Any],
    *,
    limit: int,
) -> list[dict[str, Any]]:
    """Reduce tip volume when dismissals dominate (preference summary only)."""
    responsiveness = _attr(attributes, ATTR_RECOMMENDATION_RESPONSIVENESS)
    if responsiveness is None:
        return rows

    value = (
        responsiveness.get("value")
        if isinstance(responsiveness.get("value"), dict)
        else {}
    )
    accept_rate = _float(value.get("accept_rate"))
    sample = int(responsiveness.get("sample_size") or 0)
    if accept_rate is None or sample < 5 or accept_rate >= 0.3:
        return rows

    soft_limit = max(1, min(int(limit), 3))
    factor = _factor(
        ATTR_RECOMMENDATION_RESPONSIVENESS,
        responsiveness,
        effect="cadence_reduce_secondary_tips",
        detail=(
            "Frequent tip dismissals reduce how many secondary tips are shown "
            "(preference history — not a mastery judgement)."
        ),
    )
    omit_strength = _factor(
        ATTR_RECOMMENDATION_RESPONSIVENESS,
        responsiveness,
        effect="cadence_omit_motivation_tip",
        detail=(
            "Frequent tip dismissals reduce secondary motivation tips "
            "(preference history — not a mastery judgement)."
        ),
    )

    kept: list[dict[str, Any]] = []
    omitted_strength = False
    for row in rows:
        category = str(row.get("category") or "")
        ladder = int(row.get("decision_ladder_rank") or 99)
        protected = ladder in _PROTECTED_LADDER or bool(row.get("honest_refusal"))
        if category == CATEGORY_STUDY_STRENGTH and not protected:
            omitted_strength = True
            continue
        if protected:
            kept.append(row)
            continue
        if len(kept) >= soft_limit:
            continue
        kept.append(row)

    if not kept:
        kept = rows[:1]

    for row in kept:
        _record_cadence_factor(row, factor)
        if omitted_strength:
            _record_cadence_factor(row, omit_strength)
    return kept


def _record_cadence_factor(row: dict[str, Any], factor: dict[str, Any]) -> None:
    factors = list(row.get("personalisation_factors") or [])
    effect = factor.get("effect")
    if any(f.get("effect") == effect for f in factors if isinstance(f, dict)):
        return
    factors.append(factor)
    row["personalisation_factors"] = factors
    row["personalisation_applied"] = True
    _attach_personalisation_explanation(row, [factor])


def _attach_personalisation_explanation(
    row: dict[str, Any],
    factors: list[dict[str, Any]],
) -> None:
    """Surface personalisation influence in the mandatory explanation schema."""
    if not factors:
        return

    evidence = list(row.get("supporting_evidence") or [])
    for factor in factors:
        line = str(factor.get("student_evidence") or "").strip()
        if line and line not in evidence:
            evidence.append(line)
    row["supporting_evidence"] = evidence[:6]
    observed = list(row.get("observed_facts") or [])
    for factor in factors:
        line = str(factor.get("student_evidence") or "").strip()
        if line and line not in observed:
            observed.append(line)
    row["observed_facts"] = observed[:6]

    why = str(row.get("why_recommended") or row.get("reason") or "").strip()
    note = " Personalised using your observed study habits where evidence allows."
    if note.strip() not in why:
        row["why_recommended"] = (why + note).strip()
        reason = str(row.get("reason") or "").strip()
        if note.strip() not in reason:
            row["reason"] = (reason + note).strip()


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
    student_evidence = (
        f"Personalisation evidence ({attribute_key}): {detail}"
    )
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


def _float(value: Any) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _stable_sort(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(
        rows,
        key=lambda r: (
            int(r.get("decision_ladder_rank") or 99),
            PRIORITY_ORDER.get(str(r.get("priority") or ""), 99),
            int(r.get("personalisation_tie_break") or TIE_NEUTRAL),
            str(r.get("title") or ""),
        ),
    )


def stamp_profile_id(
    rows: list[dict[str, Any]],
    profile_view: dict[str, Any] | None,
) -> list[dict[str, Any]]:
    """Attach profile_id provenance when personalisation ran."""
    if not isinstance(profile_view, dict):
        return rows
    profile_id = str(profile_view.get("profile_id") or "").strip() or None
    for row in rows:
        if row.get("personalisation_applied"):
            row["personalisation_profile_id"] = profile_id
    return rows
