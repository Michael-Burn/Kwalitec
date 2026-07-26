"""EP-002.7 Daily Plan dual-run diagnostic tests."""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any
from unittest.mock import patch

import pytest

from app.infrastructure.adapters.consumer_chain import (
    build_consumer_chain_telemetry,
    build_daily_plan_dual_run_health_metrics,
    run_daily_plan_dual_run,
    set_consumer_chain_telemetry,
    set_daily_plan_dual_run_health_metrics,
)
from app.infrastructure.adapters.consumer_chain.daily_plan_cutover import (
    is_daily_plan_cutover_eligible,
)
from app.infrastructure.diagnostics.logging import StructuredLogger
from app.infrastructure.events.registry import EventRegistry
from app.services.planning_service import PlanningService


@pytest.fixture
def telemetry():
    sink = build_consumer_chain_telemetry(
        structured=StructuredLogger("test.consumer_chain.daily_plan_dual_run"),
        events=EventRegistry(),
    )
    previous = set_consumer_chain_telemetry(sink)
    yield sink
    set_consumer_chain_telemetry(previous)


@pytest.fixture
def dual_run_metrics():
    metrics = build_daily_plan_dual_run_health_metrics()
    previous = set_daily_plan_dual_run_health_metrics(metrics)
    yield metrics
    set_daily_plan_dual_run_health_metrics(previous)


def _legacy_surface(*, title: str = "Study Fractions") -> dict[str, Any]:
    return {
        "today_mission": SimpleNamespace(
            id=1,
            title=title,
            status="Pending",
            tasks=[],
        ),
        "source_authority": "legacy",
    }


def _twin_plan(*, topic_id: str = "fractions", topic_name: str = "Fractions") -> dict:
    return {
        "availability": "available",
        "today_missions": [
            {
                "slot": "progression",
                "topic_id": topic_id,
                "topic_name": topic_name,
                "reason": "Next incomplete topic",
                "priority": 1,
            }
        ],
        "recommended_workload": {
            "available_study_minutes": 60,
            "recommended_minutes": 45,
            "rationale": "weekday load",
        },
        "topic_ordering": [
            {"position": 1, "topic_id": topic_id, "topic_name": topic_name}
        ],
        "limitations_codes": [],
    }


def test_dual_run_skips_when_twin_off(telemetry, dual_run_metrics):
    result = run_daily_plan_dual_run(
        1,
        _legacy_surface(),
        environ={
            "KWALITEC_DIGITAL_TWIN": "0",
            "APP_ENV": "development",
            "FLASK_ENV": "development",
        },
        build_daily_study_plan=lambda *_a, **_k: _twin_plan(),
        skip_request_dedupe=True,
    )
    assert result is None


def test_dual_run_skips_in_production(telemetry, dual_run_metrics):
    result = run_daily_plan_dual_run(
        1,
        _legacy_surface(),
        environ={
            "KWALITEC_DIGITAL_TWIN": "1",
            "APP_ENV": "production",
            "FLASK_ENV": "production",
        },
        build_daily_study_plan=lambda *_a, **_k: _twin_plan(),
        skip_request_dedupe=True,
    )
    assert result is None


def test_dual_run_compares_topic_agreement(telemetry, dual_run_metrics):
    result = run_daily_plan_dual_run(
        7,
        _legacy_surface(title="Study Fractions"),
        environ={
            "KWALITEC_DIGITAL_TWIN": "1",
            "APP_ENV": "development",
            "FLASK_ENV": "development",
        },
        build_daily_study_plan=lambda *_a, **_k: _twin_plan(),
        skip_request_dedupe=True,
    )
    assert result is not None
    assert result["influences_student"] is False
    assert result["diagnostic_only"] is True
    assert result["topic_agreement"] is True
    snap = dual_run_metrics.snapshot()
    assert snap.dual_run_requests == 1
    assert snap.twin_success_count == 1


def test_dual_run_fail_open_on_twin_exception(telemetry, dual_run_metrics):
    def boom(*_a, **_k):
        raise RuntimeError("twin boom")

    result = run_daily_plan_dual_run(
        3,
        _legacy_surface(),
        environ={
            "KWALITEC_DIGITAL_TWIN": "1",
            "APP_ENV": "development",
            "FLASK_ENV": "development",
        },
        build_daily_study_plan=boom,
        skip_request_dedupe=True,
    )
    assert result is not None
    assert result["twin_exception"] is True
    assert result["twin_unavailable"] is True


def test_dual_run_hook_skips_when_cutover_eligible():
    assert is_daily_plan_cutover_eligible(
        environ={
            "KWALITEC_DIGITAL_TWIN": "1",
            "KWALITEC_DAILY_PLAN_CUTOVER": "1",
            "APP_ENV": "development",
            "FLASK_ENV": "development",
        }
    )
    with patch(
        "app.infrastructure.adapters.consumer_chain.daily_plan_dual_run.run_daily_plan_dual_run"
    ) as dual:
        with patch.dict(
            "os.environ",
            {
                "KWALITEC_DIGITAL_TWIN": "1",
                "KWALITEC_DAILY_PLAN_CUTOVER": "1",
                "APP_ENV": "development",
                "FLASK_ENV": "development",
            },
            clear=False,
        ):
            PlanningService._maybe_daily_plan_dual_run(
                1, _legacy_surface(), legacy_latency_ms=1.0
            )
        dual.assert_not_called()


def test_mission_optimizer_not_imported_by_dual_run():
    import app.infrastructure.adapters.consumer_chain.daily_plan_dual_run as mod

    source = open(mod.__file__, encoding="utf-8").read()
    assert "from app.services.mission_optimizer" not in source
    assert "import mission_optimizer" not in source
    assert "generate_balanced_mission" not in source
