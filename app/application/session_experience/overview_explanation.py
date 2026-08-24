"""Attach Adaptive Decision MES to Session Overview (pass-through only).

Reuses ExplanationService.from_opaque — the same path Home and Revision use.
Never invents ranking or educational meaning.
"""

from __future__ import annotations

from dataclasses import asdict
from typing import Any

from app.application.student_experience._snapshots import explanation_snapshot
from app.application.student_experience.dto.explanation_snapshot import (
    ExplanationSnapshot,
)
from app.application.student_experience.explanation_service import (
    ExplanationService,
)


def recommendation_explanation_opaque(
    recommendation: dict[str, Any] | None,
) -> dict[str, Any] | None:
    """Serialise Adaptive recommendation → ExplanationSnapshot field dict."""
    if not recommendation:
        return None
    try:
        domain = ExplanationService().from_opaque(dict(recommendation))
        snap = explanation_snapshot(domain)
        if snap is None or not _has_mes_content(snap):
            return None
        payload = asdict(snap)
        payload["evidence_points"] = list(snap.evidence_points or ())
        return payload
    except Exception:  # noqa: BLE001 — overview seed must stay resilient
        return None


def explanation_snapshot_from_overview_opaque(
    opaque: dict[str, Any] | None,
) -> ExplanationSnapshot | None:
    """Hydrate ExplanationSnapshot from overview opaque (resume / re-open)."""
    if not opaque:
        return None
    raw = opaque.get("recommendation_explanation")
    if not isinstance(raw, dict) or not raw:
        return None
    evidence = raw.get("evidence_points") or ()
    if isinstance(evidence, str):
        points = (evidence,) if evidence.strip() else ()
    else:
        points = tuple(str(p) for p in evidence if str(p).strip())
    snap = ExplanationSnapshot(
        summary=str(raw.get("summary") or ""),
        why_recommended=str(raw.get("why_recommended") or ""),
        evidence_points=points,
        expected_benefit=str(raw.get("expected_benefit") or ""),
        confidence_label=str(raw.get("confidence_label") or ""),
        suggested_next_action=str(raw.get("suggested_next_action") or ""),
        review_point=str(raw.get("review_point") or ""),
        confidence_basis=str(raw.get("confidence_basis") or ""),
        is_complete=bool(raw.get("is_complete")),
        plan_coherence=str(raw.get("plan_coherence") or ""),
        plan_coherence_label=str(raw.get("plan_coherence_label") or ""),
        honest_refusal=bool(raw.get("honest_refusal")),
        timeliness_line=str(raw.get("timeliness_line") or ""),
        completion_loop_line=str(raw.get("completion_loop_line") or ""),
    )
    if not _has_mes_content(snap):
        return None
    return snap


def _has_mes_content(snap: ExplanationSnapshot) -> bool:
    return bool(
        snap.summary
        or snap.why_recommended
        or snap.evidence_points
        or snap.expected_benefit
        or snap.suggested_next_action
        or snap.timeliness_line
    )
