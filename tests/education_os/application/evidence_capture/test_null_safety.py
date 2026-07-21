"""Null-safety coverage for Learning Evidence Capture (V3-006)."""

from __future__ import annotations

from datetime import UTC, datetime

from application.evidence_capture import (
    CapturedEvidence,
    CompletionStatus,
    EvidenceCaptureService,
    EvidenceMapper,
    LearningSessionOutcome,
)


def test_null_safe_capture_with_missing_inputs() -> None:
    evidence = EvidenceCaptureService.capture(None, None, None)

    assert isinstance(evidence, CapturedEvidence)
    assert isinstance(evidence.outcome, LearningSessionOutcome)
    assert evidence.outcome.student_id == ""
    assert evidence.outcome.mission_id == ""
    assert evidence.outcome.session_id == ""
    assert evidence.outcome.session_started is None
    assert evidence.outcome.session_completed is None
    assert evidence.outcome.actual_duration_seconds is None
    assert evidence.outcome.completion_status is CompletionStatus.UNKNOWN
    assert evidence.outcome.confidence == ""
    assert evidence.outcome.difficulty == ""
    assert evidence.outcome.weak_concept == ""
    assert evidence.outcome.student_notes == ""
    assert evidence.outcome.reflection_summary == ""
    assert evidence.outcome.mission_title == ""
    assert evidence.captured_at == datetime(1970, 1, 1, tzinfo=UTC)
    assert evidence.evidence_id.startswith("evidence:")


def test_null_safe_mapper_with_missing_inputs() -> None:
    outcome = EvidenceMapper.map_outcome(None, None, None)

    assert outcome.completion_status is CompletionStatus.UNKNOWN
    assert outcome.actual_duration_seconds is None
    assert outcome.confidence == ""
    assert outcome.difficulty == ""


def test_blank_identity_strings_normalise_to_empty() -> None:
    outcome = EvidenceMapper.map_outcome(
        None,
        None,
        None,
        student_id="   ",
        mission_id="\t",
    )
    assert outcome.student_id == ""
    assert outcome.mission_id == ""
