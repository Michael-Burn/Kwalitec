"""Aggregation + confidence + provenance tests (EP-004.1)."""

from __future__ import annotations

from app.infrastructure.adapters.learning_feedback.contracts import (
    CLAIM_PLAN_INTERACTION,
    CLAIM_PREFERENCE_JOURNAL,
    CLAIM_STUDY_HABIT_SIGNAL,
    FEEDBACK_EVENT_PLAN_COMPLETED,
    FEEDBACK_EVENT_RECOMMENDATION_ACCEPTED,
    FEEDBACK_EVENT_RECOMMENDATION_DISMISSED,
    FEEDBACK_EVENT_RECOVERY_APPLIED,
    FEEDBACK_EVENT_REVISION_ADHERED,
    FEEDBACK_EVENT_REVISION_DEFERRED,
    FEEDBACK_EVENT_SESSION_MISSED,
    FEEDBACK_EVENT_STUDY_CONSISTENCY,
    SOURCE_PLANNING,
    SOURCE_READINESS,
    SOURCE_RECOMMENDATION,
    LearningFeedbackEvent,
    deterministic_feedback_id,
)
from app.infrastructure.adapters.personal_learning_profile import (
    ATTR_CONSISTENCY_TREND,
    ATTR_PLANNING_COMPLETION_RATE,
    ATTR_PREFERRED_SESSION_DURATION,
    ATTR_PREFERRED_STUDY_WINDOWS,
    ATTR_RECOMMENDATION_RESPONSIVENESS,
    ATTR_RECOVERY_EFFECTIVENESS,
    ATTR_REVISION_ADHERENCE,
    KIND_DERIVED_INDICATOR,
    KIND_OBSERVED_FACT,
    KIND_UNSUPPORTED,
    STATUS_AVAILABLE,
    STATUS_UNSUPPORTED,
    PersonalLearningProfileAggregator,
)


def _event(
    *,
    student_id: str,
    event_type: str,
    source: str,
    claim: str,
    payload: dict,
    timestamp: str,
    correlation_id: str = "c1",
) -> LearningFeedbackEvent:
    feedback_id = deterministic_feedback_id(
        student_id=student_id,
        timestamp=timestamp,
        event_type=event_type,
        source_authority=source,
        claim_boundary=claim,
        payload=payload,
        correlation_id=correlation_id,
    )
    return LearningFeedbackEvent(
        feedback_id=feedback_id,
        timestamp=timestamp,
        event_type=event_type,
        source_authority=source,
        claim_boundary=claim,
        student_id=student_id,
        payload=payload,
        correlation_id=correlation_id,
    )


def test_aggregate_empty_marks_unsupported_and_unavailable():
    profile = PersonalLearningProfileAggregator().aggregate(
        student_id="1",
        events=[],
        as_of="2026-07-26T10:00:00Z",
    )
    assert profile.evidence_event_count == 0
    duration = profile.get(ATTR_PREFERRED_SESSION_DURATION)
    windows = profile.get(ATTR_PREFERRED_STUDY_WINDOWS)
    assert duration is not None and duration.kind == KIND_UNSUPPORTED
    assert windows is not None and windows.status == STATUS_UNSUPPORTED
    responsiveness = profile.get(ATTR_RECOMMENDATION_RESPONSIVENESS)
    assert responsiveness is not None
    assert responsiveness.status == "unavailable"


def test_declared_session_minutes_is_observed_fact():
    profile = PersonalLearningProfileAggregator().aggregate(
        student_id="1",
        events=[],
        declared_session_minutes=45,
        as_of="2026-07-26T10:00:00Z",
    )
    attr = profile.get(ATTR_PREFERRED_SESSION_DURATION)
    assert attr is not None
    assert attr.kind == KIND_OBSERVED_FACT
    assert attr.status == STATUS_AVAILABLE
    assert attr.value == {"declared_session_minutes": 45}
    assert attr.confidence == 1.0


def test_recommendation_responsiveness_and_provenance():
    events = [
        _event(
            student_id="2",
            event_type=FEEDBACK_EVENT_RECOMMENDATION_ACCEPTED,
            source=SOURCE_RECOMMENDATION,
            claim=CLAIM_PREFERENCE_JOURNAL,
            payload={"accepted": True},
            timestamp="2026-07-26T09:00:00Z",
            correlation_id="a",
        ),
        _event(
            student_id="2",
            event_type=FEEDBACK_EVENT_RECOMMENDATION_DISMISSED,
            source=SOURCE_RECOMMENDATION,
            claim=CLAIM_PREFERENCE_JOURNAL,
            payload={"accepted": False},
            timestamp="2026-07-26T09:05:00Z",
            correlation_id="b",
        ),
        _event(
            student_id="2",
            event_type=FEEDBACK_EVENT_RECOMMENDATION_ACCEPTED,
            source=SOURCE_RECOMMENDATION,
            claim=CLAIM_PREFERENCE_JOURNAL,
            payload={"accepted": True},
            timestamp="2026-07-26T09:10:00Z",
            correlation_id="c",
        ),
    ]
    profile = PersonalLearningProfileAggregator().aggregate(
        student_id="2",
        events=events,
        as_of="2026-07-26T10:00:00Z",
    )
    attr = profile.get(ATTR_RECOMMENDATION_RESPONSIVENESS)
    assert attr is not None
    assert attr.kind == KIND_DERIVED_INDICATOR
    assert attr.value["accept_rate"] == 0.6667
    assert attr.sample_size == 3
    assert attr.confidence == 0.3
    assert len(attr.evidence_refs) == 3
    assert all(r.feedback_id for r in attr.evidence_refs)
    assert "mastery" not in attr.value
    assert attr.claim_boundary == "preference_summary"


def test_consistency_trend_direction():
    events = [
        _event(
            student_id="3",
            event_type=FEEDBACK_EVENT_STUDY_CONSISTENCY,
            source=SOURCE_READINESS,
            claim=CLAIM_STUDY_HABIT_SIGNAL,
            payload={"current_streak": 2},
            timestamp="2026-07-24T10:00:00Z",
            correlation_id="s1",
        ),
        _event(
            student_id="3",
            event_type=FEEDBACK_EVENT_STUDY_CONSISTENCY,
            source=SOURCE_READINESS,
            claim=CLAIM_STUDY_HABIT_SIGNAL,
            payload={"current_streak": 5},
            timestamp="2026-07-25T10:00:00Z",
            correlation_id="s2",
        ),
    ]
    profile = PersonalLearningProfileAggregator().aggregate(
        student_id="3",
        events=events,
        as_of="2026-07-26T10:00:00Z",
    )
    attr = profile.get(ATTR_CONSISTENCY_TREND)
    assert attr is not None
    assert attr.value["direction"] == "increasing"
    assert attr.value["latest_streak"] == 5


def test_revision_and_planning_and_recovery_rates():
    events = [
        _event(
            student_id="4",
            event_type=FEEDBACK_EVENT_RECOVERY_APPLIED,
            source=SOURCE_PLANNING,
            claim=CLAIM_PLAN_INTERACTION,
            payload={"recovery_mode": True},
            timestamp="2026-07-26T08:00:00Z",
            correlation_id="r1",
        ),
        _event(
            student_id="4",
            event_type=FEEDBACK_EVENT_PLAN_COMPLETED,
            source=SOURCE_PLANNING,
            claim=CLAIM_PLAN_INTERACTION,
            payload={"mission_id": 1},
            timestamp="2026-07-26T09:00:00Z",
            correlation_id="p1",
        ),
        _event(
            student_id="4",
            event_type=FEEDBACK_EVENT_REVISION_ADHERED,
            source=SOURCE_PLANNING,
            claim=CLAIM_PLAN_INTERACTION,
            payload={"adhered": True},
            timestamp="2026-07-26T09:01:00Z",
            correlation_id="rev1",
        ),
        _event(
            student_id="4",
            event_type=FEEDBACK_EVENT_REVISION_DEFERRED,
            source=SOURCE_PLANNING,
            claim=CLAIM_PLAN_INTERACTION,
            payload={"adhered": False},
            timestamp="2026-07-26T09:02:00Z",
            correlation_id="rev2",
        ),
        _event(
            student_id="4",
            event_type=FEEDBACK_EVENT_SESSION_MISSED,
            source=SOURCE_PLANNING,
            claim="observed_behaviour",
            payload={"mission_missed_count": 1},
            timestamp="2026-07-26T07:00:00Z",
            correlation_id="m1",
        ),
    ]
    profile = PersonalLearningProfileAggregator().aggregate(
        student_id="4",
        events=events,
        as_of="2026-07-26T10:00:00Z",
    )
    recovery = profile.get(ATTR_RECOVERY_EFFECTIVENESS)
    revision = profile.get(ATTR_REVISION_ADHERENCE)
    planning = profile.get(ATTR_PLANNING_COMPLETION_RATE)
    assert recovery is not None
    assert recovery.value["follow_through_rate"] == 1.0
    assert any("not proof" in lim.lower() for lim in recovery.limitations)
    assert revision is not None
    assert revision.value["adherence_rate"] == 0.5
    assert planning is not None
    assert planning.value["plan_completed_count"] == 1
    assert planning.value["completion_rate"] == 0.5


def test_aggregate_filters_other_students():
    events = [
        _event(
            student_id="other",
            event_type=FEEDBACK_EVENT_RECOMMENDATION_ACCEPTED,
            source=SOURCE_RECOMMENDATION,
            claim=CLAIM_PREFERENCE_JOURNAL,
            payload={"accepted": True},
            timestamp="2026-07-26T09:00:00Z",
        ),
    ]
    profile = PersonalLearningProfileAggregator().aggregate(
        student_id="5",
        events=events,
        as_of="2026-07-26T10:00:00Z",
    )
    assert profile.evidence_event_count == 0


def test_identical_evidence_yields_identical_serialization():
    events = [
        _event(
            student_id="6",
            event_type=FEEDBACK_EVENT_PLAN_COMPLETED,
            source=SOURCE_PLANNING,
            claim=CLAIM_PLAN_INTERACTION,
            payload={"mission_id": 9},
            timestamp="2026-07-26T09:00:00Z",
        ),
    ]
    agg = PersonalLearningProfileAggregator()
    a = agg.aggregate(
        student_id="6", events=events, as_of="2026-07-26T10:00:00Z"
    )
    b = agg.aggregate(
        student_id="6", events=events, as_of="2026-07-26T10:00:00Z"
    )
    assert a.serialize() == b.serialize()
