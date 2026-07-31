"""Readiness Forecast Engine — EI Phase 6 (KWP-012).

Estimates educational trajectory from existing evidence:
"If the learner continues studying in this way, what is the likely
readiness by the target exam date?"

Projection layer only — never redesigns Learning Runtime, Evidence,
Progress, Learning Strategy, Diagnostics, Difficulty, Intervention
Effectiveness, Educational Memory, Student Twin, or Mission Runtime.
"""

from __future__ import annotations

import logging
from datetime import date
from typing import Any

from app.application.readiness_forecast.dto import (
    FORECAST_TITLES,
    ForecastLabel,
    ForecastSignals,
    ReadinessForecast,
)
from app.application.readiness_forecast.guidance import (
    explanation_for,
    guidance_for,
    scrub,
)
from app.application.readiness_forecast.projection import project_trajectory
from app.application.readiness_forecast.rules import classify_forecast
from app.application.readiness_forecast.signals import extract_forecast_signals

logger = logging.getLogger(__name__)


class ReadinessForecastEngine:
    """Deterministic readiness forecast from sitting evidence."""

    AUTHORITY_ID = "readiness_forecast_engine"
    AUTHORITY_VERSION = "1.0.0"

    def forecast(
        self,
        packages: list[dict[str, Any]] | tuple[dict[str, Any], ...] = (),
        *,
        student_id: str = "",
        days_to_exam: int | None = None,
        exam_date: date | None = None,
        exam_date_label: str = "",
        current_readiness_ratio: float | None = None,
        as_of: date | None = None,
        signals: ForecastSignals | None = None,
    ) -> ReadinessForecast:
        """Return a deterministic ReadinessForecast for one learner."""
        sid = (student_id or "").strip()
        signal_set = signals or extract_forecast_signals(
            packages,
            student_id=sid,
            days_to_exam=days_to_exam,
            exam_date=exam_date,
            exam_date_label=exam_date_label,
            current_readiness_ratio=current_readiness_ratio,
            as_of=as_of,
        )
        trajectory = project_trajectory(signal_set)
        label, rule_id = classify_forecast(signal_set, trajectory)
        title = FORECAST_TITLES[label]
        guidance = scrub(
            guidance_for(label, signals=signal_set, trajectory=trajectory)
        )
        explanation = scrub(
            explanation_for(label, signals=signal_set, trajectory=trajectory)
        )
        has_forecast = label != ForecastLabel.INSUFFICIENT_EVIDENCE

        return ReadinessForecast(
            label=label,
            title=title,
            guidance=guidance,
            explanation=explanation,
            rule_id=rule_id,
            trajectory=trajectory,
            signals=signal_set,
            student_id=sid,
            has_forecast=has_forecast,
        )

    def forecast_from_store(
        self,
        store: Any,
        *,
        student_id: str,
        days_to_exam: int | None = None,
        exam_date: date | None = None,
        exam_date_label: str = "",
        current_readiness_ratio: float | None = None,
    ) -> ReadinessForecast:
        """Load Evidence Packages from a session store and forecast."""
        from app.services.educational_yield_metrics import list_evidence_packages

        packages = list_evidence_packages(store) if store is not None else []
        return self.forecast(
            packages,
            student_id=student_id,
            days_to_exam=days_to_exam,
            exam_date=exam_date,
            exam_date_label=exam_date_label,
            current_readiness_ratio=current_readiness_ratio,
        )


_ENGINE: ReadinessForecastEngine | None = None


def get_readiness_forecast_engine() -> ReadinessForecastEngine:
    global _ENGINE
    if _ENGINE is None:
        _ENGINE = ReadinessForecastEngine()
    return _ENGINE
