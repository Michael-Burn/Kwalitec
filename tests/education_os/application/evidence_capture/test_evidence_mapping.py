"""Evidence mapping coverage for Learning Evidence Capture (V3-006)."""

from __future__ import annotations

from application.evidence_capture import (
    CompletionStatus,
    EvidenceMapper,
)
from application.session_runtime import SessionStage, SessionState
from presentation.reflection import ConfidenceLevel, DifficultyLevel
from tests.education_os.application.evidence_capture import (
    fixed_completed,
    fixed_started,
    make_completed_state,
    make_reflection,
    make_session,
)


def test_mapper_forwards_reflection_fields() -> None:
    session = make_session()
    state = make_completed_state(session)
    reflection = make_reflection(
        session,
        state,
        confidence=ConfidenceLevel.MODERATELY.value,
        difficulty=DifficultyLevel.ABOUT_RIGHT.value,
        weak_concept="Bayes theorem",
        student_notes="Reviewed formula sheet.",
    )

    outcome = EvidenceMapper.map_outcome(
        session,
        state,
        reflection,
        student_id="student-ada",
        mission_id="mission-1",
        session_started=fixed_started(),
        session_completed=fixed_completed(),
    )

    assert outcome.confidence == "moderately"
    assert outcome.difficulty == "about_right"
    assert outcome.weak_concept == "Bayes theorem"
    assert outcome.student_notes == "Reviewed formula sheet."
    assert "Moderately confident" in outcome.reflection_summary
    assert "About right" in outcome.reflection_summary
    assert "Bayes theorem" in outcome.reflection_summary


def test_mapper_completion_status_from_runtime_stage() -> None:
    session = make_session()
    reflection = make_reflection(session)

    cancelled = SessionState(
        session_id="sess-cancelled",
        mission_title=session.header.title,
        stage=SessionStage.LEARNING,
        cancelled=True,
        sequence=2,
    )
    assert (
        EvidenceMapper.map_outcome(
            session, cancelled, reflection
        ).completion_status
        is CompletionStatus.CANCELLED
    )

    incomplete = SessionState(
        session_id="sess-incomplete",
        mission_title=session.header.title,
        stage=SessionStage.REFLECTION,
        sequence=6,
    )
    assert (
        EvidenceMapper.map_outcome(
            session, incomplete, reflection
        ).completion_status
        is CompletionStatus.INCOMPLETE
    )

    completed = make_completed_state(session)
    assert (
        EvidenceMapper.map_outcome(
            session, completed, reflection
        ).completion_status
        is CompletionStatus.COMPLETED
    )


def test_mapper_uses_explicit_duration_over_timestamps() -> None:
    outcome = EvidenceMapper.map_outcome(
        make_session(),
        make_completed_state(),
        make_reflection(),
        session_started=fixed_started(),
        session_completed=fixed_completed(),
        actual_duration_seconds=90,
    )
    assert outcome.actual_duration_seconds == 90


def test_mapper_falls_back_to_session_notes_when_reflection_empty() -> None:
    session = make_session()
    state = make_completed_state(session)
    reflection = make_reflection(session, state, student_notes="")

    outcome = EvidenceMapper.map_outcome(session, state, reflection)

    # Empty reflection notes fall through to study-session notes body.
    assert outcome.student_notes == session.study_notes.description
