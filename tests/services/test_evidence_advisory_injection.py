"""Runtime A Evidence Advisory injection point tests (P2-MS009)."""

from __future__ import annotations

from app.infrastructure.adapters.evidence_platform import (
    CLAIM_ORGANISATION,
    CLASS_DELIVERY_EVENT,
    ObservedEvent,
    build_evidence_platform_adapter,
)
from app.services.evidence_advisory_injection import (
    REASON_INTEGRATION_ONLY,
    RuntimeAEvidenceAdvisoryInjection,
)
from app.services.recommendation_service import RecommendationService
from tests.conftest import _make_user


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


def test_injection_reads_and_documents_advisory():
    adapter = build_evidence_platform_adapter(enabled=True)
    assert adapter is not None
    adapter.collect_event(
        _event(
            student_id="7",
            event_type="session_completed",
            observed_at="2026-08-04T09:00:00+00:00",
        )
    )
    injection = RuntimeAEvidenceAdvisoryInjection(enabled=True, port=adapter)
    advisory = injection.read_advisory(
        "7",
        reporting_period="this_week",
        as_of="2026-08-07T12:00:00+00:00",
    )
    assert advisory is not None
    record = injection.document_consideration(advisory, student_id="7")
    assert record.considered is True
    assert record.ignored_for_decisions is True
    assert record.advisory_id == advisory.advisory_id
    assert "observed_patterns" in record.fields_considered
    assert record.provenance_refs["evidence_summary_id"]
    assert record.source_description == advisory.source_description
    assert record.reason == REASON_INTEGRATION_ONLY


def test_injection_prepare_for_recommendation_documents_without_requiring_port():
    injection = RuntimeAEvidenceAdvisoryInjection(enabled=True, port=None)
    record = injection.prepare_for_recommendation(99)
    assert record.considered is False
    assert record.ignored_for_decisions is True
    assert injection.last_consideration is record


def test_recommendation_output_unchanged_with_advisory_injection(ctx):
    """Integration point may document advisory; ranking behaviour unchanged."""
    user = _make_user()
    adapter = build_evidence_platform_adapter(enabled=True)
    assert adapter is not None
    adapter.collect_event(
        _event(
            student_id=str(user.id),
            event_type="session_completed",
            observed_at="2026-08-05T10:00:00+00:00",
        )
    )
    injection = RuntimeAEvidenceAdvisoryInjection(enabled=True, port=adapter)

    without = RecommendationService.generate_recommendations(user.id, limit=5)
    with_injection = RecommendationService.generate_recommendations(
        user.id, limit=5, advisory_injection=injection
    )

    def _identity(rows: list[dict]) -> list[dict]:
        cleaned = []
        for row in rows:
            item = dict(row)
            item.pop("generated_at", None)
            cleaned.append(item)
        return cleaned

    assert _identity(without) == _identity(with_injection)
    assert injection.last_consideration is not None
    assert injection.last_consideration.ignored_for_decisions is True


def test_provenance_preserved_through_injection():
    adapter = build_evidence_platform_adapter(enabled=True)
    assert adapter is not None
    adapter.collect_event(
        _event(
            student_id="11",
            event_type="session_completed",
            observed_at="2026-08-03T10:00:00+00:00",
        )
    )
    injection = RuntimeAEvidenceAdvisoryInjection(enabled=True, port=adapter)
    record = injection.prepare_for_recommendation(
        11, as_of="2026-08-07T12:00:00+00:00"
    )
    assert record.considered is True
    assert "1–7 August" in record.source_description
    assert record.provenance_refs["evidence_refs"]
    assert record.provenance_refs["evidence_provenance"]["source_service"]
