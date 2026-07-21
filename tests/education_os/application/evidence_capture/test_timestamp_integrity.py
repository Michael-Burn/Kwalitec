"""Timestamp integrity coverage for Learning Evidence Capture (V3-006)."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest

from application.evidence_capture import (
    EvidenceCaptureService,
    EvidenceMapper,
)
from tests.education_os.application.evidence_capture import (
    fixed_captured_at,
    fixed_completed,
    fixed_started,
    make_completed_state,
    make_reflection,
    make_session,
)


def test_duration_derived_from_start_and_complete() -> None:
    started = fixed_started()
    completed = started + timedelta(minutes=12, seconds=30)

    outcome = EvidenceMapper.map_outcome(
        make_session(),
        make_completed_state(),
        make_reflection(),
        session_started=started,
        session_completed=completed,
    )

    assert outcome.actual_duration_seconds == 12 * 60 + 30
    assert outcome.session_started == started
    assert outcome.session_completed == completed


def test_captured_at_falls_back_to_session_completed() -> None:
    evidence = EvidenceCaptureService.capture(
        make_session(),
        make_completed_state(),
        make_reflection(),
        student_id="student-ada",
        mission_id="mission-1",
        session_completed=fixed_completed(),
    )

    assert evidence.captured_at == fixed_completed()


def test_explicit_captured_at_takes_precedence() -> None:
    evidence = EvidenceCaptureService.capture(
        make_session(),
        make_completed_state(),
        make_reflection(),
        session_completed=fixed_completed(),
        captured_at=fixed_captured_at(),
    )

    assert evidence.captured_at == fixed_captured_at()
    assert evidence.outcome.session_completed == fixed_completed()


def test_mapper_rejects_inverted_timestamps_for_duration() -> None:
    with pytest.raises(ValueError, match="session_completed"):
        EvidenceMapper.map_outcome(
            make_session(),
            make_completed_state(),
            make_reflection(),
            session_started=fixed_completed(),
            session_completed=fixed_started(),
        )


def test_timezone_aware_timestamps_are_preserved() -> None:
    started = datetime(2026, 7, 20, 12, 0, 0, tzinfo=UTC)
    completed = datetime(2026, 7, 20, 12, 10, 0, tzinfo=UTC)
    captured = datetime(2026, 7, 20, 12, 10, 5, tzinfo=UTC)

    evidence = EvidenceCaptureService.capture(
        make_session(),
        make_completed_state(),
        make_reflection(),
        session_started=started,
        session_completed=completed,
        captured_at=captured,
    )

    assert evidence.outcome.session_started.tzinfo is UTC
    assert evidence.outcome.session_completed.tzinfo is UTC
    assert evidence.captured_at.tzinfo is UTC
    assert evidence.outcome.actual_duration_seconds == 600
