"""Adaptive Decision Engine protocol (ADR-027 M0)."""

from __future__ import annotations

from typing import Protocol

from app.application.adaptive_decision.types import (
    DailySittingRequest,
    SittingDecision,
)


class AdaptiveDecisionEngine(Protocol):
    """Intent-specific Decision Engine for daily sitting selection."""

    def decide_daily_sitting(
        self, request: DailySittingRequest
    ) -> SittingDecision:
        """Always return exactly one of ADAPTIVE | SAFE_FALLBACK | BLOCKED."""
        ...
