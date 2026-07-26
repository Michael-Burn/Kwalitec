"""EP-002.4 Study Insights dual-run tests.

Covers dual-run execution, regression (legacy authority), comparison integrity,
feature-flag matrix, and rollback validation.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any
from unittest.mock import MagicMock

import pytest

from app.infrastructure.adapters.consumer_chain import (
    API_BUILD_STUDY_INSIGHTS,
    build_consumer_chain_telemetry,
    build_study_insights_dual_run_health_metrics,
    compare_legacy_vs_build,
    diagnostic_compare_study_insights,
    is_dual_run_diagnostics_eligible,
    run_study_insights_dual_run,
    set_consumer_chain_telemetry,
    set_study_insights_dual_run_health_metrics,
)
from app.infrastructure.diagnostics.correlation import CorrelationContext
from app.infrastructure.diagnostics.logging import StructuredLogger
from app.infrastructure.events.registry import EventRegistry
from app.infrastructure.events.types import CONSUMER_CHAIN_DUAL_RUN
from app.services.recommendation_service import RecommendationService


@pytest.fixture
def telemetry():
    sink = build_consumer_chain_telemetry(
        structured=StructuredLogger("test.consumer_chain.dual_run"),
        events=EventRegistry(),
    )
    previous = set_consumer_chain_telemetry(sink)
    yield sink
    set_consumer_chain_telemetry(previous)


@pytest.fixture
def dual_run_metrics():
    metrics = build_study_insights_dual_run_health_metrics()
    previous = set_study_insights_dual_run_health_metrics(metrics)
    yield metrics
    set_study_insights_dual_run_health_metrics(previous)


def _eligible_environ(**extra: str) -> dict[str, str]:
    env = {
        "KWALITEC_DIGITAL_TWIN": "1",
        "KWALITEC_DIGITAL_TWIN_AUTHORITY": "0",
        "APP_ENV": "development",
        "FLASK_ENV": "development",
    }
    env.update(extra)
    return env


def _legacy_rows() -> list[dict[str, Any]]:
    return [
        {
            "title": "Review Fractions",
            "category": "Review",
            "priority": "High",
            "explanation": "Due for review",
        },
        {
            "title": "Strengthen Algebra",
            "category": "Weak Topic",
            "priority": "Critical",
            "explanation": "Low mastery",
        },
    ]


def _twin_payload() -> dict[str, Any]:
    return {
        "todays_key_focus": {
            "field_id": "todays_key_focus",
            "title": "Focus",
            "message": "Review Fractions",
            "topic_id": "t1",
            "source": "planner",
        },
        "recommended_next_action": {
            "field_id": "recommended_next_action",
            "title": "Next",
            "message": "Complete review mission",
            "topic_id": "t1",
            "source": "planner",
        },
        "greatest_risk": None,
        "strongest_area": None,
        "confidence_level": "medium",
        "limitations_codes": ["planner_outputs_unavailable"],
    }


# ── Dual-run tests ───────────────────────────────────────────────────────────


def test_run_study_insights_dual_run_executes_twin_when_eligible(
    telemetry, dual_run_metrics, monkeypatch
) -> None:
    twin_calls: list[int] = []

    def fake_build(user_id: int, **_kwargs: Any) -> dict[str, Any]:
        twin_calls.append(user_id)
        return _twin_payload()

    legacy = _legacy_rows()
    result = run_study_insights_dual_run(
        7,
        legacy,
        legacy_latency_ms=12.5,
        telemetry=telemetry,
        environ=_eligible_environ(),
        build_study_insights=fake_build,
        skip_request_dedupe=True,
    )
    assert twin_calls == [7]
    assert result is not None
    assert result["diagnostic_only"] is True
    assert result["influences_student"] is False
    assert result["legacy_categories"] == ["Review", "Weak Topic"]
    assert "todays_key_focus" in result["twin_field_ids"]
    assert result["limitation_codes"] == ["planner_outputs_unavailable"]
    assert result["confidence_level"] == "medium"
    assert result["legacy_latency_ms"] == 12.5
    assert result["twin_latency_ms"] is not None
    assert result["twin_unavailable"] is False
    assert any(
        e.event_type == CONSUMER_CHAIN_DUAL_RUN for e in telemetry.events.published()
    )
    snap = dual_run_metrics.snapshot()
    assert snap.dual_run_requests == 1
    assert snap.twin_success_count == 1
    assert snap.legacy_success_count == 1


def test_twin_exception_fail_open_still_compares(
    telemetry, dual_run_metrics
) -> None:
    def boom(_user_id: int, **_kwargs: Any) -> dict[str, Any]:
        raise RuntimeError("twin exploded")

    legacy = _legacy_rows()
    result = run_study_insights_dual_run(
        3,
        legacy,
        telemetry=telemetry,
        environ=_eligible_environ(),
        build_study_insights=boom,
        skip_request_dedupe=True,
    )
    assert result is not None
    assert result["twin_unavailable"] is True
    assert result["twin_exception"] is True
    assert dual_run_metrics.snapshot().twin_exception_count == 1


# ── Regression — legacy authority ────────────────────────────────────────────


def test_request_dedupe_runs_twin_once_per_user(app, telemetry) -> None:
    calls: list[int] = []

    def fake_build(user_id: int, **_kwargs: Any) -> dict[str, Any]:
        calls.append(user_id)
        return _twin_payload()

    with app.test_request_context("/dashboard"):
        first = run_study_insights_dual_run(
            11,
            _legacy_rows(),
            telemetry=telemetry,
            environ=_eligible_environ(),
            build_study_insights=fake_build,
        )
        second = run_study_insights_dual_run(
            11,
            _legacy_rows(),
            telemetry=telemetry,
            environ=_eligible_environ(),
            build_study_insights=fake_build,
        )
    assert first is not None
    assert second is None
    assert calls == [11]


def test_generate_recommendations_unchanged_when_dual_run_on(
    ctx, user, monkeypatch, telemetry
) -> None:
    monkeypatch.setenv("KWALITEC_DIGITAL_TWIN", "1")
    monkeypatch.setenv("APP_ENV", "development")
    twin_calls = {"n": 0}

    def fake_build(user_id: int, **_kwargs: Any) -> dict[str, Any]:
        twin_calls["n"] += 1
        return _twin_payload()

    monkeypatch.setattr(
        RecommendationService,
        "build_study_insights",
        staticmethod(fake_build),
    )

    baseline = RecommendationService.generate_recommendations(user.id, limit=5)
    again = RecommendationService.generate_recommendations(user.id, limit=5)
    assert again == baseline
    assert isinstance(again, list)
    assert twin_calls["n"] >= 1


def test_dual_run_does_not_mutate_legacy_list(telemetry) -> None:
    legacy = _legacy_rows()
    original = deepcopy(legacy)

    def fake_build(_user_id: int, **_kwargs: Any) -> dict[str, Any]:
        # Attempt hostile mutation of caller list via shared refs — dual-run
        # snapshots before fingerprinting; caller list must stay intact.
        return _twin_payload()

    run_study_insights_dual_run(
        1,
        legacy,
        telemetry=telemetry,
        environ=_eligible_environ(),
        build_study_insights=fake_build,
        skip_request_dedupe=True,
    )
    assert legacy == original


# ── Comparison integrity ─────────────────────────────────────────────────────


def test_comparison_captures_required_fields(telemetry) -> None:
    with CorrelationContext.bind(correlation_id="corr-ep0024", causation_id="cause-1"):
        result = compare_legacy_vs_build(
            legacy_payload=_legacy_rows(),
            build_payload=_twin_payload(),
            user_id=9,
            api_name=API_BUILD_STUDY_INSIGHTS,
            telemetry=telemetry,
            environ=_eligible_environ(),
            legacy_latency_ms=4.0,
            twin_latency_ms=8.0,
        )
    assert result is not None
    assert result["correlation_id"] == "corr-ep0024"
    assert result["causation_id"] == "cause-1"
    assert result["twin_enabled"] is True
    assert result["authority_enabled"] is False
    assert result["legacy_unavailable"] is False
    assert result["twin_unavailable"] is False
    assert result["legacy_categories"] == ["Review", "Weak Topic"]
    assert set(result["twin_field_ids"]) >= {
        "todays_key_focus",
        "recommended_next_action",
    }
    assert result["limitation_codes"] == ["planner_outputs_unavailable"]
    assert result["confidence_available"] is True
    assert result["fingerprints_match"] is False


def test_empty_legacy_and_none_twin_marked_unavailable(telemetry) -> None:
    result = compare_legacy_vs_build(
        legacy_payload=[],
        build_payload=None,
        user_id=1,
        telemetry=telemetry,
        environ=_eligible_environ(),
    )
    assert result is not None
    assert result["legacy_unavailable"] is True
    assert result["twin_unavailable"] is True


# ── Feature flag matrix ──────────────────────────────────────────────────────


@pytest.mark.parametrize(
    ("environ", "eligible"),
    [
        (_eligible_environ(), True),
        (_eligible_environ(KWALITEC_DIGITAL_TWIN_AUTHORITY="1"), True),
        (
            {
                "KWALITEC_DIGITAL_TWIN": "0",
                "KWALITEC_DIGITAL_TWIN_AUTHORITY": "0",
                "APP_ENV": "development",
            },
            False,
        ),
        (
            {
                "KWALITEC_DIGITAL_TWIN": "0",
                "KWALITEC_DIGITAL_TWIN_AUTHORITY": "1",
                "APP_ENV": "development",
            },
            False,
        ),
        (
            {
                "KWALITEC_DIGITAL_TWIN": "1",
                "APP_ENV": "production",
            },
            False,
        ),
        (
            {
                "KWALITEC_DIGITAL_TWIN": "1",
                "APP_ENV": "prod",
            },
            False,
        ),
    ],
)
def test_dual_run_eligibility_matrix(environ: dict[str, str], eligible: bool) -> None:
    assert is_dual_run_diagnostics_eligible(environ=environ) is eligible


def test_authority_on_recorded_but_does_not_change_student_payload(
    telemetry,
) -> None:
    legacy = _legacy_rows()
    env = _eligible_environ(KWALITEC_DIGITAL_TWIN_AUTHORITY="1")
    result = run_study_insights_dual_run(
        5,
        legacy,
        telemetry=telemetry,
        environ=env,
        build_study_insights=lambda _uid, **_k: _twin_payload(),
        skip_request_dedupe=True,
    )
    assert result is not None
    assert result["authority_enabled"] is True
    assert result["influences_student"] is False
    assert legacy == _legacy_rows()


# ── Rollback validation ──────────────────────────────────────────────────────


def test_rollback_twin_off_skips_dual_run(telemetry, dual_run_metrics) -> None:
    called = {"n": 0}

    def fake_build(_user_id: int, **_kwargs: Any) -> dict[str, Any]:
        called["n"] += 1
        return _twin_payload()

    result = run_study_insights_dual_run(
        1,
        _legacy_rows(),
        telemetry=telemetry,
        environ={
            "KWALITEC_DIGITAL_TWIN": "0",
            "APP_ENV": "development",
        },
        build_study_insights=fake_build,
        skip_request_dedupe=True,
    )
    assert result is None
    assert called["n"] == 0
    assert dual_run_metrics.snapshot().dual_run_requests == 0
    assert not any(
        e.event_type == CONSUMER_CHAIN_DUAL_RUN for e in telemetry.events.published()
    )


def test_production_env_skips_even_when_twin_on(telemetry) -> None:
    called = {"n": 0}

    def fake_build(_user_id: int, **_kwargs: Any) -> dict[str, Any]:
        called["n"] += 1
        return _twin_payload()

    result = run_study_insights_dual_run(
        1,
        _legacy_rows(),
        telemetry=telemetry,
        environ={
            "KWALITEC_DIGITAL_TWIN": "1",
            "APP_ENV": "production",
        },
        build_study_insights=fake_build,
        skip_request_dedupe=True,
    )
    assert result is None
    assert called["n"] == 0


def test_generate_recommendations_hook_skips_when_ineligible(
    ctx, user, monkeypatch, telemetry
) -> None:
    monkeypatch.setenv("KWALITEC_DIGITAL_TWIN", "0")
    monkeypatch.setenv("APP_ENV", "development")
    twin = MagicMock(return_value=_twin_payload())
    monkeypatch.setattr(
        RecommendationService, "build_study_insights", staticmethod(twin)
    )
    RecommendationService.generate_recommendations(user.id, limit=3)
    twin.assert_not_called()


def test_diagnostic_compare_study_insights_ops_helper(
    ctx, user, monkeypatch, telemetry
) -> None:
    monkeypatch.setenv("KWALITEC_DIGITAL_TWIN", "1")
    monkeypatch.setenv("APP_ENV", "development")
    monkeypatch.setattr(
        RecommendationService,
        "build_study_insights",
        staticmethod(lambda _uid, **_k: _twin_payload()),
    )
    result = diagnostic_compare_study_insights(
        user.id,
        limit=3,
        telemetry=telemetry,
        environ=_eligible_environ(),
    )
    assert result is not None
    assert result["api_name"] == API_BUILD_STUDY_INSIGHTS
    assert result["diagnostic_only"] is True


def test_health_snapshot_readiness_blocked_on_regression(dual_run_metrics) -> None:
    dual_run_metrics.record(
        {
            "legacy_unavailable": False,
            "twin_unavailable": False,
            "twin_exception": False,
            "fingerprints_match": False,
            "legacy_latency_ms": 1.0,
            "twin_latency_ms": 2.0,
            "limitation_codes": ["sparse_evidence"],
        }
    )
    dual_run_metrics.mark_behavioural_regression()
    snap = dual_run_metrics.snapshot()
    assert snap.overall_dual_run_readiness == "blocked"
    assert snap.limitation_code_frequency[0][0] == "sparse_evidence"
