"""EvidenceCaptureService — record a completed study session as evidence.

Captures observational facts only. Never diagnoses, recommends, prioritises,
plans study, persists, orchestrates learning engines, or invokes AI.
"""

from __future__ import annotations

from datetime import UTC, datetime

from application.errors import ApplicationError
from application.evidence_capture.captured_evidence import CapturedEvidence
from application.evidence_capture.evidence_mapper import EvidenceMapper
from application.evidence_capture.learning_session_outcome import (
    LearningSessionOutcome,
)
from application.session_runtime.session_state import SessionState
from presentation.reflection.reflection_view_model import ReflectionViewModel
from presentation.study_session.session_view_model import StudySessionViewModel

_DEFAULT_PROVENANCE = "study_session_reflection"


class EvidenceCaptureError(ApplicationError):
    """Base error for Learning Evidence Capture failures."""


class EvidenceCaptureService:
    """Capture a study-session outcome as immutable educational evidence.

    Input: ``StudySessionViewModel``, ``SessionState``, ``ReflectionViewModel``
    (plus optional identity / timestamp facts supplied by the caller).

    Output: ``LearningSessionOutcome`` wrapped as ``CapturedEvidence``.
    """

    @classmethod
    def capture(
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
        captured_at: datetime | None = None,
        evidence_id: str | None = None,
        provenance: str | None = None,
    ) -> CapturedEvidence:
        """Record what happened in a study session as ``CapturedEvidence``.

        Timestamps and identities are caller-supplied so capture remains
        replayable and free of wall-clock side effects. When ``captured_at``
        is omitted, ``session_completed`` is used; when both are omitted, a
        fixed UTC epoch sentinel is used for null-safe capture.

        Args:
            session: Optional study-session view model.
            state: Optional session runtime state.
            reflection: Optional reflection view model.
            student_id: Optional learner identity.
            mission_id: Optional mission identity.
            session_started: Optional session start timestamp.
            session_completed: Optional session completion timestamp.
            actual_duration_seconds: Optional observed duration override.
            captured_at: Optional evidence capture timestamp.
            evidence_id: Optional stable evidence identity override.
            provenance: Optional capture-channel attribution.

        Returns:
            Immutable ``CapturedEvidence`` containing the session outcome.
        """
        outcome = EvidenceMapper.map_outcome(
            session,
            state,
            reflection,
            student_id=student_id,
            mission_id=mission_id,
            session_started=session_started,
            session_completed=session_completed,
            actual_duration_seconds=actual_duration_seconds,
        )
        return cls.from_outcome(
            outcome,
            captured_at=captured_at,
            evidence_id=evidence_id,
            provenance=provenance,
        )

    @classmethod
    def from_outcome(
        cls,
        outcome: LearningSessionOutcome,
        *,
        captured_at: datetime | None = None,
        evidence_id: str | None = None,
        provenance: str | None = None,
    ) -> CapturedEvidence:
        """Wrap an existing outcome as timestamped ``CapturedEvidence``.

        Args:
            outcome: Observational session outcome.
            captured_at: Optional capture timestamp.
            evidence_id: Optional stable evidence identity.
            provenance: Optional capture-channel attribution.

        Returns:
            Immutable ``CapturedEvidence``.

        Raises:
            EvidenceCaptureError: When ``outcome`` is missing.
        """
        if outcome is None:
            raise EvidenceCaptureError("outcome is required")

        stamp = cls._resolve_captured_at(
            captured_at=captured_at,
            session_completed=outcome.session_completed,
        )
        identity = (evidence_id or "").strip() or cls._default_evidence_id(
            outcome, stamp
        )
        return CapturedEvidence(
            evidence_id=identity,
            captured_at=stamp,
            outcome=outcome,
            provenance=(provenance or "").strip() or _DEFAULT_PROVENANCE,
        )

    @classmethod
    def _resolve_captured_at(
        cls,
        *,
        captured_at: datetime | None,
        session_completed: datetime | None,
    ) -> datetime:
        if captured_at is not None:
            if not isinstance(captured_at, datetime):
                raise EvidenceCaptureError("captured_at must be a datetime")
            return captured_at
        if session_completed is not None:
            if not isinstance(session_completed, datetime):
                raise EvidenceCaptureError(
                    "session_completed must be a datetime"
                )
            return session_completed
        return datetime(1970, 1, 1, tzinfo=UTC)

    @classmethod
    def _default_evidence_id(
        cls,
        outcome: LearningSessionOutcome,
        captured_at: datetime,
    ) -> str:
        stamp = captured_at.strftime("%Y%m%dT%H%M%S")
        student = _slug(outcome.student_id) or "anon"
        mission = (
            _slug(outcome.mission_id)
            or _slug(outcome.session_id)
            or "session"
        )
        return f"evidence:{student}:{mission}:{stamp}"


def _slug(value: str) -> str:
    cleaned = "".join(ch.lower() if ch.isalnum() else "-" for ch in value)
    cleaned = cleaned.strip("-")
    while "--" in cleaned:
        cleaned = cleaned.replace("--", "-")
    return cleaned
