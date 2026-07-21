"""EvidenceMapper — presentation / runtime inputs → LearningSessionOutcome.

Forwards already-captured display and lifecycle facts into an immutable
outcome record. Performs no educational reasoning, diagnosis, or planning.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from application.evidence_capture.learning_session_outcome import (
    CompletionStatus,
    LearningSessionOutcome,
)
from application.session_runtime.session_state import SessionStage, SessionState
from presentation.reflection.reflection_view_model import ReflectionViewModel
from presentation.study_session.session_view_model import StudySessionViewModel


class EvidenceMapper:
    """Map study-session, runtime, and reflection inputs into an outcome."""

    @classmethod
    def map_outcome(
        cls,
        session: StudySessionViewModel | None = None,
        state: SessionState | None = None,
        reflection: ReflectionViewModel | None = None,
        *,
        student_id: str | None = None,
        mission_id: str | None = None,
        session_started: datetime | None = None,
        session_completed: datetime | None = None,
        actual_duration_seconds: int | None = None,
    ) -> LearningSessionOutcome:
        """Build a ``LearningSessionOutcome`` from observational inputs.

        Missing inputs yield empty / unknown fields (null-safe). Duration is
        taken from ``actual_duration_seconds`` when provided; otherwise derived
        from start/complete timestamps when both are present.

        Args:
            session: Optional study-session view model.
            state: Optional session runtime state.
            reflection: Optional reflection view model.
            student_id: Optional learner identity.
            mission_id: Optional mission identity.
            session_started: Optional session start timestamp.
            session_completed: Optional session completion timestamp.
            actual_duration_seconds: Optional observed duration override.

        Returns:
            Immutable ``LearningSessionOutcome`` with forwarded facts only.
        """
        duration = cls._duration_seconds(
            actual_duration_seconds=actual_duration_seconds,
            session_started=session_started,
            session_completed=session_completed,
        )
        return LearningSessionOutcome(
            student_id=_text(student_id),
            mission_id=_text(mission_id),
            session_id=cls._session_id(state=state, reflection=reflection),
            session_started=session_started,
            session_completed=session_completed,
            actual_duration_seconds=duration,
            completion_status=cls._completion_status(
                state=state, reflection=reflection
            ),
            confidence=cls._confidence(reflection),
            difficulty=cls._difficulty(reflection),
            weak_concept=cls._weak_concept(reflection),
            student_notes=cls._student_notes(
                session=session, reflection=reflection
            ),
            reflection_summary=cls._reflection_summary(reflection),
            mission_title=cls._mission_title(
                session=session, state=state, reflection=reflection
            ),
        )

    @classmethod
    def _session_id(
        cls,
        *,
        state: SessionState | None,
        reflection: ReflectionViewModel | None,
    ) -> str:
        from_state = _text(getattr(state, "session_id", None))
        if from_state:
            return from_state
        return _text(getattr(reflection, "session_id", None))

    @classmethod
    def _mission_title(
        cls,
        *,
        session: StudySessionViewModel | None,
        state: SessionState | None,
        reflection: ReflectionViewModel | None,
    ) -> str:
        from_reflection = _text(getattr(reflection, "mission_title", None))
        if from_reflection:
            return from_reflection
        from_state = _text(getattr(state, "mission_title", None))
        if from_state:
            return from_state
        header = getattr(session, "header", None) if session else None
        from_header = _text(getattr(header, "title", None))
        if from_header:
            return from_header
        card = getattr(session, "mission_card", None) if session else None
        return _text(getattr(card, "title", None))

    @classmethod
    def _completion_status(
        cls,
        *,
        state: SessionState | None,
        reflection: ReflectionViewModel | None,
    ) -> CompletionStatus:
        if state is not None:
            if bool(getattr(state, "cancelled", False)):
                return CompletionStatus.CANCELLED
            stage = getattr(state, "stage", None)
            if stage is SessionStage.COMPLETED:
                return CompletionStatus.COMPLETED
            if stage is SessionStage.REFLECTION:
                return CompletionStatus.INCOMPLETE
            if stage is not None:
                return CompletionStatus.INCOMPLETE

        completion = getattr(reflection, "mission_completion", None)
        if completion is not None:
            if bool(getattr(completion, "is_complete", False)):
                return CompletionStatus.COMPLETED
            return CompletionStatus.INCOMPLETE

        return CompletionStatus.UNKNOWN

    @classmethod
    def _confidence(cls, reflection: ReflectionViewModel | None) -> str:
        field = getattr(reflection, "confidence", None)
        if field is None:
            return ""
        scale = getattr(field, "scale", None)
        selected_key = _text(getattr(scale, "selected_key", None))
        if selected_key:
            return selected_key
        return _text(getattr(field, "value_label", None))

    @classmethod
    def _difficulty(cls, reflection: ReflectionViewModel | None) -> str:
        field = getattr(reflection, "difficulty", None)
        if field is None:
            return ""
        scale = getattr(field, "scale", None)
        selected_key = _text(getattr(scale, "selected_key", None))
        if selected_key:
            return selected_key
        return _text(getattr(field, "value_label", None))

    @classmethod
    def _weak_concept(cls, reflection: ReflectionViewModel | None) -> str:
        field = getattr(reflection, "weak_concept", None)
        return _text(getattr(field, "value", None))

    @classmethod
    def _student_notes(
        cls,
        *,
        session: StudySessionViewModel | None,
        reflection: ReflectionViewModel | None,
    ) -> str:
        notes_field = getattr(reflection, "student_notes", None)
        from_reflection = _text(getattr(notes_field, "value", None))
        if from_reflection:
            return from_reflection
        study_notes = getattr(session, "study_notes", None) if session else None
        return _text(getattr(study_notes, "description", None))

    @classmethod
    def _reflection_summary(cls, reflection: ReflectionViewModel | None) -> str:
        summary = getattr(reflection, "reflection_summary", None)
        if summary is None:
            return ""
        lines = getattr(summary, "lines", None) or ()
        joined = " | ".join(
            part for part in (_text(line) for line in lines) if part
        )
        if joined:
            return joined
        detail = _text(getattr(summary, "detail", None))
        if detail:
            return detail
        return _text(getattr(summary, "headline", None))

    @classmethod
    def _duration_seconds(
        cls,
        *,
        actual_duration_seconds: int | None,
        session_started: datetime | None,
        session_completed: datetime | None,
    ) -> int | None:
        if actual_duration_seconds is not None:
            if isinstance(actual_duration_seconds, bool) or not isinstance(
                actual_duration_seconds, int
            ):
                raise ValueError("actual_duration_seconds must be an int or None")
            if actual_duration_seconds < 0:
                raise ValueError("actual_duration_seconds must be >= 0")
            return actual_duration_seconds
        if session_started is None or session_completed is None:
            return None
        delta = session_completed - session_started
        seconds = int(delta.total_seconds())
        if seconds < 0:
            raise ValueError(
                "session_completed must not precede session_started"
            )
        return seconds


def _text(value: Any, *, fallback: str = "") -> str:
    if value is None:
        return fallback
    cleaned = str(value).strip()
    return cleaned if cleaned else fallback
