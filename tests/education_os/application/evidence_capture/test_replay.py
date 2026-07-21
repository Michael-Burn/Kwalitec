"""Replay coverage for Learning Evidence Capture (V3-006)."""

from __future__ import annotations

from application.evidence_capture import EvidenceCaptureService
from tests.education_os.application.evidence_capture import (
    fixed_captured_at,
    fixed_completed,
    fixed_started,
    make_completed_state,
    make_reflection,
    make_session,
)


def test_same_inputs_replay_to_identical_evidence() -> None:
    session = make_session()
    state = make_completed_state(session)
    reflection = make_reflection(session, state)
    kwargs = {
        "student_id": "student-ada",
        "mission_id": "mission-bayes-1",
        "session_started": fixed_started(),
        "session_completed": fixed_completed(),
        "captured_at": fixed_captured_at(),
        "evidence_id": "evidence:replay-fixed",
    }

    first = EvidenceCaptureService.capture(
        session, state, reflection, **kwargs
    )
    second = EvidenceCaptureService.capture(
        session, state, reflection, **kwargs
    )

    assert first == second
    assert first.evidence_id == second.evidence_id
    assert first.outcome == second.outcome
    assert first.captured_at == second.captured_at


def test_repeated_capture_is_stable_across_many_runs() -> None:
    session = make_session()
    state = make_completed_state(session)
    reflection = make_reflection(session, state)
    kwargs = {
        "student_id": "student-ada",
        "mission_id": "mission-1",
        "session_started": fixed_started(),
        "session_completed": fixed_completed(),
        "actual_duration_seconds": 1500,
        "captured_at": fixed_captured_at(),
    }

    captures = [
        EvidenceCaptureService.capture(session, state, reflection, **kwargs)
        for _ in range(20)
    ]
    assert all(item == captures[0] for item in captures)


def test_default_evidence_id_is_deterministic_from_facts() -> None:
    session = make_session()
    state = make_completed_state(session, session_id="session-evidence-1")
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

    assert evidence.evidence_id == (
        "evidence:student-ada:mission-bayes-1:20260720T142530"
    )
