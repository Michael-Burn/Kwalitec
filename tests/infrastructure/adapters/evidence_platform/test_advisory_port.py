"""EvidenceAdvisoryPort + feature-flag isolation tests (P2-MS009)."""

from __future__ import annotations

from app.application.config.v2_flags import resolve_v2_feature_flags
from app.infrastructure.adapters.evidence_platform import (
    CLAIM_ORGANISATION,
    CLASS_DELIVERY_EVENT,
    EvidenceAdvisory,
    EvidenceAdvisoryPort,
    EvidencePlatformAdapter,
    ObservedEvent,
    build_evidence_platform_adapter,
)
from app.infrastructure.adapters.student_experience.composition import (
    build_production_experience,
)
from app.infrastructure.diagnostics.dual_run import build_dual_run_status
from app.services.evidence_advisory_injection import (
    RuntimeAEvidenceAdvisoryInjection,
    build_runtime_a_evidence_advisory_injection,
)


def _event(
    *,
    student_id: str,
    event_type: str,
    observed_at: str,
) -> ObservedEvent:
    return ObservedEvent(
        student_id=student_id,
        event_type=event_type,
        observed_at=observed_at,
        ingested_at=observed_at,
        as_of=observed_at,
        claim_boundary=CLAIM_ORGANISATION,
        evidence_class=CLASS_DELIVERY_EVENT,
        payload_summary={"experience_event": event_type},
    )


def test_evidence_advisory_flag_defaults_off():
    flags = resolve_v2_feature_flags(environ={})
    assert flags.ENABLE_EVIDENCE_ADVISORY is False
    dual = build_dual_run_status(flags=flags)
    assert dual.evidence_advisory is False


def test_evidence_advisory_flag_enables_dual_run_field():
    flags = resolve_v2_feature_flags(
        environ={"KWALITEC_EVIDENCE_ADVISORY": "1"}
    )
    assert flags.ENABLE_EVIDENCE_ADVISORY is True
    dual = build_dual_run_status(flags=flags)
    assert dual.evidence_advisory is True


def test_flag_isolation_from_all_prior_flags():
    advisory_only = resolve_v2_feature_flags(
        environ={"KWALITEC_EVIDENCE_ADVISORY": "1"}
    )
    assert advisory_only.ENABLE_EVIDENCE_ADVISORY is True
    assert advisory_only.ENABLE_EXPERIENCE_FEEDBACK is False
    assert advisory_only.ENABLE_EXPERIENCE_OBSERVATION is False
    assert advisory_only.ENABLE_EXPERIENCE_DIAGNOSTICS is False
    assert advisory_only.ENABLE_EVIDENCE_PLATFORM is False
    assert advisory_only.ENABLE_UNIFIED_JOURNEY is False
    assert advisory_only.ENABLE_STRATEGY_ENGINE is False
    assert advisory_only.ENABLE_DIGITAL_TWIN is False
    assert advisory_only.ENABLE_ADAPTIVE_ENGINE is False

    others_only = resolve_v2_feature_flags(
        environ={
            "KWALITEC_EXPERIENCE_FEEDBACK": "1",
            "KWALITEC_EXPERIENCE_OBSERVATION": "1",
            "KWALITEC_EXPERIENCE_DIAGNOSTICS": "1",
            "KWALITEC_EVIDENCE_PLATFORM": "1",
            "KWALITEC_UNIFIED_JOURNEY": "1",
            "KWALITEC_STRATEGY_ENGINE": "1",
            "KWALITEC_DIGITAL_TWIN": "1",
            "KWALITEC_ADAPTIVE_ENGINE": "1",
        }
    )
    assert others_only.ENABLE_EVIDENCE_ADVISORY is False


def test_adapter_implements_advisory_port():
    adapter = build_evidence_platform_adapter(enabled=True)
    assert adapter is not None
    assert isinstance(adapter, EvidenceAdvisoryPort)
    assert adapter.port_id == "evidence_advisory_port"
    assert adapter.is_available() is True


def test_query_advisory_from_collect_event():
    adapter = build_evidence_platform_adapter(enabled=True)
    assert adapter is not None
    adapter.collect_event(
        _event(
            student_id="42",
            event_type="session_completed",
            observed_at="2026-08-05T10:00:00+00:00",
        )
    )
    adapter.collect_event(
        _event(
            student_id="42",
            event_type="reflection_completed",
            observed_at="2026-08-06T10:00:00+00:00",
        )
    )
    result = adapter.query_advisory(
        "42",
        reporting_period="this_week",
        as_of="2026-08-07T12:00:00+00:00",
    )
    assert result.ok is True
    assert isinstance(result.value, EvidenceAdvisory)
    advisory = result.value
    assert advisory.student_id == "42"
    assert advisory.engagement_summary.study_sessions == 1
    assert advisory.engagement_summary.completed_reflections == 1
    assert "August" in advisory.source_description
    assert advisory.provenance["evidence_summary_id"]


def test_composition_wires_injection_when_flag_on():
    flags_off = resolve_v2_feature_flags(environ={})
    composition_off, _ = build_production_experience(flags=flags_off)
    assert composition_off.evidence_advisory_injection is None

    flags_on = resolve_v2_feature_flags(
        environ={
            "KWALITEC_EVIDENCE_ADVISORY": "1",
            "KWALITEC_EVIDENCE_PLATFORM": "1",
        }
    )
    composition_on, _ = build_production_experience(flags=flags_on)
    assert isinstance(
        composition_on.evidence_advisory_injection,
        RuntimeAEvidenceAdvisoryInjection,
    )
    assert isinstance(composition_on.evidence_platform, EvidencePlatformAdapter)
    assert (
        composition_on.evidence_advisory_injection.port
        is composition_on.evidence_platform
    )


def test_build_injection_respects_enabled_flag():
    assert build_runtime_a_evidence_advisory_injection(enabled=False) is None
    injection = build_runtime_a_evidence_advisory_injection(enabled=True)
    assert isinstance(injection, RuntimeAEvidenceAdvisoryInjection)
