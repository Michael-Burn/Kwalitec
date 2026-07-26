"""RecoveryContext / RecoveryPlanCandidate contract tests (P2-MS010)."""

from __future__ import annotations

import pytest

from app.infrastructure.adapters.recovery_planner.contracts import (
    AUTHORITY_RECOVERY_PLANNER,
    RECOVERY_VERSION,
    STRATEGY_STRUCTURAL_PLACEHOLDER,
    DisruptionSummary,
    MissedSessionFact,
    RecoveryContext,
    RecoveryPlanCandidate,
    StudyCapacityFact,
)


def test_recovery_context_is_frozen():
    context = RecoveryContext(
        recovery_id="rcv-test",
        reporting_period="this_week",
        generated_at="2026-08-07T12:00:00+00:00",
        student_id="42",
    )
    with pytest.raises(Exception):
        context.recovery_id = "mutated"  # type: ignore[misc]


def test_recovery_context_requires_traceable_fields():
    context = RecoveryContext(
        recovery_id="rcv-1",
        reporting_period="this_week",
        disruption_summary=DisruptionSummary(
            summary="2 planned sessions were not completed.",
            disruption_kind="missed_planned_sessions",
            missed_count=2,
            source_description="Derived from recorded plan vs completion.",
        ),
        missed_sessions=(
            MissedSessionFact(
                session_ref="session-1",
                planned_at="2026-08-03T09:00:00+00:00",
                status="missed",
                source_description="Plan ledger session-1",
            ),
            MissedSessionFact(
                session_ref="session-2",
                planned_at="2026-08-05T09:00:00+00:00",
                status="missed",
                source_description="Plan ledger session-2",
            ),
        ),
        available_study_capacity=StudyCapacityFact(
            available_minutes=90,
            available_slots=2,
            source_description="Declared remaining capacity this week.",
        ),
        current_plan_version="plan-v3",
        evidence_provenance={
            "source_service": "caller",
            "evidence_refs": ["ev-1"],
        },
        generated_at="2026-08-07T12:00:00+00:00",
        student_id="42",
    )
    payload = context.to_canonical_dict()
    assert payload["recovery_id"] == "rcv-1"
    assert payload["authority"] == AUTHORITY_RECOVERY_PLANNER
    assert payload["recovery_version"] == RECOVERY_VERSION
    assert payload["disruption_summary"]["missed_count"] == 2
    assert payload["missed_sessions"][0]["session_ref"] == "session-1"
    assert payload["available_study_capacity"]["available_minutes"] == 90
    assert payload["current_plan_version"] == "plan-v3"
    assert "evidence_provenance" in payload
    assert context.serialize() == RecoveryContext(**{
        k: getattr(context, k)
        for k in (
            "recovery_id",
            "reporting_period",
            "disruption_summary",
            "missed_sessions",
            "available_study_capacity",
            "current_plan_version",
            "evidence_provenance",
            "generated_at",
            "student_id",
            "authority",
            "availability",
            "unavailable_reason",
            "recovery_version",
        )
    }).serialize()


def test_recovery_plan_candidate_is_frozen_and_advisory_only():
    candidate = RecoveryPlanCandidate(
        candidate_id="rcv-cand-1",
        strategy_type=STRATEGY_STRUCTURAL_PLACEHOLDER,
        affected_period="this_week",
        rationale="Placeholder only.",
        provenance={"source_service": "study_recovery_planner"},
        advisory_only=False,  # coerced to True
        recovery_id="rcv-1",
        student_id="42",
        generated_at="2026-08-07T12:00:00+00:00",
    )
    assert candidate.advisory_only is True
    with pytest.raises(Exception):
        candidate.candidate_id = "mutated"  # type: ignore[misc]
    payload = candidate.to_canonical_dict()
    assert payload["advisory_only"] is True
    assert payload["strategy_type"] == STRATEGY_STRUCTURAL_PLACEHOLDER
    assert payload["provenance"]["source_service"] == "study_recovery_planner"


def test_missed_session_requires_ref():
    with pytest.raises(ValueError, match="session_ref"):
        MissedSessionFact(session_ref="")


def test_study_capacity_rejects_negative():
    with pytest.raises(ValueError):
        StudyCapacityFact(available_minutes=-1)


def test_no_recommendation_fields_on_context_or_candidate():
    forbidden = {
        "recommendation",
        "next_action",
        "mastery",
        "prediction",
        "score",
        "suggested_topic",
        "optimised_schedule",
    }
    assert set(RecoveryContext.__dataclass_fields__).isdisjoint(forbidden)
    assert set(RecoveryPlanCandidate.__dataclass_fields__).isdisjoint(forbidden)
