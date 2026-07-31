"""Capture and restore educational intelligence snapshots (KWP-011).

Evaluates Strategy / Diagnostics / Difficulty / Effectiveness once at
sitting close and freezes student-facing Sitting Report fields.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from app.application.educational_memory.dto import IntelligenceSnapshot
from app.application.intervention_effectiveness import (
    get_intervention_effectiveness_engine,
)
from app.application.intervention_effectiveness.dto import (
    PriorIntervention,
    prior_from_enrichment,
    prior_from_sitting,
)
from app.application.learning_diagnostics import get_learning_diagnostics_engine
from app.application.learning_difficulty import get_learning_difficulty_engine
from app.application.learning_strategy import get_learning_strategy_engine
from app.application.learning_strategy.dto import StrategyEvidenceInput


def capture_intelligence_snapshot(
    package: dict[str, Any],
    *,
    prior: PriorIntervention | None = None,
    metadata: dict[str, Any] | None = None,
    twin_signals: dict[str, Any] | None = None,
    cadence: dict[str, Any] | None = None,
    captured_at: str | None = None,
) -> IntelligenceSnapshot:
    """Evaluate EI engines once and freeze outputs onto a snapshot.

    Never invents evidence. Thin packages still receive a lawful snapshot
    with whatever engines return for thin sittings.
    """
    opaque = dict(package or {})
    meta = dict(metadata or {})
    twin = dict(twin_signals or {})
    cad = dict(cadence or {})

    resolved_prior = prior
    if resolved_prior is None:
        resolved_prior = prior_from_enrichment(
            opaque=opaque, metadata=meta, cadence=cad, twin_signals=twin
        )
    if resolved_prior is not None and resolved_prior.has_recommendation:
        opaque = {**opaque, "prior_intervention": _prior_to_opaque(resolved_prior)}
        meta = {**meta, "prior_intervention": _prior_to_opaque(resolved_prior)}

    strategy = get_learning_strategy_engine().evaluate_opaque(
        opaque, metadata=meta, twin_signals=twin, cadence=cad
    )
    diagnostics = get_learning_diagnostics_engine().evaluate_opaque(
        opaque, metadata=meta, twin_signals=twin, cadence=cad
    )
    difficulty = get_learning_difficulty_engine().evaluate_opaque(
        opaque, metadata=meta, twin_signals=twin, cadence=cad
    )
    effectiveness = get_intervention_effectiveness_engine().evaluate_opaque(
        opaque, metadata=meta, twin_signals=twin, cadence=cad
    )

    # Prefer cause-level WHY when diagnostics have a concrete signal.
    from app.application.learning_diagnostics.dto import DiagnosticCategory

    composed_why = strategy.explanation
    if diagnostics.primary.category is not DiagnosticCategory.INSUFFICIENT_SIGNAL:
        cause = (diagnostics.explanation or "").strip()
        if cause:
            composed_why = cause

    practice = StrategyEvidenceInput.from_opaque(
        opaque, metadata=meta, twin_signals=twin, cadence=cad
    )
    outgoing = prior_from_sitting(
        strategy_action=strategy.action.value,
        load_recommendation=difficulty.recommendation.value,
        topic_title=practice.topic_title or str(opaque.get("topic_title") or ""),
        practice_correct=practice.practice_correct,
        practice_incorrect=practice.practice_incorrect,
        practice_attempted=practice.practice_attempted,
        session_duration_minutes=_optional_int(
            opaque.get("session_duration_minutes")
            or opaque.get("actual_duration_minutes")
        ),
        finish_verdict=practice.finish_verdict,
        progress_advanced=practice.progress_advanced,
        source="educational_memory",
    )

    student_report = {
        "strategy_title": strategy.recommendation_title,
        "strategy_body": strategy.recommendation_body,
        "strategy_explanation": composed_why or strategy.explanation,
        "strategy_spacing_guidance": strategy.spacing_guidance,
        "strategy_momentum_guidance": strategy.momentum_guidance,
        "strategy_confidence_guidance": strategy.confidence_guidance,
        "diagnostic_guidance": diagnostics.guidance,
        "diagnostic_explanation": diagnostics.explanation,
        "difficulty_title": difficulty.recommendation_title,
        "difficulty_guidance": difficulty.guidance,
        "difficulty_explanation": difficulty.explanation,
        "effectiveness_feedback": (
            effectiveness.feedback if effectiveness.has_student_feedback else ""
        ),
        "effectiveness_explanation": (
            effectiveness.explanation
            if effectiveness.has_student_feedback
            else ""
        ),
    }

    stamp = captured_at or datetime.now(UTC).isoformat()
    return IntelligenceSnapshot(
        captured_at=stamp,
        student_id=str(opaque.get("student_id") or ""),
        session_id=str(opaque.get("session_id") or ""),
        package_id=str(opaque.get("package_id") or ""),
        topic_title=str(
            opaque.get("topic_title") or practice.topic_title or ""
        ).strip(),
        topic_id=str(opaque.get("topic_id") or "").strip(),
        strategy=strategy.to_opaque(),
        diagnostics=diagnostics.to_opaque(),
        difficulty=difficulty.to_opaque(),
        effectiveness=effectiveness.to_opaque(),
        prior_intervention=_prior_to_opaque(resolved_prior)
        if resolved_prior and resolved_prior.has_recommendation
        else {},
        outgoing_intervention=_prior_to_opaque(outgoing),
        student_sitting_report=student_report,
    )


def attach_snapshot_to_package(
    package: dict[str, Any], snapshot: IntelligenceSnapshot
) -> dict[str, Any]:
    """Return a package copy with ``intelligence_snapshot`` attached."""
    updated = dict(package)
    updated["intelligence_snapshot"] = snapshot.to_opaque()
    # Convenience: prior chain for Effectiveness on subsequent sittings.
    if snapshot.outgoing_intervention:
        updated["outgoing_intervention"] = dict(snapshot.outgoing_intervention)
    return updated


def snapshot_from_package(
    package: dict[str, Any] | None,
) -> IntelligenceSnapshot | None:
    """Load a frozen snapshot from a persisted Evidence Package."""
    if not isinstance(package, dict):
        return None
    return IntelligenceSnapshot.from_opaque(package.get("intelligence_snapshot"))


def resolve_prior_from_packages(
    packages: list[dict[str, Any]] | tuple[dict[str, Any], ...],
    *,
    student_id: str,
    topic_title: str = "",
    topic_id: str = "",
    exclude_session_id: str = "",
) -> PriorIntervention | None:
    """Find the most recent same-topic outgoing intervention for continuity.

    Packages should be chronological (oldest first) or unordered — we pick
    the newest matching prior by ``created_at`` / snapshot ``captured_at``.
    """
    sid = (student_id or "").strip()
    topic = (topic_title or "").strip().lower()
    tid = (topic_id or "").strip()
    exclude = (exclude_session_id or "").strip()
    if not sid:
        return None

    candidates: list[tuple[str, dict[str, Any]]] = []
    for raw in packages:
        if not isinstance(raw, dict):
            continue
        if str(raw.get("student_id") or "").strip() != sid:
            continue
        if exclude and str(raw.get("session_id") or "").strip() == exclude:
            continue
        raw_topic = str(raw.get("topic_title") or "").strip().lower()
        raw_tid = str(raw.get("topic_id") or "").strip()
        topic_match = bool(tid and raw_tid and tid == raw_tid) or (
            bool(topic) and bool(raw_topic) and topic == raw_topic
        )
        if not topic_match:
            continue
        snap = snapshot_from_package(raw)
        outgoing = {}
        if snap is not None and snap.outgoing_intervention:
            outgoing = dict(snap.outgoing_intervention)
        elif isinstance(raw.get("outgoing_intervention"), dict):
            outgoing = dict(raw["outgoing_intervention"])
        if not outgoing:
            # Fall back: reconstruct from strategy/difficulty snapshot fields.
            if snap is not None and snap.strategy:
                outgoing = {
                    "strategy_action": str(snap.strategy.get("action") or ""),
                    "load_recommendation": str(
                        (snap.difficulty or {}).get("recommendation") or ""
                    ),
                    "topic_title": snap.topic_title,
                    "source": "snapshot_fallback",
                }
        if not outgoing:
            continue
        stamp = str(
            (snap.captured_at if snap else "")
            or raw.get("created_at")
            or ""
        )
        candidates.append((stamp, outgoing))

    if not candidates:
        return None
    candidates.sort(key=lambda item: item[0])
    latest = candidates[-1][1]
    return prior_from_enrichment(opaque={"prior_intervention": latest})


def student_report_metadata_pairs(
    snapshot: IntelligenceSnapshot,
) -> list[tuple[str, str]]:
    """Flatten frozen student Sitting Report fields into metadata pairs."""
    pairs: list[tuple[str, str]] = [("intelligence_captured", "true")]
    report = snapshot.student_sitting_report
    for key in (
        "strategy_title",
        "strategy_body",
        "strategy_explanation",
        "strategy_spacing_guidance",
        "strategy_momentum_guidance",
        "strategy_confidence_guidance",
        "diagnostic_guidance",
        "diagnostic_explanation",
        "difficulty_title",
        "difficulty_guidance",
        "difficulty_explanation",
        "effectiveness_feedback",
        "effectiveness_explanation",
    ):
        value = str(report.get(key) or "").strip()
        if value:
            pairs.append((key, value))
    if snapshot.captured_at:
        pairs.append(("intelligence_captured_at", snapshot.captured_at))
    return pairs


def _prior_to_opaque(prior: PriorIntervention | None) -> dict[str, Any]:
    if prior is None:
        return {}
    return {
        "kind": prior.kind.value,
        "strategy_action": prior.strategy_action,
        "load_recommendation": prior.load_recommendation,
        "topic_title": prior.topic_title,
        "baseline_correct": prior.baseline_correct,
        "baseline_incorrect": prior.baseline_incorrect,
        "baseline_attempted": prior.baseline_attempted,
        "baseline_duration_minutes": prior.baseline_duration_minutes,
        "baseline_finish_verdict": prior.baseline_finish_verdict,
        "baseline_progress_advanced": prior.baseline_progress_advanced,
        "source": prior.source,
    }


def _optional_int(value: Any) -> int | None:
    if value is None or value == "":
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None
