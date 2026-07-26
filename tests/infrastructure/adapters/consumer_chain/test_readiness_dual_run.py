"""EP-002.6 Readiness Intelligence dual-run tests."""

from __future__ import annotations

from typing import Any
from unittest.mock import patch

import pytest

from app.infrastructure.adapters.consumer_chain import (
    build_consumer_chain_telemetry,
    build_readiness_dual_run_health_metrics,
    run_readiness_intelligence_dual_run,
    set_consumer_chain_telemetry,
    set_readiness_dual_run_health_metrics,
)
from app.infrastructure.adapters.consumer_chain.readiness_dual_run import (
    compare_legacy_vs_readiness_intelligence,
)
from app.infrastructure.diagnostics.logging import StructuredLogger
from app.infrastructure.events.registry import EventRegistry


@pytest.fixture
def telemetry():
    sink = build_consumer_chain_telemetry(
        structured=StructuredLogger("test.consumer_chain.readiness_dual_run"),
        events=EventRegistry(),
    )
    previous = set_consumer_chain_telemetry(sink)
    yield sink
    set_consumer_chain_telemetry(previous)


@pytest.fixture
def dual_run_metrics():
    metrics = build_readiness_dual_run_health_metrics()
    previous = set_readiness_dual_run_health_metrics(metrics)
    yield metrics
    set_readiness_dual_run_health_metrics(previous)


def _eligible_environ(**extra: str) -> dict[str, str]:
    env = {
        "KWALITEC_DIGITAL_TWIN": "1",
        "APP_ENV": "development",
        "FLASK_ENV": "development",
    }
    env.update(extra)
    return env


def _legacy_surface() -> dict[str, Any]:
    return {
        "readiness": {
            "score": 62.0,
            "coverage_pct": 50.0,
            "avg_mastery": 70.0,
            "review_discipline": 80.0,
            "total_topics": 10,
            "topics_started": 5,
            "topics_mastered": 2,
        },
        "weakest_topics": [
            {
                "topic_id": "fractions",
                "topic_name": "Fractions",
                "mastery_score": 40.0,
            }
        ],
        "strongest_topics": [
            {
                "topic_id": "algebra",
                "topic_name": "Algebra",
                "mastery_score": 90.0,
            }
        ],
        "source_authority": "legacy",
    }


def _twin_payload(*, score: float = 65.0) -> dict[str, Any]:
    return {
        "readiness_score": score,
        "confidence_level": "medium",
        "availability": "available",
        "weakest_areas": [
            {
                "topic_id": "fractions",
                "topic_name": "Fractions",
                "mastery_score": 42.0,
                "reason": "Low mastery",
            }
        ],
        "strongest_areas": [
            {
                "topic_id": "algebra",
                "topic_name": "Algebra",
                "mastery_score": 88.0,
                "reason": "Strong mastery",
            }
        ],
        "limitations_codes": [],
        "readiness_drivers": [],
        "recommended_next_actions": [],
    }


def test_dual_run_skipped_when_twin_off(telemetry, dual_run_metrics):
    result = run_readiness_intelligence_dual_run(
        1,
        _legacy_surface(),
        environ=_eligible_environ(KWALITEC_DIGITAL_TWIN="0"),
        build_readiness_intelligence=lambda _uid: _twin_payload(),
        skip_request_dedupe=True,
    )
    assert result is None
    assert dual_run_metrics.snapshot().dual_run_requests == 0


def test_dual_run_skipped_in_production(telemetry, dual_run_metrics):
    result = run_readiness_intelligence_dual_run(
        1,
        _legacy_surface(),
        environ=_eligible_environ(APP_ENV="production"),
        build_readiness_intelligence=lambda _uid: _twin_payload(),
        skip_request_dedupe=True,
    )
    assert result is None


def test_dual_run_compares_and_records_agreement(telemetry, dual_run_metrics):
    result = run_readiness_intelligence_dual_run(
        7,
        _legacy_surface(),
        environ=_eligible_environ(),
        build_readiness_intelligence=lambda _uid: _twin_payload(score=64.0),
        skip_request_dedupe=True,
        legacy_latency_ms=12.0,
    )
    assert result is not None
    assert result["influences_student"] is False
    assert result["diagnostic_only"] is True
    assert result["readiness_agreement"] is True
    assert result["confidence_agreement"] is True
    assert result["area_overlap"] is True
    snap = dual_run_metrics.snapshot()
    assert snap.dual_run_requests == 1
    assert snap.twin_success_count == 1
    assert snap.readiness_agreement_count == 1


def test_dual_run_fail_open_on_twin_exception(telemetry, dual_run_metrics):
    def _boom(_uid: int) -> dict[str, Any]:
        raise RuntimeError("twin failed")

    result = run_readiness_intelligence_dual_run(
        3,
        _legacy_surface(),
        environ=_eligible_environ(),
        build_readiness_intelligence=_boom,
        skip_request_dedupe=True,
    )
    assert result is not None
    assert result["twin_exception"] is True
    assert result["twin_unavailable"] is True
    assert dual_run_metrics.snapshot().twin_exception_count == 1


def test_compare_captures_score_disagreement():
    comparison = compare_legacy_vs_readiness_intelligence(
        legacy_surface=_legacy_surface(),
        twin_payload=_twin_payload(score=90.0),
        user_id=1,
        environ=_eligible_environ(),
    )
    assert comparison is not None
    assert comparison["readiness_agreement"] is False


def test_get_overall_readiness_not_wrapped_by_dual_run():
    """Collector invariant: get_overall_readiness must not call dual-run."""
    import inspect

    from app.services.readiness_service import ReadinessService

    source = inspect.getsource(ReadinessService.get_overall_readiness)
    assert "run_readiness_intelligence_dual_run" not in source
    assert "build_readiness_intelligence" not in source


def test_surface_facade_runs_dual_run_when_cutover_off(ctx):
    legacy = _legacy_surface()
    with (
        patch(
            "app.services.readiness_service.ReadinessService.get_overall_readiness",
            return_value=legacy["readiness"],
        ),
        patch(
            "app.services.readiness_service.ReadinessService.get_weakest_topics",
            return_value=legacy["weakest_topics"],
        ),
        patch(
            "app.services.readiness_service.ReadinessService.get_strongest_topics",
            return_value=legacy["strongest_topics"],
        ),
        patch(
            "app.infrastructure.adapters.consumer_chain.readiness_dual_run."
            "run_readiness_intelligence_dual_run"
        ) as dual_run,
        patch.dict(
            "os.environ",
            _eligible_environ(KWALITEC_READINESS_INTELLIGENCE_CUTOVER="0"),
            clear=False,
        ),
    ):
        from app.services.readiness_service import ReadinessService

        surface = ReadinessService.get_dashboard_readiness_surface(1)
        assert surface["source_authority"] == "legacy"
        dual_run.assert_called_once()
