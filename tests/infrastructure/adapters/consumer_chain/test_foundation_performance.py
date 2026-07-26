"""EP-002.2 — Before/after Foundation assemble performance comparison.

Simulates pre-DI nested triple assemble vs post-DI shared CLS injection
using EP-002.1/2 consumer-chain observability counters.
"""

from __future__ import annotations

import time
from types import MappingProxyType
from unittest.mock import MagicMock

import pytest

from app.infrastructure.adapters.consumer_chain import (
    API_BUILD_DAILY_STUDY_PLAN,
    API_BUILD_READINESS_INTELLIGENCE,
    API_BUILD_STUDY_INSIGHTS,
    SERVICE_PLANNING,
    SERVICE_READINESS,
    SERVICE_RECOMMENDATION,
    assemble_shared_canonical_state,
    build_consumer_chain_telemetry,
    observe_build_api,
    set_consumer_chain_telemetry,
)
from app.infrastructure.adapters.digital_twin.contracts import (
    AVAILABILITY_AVAILABLE,
)
from app.infrastructure.adapters.digital_twin.foundation import (
    FOUNDATION_VERSION,
    CanonicalLearnerState,
)
from app.infrastructure.diagnostics.logging import StructuredLogger
from app.infrastructure.events.registry import EventRegistry


def _block(payload: dict) -> dict:
    return {
        "availability": AVAILABILITY_AVAILABLE,
        "unavailable_reason": "",
        "authority": "runtime_a",
        "source_field": "test",
        "evidence_refs": [],
        "payload": payload,
    }


def _canonical_state() -> CanonicalLearnerState:
    return CanonicalLearnerState(
        student_id="7",
        as_of="2026-07-26T10:00:00",
        foundation_version=FOUNDATION_VERSION,
        twin_id="twin-7",
        study_state=_block({"exam_readiness": 50.0}),
        topic_mastery=_block({"topics": []}),
        topic_progress=_block({"topics": []}),
        learning_evidence=_block({}),
        practice_performance=_block({}),
        mock_performance=_block({}),
        study_behaviour=_block({}),
        study_consistency=_block({}),
        streaks=_block({"current_streak_days": 1}),
        mission_completion=_block({}),
        facet_labels=MappingProxyType({}),
        limitations_codes=(),
        provenance_refs=(),
        availability=AVAILABILITY_AVAILABLE,
        unavailable_reason="",
    )


@pytest.fixture
def telemetry():
    sink = build_consumer_chain_telemetry(
        structured=StructuredLogger("test.foundation_perf"),
        events=EventRegistry(),
    )
    previous = set_consumer_chain_telemetry(sink)
    yield sink
    set_consumer_chain_telemetry(previous)


def _slow_assemble(foundation: MagicMock, delay_s: float = 0.002):
    state = _canonical_state()

    def _assemble(_sid: str):
        time.sleep(delay_s)
        return state

    foundation.assemble.side_effect = _assemble
    foundation.is_enabled.return_value = True
    return foundation


def _count_assembles(telemetry) -> tuple[int, int]:
    records = [
        r
        for r in telemetry.records
        if r["message"] == "consumer_chain.foundation_assemble"
    ]
    assembled = sum(1 for r in records if r["assembled"] is True)
    injected = sum(1 for r in records if r["assembled"] is False)
    return assembled, injected


def test_before_vs_after_assemble_count_and_latency(telemetry) -> None:
    """Before: 3 assembles. After: 1 assemble + 2 share-hits. Latency improves."""
    foundation = _slow_assemble(MagicMock(), delay_s=0.003)

    # --- BEFORE: nested services each call foundation.assemble ---
    telemetry.clear()
    started = time.perf_counter()

    def before_chain():
        def insight_body():
            assemble_shared_canonical_state(
                foundation,
                "7",
                service_name=SERVICE_RECOMMENDATION,
                api_name=API_BUILD_STUDY_INSIGHTS,
            )
            observe_build_api(
                service_name=SERVICE_PLANNING,
                api_name=API_BUILD_DAILY_STUDY_PLAN,
                user_id=7,
                call=lambda: assemble_shared_canonical_state(
                    foundation,
                    "7",
                    service_name=SERVICE_PLANNING,
                    api_name=API_BUILD_DAILY_STUDY_PLAN,
                )
                or True,
            )
            observe_build_api(
                service_name=SERVICE_READINESS,
                api_name=API_BUILD_READINESS_INTELLIGENCE,
                user_id=7,
                call=lambda: assemble_shared_canonical_state(
                    foundation,
                    "7",
                    service_name=SERVICE_READINESS,
                    api_name=API_BUILD_READINESS_INTELLIGENCE,
                )
                or True,
            )
            return {"availability": AVAILABILITY_AVAILABLE}

        return observe_build_api(
            service_name=SERVICE_RECOMMENDATION,
            api_name=API_BUILD_STUDY_INSIGHTS,
            user_id=7,
            call=insight_body,
        )

    before_chain()
    before_ms = (time.perf_counter() - started) * 1000.0
    before_assembled, before_injected = _count_assembles(telemetry)
    assert before_assembled == 3
    assert before_injected == 0
    assert foundation.assemble.call_count == 3

    # --- AFTER: assemble once; nested share injected CLS ---
    foundation.assemble.reset_mock()
    foundation.assemble.side_effect = None
    foundation = _slow_assemble(MagicMock(), delay_s=0.003)
    telemetry.clear()
    started = time.perf_counter()

    def after_chain():
        def insight_body():
            state = assemble_shared_canonical_state(
                foundation,
                "7",
                service_name=SERVICE_RECOMMENDATION,
                api_name=API_BUILD_STUDY_INSIGHTS,
            )
            observe_build_api(
                service_name=SERVICE_PLANNING,
                api_name=API_BUILD_DAILY_STUDY_PLAN,
                user_id=7,
                call=lambda: assemble_shared_canonical_state(
                    foundation,
                    "7",
                    canonical_state=state,
                    service_name=SERVICE_PLANNING,
                    api_name=API_BUILD_DAILY_STUDY_PLAN,
                )
                or True,
            )
            observe_build_api(
                service_name=SERVICE_READINESS,
                api_name=API_BUILD_READINESS_INTELLIGENCE,
                user_id=7,
                call=lambda: assemble_shared_canonical_state(
                    foundation,
                    "7",
                    canonical_state=state,
                    service_name=SERVICE_READINESS,
                    api_name=API_BUILD_READINESS_INTELLIGENCE,
                )
                or True,
            )
            return {"availability": AVAILABILITY_AVAILABLE}

        return observe_build_api(
            service_name=SERVICE_RECOMMENDATION,
            api_name=API_BUILD_STUDY_INSIGHTS,
            user_id=7,
            call=insight_body,
        )

    after_chain()
    after_ms = (time.perf_counter() - started) * 1000.0
    after_assembled, after_injected = _count_assembles(telemetry)

    assert after_assembled == 1
    assert after_injected == 2
    assert foundation.assemble.call_count == 1
    assert after_ms < before_ms

    # Documented comparison anchors for COMPLETION_REPORT
    assert before_assembled / after_assembled == 3
    assert after_ms <= before_ms * 0.7  # expect ~3x assemble cost reduction
