"""Unit tests for EP-002.1 consumer-chain observability."""

from __future__ import annotations

import pytest

from app.infrastructure.adapters.consumer_chain import (
    API_BUILD_DAILY_STUDY_PLAN,
    API_BUILD_READINESS_INTELLIGENCE,
    API_BUILD_STUDY_INSIGHTS,
    OUTCOME_LIMITATION,
    OUTCOME_SUCCESS,
    OUTCOME_UNAVAILABLE,
    SERVICE_PLANNING,
    build_consumer_chain_telemetry,
    classify_build_result,
    compare_legacy_vs_build,
    fingerprint_payload,
    is_dual_run_diagnostics_eligible,
    observe_build_api,
    set_consumer_chain_telemetry,
)
from app.infrastructure.diagnostics.correlation import CorrelationContext
from app.infrastructure.diagnostics.logging import StructuredLogger
from app.infrastructure.events.registry import EventRegistry
from app.infrastructure.events.types import (
    CONSUMER_CHAIN_COMPLETED,
    CONSUMER_CHAIN_DUAL_RUN,
    CONSUMER_CHAIN_EVENT_TYPES,
    CONSUMER_CHAIN_FAILED,
    CONSUMER_CHAIN_LATENCY,
    CONSUMER_CHAIN_REQUESTED,
    EVENT_TYPES,
)
from app.services.planning_service import PlanningService
from app.services.readiness_service import ReadinessService
from app.services.recommendation_service import RecommendationService


@pytest.fixture
def telemetry():
    sink = build_consumer_chain_telemetry(
        structured=StructuredLogger("test.consumer_chain"),
        events=EventRegistry(),
    )
    previous = set_consumer_chain_telemetry(sink)
    yield sink
    set_consumer_chain_telemetry(previous)


def test_consumer_chain_event_types_registered() -> None:
    for event_type in CONSUMER_CHAIN_EVENT_TYPES:
        assert event_type in EVENT_TYPES


def test_classify_none_unavailable() -> None:
    outcome, returned_none, codes, confidence = classify_build_result(None)
    assert outcome == OUTCOME_UNAVAILABLE
    assert returned_none is True
    assert codes == ()
    assert confidence is None


def test_classify_success_and_limitation() -> None:
    outcome, returned_none, codes, confidence = classify_build_result(
        {"confidence_level": "high"}
    )
    assert outcome == OUTCOME_SUCCESS
    assert returned_none is False
    assert codes == ()
    assert confidence is True

    outcome, returned_none, codes, confidence = classify_build_result(
        {
            "limitations_codes": ["planner_unavailable"],
            "confidence_level": "",
        }
    )
    assert outcome == OUTCOME_LIMITATION
    assert returned_none is False
    assert codes == ("planner_unavailable",)
    assert confidence is False


def test_observe_build_api_emits_requested_and_completed(telemetry) -> None:
    with CorrelationContext.bind(correlation_id="corr-test-1"):
        result = observe_build_api(
            service_name=SERVICE_PLANNING,
            api_name=API_BUILD_DAILY_STUDY_PLAN,
            user_id=7,
            call=lambda: {"availability": "available"},
            telemetry=telemetry,
            environ={"KWALITEC_DIGITAL_TWIN": "1"},
        )
    assert result == {"availability": "available"}
    messages = [r["message"] for r in telemetry.records]
    assert "consumer_chain.invoked" in messages
    assert "consumer_chain.completed" in messages
    completed = next(
        r for r in telemetry.records if r["message"] == "consumer_chain.completed"
    )
    assert completed["api_name"] == API_BUILD_DAILY_STUDY_PLAN
    assert completed["outcome"] == OUTCOME_SUCCESS
    assert completed["returned_none"] is False
    assert completed["twin_enabled"] is True
    assert completed["authority_enabled"] is False
    assert completed["correlation_id"] == "corr-test-1"
    assert completed["duration_ms"] >= 0
    published = {e.event_type for e in telemetry.events.published()}
    assert CONSUMER_CHAIN_REQUESTED in published
    assert CONSUMER_CHAIN_COMPLETED in published
    assert CONSUMER_CHAIN_LATENCY in published


def test_observe_build_api_records_unavailable(telemetry) -> None:
    result = observe_build_api(
        service_name=SERVICE_PLANNING,
        api_name=API_BUILD_DAILY_STUDY_PLAN,
        user_id=1,
        call=lambda: None,
        telemetry=telemetry,
        environ={},
    )
    assert result is None
    completed = next(
        r for r in telemetry.records if r["message"] == "consumer_chain.completed"
    )
    assert completed["outcome"] == OUTCOME_UNAVAILABLE
    assert completed["returned_none"] is True
    assert completed["twin_enabled"] is False


def _raise_boom() -> None:
    raise RuntimeError("boom")


def test_observe_build_api_records_exception_and_reraises(telemetry) -> None:
    with pytest.raises(RuntimeError, match="boom"):
        observe_build_api(
            service_name=SERVICE_PLANNING,
            api_name=API_BUILD_DAILY_STUDY_PLAN,
            user_id=1,
            call=_raise_boom,
            telemetry=telemetry,
        )
    failed = next(
        r for r in telemetry.records if r["message"] == "consumer_chain.failed"
    )
    assert failed["outcome"] == "exception"
    assert failed["error_code"] == "RuntimeError"
    assert any(
        e.event_type == CONSUMER_CHAIN_FAILED for e in telemetry.events.published()
    )


def test_planning_service_emits_when_twin_off(telemetry, monkeypatch) -> None:
    monkeypatch.setattr(
        PlanningService,
        "_resolve_twin_foundation",
        staticmethod(lambda: None),
    )
    assert PlanningService.build_daily_study_plan(1) is None
    apis = [
        r["api_name"]
        for r in telemetry.records
        if r["message"] == "consumer_chain.completed"
    ]
    assert API_BUILD_DAILY_STUDY_PLAN in apis


def test_readiness_and_insights_emit_when_twin_off(telemetry, monkeypatch) -> None:
    monkeypatch.setattr(
        ReadinessService,
        "_resolve_twin_foundation",
        staticmethod(lambda: None),
    )
    monkeypatch.setattr(
        RecommendationService,
        "_resolve_twin_foundation",
        staticmethod(lambda: None),
    )
    assert ReadinessService.build_readiness_intelligence(2) is None
    assert RecommendationService.build_study_insights(3) is None
    completed_apis = {
        r["api_name"]
        for r in telemetry.records
        if r["message"] == "consumer_chain.completed"
    }
    assert API_BUILD_READINESS_INTELLIGENCE in completed_apis
    assert API_BUILD_STUDY_INSIGHTS in completed_apis


def test_authority_flag_recorded_when_both_on(telemetry) -> None:
    observe_build_api(
        service_name=SERVICE_PLANNING,
        api_name=API_BUILD_DAILY_STUDY_PLAN,
        user_id=9,
        call=lambda: None,
        telemetry=telemetry,
        environ={
            "KWALITEC_DIGITAL_TWIN": "1",
            "KWALITEC_DIGITAL_TWIN_AUTHORITY": "1",
        },
    )
    completed = next(
        r for r in telemetry.records if r["message"] == "consumer_chain.completed"
    )
    assert completed["twin_enabled"] is True
    assert completed["authority_enabled"] is True


def test_authority_requires_twin(telemetry) -> None:
    """Authority alone does not enable Twin (AND-gated in v2_flags)."""
    observe_build_api(
        service_name=SERVICE_PLANNING,
        api_name=API_BUILD_DAILY_STUDY_PLAN,
        user_id=9,
        call=lambda: None,
        telemetry=telemetry,
        environ={
            "KWALITEC_DIGITAL_TWIN": "0",
            "KWALITEC_DIGITAL_TWIN_AUTHORITY": "1",
        },
    )
    completed = next(
        r for r in telemetry.records if r["message"] == "consumer_chain.completed"
    )
    assert completed["twin_enabled"] is False
    assert completed["authority_enabled"] is False


def test_fingerprint_stable() -> None:
    assert fingerprint_payload({"a": 1, "b": 2}) == fingerprint_payload(
        {"b": 2, "a": 1}
    )


def test_dual_run_ineligible_in_production() -> None:
    assert (
        is_dual_run_diagnostics_eligible(
            environ={
                "KWALITEC_DIGITAL_TWIN": "1",
                "APP_ENV": "production",
            }
        )
        is False
    )


def test_dual_run_ineligible_when_twin_off() -> None:
    assert (
        is_dual_run_diagnostics_eligible(
            environ={
                "KWALITEC_DIGITAL_TWIN": "0",
                "APP_ENV": "development",
            }
        )
        is False
    )


def test_dual_run_compare_emits_when_eligible(telemetry) -> None:
    result = compare_legacy_vs_build(
        legacy_payload=[{"id": 1}],
        build_payload={"todays_key_focus": None},
        user_id=42,
        api_name=API_BUILD_STUDY_INSIGHTS,
        telemetry=telemetry,
        environ={
            "KWALITEC_DIGITAL_TWIN": "1",
            "APP_ENV": "development",
        },
    )
    assert result is not None
    assert result["diagnostic_only"] is True
    assert result["influences_student"] is False
    assert result["fingerprints_match"] is False
    assert any(
        e.event_type == CONSUMER_CHAIN_DUAL_RUN for e in telemetry.events.published()
    )


def test_dual_run_compare_skipped_in_production(telemetry) -> None:
    result = compare_legacy_vs_build(
        legacy_payload=[1],
        build_payload=[1],
        user_id=1,
        telemetry=telemetry,
        environ={
            "KWALITEC_DIGITAL_TWIN": "1",
            "APP_ENV": "production",
        },
    )
    assert result is None
    assert not any(
        e.event_type == CONSUMER_CHAIN_DUAL_RUN for e in telemetry.events.published()
    )
