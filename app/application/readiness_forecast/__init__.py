"""Readiness Forecast & Study Trajectory — EI Phase 6 (KWP-012).

Projection layer that estimates where a learner is heading from existing
educational evidence. Does not redesign Runtime, Evidence, Progress,
Strategy, Diagnostics, Difficulty, Effectiveness, Memory, Twin, or Mission.
"""

from __future__ import annotations

from app.application.readiness_forecast.dto import (
    CONFIDENCE_TITLES,
    FORECAST_TITLES,
    TARGET_READINESS_RATIO,
    TARGET_READINESS_STAGE,
    TREND_TITLES,
    ForecastConfidence,
    ForecastLabel,
    ForecastSignals,
    ReadinessForecast,
    StudyTrajectory,
    TrendDirection,
)
from app.application.readiness_forecast.engine import (
    ReadinessForecastEngine,
    get_readiness_forecast_engine,
)

__all__ = [
    "CONFIDENCE_TITLES",
    "FORECAST_TITLES",
    "TARGET_READINESS_RATIO",
    "TARGET_READINESS_STAGE",
    "TREND_TITLES",
    "ForecastConfidence",
    "ForecastLabel",
    "ForecastSignals",
    "ReadinessForecast",
    "ReadinessForecastEngine",
    "StudyTrajectory",
    "TrendDirection",
    "get_readiness_forecast_engine",
]
