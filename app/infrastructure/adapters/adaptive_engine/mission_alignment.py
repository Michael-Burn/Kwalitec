"""Mission-alignment policy for Adaptive Engine delivery and soak (MS-001).

Delivery / observation invariant: when a today SQL mission exists, Adaptive's
student-facing primary recommendation identity MUST equal that mission.
Adaptive's independent pick is demoted to alternatives / advisory.

PlanningService / mission creation / Start binding are never called here —
read-only MissionService lookup (or AdaptiveInputBundle.mission.today) only.
"""

from __future__ import annotations

from dataclasses import replace
from datetime import date, datetime
from types import SimpleNamespace
from typing import Any

from app.infrastructure.adapters.adaptive_engine.contracts import (
    AdaptiveInputBundle,
    AdaptiveOutputBundle,
    RecommendationPlaceholder,
    TopicRef,
)


def resolve_today_as_of() -> str:
    """ISO calendar date for paths that claim to represent 'today'.

    Matches Stage A / Bridge ``date.today()`` resolution (not assembler
    auto-clock — callers pass this explicitly into ``assemble``).
    """
    return date.today().isoformat()


def parse_as_of_to_date(as_of: str | None) -> date:
    """Parse ISO as_of into a date; default to today when absent/invalid."""
    if as_of is None or not str(as_of).strip():
        return date.today()
    text = str(as_of).strip()
    try:
        if "T" in text:
            return datetime.fromisoformat(text.replace("Z", "+00:00")).date()
        return date.fromisoformat(text[:10])
    except ValueError:
        return date.today()


def _norm(value: Any) -> str:
    return str(value or "").strip().lower()


def mission_identity_from_bundle(
    inputs: AdaptiveInputBundle | None,
) -> SimpleNamespace | None:
    """Extract today's mission identity from an assembled AdaptiveInputBundle."""
    if inputs is None:
        return None
    today = (dict(inputs.mission or {})).get("today")
    if not isinstance(today, dict):
        return None
    title = str(today.get("title") or "").strip()
    if not title:
        return None
    return SimpleNamespace(
        id=str(today.get("mission_id") or "").strip(),
        title=title,
        topic_code=str(today.get("topic_code") or "").strip(),
    )


def read_today_mission(
    student_id: str,
    *,
    as_of: str | None = None,
    mission_service: Any | None = None,
) -> Any | None:
    """Read-only today mission from Stage A. Never creates or self-heals.

    Prefer an injected ``mission_service`` (tests). Otherwise query Mission via
    the Adaptive assembler's read-only active-plan helper — never
    ``MissionService.get_today_mission`` / ``StudyPlanService.get_user_active_plan``
    (those may bind curriculum and mutate TopicProgress).
    """
    sid = (student_id or "").strip()
    if not sid:
        return None
    try:
        user_id = int(sid)
    except (TypeError, ValueError):
        return None
    mission_date = parse_as_of_to_date(as_of)
    if mission_service is not None:
        try:
            mission = mission_service.get_today_mission(
                user_id, mission_date=mission_date
            )
        except Exception:  # noqa: BLE001 — alignment fail-open
            return None
        if mission is None:
            return None
        title = str(getattr(mission, "title", "") or "").strip()
        return mission if title else None

    try:
        from app.infrastructure.adapters.adaptive_engine.collectors import (
            read_active_study_plan,
        )
        from app.models.mission import Mission

        plan = read_active_study_plan(user_id)
        query = Mission.query.filter_by(user_id=user_id, mission_date=mission_date)
        if plan is not None:
            query = query.filter_by(study_plan_id=plan.id)
        mission = query.order_by(Mission.id.desc()).first()
    except Exception:  # noqa: BLE001 — alignment fail-open to no mission
        return None
    if mission is None:
        return None
    title = str(getattr(mission, "title", "") or "").strip()
    if not title:
        return None
    return mission


def resolve_mission_for_alignment(
    student_id: str,
    *,
    as_of: str | None = None,
    inputs: AdaptiveInputBundle | None = None,
    mission_service: Any | None = None,
) -> Any | None:
    """Prefer assembled mission.today; fall back to Stage A read-only lookup."""
    from_bundle = mission_identity_from_bundle(inputs)
    if from_bundle is not None:
        return from_bundle
    return read_today_mission(
        student_id, as_of=as_of, mission_service=mission_service
    )


def mission_baseline_dict(mission: Any) -> dict[str, Any] | None:
    """Soak / compare baseline identity from a today mission."""
    if mission is None:
        return None
    title = str(getattr(mission, "title", "") or "").strip()
    if not title:
        return None
    topic_code = str(getattr(mission, "topic_code", "") or "").strip()
    mission_id = str(getattr(mission, "id", "") or "").strip()
    return {
        "title": title,
        "recommendation_label": title,
        "topic_title": title,
        "topic_code": topic_code,
        "category": "Mission",
        "mission_id": mission_id,
        "mission_aligned": True,
        "baseline_kind": "mission",
    }


def _mission_title(mission: Any) -> str:
    return str(getattr(mission, "title", "") or "").strip()


def _mission_id(mission: Any) -> str:
    return str(getattr(mission, "id", "") or "").strip()


def _mission_topic_code(mission: Any) -> str:
    return str(getattr(mission, "topic_code", "") or "").strip()


def apply_mission_alignment_to_projection(
    projection: dict[str, Any] | None,
    mission: Any | None,
) -> dict[str, Any] | None:
    """Hard-override Experience recommendation primary to today's mission.

    Mirrors Recommendation Bridge MS-001: mission title becomes primary;
    Adaptive's independent primary is preserved as an alternative when it
    differs. Learning and Revision are treated identically when a mission
    exists.
    """
    if projection is None:
        return None
    if mission is None:
        return projection
    title = _mission_title(mission)
    if not title:
        return projection

    out = dict(projection)
    old_label = str(
        out.get("recommendation_label")
        or out.get("title")
        or out.get("topic_title")
        or ""
    ).strip()
    old_code = str(out.get("topic_code") or "").strip()
    alts = [dict(a) for a in (out.get("alternatives") or []) if isinstance(a, dict)]

    if old_label and _norm(old_label) != _norm(title):
        already = any(
            _norm(a.get("title") or a.get("recommendation_label")) == _norm(old_label)
            for a in alts
        )
        if not already:
            alts.insert(
                0,
                {
                    "topic_code": old_code,
                    "title": old_label,
                    "recommendation_label": old_label,
                    "reason": "adaptive_independent_pick",
                    "role": "alternative",
                },
            )

    mission_code = _mission_topic_code(mission)
    out["recommendation_label"] = title
    out["title"] = title
    out["topic_title"] = title
    out["topic_code"] = mission_code
    out["mission_id"] = _mission_id(mission) or out.get("mission_id")
    out["mission_aligned"] = True
    out["alternatives"] = alts
    if not str(out.get("summary") or "").strip():
        out["summary"] = f"Today's mission: {title}"
    explanation = out.get("explanation")
    if isinstance(explanation, dict):
        explanation = dict(explanation)
        explanation["mission_note"] = (
            explanation.get("mission_note")
            or "Primary follows today's mission (delivery alignment)."
        )
        out["explanation"] = explanation
    return out


def apply_mission_alignment_to_output(
    output: AdaptiveOutputBundle | None,
    mission: Any | None,
) -> AdaptiveOutputBundle | None:
    """Return a delivery-aligned AdaptiveOutputBundle copy for soak compare.

    Does not mutate the original Engine output. When no mission exists,
    returns the original reference unchanged.
    """
    if output is None:
        return None
    if mission is None:
        return output
    title = _mission_title(mission)
    if not title:
        return output

    rec = output.recommendation
    old_label = str(rec.label or rec.title or rec.topic_code or "").strip()
    old_code = str(rec.topic_code or "").strip()
    already_aligned = _norm(old_label) == _norm(title)

    topic_refs = list(output.explanation.topic_refs or ())
    if old_label and not already_aligned:
        topic_refs = [
            TopicRef(
                topic_code=old_code,
                title=old_label,
                role="alternative",
            ),
            *[
                ref
                for ref in topic_refs
                if (ref.role or "").strip().lower() not in {"primary", "selected", ""}
                or (
                    _norm(ref.title) != _norm(old_label)
                    and _norm(ref.topic_code) != _norm(old_code)
                )
            ],
        ]

    mission_code = _mission_topic_code(mission) or None
    new_rec = RecommendationPlaceholder(
        topic_code=mission_code,
        title=title,
        decision_kind=rec.decision_kind or "COMPOSITE",
        label=title,
    )
    explanation = output.explanation
    new_explanation = replace(
        explanation,
        recommendation_rationale=explanation.recommendation_rationale
        or f"Delivery alignment: primary follows today's mission ({title}).",
        why_summary=explanation.why_summary
        or f"Continue today's mission: {title}.",
        topic_refs=tuple(topic_refs),
        alternatives_rationale=explanation.alternatives_rationale
        or (
            ""
            if already_aligned
            else (
                "Adaptive independent pick retained as alternative "
                "under mission alignment."
            )
        ),
        mission_aligned=True,
        mission_note=explanation.mission_note
        or "Primary follows today's mission (delivery alignment).",
    )
    return replace(
        output,
        recommendation=new_rec,
        explanation=new_explanation,
    )


__all__ = [
    "apply_mission_alignment_to_output",
    "apply_mission_alignment_to_projection",
    "mission_baseline_dict",
    "mission_identity_from_bundle",
    "parse_as_of_to_date",
    "read_today_mission",
    "resolve_mission_for_alignment",
    "resolve_today_as_of",
]
