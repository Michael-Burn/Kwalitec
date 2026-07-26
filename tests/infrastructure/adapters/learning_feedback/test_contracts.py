"""Learning Feedback contract / schema validation tests (EP-003.4)."""

from __future__ import annotations

import pytest

from app.infrastructure.adapters.learning_feedback.contracts import (
    AUTHORITY_LEARNING_FEEDBACK,
    CLAIM_PREFERENCE_JOURNAL,
    CONTRACT_VERSION,
    EVIDENCE_KIND_OBSERVED,
    FEEDBACK_EVENT_RECOMMENDATION_ACCEPTED,
    SOURCE_RECOMMENDATION,
    LearningFeedbackEvent,
    deterministic_feedback_id,
)


def test_learning_feedback_event_is_frozen():
    event = LearningFeedbackEvent(
        feedback_id="lfeed-1",
        timestamp="2026-07-26T10:00:00Z",
        event_type=FEEDBACK_EVENT_RECOMMENDATION_ACCEPTED,
        source_authority=SOURCE_RECOMMENDATION,
        claim_boundary=CLAIM_PREFERENCE_JOURNAL,
        student_id="42",
        payload={"accepted": True},
    )
    with pytest.raises(Exception):
        event.event_type = "mutated"  # type: ignore[misc]


def test_event_rejects_unknown_type_and_source():
    with pytest.raises(ValueError, match="unknown feedback event_type"):
        LearningFeedbackEvent(
            feedback_id="lfeed-1",
            timestamp="2026-07-26T10:00:00Z",
            event_type="mastery_inferred",
            source_authority=SOURCE_RECOMMENDATION,
            claim_boundary=CLAIM_PREFERENCE_JOURNAL,
            student_id="42",
        )
    with pytest.raises(ValueError, match="unknown source_authority"):
        LearningFeedbackEvent(
            feedback_id="lfeed-1",
            timestamp="2026-07-26T10:00:00Z",
            event_type=FEEDBACK_EVENT_RECOMMENDATION_ACCEPTED,
            source_authority="presentation_adapter",
            claim_boundary=CLAIM_PREFERENCE_JOURNAL,
            student_id="42",
        )


def test_event_rejects_forbidden_inference_payload_keys():
    with pytest.raises(ValueError, match="forbidden inference"):
        LearningFeedbackEvent(
            feedback_id="lfeed-1",
            timestamp="2026-07-26T10:00:00Z",
            event_type=FEEDBACK_EVENT_RECOMMENDATION_ACCEPTED,
            source_authority=SOURCE_RECOMMENDATION,
            claim_boundary=CLAIM_PREFERENCE_JOURNAL,
            student_id="42",
            payload={"mastery": 0.9},
        )


def test_evidence_kind_must_be_observed():
    with pytest.raises(ValueError, match="evidence_kind"):
        LearningFeedbackEvent(
            feedback_id="lfeed-1",
            timestamp="2026-07-26T10:00:00Z",
            event_type=FEEDBACK_EVENT_RECOMMENDATION_ACCEPTED,
            source_authority=SOURCE_RECOMMENDATION,
            claim_boundary=CLAIM_PREFERENCE_JOURNAL,
            student_id="42",
            evidence_kind="inferred_conclusion",
        )


def test_canonical_dict_and_deterministic_id():
    payload = {"accepted": True, "recommendation_title": "Review"}
    feedback_id = deterministic_feedback_id(
        student_id="7",
        timestamp="2026-07-26T10:00:00Z",
        event_type=FEEDBACK_EVENT_RECOMMENDATION_ACCEPTED,
        source_authority=SOURCE_RECOMMENDATION,
        claim_boundary=CLAIM_PREFERENCE_JOURNAL,
        payload=payload,
        correlation_id="c1",
    )
    event = LearningFeedbackEvent(
        feedback_id=feedback_id,
        timestamp="2026-07-26T10:00:00Z",
        event_type=FEEDBACK_EVENT_RECOMMENDATION_ACCEPTED,
        source_authority=SOURCE_RECOMMENDATION,
        claim_boundary=CLAIM_PREFERENCE_JOURNAL,
        student_id="7",
        payload=payload,
        correlation_id="c1",
    )
    again = deterministic_feedback_id(
        student_id="7",
        timestamp="2026-07-26T10:00:00Z",
        event_type=FEEDBACK_EVENT_RECOMMENDATION_ACCEPTED,
        source_authority=SOURCE_RECOMMENDATION,
        claim_boundary=CLAIM_PREFERENCE_JOURNAL,
        payload=payload,
        correlation_id="c1",
    )
    assert feedback_id == again
    assert feedback_id.startswith("lfeed-")
    canonical = event.to_canonical_dict()
    assert canonical["authority"] == AUTHORITY_LEARNING_FEEDBACK
    assert canonical["contract_version"] == CONTRACT_VERSION
    assert canonical["evidence_kind"] == EVIDENCE_KIND_OBSERVED
    assert "readiness_score" not in canonical["payload"]
