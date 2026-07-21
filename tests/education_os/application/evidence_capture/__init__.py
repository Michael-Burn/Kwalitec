"""Shared helpers for Learning Evidence Capture tests (V3-006)."""

from __future__ import annotations

from datetime import UTC, datetime

from application.session_runtime import SessionStage, SessionState
from presentation.reflection import (
    ConfidenceLevel,
    DifficultyLevel,
    ReflectionPresenter,
    ReflectionViewModel,
)
from presentation.study_session import SessionPresenter, StudySessionViewModel


def make_session() -> StudySessionViewModel:
    """Return a deterministic null-safe study session view model."""
    return SessionPresenter.present(None)


def make_completed_state(
    session: StudySessionViewModel | None = None,
    *,
    session_id: str = "session-evidence-1",
) -> SessionState:
    """Return a completed session runtime state."""
    view = session or make_session()
    return SessionState(
        session_id=session_id,
        mission_title=view.header.title,
        stage=SessionStage.COMPLETED,
        sequence=7,
        section_keys=tuple(section.key for section in view.sections),
    )


def make_reflection(
    session: StudySessionViewModel | None = None,
    state: SessionState | None = None,
    *,
    confidence: str | None = ConfidenceLevel.CONFIDENT.value,
    difficulty: str | None = DifficultyLevel.HARD.value,
    weak_concept: str | None = "Conditional probability",
    student_notes: str | None = "Need another worked example.",
) -> ReflectionViewModel:
    """Return a reflection view model with captured evidence fields."""
    view = session or make_session()
    runtime = state or make_completed_state(view)
    return ReflectionPresenter.present(
        view,
        runtime,
        confidence=confidence,
        difficulty=difficulty,
        weak_concept=weak_concept,
        student_notes=student_notes,
    )


def fixed_started() -> datetime:
    return datetime(2026, 7, 20, 14, 0, 0, tzinfo=UTC)


def fixed_completed() -> datetime:
    return datetime(2026, 7, 20, 14, 25, 0, tzinfo=UTC)


def fixed_captured_at() -> datetime:
    return datetime(2026, 7, 20, 14, 25, 30, tzinfo=UTC)
