"""Presenter mapping, null-safety, determinism, and immutability (V3-005)."""

from __future__ import annotations

from dataclasses import FrozenInstanceError, replace

import pytest

from application.pipeline import EducationalPipeline, PipelineResult
from application.session_runtime import SessionStage, SessionState
from presentation.design_system import ContainerWidth, PageHeader
from presentation.reflection import (
    ConfidenceLevel,
    DifficultyLevel,
    ReflectionMapper,
    ReflectionPresenter,
    ReflectionViewModel,
)
from presentation.study_session import SessionPresenter, StudySessionViewModel
from tests.education_os.application.pipeline.test_educational_pipeline import (
    make_pipeline_request,
)


@pytest.fixture(scope="module")
def pipeline_result() -> PipelineResult:
    return EducationalPipeline().run(make_pipeline_request())


@pytest.fixture(scope="module")
def study_session(pipeline_result: PipelineResult) -> StudySessionViewModel:
    return SessionPresenter.present(pipeline_result)


@pytest.fixture
def completed_state(study_session: StudySessionViewModel) -> SessionState:
    return SessionState(
        session_id="session-reflection-1",
        mission_title=study_session.header.title,
        stage=SessionStage.COMPLETED,
        sequence=7,
        section_keys=tuple(section.key for section in study_session.sections),
    )


def test_presenter_maps_session_and_state(
    study_session: StudySessionViewModel,
    completed_state: SessionState,
) -> None:
    view = ReflectionPresenter.present(study_session, completed_state)

    assert isinstance(view, ReflectionViewModel)
    assert isinstance(view.header, PageHeader)
    assert view.header.title == "Reflection"
    assert view.mission_title == study_session.header.title
    assert view.session_id == "session-reflection-1"
    assert view.stage_label == "Completed"
    assert view.is_ready is True
    assert view.container_width is ContainerWidth.CONTENT
    assert view.mission_completion.is_complete is True
    assert view.confidence.scale.options
    assert view.difficulty.scale.options
    assert view.weak_concept.prompt
    assert view.student_notes.section.title == "Student notes"
    assert view.reflection_summary.headline == "Reflection summary"
    assert view.primary_button is not None
    assert view.primary_button.label == "Continue to Summary"


def test_presenter_forwards_captured_evidence(
    study_session: StudySessionViewModel,
    completed_state: SessionState,
) -> None:
    view = ReflectionPresenter.present(
        study_session,
        completed_state,
        confidence=ConfidenceLevel.CONFIDENT.value,
        difficulty=DifficultyLevel.HARD.value,
        weak_concept="Conditional probability",
        student_notes="Need another worked example.",
    )

    assert view.confidence.value_label == "Confident"
    assert view.difficulty.value_label == "Hard"
    assert view.weak_concept.value == "Conditional probability"
    assert view.student_notes.value == "Need another worked example."
    assert any("Confident" in line for line in view.reflection_summary.lines)
    assert any("Hard" in line for line in view.reflection_summary.lines)
    assert any(
        "Conditional probability" in line for line in view.reflection_summary.lines
    )


def test_mapper_builds_fields_independently(
    study_session: StudySessionViewModel,
    completed_state: SessionState,
) -> None:
    confidence = ReflectionMapper.map_confidence(
        selected=ConfidenceLevel.MODERATELY.value
    )
    difficulty = ReflectionMapper.map_difficulty(
        selected=DifficultyLevel.ABOUT_RIGHT.value
    )
    completion = ReflectionMapper.map_mission_completion(
        study_session, completed_state
    )
    weak = ReflectionMapper.map_weak_concept(value="Bayes theorem")
    notes = ReflectionMapper.map_student_notes(
        study_session, value="Reviewed formula sheet."
    )
    summary = ReflectionMapper.map_summary(
        confidence=confidence,
        mission_completion=completion,
        difficulty=difficulty,
        weak_concept=weak,
        student_notes=notes,
    )

    assert confidence.value_label == "Moderately confident"
    assert difficulty.value_label == "About right"
    assert completion.is_complete is True
    assert weak.value == "Bayes theorem"
    assert notes.value == "Reviewed formula sheet."
    assert summary.lines
    assert summary.card.title == "Reflection summary"


def test_null_safe_rendering_for_missing_inputs() -> None:
    view = ReflectionPresenter.present(None, None)

    assert view.header.title == "Reflection"
    assert view.header.description
    assert view.mission_title == "Today's Session"
    assert view.session_id == ""
    assert view.stage_label == ""
    assert view.is_ready is False
    assert view.mission_completion.is_complete is False
    assert view.confidence.value_label == ""
    assert view.difficulty.value_label == ""
    assert view.weak_concept.value == ""
    assert view.student_notes.value == ""
    assert view.reflection_summary.detail
    assert view.primary_button is not None
    assert view.primary_button.label == "Return Home"


def test_null_safe_rendering_for_reflection_stage(
    study_session: StudySessionViewModel,
) -> None:
    state = SessionState(
        session_id="session-2",
        mission_title=study_session.header.title,
        stage=SessionStage.REFLECTION,
    )
    view = ReflectionPresenter.present(study_session, state)

    assert view.is_ready is True
    assert view.stage_label == "Reflection"
    assert view.mission_completion.is_complete is True
    assert view.primary_button is not None
    assert view.primary_button.label == "Continue to Summary"


def test_uses_session_study_notes_when_override_absent(
    study_session: StudySessionViewModel,
    completed_state: SessionState,
) -> None:
    view = ReflectionPresenter.present(study_session, completed_state)
    assert view.student_notes.value == study_session.study_notes.description


def test_deterministic_output(
    study_session: StudySessionViewModel,
    completed_state: SessionState,
) -> None:
    first = ReflectionPresenter.present(
        study_session,
        completed_state,
        confidence="confident",
        difficulty="easy",
        weak_concept="Variance",
    )
    second = ReflectionPresenter.present(
        study_session,
        completed_state,
        confidence="confident",
        difficulty="easy",
        weak_concept="Variance",
    )
    assert first == second


def test_view_model_is_immutable(
    study_session: StudySessionViewModel,
    completed_state: SessionState,
) -> None:
    view = ReflectionPresenter.present(study_session, completed_state)

    with pytest.raises(FrozenInstanceError):
        view.mission_title = "mutated"  # type: ignore[misc]

    with pytest.raises(FrozenInstanceError):
        view.header.title = "mutated"  # type: ignore[misc]

    updated = replace(view, mission_title="Override")
    assert updated.mission_title == "Override"
    assert view.mission_title != "Override"


def test_paused_session_is_not_ready(
    study_session: StudySessionViewModel,
) -> None:
    state = SessionState(
        session_id="session-3",
        mission_title=study_session.header.title,
        stage=SessionStage.REFLECTION,
        paused=True,
    )
    view = ReflectionPresenter.present(study_session, state)
    assert view.is_ready is False
    assert view.primary_button is not None
    assert view.primary_button.label == "Return Home"
