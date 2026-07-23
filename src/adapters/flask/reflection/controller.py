"""ReflectionController — HTTP orchestration for the Reflection Workspace.

Thin application-adapter controller. Invokes the reflection presenter, evidence
capture, and optional experience refresh cascade. No educational decisions or AI.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from adapters.flask.dashboard.dependency_provider import AdapterDependencies
from application.evidence_capture import CapturedEvidence, EvidenceCaptureService
from application.session_runtime import SessionState
from application.student_experience.integration.models import (
    ExperienceJourneyViewModel,
)
from presentation.reflection import ReflectionPresenter, ReflectionViewModel
from presentation.study_session import StudySessionViewModel


@dataclass(frozen=True, slots=True)
class ReflectionSubmitResult:
    """Outcome of reflection capture + optional evidence / experience update."""

    view_model: ReflectionViewModel
    captured: CapturedEvidence
    update_result: Any = None
    experience: ExperienceJourneyViewModel | None = None


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
        student_id: str | None = None,
    ) -> ReflectionViewModel:
        """Present the reflection workspace from session / runtime inputs."""
        # Warm the request-scoped experience so reflection + follow-on pages
        # share one snapshot (null-safe when identity is missing).
        resolved = (student_id or "").strip()
        if not resolved:
            resolved = self._dependencies.student_id_resolver()
        if resolved:
            self._dependencies.experience_gateway.get(resolved)
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
        """Present, capture, persist evidence, and refresh the experience cascade."""
        resolved = (student_id or "").strip()
        if not resolved:
            resolved = self._dependencies.student_id_resolver()
        view_model = self.show(
            session,
            state,
            confidence=confidence,
            difficulty=difficulty,
            weak_concept=weak_concept,
            student_notes=student_notes,
            student_id=resolved,
        )
        captured = self.capture(
            session,
            state,
            view_model,
            student_id=resolved or None,
            mission_id=mission_id,
            evidence_id=evidence_id,
        )
        update_result = self._dependencies.update_evidence(captured)
        experience = None
        if resolved:
            experience = self._dependencies.experience_gateway.refresh_after_reflection(
                resolved
            )
        return ReflectionSubmitResult(
            view_model=view_model,
            captured=captured,
            update_result=update_result,
            experience=experience,
        )

    def current_experience(
        self, student_id: str | None = None
    ) -> ExperienceJourneyViewModel | None:
        """Expose the request-scoped experience snapshot for page chrome."""
        resolved = (student_id or "").strip()
        if not resolved:
            resolved = self._dependencies.student_id_resolver()
        return self._dependencies.experience_gateway.get(resolved)
