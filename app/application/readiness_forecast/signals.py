"""Extract forecast signals from existing evidence only (KWP-012).

Consumes Evidence Packages, intelligence snapshots, StrategyEvidenceInput,
and Educational Memory patterns. Never invents missing facts.
"""

from __future__ import annotations

from datetime import date, datetime
from typing import Any

from app.application.educational_memory.patterns import detect_longitudinal_patterns
from app.application.educational_memory.snapshot import snapshot_from_package
from app.application.learning_strategy.dto import StrategyEvidenceInput
from app.application.readiness_forecast.dto import ForecastSignals


def extract_forecast_signals(
    packages: list[dict[str, Any]] | tuple[dict[str, Any], ...],
    *,
    student_id: str = "",
    days_to_exam: int | None = None,
    exam_date: date | None = None,
    exam_date_label: str = "",
    current_readiness_ratio: float | None = None,
    as_of: date | None = None,
) -> ForecastSignals:
    """Build ForecastSignals from chronological sitting evidence."""
    ordered = _chronological(packages, student_id=student_id)
    today = as_of or date.today()

    resolved_days = days_to_exam
    label = (exam_date_label or "").strip()
    if exam_date is not None:
        resolved_days = (exam_date - today).days
        if not label:
            label = exam_date.isoformat()

    if not ordered:
        return ForecastSignals(
            days_to_exam=resolved_days,
            exam_date_label=label,
            current_readiness_ratio=current_readiness_ratio,
            as_of=today.isoformat(),
        )

    practices = [StrategyEvidenceInput.from_opaque(p) for p in ordered]
    n = len(practices)
    strong_flags = [_is_strong(p) for p in practices]
    strong_ratio = sum(1 for s in strong_flags if s) / n

    half = max(1, n // 2)
    early = strong_flags[:half]
    recent = strong_flags[half:] if n > 1 else strong_flags
    early_ratio = sum(1 for s in early if s) / max(1, len(early))
    recent_ratio = sum(1 for s in recent if s) / max(1, len(recent))

    advances = sum(1 for p in practices if p.progress_advanced)
    reflections = sum(1 for p in practices if p.has_reflection)
    retention = sum(1 for p in practices if p.retention_risk)

    recovery_hits = 0
    demand_hits = 0
    help_hits = 0
    help_total = 0
    mismatch_hits = 0
    snap_count = 0

    for package in ordered:
        snap = snapshot_from_package(package)
        if snap is None:
            continue
        snap_count += 1
        action = str(snap.strategy.get("action") or "")
        calibration = str(snap.strategy.get("calibration") or "")
        diag = str(snap.diagnostics.get("category") or "")
        load = str(snap.difficulty.get("recommendation") or "")
        observed = str(snap.difficulty.get("observed_difficulty") or "")
        verdict = str(snap.effectiveness.get("verdict") or "")

        if action == "recover_prior_knowledge" or diag == "retention_decay":
            recovery_hits += 1
        if observed in {"demanding", "very_demanding"} or load in {
            "reduce_session_length",
            "take_consolidation_session",
            "split_topic",
        }:
            demand_hits += 1
        if calibration in {"over_confident", "under_confident"} or diag == (
            "confidence_mismatch"
        ):
            mismatch_hits += 1
        if verdict:
            help_total += 1
            if verdict in {"effective", "partially_effective"}:
                help_hits += 1

    patterns = detect_longitudinal_patterns(ordered, student_id=student_id)
    pattern_kinds = {p.kind.value for p in patterns}
    memory_improving = bool(
        pattern_kinds
        & {
            "increasing_independence",
            "improving_consistency",
            "long_term_retention_improvements",
        }
    )
    memory_recovery = "repeated_successful_recoveries" in pattern_kinds

    consistency = _consistency_score(practices, ordered)
    cadence = _sittings_per_week(ordered, today=today)

    # Prefer explicit readiness; otherwise derive a calm proxy from evidence.
    readiness = current_readiness_ratio
    if readiness is None:
        readiness = _derive_readiness_proxy(
            strong_ratio=recent_ratio if n >= 2 else strong_ratio,
            advance_rate=advances / n,
            consistency=consistency,
            recovery_pressure=recovery_hits / max(1, snap_count or n),
        )

    topics = {
        str(p.get("topic_title") or "").strip().lower()
        for p in ordered
        if str(p.get("topic_title") or "").strip()
    }

    return ForecastSignals(
        sitting_count=n,
        topic_count=len(topics),
        strong_finish_ratio=strong_ratio,
        recent_strong_ratio=recent_ratio,
        early_strong_ratio=early_ratio,
        progress_advance_rate=advances / n,
        consistency_score=consistency,
        sittings_per_week=cadence,
        recovery_pressure=recovery_hits / max(1, snap_count or n),
        retention_risk_rate=retention / n,
        difficulty_demand_rate=demand_hits / max(1, snap_count or n),
        intervention_help_rate=(
            help_hits / help_total if help_total else 0.0
        ),
        confidence_mismatch_rate=mismatch_hits / max(1, snap_count or n),
        reflection_rate=reflections / n,
        memory_improving=memory_improving,
        memory_recovery_success=memory_recovery,
        current_readiness_ratio=readiness,
        days_to_exam=resolved_days,
        exam_date_label=label,
        as_of=today.isoformat(),
    )


def _chronological(
    packages: list[dict[str, Any]] | tuple[dict[str, Any], ...],
    *,
    student_id: str = "",
) -> list[dict[str, Any]]:
    sid = (student_id or "").strip()
    rows = [
        p
        for p in packages
        if isinstance(p, dict)
        and (not sid or str(p.get("student_id") or "").strip() == sid)
    ]
    rows.sort(key=lambda p: str(p.get("created_at") or ""))
    return rows


def _is_strong(practice: StrategyEvidenceInput) -> bool:
    scored = practice.practice_correct + practice.practice_incorrect
    if scored <= 0:
        return bool(practice.progress_advanced and practice.finish_verdict == "yes")
    return practice.practice_correct >= practice.practice_incorrect and scored >= 2


def _consistency_score(
    practices: list[StrategyEvidenceInput],
    packages: list[dict[str, Any]],
) -> float:
    """0–1 consistency from cadence / streak / finish honesty."""
    if not practices:
        return 0.0
    latest = practices[-1]
    streak = latest.streak_days
    recent = latest.recent_session_count
    score = 0.0
    if streak is not None:
        score += min(1.0, streak / 5.0) * 0.45
    if recent is not None:
        score += min(1.0, recent / 5.0) * 0.35
    honest = sum(
        1
        for p in practices
        if p.finish_verdict in {"yes", "partially", "no"} and not p.abandoned
    )
    score += (honest / len(practices)) * 0.20
    # Sparse calendar history demotes consistency even if finishes look fine.
    if len(packages) >= 2:
        span_days = _span_days(packages)
        if span_days is not None and span_days >= 14:
            rate = len(packages) / max(1.0, span_days / 7.0)
            if rate < 1.0:
                score *= 0.7
    return max(0.0, min(1.0, score))


def _sittings_per_week(
    packages: list[dict[str, Any]],
    *,
    today: date,
) -> float:
    if not packages:
        return 0.0
    span = _span_days(packages)
    if span is None or span < 1:
        # Single sitting / same-day — treat as one week sample.
        return float(len(packages))
    weeks = max(1.0, span / 7.0)
    return len(packages) / weeks


def _span_days(packages: list[dict[str, Any]]) -> int | None:
    stamps: list[date] = []
    for package in packages:
        parsed = _parse_date(package.get("created_at"))
        if parsed is not None:
            stamps.append(parsed)
    if len(stamps) < 2:
        return None
    return max(0, (max(stamps) - min(stamps)).days)


def _parse_date(raw: Any) -> date | None:
    text = str(raw or "").strip()
    if not text:
        return None
    try:
        if text.endswith("Z"):
            text = text[:-1] + "+00:00"
        return datetime.fromisoformat(text).date()
    except ValueError:
        try:
            return date.fromisoformat(text[:10])
        except ValueError:
            return None


def _derive_readiness_proxy(
    *,
    strong_ratio: float,
    advance_rate: float,
    consistency: float,
    recovery_pressure: float,
) -> float:
    """Deterministic readiness proxy in [0, 1] from sitting evidence."""
    base = (
        0.45 * strong_ratio
        + 0.25 * advance_rate
        + 0.20 * consistency
        + 0.10 * max(0.0, 1.0 - recovery_pressure)
    )
    return max(0.05, min(0.95, base))
