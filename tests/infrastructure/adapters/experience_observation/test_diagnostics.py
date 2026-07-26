"""Health check + diagnostic aggregation tests (P2-MS007)."""

from __future__ import annotations

from dataclasses import dataclass

from app.application.unified_journey import mission_started, session_started
from app.infrastructure.adapters.evidence_platform import ObservedEvent
from app.infrastructure.adapters.experience_observation import (
    CHECK_DI_WIRING,
    CHECK_EVIDENCE_INTAKE,
    CHECK_FEATURE_FLAGS,
    CHECK_PUBLISHER,
    HEALTH_STATUS_OK,
    HEALTH_STATUS_UNAVAILABLE,
    PUBLISH_STATUS_FAILED,
    PUBLISH_STATUS_PUBLISHED,
    PUBLISH_STATUS_SKIPPED,
    ExperienceObservationPublisher,
    ObservationDiagnosticsService,
    build_experience_observation_diagnostics,
    build_pipeline_health_checker,
)


@dataclass
class _FakeEvidence:
    calls: list
    fail: bool = False

    def collect_event(self, event: ObservedEvent):
        if self.fail:
            raise RuntimeError("intake rejected")
        self.calls.append(event)

        @dataclass(frozen=True)
        class _Record:
            evidence_id: str

        return _Record(evidence_id=f"ev-{event.event_type}")


def test_health_checks_when_all_flags_and_wiring_ok():
    sink = _FakeEvidence([])
    publisher = ExperienceObservationPublisher(enabled=True, evidence=sink)
    checker = build_pipeline_health_checker(
        diagnostics_enabled=True,
        observation_flag=True,
        evidence_flag=True,
        publisher=publisher,
        evidence=sink,
    )
    report = checker.evaluate()
    assert report.overall_status == HEALTH_STATUS_OK
    assert report.overall_ok is True
    names = {c.name for c in report.checks}
    assert names == {
        CHECK_PUBLISHER,
        CHECK_EVIDENCE_INTAKE,
        CHECK_FEATURE_FLAGS,
        CHECK_DI_WIRING,
    }
    assert all(c.ok for c in report.checks)


def test_health_checks_surface_missing_publisher():
    checker = build_pipeline_health_checker(
        diagnostics_enabled=True,
        observation_flag=True,
        evidence_flag=False,
        publisher=None,
        evidence=None,
    )
    report = checker.evaluate()
    publisher_check = next(c for c in report.checks if c.name == CHECK_PUBLISHER)
    assert publisher_check.status == HEALTH_STATUS_UNAVAILABLE
    assert publisher_check.ok is False
    assert report.overall_ok is False


def test_di_wiring_degraded_when_evidence_not_bound():
    publisher = ExperienceObservationPublisher(enabled=True, evidence=None)
    checker = build_pipeline_health_checker(
        diagnostics_enabled=True,
        observation_flag=True,
        evidence_flag=True,
        publisher=publisher,
        evidence=_FakeEvidence([]),
    )
    di = next(c for c in checker.evaluate().checks if c.name == CHECK_DI_WIRING)
    assert di.ok is False
    assert "publisher.evidence is None" in di.detail


def test_diagnostic_aggregation_counters_and_dashboard():
    sink = _FakeEvidence([])
    diagnostics = ObservationDiagnosticsService(
        enabled=True,
        observation_flag=True,
        evidence_flag=True,
        publisher=None,
        evidence=sink,
    )
    publisher = ExperienceObservationPublisher(
        enabled=True, evidence=sink, diagnostics=diagnostics
    )
    diagnostics.bind_publisher(publisher)

    published = publisher.publish_journey_event(
        session_started(),
        student_id="42",
        timestamp="2026-07-25T10:00:00+00:00",
        correlation_id="corr-agg",
    )
    assert published.status == PUBLISH_STATUS_PUBLISHED

    sink.fail = True
    failed = publisher.publish_journey_event(
        mission_started(),
        student_id="42",
        timestamp="2026-07-25T10:01:00+00:00",
        correlation_id="corr-fail",
    )
    assert failed.status == PUBLISH_STATUS_FAILED

    skip_pub = ExperienceObservationPublisher(
        enabled=True, evidence=None, diagnostics=diagnostics
    )
    skipped = skip_pub.publish_journey_event(
        session_started(),
        student_id="42",
        timestamp="2026-07-25T10:02:00+00:00",
        correlation_id="corr-skip",
    )
    assert skipped.status == PUBLISH_STATUS_SKIPPED

    counters = diagnostics.counters()
    assert counters.observations_published == 1
    assert counters.observations_accepted == 1
    assert counters.observations_rejected == 1
    assert counters.observations_skipped == 1
    assert counters.journey_events_traced == 3
    assert counters.intake_latency_ms_count >= 1

    lineage = diagnostics.traces_for("corr-agg")
    stages = {t.pipeline_stage for t in lineage}
    assert "journey_event" in stages
    assert "assembled" in stages
    assert "evidence_ack" in stages

    dashboard = diagnostics.dashboard()
    assert dashboard.audience == "internal_ops"
    assert dashboard.influences_student is False
    assert dashboard.diagnostics_enabled is True
    assert "student_id" not in dashboard.to_canonical_dict()["counters"]
    assert dashboard.pipeline_health.publisher_available is True


def test_build_diagnostics_respects_enabled_flag():
    assert build_experience_observation_diagnostics(enabled=False) is None
    service = build_experience_observation_diagnostics(
        enabled=True, observation_flag=True
    )
    assert isinstance(service, ObservationDiagnosticsService)
    assert service.enabled is True
