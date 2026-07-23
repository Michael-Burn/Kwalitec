"""ReflectionPresenter — StudySessionViewModel / SessionState → ReflectionViewModel.

Presentation orchestration only. Assembles Design System chrome for structured
post-session reflection capture. Never diagnoses, recommends, persists,
orchestrates learning, or calls AI.
"""

from __future__ import annotations

from dataclasses import replace
from typing import Any

from application.session_runtime import SessionStage, SessionState
from presentation.design_system import ContainerWidth, PageHeader
from presentation.provenance import ProvenanceMapper
from presentation.reflection.reflection_mapper import ReflectionMapper
from presentation.reflection.reflection_view_model import ReflectionViewModel
from presentation.study_session.session_view_model import StudySessionViewModel

_DEFAULT_HEADER_TITLE = "Reflection"
_DEFAULT_HEADER_DESCRIPTION = (
    "Capture how the session felt — confidence, difficulty, notes, "
    "and anything that still needs practice."
)
_STAGE_LABELS: dict[str, str] = {
    SessionStage.NOT_STARTED.value: "Not started",
    SessionStage.PREPARING.value: "Preparing",
    SessionStage.LEARNING.value: "Learning",
    SessionStage.WORKED_EXAMPLE.value: "Worked example",
    SessionStage.NOTES.value: "Notes",
    SessionStage.REFLECTION.value: "Reflection",
    SessionStage.COMPLETED.value: "Completed",
}


class ReflectionPresenter:
    """Present the structured reflection workspace after a study session."""

    @classmethod
    def present(
        cls,
        session: StudySessionViewModel | None = None,
        state: SessionState | None = None,
        *,
        confidence: str | None = None,
        difficulty: str | None = None,
        weak_concept: str | None = None,
        student_notes: str | None = None,
    ) -> ReflectionViewModel:
        """Map session and runtime inputs into a reflection view model.

        Args:
            session: Optional ``StudySessionViewModel`` providing mission,
                notes, completion, and reflection prompt chrome.
            state: Optional ``SessionState`` for lifecycle posture.
            confidence: Optional already-captured confidence scale key.
            difficulty: Optional already-captured difficulty scale key.
            weak_concept: Optional student-noted weak concept text.
            student_notes: Optional notes override; defaults to session notes.

        Returns:
            Immutable ``ReflectionViewModel`` with null-safe Design System chrome.
        """
        mission_title = cls._mission_title(session=session, state=state)
        stage_label = cls._stage_label(state)
        is_ready = cls._is_ready(state)

        reflection_section = getattr(session, "reflection", None) if session else None
        reflection_prompt = _text(getattr(reflection_section, "description", None))

        objective = getattr(session, "objective", None) if session else None
        mission_objective = _text(getattr(objective, "description", None))

        confidence_field = ReflectionMapper.map_confidence(selected=confidence)
        difficulty_field = ReflectionMapper.map_difficulty(selected=difficulty)
        mission_completion = ReflectionMapper.map_mission_completion(
            session, state
        )
        weak_concept_field = ReflectionMapper.map_weak_concept(
            value=weak_concept,
            mission_objective=mission_objective,
        )
        notes_field = ReflectionMapper.map_student_notes(
            session,
            value=student_notes,
        )
        summary = ReflectionMapper.map_summary(
            confidence=confidence_field,
            mission_completion=mission_completion,
            difficulty=difficulty_field,
            weak_concept=weak_concept_field,
            student_notes=notes_field,
            reflection_prompt=reflection_prompt,
        )
        provenance = ProvenanceMapper.for_reflection(
            summary,
            session=session,
            weak_concept=weak_concept_field.value or None,
        )
        summary = replace(summary, provenance=provenance)
        primary = ReflectionMapper.primary_action(is_ready=is_ready)

        header_description = reflection_prompt or _DEFAULT_HEADER_DESCRIPTION
        header = PageHeader(
            title=_DEFAULT_HEADER_TITLE,
            description=header_description,
            eyebrow=stage_label or "Session",
        )

        return ReflectionViewModel(
            header=header,
            confidence=confidence_field,
            mission_completion=mission_completion,
            difficulty=difficulty_field,
            weak_concept=weak_concept_field,
            student_notes=notes_field,
            reflection_summary=summary,
            primary_button=primary,
            container_width=ContainerWidth.CONTENT,
            session_id=_session_id(state),
            mission_title=mission_title,
            stage_label=stage_label,
            is_ready=is_ready,
            provenance=provenance,
        )

    @classmethod
    def _mission_title(
        cls,
        *,
        session: StudySessionViewModel | None,
        state: SessionState | None,
    ) -> str:
        from_state = _text(getattr(state, "mission_title", None))
        if from_state:
            return from_state
        header = getattr(session, "header", None) if session else None
        from_header = _text(getattr(header, "title", None))
        if from_header:
            return from_header
        card = getattr(session, "mission_card", None) if session else None
        return _text(getattr(card, "title", None), fallback="Today's Session")

    @classmethod
    def _stage_label(cls, state: SessionState | None) -> str:
        if state is None:
            return ""
        stage = getattr(state, "stage", None)
        raw = getattr(stage, "value", stage)
        key = str(raw).strip().lower() if raw is not None else ""
        if key in _STAGE_LABELS:
            return _STAGE_LABELS[key]
        return _humanise(key)

    @classmethod
    def _is_ready(cls, state: SessionState | None) -> bool:
        if state is None:
            return False
        if bool(getattr(state, "paused", False)):
            return False
        if bool(getattr(state, "cancelled", False)):
            return False
        stage = getattr(state, "stage", None)
        return stage in {SessionStage.REFLECTION, SessionStage.COMPLETED}


def _session_id(state: Any) -> str:
    return _text(getattr(state, "session_id", None))


def _text(value: str | None, *, fallback: str = "") -> str:
    if value is None:
        return fallback
    cleaned = str(value).strip()
    return cleaned if cleaned else fallback


def _humanise(value: str) -> str:
    cleaned = value.strip()
    if not cleaned:
        return cleaned
    return cleaned.replace("_", " ").replace("-", " ").strip().capitalize()
