"""Runtime A Recovery Planner injection point tests (P2-MS010)."""

from __future__ import annotations

from app.infrastructure.adapters.recovery_planner import (
    DisruptionSummary,
    MissedSessionFact,
    RecoveryContext,
    StudyCapacityFact,
    build_study_recovery_planner_adapter,
)
from app.services.recommendation_service import RecommendationService
from app.services.recovery_injection import (
    REASON_CONTEXT_NOT_SUPPLIED,
    REASON_INTEGRATION_ONLY,
    RuntimeARecoveryInjection,
)
from tests.conftest import _make_user


def _context(*, student_id: str) -> RecoveryContext:
    return RecoveryContext(
        recovery_id="rcv-inj",
        reporting_period="this_week",
        disruption_summary=DisruptionSummary(
            summary="1 planned session was not completed.",
            disruption_kind="missed_planned_sessions",
            missed_count=1,
            source_description="Derived from recorded plan vs completion.",
        ),
        missed_sessions=(
            MissedSessionFact(
                session_ref="session-x",
                planned_at="2026-08-05T10:00:00+00:00",
                source_description="Plan ledger session-x",
            ),
        ),
        available_study_capacity=StudyCapacityFact(
            available_minutes=45,
            available_slots=1,
            source_description="Declared remaining capacity.",
        ),
        current_plan_version="plan-v2",
        evidence_provenance={
            "source_service": "test",
            "evidence_refs": ["ev-inj"],
        },
        generated_at="2026-08-07T12:00:00+00:00",
        student_id=student_id,
    )


def test_injection_reads_and_documents_candidate():
    adapter = build_study_recovery_planner_adapter(enabled=True)
    assert adapter is not None
    injection = RuntimeARecoveryInjection(enabled=True, port=adapter)
    candidate = injection.plan_recovery(_context(student_id="7"))
    assert candidate is not None
    assert candidate.advisory_only is True
    record = injection.document_consideration(candidate, student_id="7")
    assert record.considered is True
    assert record.ignored_for_decisions is True
    assert record.advisory_only is True
    assert record.candidate_id == candidate.candidate_id
    assert "strategy_type" in record.fields_considered
    assert record.provenance_refs["recovery_provenance"]["source_service"]
    assert record.reason == REASON_INTEGRATION_ONLY


def test_injection_prepare_without_context_documents_skip():
    injection = RuntimeARecoveryInjection(enabled=True, port=None)
    record = injection.prepare_for_recommendation(99)
    assert record.considered is False
    assert record.ignored_for_decisions is True
    assert record.reason == REASON_CONTEXT_NOT_SUPPLIED
    assert injection.last_consideration is record


def test_recommendation_output_unchanged_with_recovery_injection(ctx):
    """Integration point may document recovery; ranking behaviour unchanged."""
    user = _make_user()
    adapter = build_study_recovery_planner_adapter(enabled=True)
    assert adapter is not None
    injection = RuntimeARecoveryInjection(enabled=True, port=adapter)

    without = RecommendationService.generate_recommendations(user.id, limit=5)
    with_injection = RecommendationService.generate_recommendations(
        user.id, limit=5, recovery_injection=injection
    )
    assert without == with_injection
    assert injection.last_consideration is not None
    assert injection.last_consideration.ignored_for_decisions is True
    assert injection.last_consideration.reason == REASON_CONTEXT_NOT_SUPPLIED


def test_recommendation_unchanged_when_context_supplied(ctx):
    user = _make_user()
    adapter = build_study_recovery_planner_adapter(enabled=True)
    assert adapter is not None
    injection = RuntimeARecoveryInjection(enabled=True, port=adapter)
    context = _context(student_id=str(user.id))

    without = RecommendationService.generate_recommendations(user.id, limit=5)
    # prepare is invoked by generate_recommendations without context; call
    # explicitly then generate to prove candidate presence does not alter output.
    considered = injection.prepare_for_recommendation(user.id, context=context)
    assert considered.considered is True
    assert considered.ignored_for_decisions is True
    with_candidate = RecommendationService.generate_recommendations(
        user.id, limit=5, recovery_injection=injection
    )
    assert without == with_candidate


def test_provenance_preserved_through_injection():
    adapter = build_study_recovery_planner_adapter(enabled=True)
    assert adapter is not None
    injection = RuntimeARecoveryInjection(enabled=True, port=adapter)
    record = injection.prepare_for_recommendation(
        11, context=_context(student_id="11")
    )
    assert record.considered is True
    assert record.advisory_only is True
    assert record.provenance_refs["recovery_id"]
    assert record.provenance_refs["recovery_provenance"]["evidence_provenance"][
        "evidence_refs"
    ] == ["ev-inj"]
    assert "session-x" in record.provenance_refs["recovery_provenance"][
        "missed_session_refs"
    ]
