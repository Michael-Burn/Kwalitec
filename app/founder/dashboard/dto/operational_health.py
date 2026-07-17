"""Operational Health DTOs (V1SP-001C).

Deterministic, explainable operational cards for the Founder Command Centre.
No scoring, ranking, forecasting, or Version 2 educational intelligence.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class OperationalInsightCard:
    """One Needs Attention insight with a primary action."""

    rule_id: str
    group: str
    title: str
    count: int
    explanation: str
    why_it_matters: str
    primary_action_label: str
    href: str


@dataclass(frozen=True)
class HealthyActivityMetric:
    """One Healthy Activity metric — platform health, not vanity."""

    metric_id: str
    label: str
    value: int
    explanation: str
    href: str | None = None


@dataclass(frozen=True)
class TrendSeries:
    """Short-term operational trend (no forecasting)."""

    series_id: str
    label: str
    labels: tuple[str, ...]
    values: tuple[int, ...]
    summary: str


@dataclass(frozen=True)
class OperationalHealthPage:
    """Full Operational Health page model."""

    refreshed_at: str
    timezone_policy: str
    needs_attention: tuple[OperationalInsightCard, ...]
    healthy_activity: tuple[HealthyActivityMetric, ...]
    trends: tuple[TrendSeries, ...]
    attention_total: int
