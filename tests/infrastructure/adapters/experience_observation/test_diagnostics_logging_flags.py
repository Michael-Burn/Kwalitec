"""Logging contracts + feature-flag isolation (P2-MS007)."""

from __future__ import annotations

from dataclasses import dataclass

from app.application.config.v2_flags import resolve_v2_feature_flags
from app.application.unified_journey import session_started
from app.infrastructure.adapters.evidence_platform import ObservedEvent
from app.infrastructure.adapters.experience_observation import (
    ExperienceDiagnosticsLogger,
    ExperienceObservationPublisher,
    ObservationDiagnosticsService,
    build_experience_observation_diagnostics,
)
from app.infrastructure.adapters.student_experience.composition import (
    build_production_experience,
)
from app.infrastructure.diagnostics.dual_run import build_dual_run_status
from app.infrastructure.diagnostics.logging import StructuredLogger
from app.infrastructure.events.registry import EventRegistry
from app.infrastructure.events.types import (
    EXPERIENCE_DIAG_EVENT_TYPES,
    EXPERIENCE_DIAG_EVIDENCE_ACK,
    EXPERIENCE_DIAG_JOURNEY_EVENT,
    EXPERIENCE_DIAG_OBSERVATION_PUBLISHED,
)


@dataclass
class _FakeEvidence:
    calls: list

    def collect_event(self, event: ObservedEvent):
        self.calls.append(event)

        @dataclass(frozen=True)
        class _Record:
            evidence_id: str

        return _Record(evidence_id=f"ev-{event.event_type}")


def test_experience_diagnostics_flag_defaults_off():
    flags = resolve_v2_feature_flags(environ={})
    assert flags.ENABLE_EXPERIENCE_DIAGNOSTICS is False
    dual = build_dual_run_status(flags=flags)
    assert dual.experience_diagnostics is False


def test_experience_diagnostics_flag_enables_dual_run_field():
    flags = resolve_v2_feature_flags(
        environ={"KWALITEC_EXPERIENCE_DIAGNOSTICS": "1"}
    )
    assert flags.ENABLE_EXPERIENCE_DIAGNOSTICS is True
    dual = build_dual_run_status(flags=flags)
    assert dual.experience_diagnostics is True


def test_diagnostics_flag_is_independent_of_observation_and_evidence():
    diag_only = resolve_v2_feature_flags(
        environ={"KWALITEC_EXPERIENCE_DIAGNOSTICS": "1"}
    )
    assert diag_only.ENABLE_EXPERIENCE_DIAGNOSTICS is True
    assert diag_only.ENABLE_EXPERIENCE_OBSERVATION is False
    assert diag_only.ENABLE_EVIDENCE_PLATFORM is False

    obs_only = resolve_v2_feature_flags(
        environ={"KWALITEC_EXPERIENCE_OBSERVATION": "1"}
    )
    assert obs_only.ENABLE_EXPERIENCE_OBSERVATION is True
    assert obs_only.ENABLE_EXPERIENCE_DIAGNOSTICS is False

    all_on = resolve_v2_feature_flags(
        environ={
            "KWALITEC_EXPERIENCE_DIAGNOSTICS": "1",
            "KWALITEC_EXPERIENCE_OBSERVATION": "1",
            "KWALITEC_EVIDENCE_PLATFORM": "1",
        }
    )
    assert all_on.ENABLE_EXPERIENCE_DIAGNOSTICS is True
    assert all_on.ENABLE_EXPERIENCE_OBSERVATION is True
    assert all_on.ENABLE_EVIDENCE_PLATFORM is True


def test_composition_wires_diagnostics_only_when_flag_on():
    flags_off = resolve_v2_feature_flags(environ={})
    composition_off, _ = build_production_experience(flags=flags_off)
    assert composition_off.experience_diagnostics is None

    flags_diag = resolve_v2_feature_flags(
        environ={"KWALITEC_EXPERIENCE_DIAGNOSTICS": "1"}
    )
    composition_diag, _ = build_production_experience(flags=flags_diag)
    assert isinstance(
        composition_diag.experience_diagnostics, ObservationDiagnosticsService
    )
    assert composition_diag.experience_observation is None

    flags_both = resolve_v2_feature_flags(
        environ={
            "KWALITEC_EXPERIENCE_DIAGNOSTICS": "1",
            "KWALITEC_EXPERIENCE_OBSERVATION": "1",
            "KWALITEC_EVIDENCE_PLATFORM": "1",
        }
    )
    composition_both, _ = build_production_experience(flags=flags_both)
    assert composition_both.experience_diagnostics is not None
    assert composition_both.experience_observation is not None
    assert (
        composition_both.experience_observation.diagnostics
        is composition_both.experience_diagnostics
    )


def test_structured_logging_contracts_exclude_pii_and_include_correlation():
    events = EventRegistry()
    structured = StructuredLogger("test.experience_diagnostics")
    log = ExperienceDiagnosticsLogger(
        structured=structured, events=events, enabled=True
    )
    log.log_journey_event(
        correlation_id="corr-log",
        journey_stage="study_session",
        experience_event="session_started",
        trace_id="jtrace-1",
        pipeline_stage="journey_event",
    )
    log.log_observation_published(
        correlation_id="corr-log",
        journey_stage="study_session",
        experience_event="session_started",
        observation_status="published",
        observation_id="expobs-1",
        trace_id="jtrace-2",
        latency_ms=4.2,
    )
    log.log_evidence_ack(
        correlation_id="corr-log",
        experience_event="session_started",
        observation_id="expobs-1",
        evidence_id="ev-1",
        observation_status="published",
        trace_id="jtrace-3",
        latency_ms=4.2,
    )
    assert len(structured.records) == 3
    for record in structured.records:
        assert record["correlation_id"] == "corr-log"
        assert record["influences_student"] is False
        assert "student_id" not in record
        assert "email" not in record

    published_types = {e.event_type for e in events.published()}
    assert EXPERIENCE_DIAG_JOURNEY_EVENT in published_types
    assert EXPERIENCE_DIAG_OBSERVATION_PUBLISHED in published_types
    assert EXPERIENCE_DIAG_EVIDENCE_ACK in published_types
    assert set(EXPERIENCE_DIAG_EVENT_TYPES).issubset(published_types)


def test_logger_strips_student_id_if_accidentally_passed():
    # Direct call path uses _base_fields which strips PII keys.
    from app.infrastructure.adapters.experience_observation.telemetry import (
        _base_fields,
    )

    payload = _base_fields(
        correlation_id="c",
        student_id="should-not-appear",
        email="x@y.z",
        user_id="u1",
    )
    assert "student_id" not in payload
    assert "email" not in payload
    assert "user_id" not in payload


def test_publisher_emits_diagnostics_logs_when_bound():
    events = EventRegistry()
    structured = StructuredLogger("test.publisher.diag")
    diagnostics = ObservationDiagnosticsService(
        enabled=True,
        observation_flag=True,
        evidence_flag=True,
        events=events,
        logger=ExperienceDiagnosticsLogger(
            structured=structured, events=events, enabled=True
        ),
    )
    sink = _FakeEvidence([])
    publisher = ExperienceObservationPublisher(
        enabled=True, evidence=sink, diagnostics=diagnostics
    )
    result = publisher.publish_journey_event(
        session_started(),
        student_id="99",
        timestamp="2026-07-25T12:00:00+00:00",
        correlation_id="corr-pub-log",
    )
    assert result.ok is True
    assert any(
        r.get("message", "").endswith("journey_event") for r in structured.records
    )
    assert any(
        r.get("message", "").endswith("observation_published")
        for r in structured.records
    )
    assert any(
        r.get("message", "").endswith("evidence_ack") for r in structured.records
    )
    # Privacy: student_id never lands in structured records.
    assert all("student_id" not in r for r in structured.records)


def test_disabled_diagnostics_are_noops():
    assert build_experience_observation_diagnostics(enabled=False) is None
    diagnostics = ObservationDiagnosticsService(enabled=False)
    assert diagnostics.record_journey_event(
        experience_event="session_started",
        journey_stage="study_session",
        timestamp="2026-07-25T12:00:00+00:00",
        correlation_id="c",
    ) is None
    publisher = ExperienceObservationPublisher(
        enabled=True, evidence=_FakeEvidence([]), diagnostics=diagnostics
    )
    publisher.publish_journey_event(
        session_started(),
        student_id="1",
        timestamp="2026-07-25T12:00:00+00:00",
        correlation_id="c",
    )
    assert diagnostics.counters().observations_published == 0
    assert len(diagnostics.trace_store) == 0
