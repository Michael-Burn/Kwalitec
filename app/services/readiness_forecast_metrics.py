"""Readiness forecast metrics for Founder observability (KWP-012).

Aggregates trajectory labels, confidence, recovery projections, and a
simple retrospective accuracy check from Evidence Packages.
Does not mutate Evidence, Progress, Strategy, Diagnostics, Difficulty,
Effectiveness, Memory, Twin, or Session runtime.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from typing import Any

from app.application.readiness_forecast.dto import (
    FORECAST_TITLES,
    ForecastConfidence,
    ForecastLabel,
)
from app.application.readiness_forecast.engine import ReadinessForecastEngine
from app.application.readiness_forecast.projection import readiness_stage_for_ratio
from app.application.readiness_forecast.signals import extract_forecast_signals


@dataclass(frozen=True)
class ReadinessForecastMetricsSnapshot:
    """Founder-facing readiness forecast / trajectory summary."""

    learners_forecasted: int = 0
    sittings_scanned: int = 0
    label_counts: dict[str, int] = field(default_factory=dict)
    confidence_counts: dict[str, int] = field(default_factory=dict)
    trend_counts: dict[str, int] = field(default_factory=dict)
    recovery_projection_count: int = 0
    on_track_rate: float = 0.0
    below_pace_rate: float = 0.0
    average_projected_readiness: float = 0.0
    forecast_accuracy: float = 0.0
    accuracy_pairs: int = 0
    established_confidence_rate: float = 0.0
    readiness_progression_labels: tuple[str, ...] = ()

    def to_opaque(self) -> dict[str, Any]:
        return {
            "learners_forecasted": self.learners_forecasted,
            "sittings_scanned": self.sittings_scanned,
            "label_counts": dict(self.label_counts),
            "confidence_counts": dict(self.confidence_counts),
            "trend_counts": dict(self.trend_counts),
            "recovery_projection_count": self.recovery_projection_count,
            "on_track_rate": round(self.on_track_rate, 4),
            "below_pace_rate": round(self.below_pace_rate, 4),
            "average_projected_readiness": round(
                self.average_projected_readiness, 4
            ),
            "forecast_accuracy": round(self.forecast_accuracy, 4),
            "accuracy_pairs": self.accuracy_pairs,
            "established_confidence_rate": round(
                self.established_confidence_rate, 4
            ),
            "readiness_progression_labels": list(
                self.readiness_progression_labels
            ),
            "label_titles": {
                k: FORECAST_TITLES[ForecastLabel(k)]
                for k in self.label_counts
                if k in {v.value for v in ForecastLabel}
            },
        }


class ReadinessForecastMetrics:
    """Compute forecast analytics from persisted sitting packages."""

    @staticmethod
    def from_packages(
        packages: list[dict[str, Any]] | tuple[dict[str, Any], ...],
        *,
        engine: ReadinessForecastEngine | None = None,
    ) -> ReadinessForecastMetricsSnapshot:
        rows = [p for p in packages if isinstance(p, dict)]
        if not rows:
            return ReadinessForecastMetricsSnapshot()

        engine = engine or ReadinessForecastEngine()
        by_student: dict[str, list[dict[str, Any]]] = {}
        for package in rows:
            sid = str(package.get("student_id") or "").strip() or "_unknown"
            by_student.setdefault(sid, []).append(package)

        label_counts: Counter[str] = Counter()
        confidence_counts: Counter[str] = Counter()
        trend_counts: Counter[str] = Counter()
        recovery_count = 0
        projected_values: list[float] = []
        progression: list[str] = []
        accuracy_hits = 0
        accuracy_pairs = 0
        established = 0
        forecasted = 0

        for sid, student_rows in by_student.items():
            student_rows.sort(key=lambda p: str(p.get("created_at") or ""))
            if len(student_rows) < 2:
                continue
            forecasted += 1
            key = "" if sid == "_unknown" else sid
            forecast = engine.forecast(student_rows, student_id=key)
            label_counts[forecast.label.value] += 1
            confidence_counts[forecast.trajectory.confidence.value] += 1
            trend_counts[forecast.trajectory.current_trend.value] += 1
            if forecast.label == ForecastLabel.RECOVERY_REQUIRED:
                recovery_count += 1
            if forecast.trajectory.confidence == ForecastConfidence.ESTABLISHED:
                established += 1
            if forecast.trajectory.projected_readiness_ratio is not None:
                projected_values.append(
                    forecast.trajectory.projected_readiness_ratio
                )
            current = forecast.trajectory.current_readiness_stage
            projected = forecast.trajectory.projected_readiness_stage
            if current and projected and current != projected:
                progression.append(f"{current} → {projected}")

            # Retrospective accuracy: forecast from first half vs later proxy.
            mid = max(2, len(student_rows) // 2)
            if len(student_rows) >= 4:
                early = engine.forecast(student_rows[:mid], student_id=key)
                later_signals = extract_forecast_signals(
                    student_rows, student_id=key
                )
                accuracy_pairs += 1
                if _direction_matches(
                    early.trajectory.projected_readiness_ratio,
                    later_signals.current_readiness_ratio,
                    early.trajectory.current_readiness_stage,
                ):
                    accuracy_hits += 1

        on_track = label_counts.get(ForecastLabel.ON_TRACK.value, 0) + (
            label_counts.get(ForecastLabel.AHEAD_OF_SCHEDULE.value, 0)
        )
        below = label_counts.get(ForecastLabel.BELOW_TARGET_PACE.value, 0)

        return ReadinessForecastMetricsSnapshot(
            learners_forecasted=forecasted,
            sittings_scanned=len(rows),
            label_counts=dict(label_counts),
            confidence_counts=dict(confidence_counts),
            trend_counts=dict(trend_counts),
            recovery_projection_count=recovery_count,
            on_track_rate=on_track / forecasted if forecasted else 0.0,
            below_pace_rate=below / forecasted if forecasted else 0.0,
            average_projected_readiness=(
                sum(projected_values) / len(projected_values)
                if projected_values
                else 0.0
            ),
            forecast_accuracy=(
                accuracy_hits / accuracy_pairs if accuracy_pairs else 0.0
            ),
            accuracy_pairs=accuracy_pairs,
            established_confidence_rate=(
                established / forecasted if forecasted else 0.0
            ),
            readiness_progression_labels=tuple(dict.fromkeys(progression))[:8],
        )

    @classmethod
    def from_store(cls, store: Any) -> ReadinessForecastMetricsSnapshot:
        from app.services.educational_yield_metrics import list_evidence_packages

        return cls.from_packages(list_evidence_packages(store))


def _direction_matches(
    projected: float | None,
    later: float | None,
    early_stage: str,
) -> bool:
    """Soft accuracy: later readiness is on the projected side of early."""
    if projected is None or later is None:
        return False
    early_ratio_proxy = _stage_midpoint(early_stage)
    # Projected rise and later rose (or projected fall and later fell).
    projected_delta = projected - early_ratio_proxy
    later_delta = later - early_ratio_proxy
    if abs(projected_delta) < 0.05:
        return abs(later_delta) < 0.12
    return projected_delta * later_delta > 0


def _stage_midpoint(stage: str) -> float:
    """Approximate midpoint for a KWP-006 stage label."""
    mapping = {
        "Building": 0.10,
        "Developing": 0.30,
        "Strengthening": 0.50,
        "Ready for Revision": 0.70,
        "Ready for Assessment": 0.90,
    }
    if stage in mapping:
        return mapping[stage]
    # Fallback via ratio helper for unknown labels.
    for ratio in (0.1, 0.3, 0.5, 0.7, 0.9):
        if readiness_stage_for_ratio(ratio) == stage:
            return ratio
    return 0.4
