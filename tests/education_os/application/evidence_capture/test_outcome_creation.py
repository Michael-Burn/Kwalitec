"""Outcome creation coverage for Learning Evidence Capture (V3-006)."""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from application.evidence_capture import (
    CapturedEvidence,
    CompletionStatus,
    EvidenceCaptureService,
    LearningSessionOutcome,
)
from tests.education_os.application.evidence_capture import (
    fixed_captured_at,
    fixed_completed,
    fixed_started,
    make_completed_state,
    make_reflection,
    make_session,
)


def test_outcome_creation_from_session_inputs() -> None:
    session = make_session()
    state = make_completed_state(session)
    reflection = make_reflection(session, state)

    evidence = EvidenceCaptureService.capture(
        session,
        state,
        reflection,
        student_id="student-ada",
        mission_id="mission-bayes-1",
        session_started=fixed_started(),
        session_completed=fixed_completed(),
        captured_at=fixed_captured_at(),
    )

    assert isinstance(evidence, CapturedEvidence)
    outcome = evidence.outcome
    assert isinstance(outcome, LearningSessionOutcome)
    assert outcome.student_id == "student-ada"
    assert outcome.mission_id == "mission-bayes-1"
    assert outcome.session_id == "session-evidence-1"
    assert outcome.session_started == fixed_started()
    assert outcome.session_completed == fixed_completed()
    assert outcome.actual_duration_seconds == 25 * 60
    assert outcome.completion_status is CompletionStatus.COMPLETED
    assert outcome.confidence == "confident"
    assert outcome.difficulty == "hard"
    assert outcome.weak_concept == "Conditional probability"
    assert outcome.student_notes == "Need another worked example."
    assert "Confident" in outcome.reflection_summary
    assert outcome.mission_title == session.header.title
    assert evidence.captured_at == fixed_captured_at()
    assert evidence.provenance == "study_session_reflection"
    assert evidence.evidence_id.startswith("evidence:")


def test_outcome_rejects_negative_duration() -> None:
    with pytest.raises(ValueError, match="actual_duration_seconds"):
        LearningSessionOutcome(
            student_id="s1",
            mission_id="m1",
            session_id="sess-1",
            session_started=None,
            session_completed=None,
            actual_duration_seconds=-1,
            completion_status=CompletionStatus.UNKNOWN,
            confidence="",
            difficulty="",
            weak_concept="",
            student_notes="",
            reflection_summary="",
        )


def test_outcome_rejects_inverted_timestamps() -> None:
    with pytest.raises(ValueError, match="session_completed"):
        LearningSessionOutcome(
            student_id="s1",
            mission_id="m1",
            session_id="sess-1",
            session_started=fixed_completed(),
            session_completed=fixed_started(),
            actual_duration_seconds=None,
            completion_status=CompletionStatus.UNKNOWN,
            confidence="",
            difficulty="",
            weak_concept="",
            student_notes="",
            reflection_summary="",
        )


def test_outcome_and_evidence_are_immutable() -> None:
    evidence = EvidenceCaptureService.capture(
        make_session(),
        make_completed_state(),
        make_reflection(),
        student_id="student-ada",
        mission_id="mission-1",
        session_started=fixed_started(),
        session_completed=fixed_completed(),
        captured_at=fixed_captured_at(),
    )

    with pytest.raises(FrozenInstanceError):
        evidence.outcome.confidence = "mutated"  # type: ignore[misc]
    with pytest.raises(FrozenInstanceError):
        evidence.evidence_id = "mutated"  # type: ignore[misc]
