"""EP-002.1 regression: Twin-gated build_* behaviour unchanged under observability."""

from __future__ import annotations

from datetime import date
from unittest.mock import MagicMock

import pytest

from app.infrastructure.adapters.consumer_chain import (
    build_consumer_chain_telemetry,
    set_consumer_chain_telemetry,
)
from app.infrastructure.diagnostics.logging import StructuredLogger
from app.infrastructure.events.registry import EventRegistry
from app.services.planning_service import PlanningService
from app.services.readiness_service import ReadinessService
from app.services.recommendation_service import RecommendationService


@pytest.fixture
def telemetry():
    sink = build_consumer_chain_telemetry(
        structured=StructuredLogger("test.consumer_chain.regression"),
        events=EventRegistry(),
    )
    previous = set_consumer_chain_telemetry(sink)
    yield sink
    set_consumer_chain_telemetry(previous)


def test_build_daily_study_plan_still_none_when_twin_off(
    telemetry, monkeypatch
) -> None:
    monkeypatch.setattr(
        PlanningService,
        "_resolve_twin_foundation",
        staticmethod(lambda: None),
    )
    assert PlanningService.build_daily_study_plan(1) is None


def test_build_readiness_intelligence_still_none_when_twin_off(
    telemetry, monkeypatch
) -> None:
    monkeypatch.setattr(
        ReadinessService,
        "_resolve_twin_foundation",
        staticmethod(lambda: None),
    )
    assert ReadinessService.build_readiness_intelligence(1) is None


def test_build_study_insights_still_none_when_twin_off(
    telemetry, monkeypatch
) -> None:
    monkeypatch.setattr(
        RecommendationService,
        "_resolve_twin_foundation",
        staticmethod(lambda: None),
    )
    assert RecommendationService.build_study_insights(1) is None


def test_public_signatures_accept_existing_kwargs() -> None:
    """Keyword surface used by EP-001.2–4 / EP-002.2 callers remains compatible."""
    assert PlanningService.build_daily_study_plan(
        1, today=date.today(), canonical_state=None
    ) is None
    assert (
        ReadinessService.build_readiness_intelligence(
            1,
            daily_plan=None,
            include_planner=False,
            canonical_state=None,
        )
        is None
    )
    assert (
        RecommendationService.build_study_insights(
            1,
            daily_plan=None,
            readiness_intelligence=None,
            include_planner=False,
            include_readiness=False,
            canonical_state=None,
        )
        is None
    )


def test_observability_disabled_still_returns_payload(monkeypatch) -> None:
    sink = build_consumer_chain_telemetry(enabled=False)
    previous = set_consumer_chain_telemetry(sink)
    try:
        monkeypatch.setattr(
            PlanningService,
            "_resolve_twin_foundation",
            staticmethod(lambda: None),
        )
        assert PlanningService.build_daily_study_plan(99) is None
        assert sink.records == ()
    finally:
        set_consumer_chain_telemetry(previous)


def test_injected_foundation_unavailable_path_emits_and_returns_none(
    monkeypatch, telemetry
) -> None:
    """Injected disabled foundation still returns None; observability fires."""
    foundation = MagicMock()
    foundation.is_enabled.return_value = False
    result = PlanningService.build_daily_study_plan(42, foundation=foundation)
    assert result is None
    assert any(
        r["message"] == "consumer_chain.completed"
        and r["api_name"] == "build_daily_study_plan"
        and r["returned_none"] is True
        for r in telemetry.records
    )
