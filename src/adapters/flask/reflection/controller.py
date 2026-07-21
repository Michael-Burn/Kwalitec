"""ReflectionController — HTTP orchestration for the Reflection Workspace.

Thin application-adapter controller. Invokes the reflection presenter, evidence
capture, and optional evidence update. No educational decisions or AI.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from adapters.flask.dashboard.dependency_provider import AdapterDependencies
from application.evidence_capture import CapturedEvidence, EvidenceCaptureService
from application.session_runtime import SessionState
from presentation.reflection import ReflectionPresenter, ReflectionViewModel
from presentation.study_session import StudySessionViewModel


@dataclass(frozen=True, slots=True)
class ReflectionSubmitResult:
    """Outcome of reflection capture + optional evidence update."""

    view_model: ReflectionViewModel
    captured: CapturedEvidence
    update_result: Any = None


class ReflectionController:
    """Present reflection chrome and capture observational session evidence."""

    def __init__(self, dependencies: AdapterDependencies | None = None) -> None:
        self._dependencies = dependencies or AdapterDependencies()

    def show(
        self,
        session: StudySessionViewModel | None = None,
        state: SessionState | None = None,
        *,
        confidence: str | None = None,
        difficulty: str | None = None,
        weak_concept: str | None = None,
        student_notes: str | None = None,
    ) -> ReflectionViewModel:
        """Present the reflection workspace from session / runtime inputs."""
        return ReflectionPresenter.present(
            session,
            state,
            confidence=confidence,
            difficulty=difficulty,
            weak_concept=weak_concept,
            student_notes=student_notes,
        )

    def capture(
        self,
        session: StudySessionViewModel | None = None,
        state: SessionState | None = None,
        reflection: ReflectionViewModel | None = None,
        *,
        student_id: str | None = None,
        mission_id: str | None = None,
        evidence_id: str | None = None,
        provenance: str | None = None,
    ) -> CapturedEvidence:
        """Capture observational evidence from a completed reflection."""
        return EvidenceCaptureService.capture(
            session,
            state,
            reflection,
            student_id=student_id,
            mission_id=mission_id,
            evidence_id=evidence_id,
            provenance=provenance,
        )

    def submit(
        self,
        session: StudySessionViewModel | None = None,
        state: SessionState | None = None,
        *,
        student_id: str | None = None,
        mission_id: str | None = None,
        evidence_id: str | None = None,
        confidence: str | None = None,
        difficulty: str | None = None,
        weak_concept: str | None = None,
        student_notes: str | None = None,
    ) -> ReflectionSubmitResult:
        """Present, capture, and optionally persist reflection evidence."""
        view_model = self.show(
            session,
            state,
            confidence=confidence,
            difficulty=difficulty,
            weak_concept=weak_concept,
            student_notes=student_notes,
        )
        captured = self.capture(
            session,
            state,
            view_model,
            student_id=student_id,
            mission_id=mission_id,
            evidence_id=evidence_id,
        )
        update_result = self._dependencies.update_evidence(captured)
        return ReflectionSubmitResult(
            view_model=view_model,
            captured=captured,
            update_result=update_result,
        )
