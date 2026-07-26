"""Contract tests — Unified Student Journey Framework (P2-MS001)."""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from app.application.unified_journey import (
    AVAILABILITY_PLACEHOLDER,
    CANONICAL_JOURNEY_STAGES,
    CONTRACT_VERSION,
    PRIMARY_NAV_STAGES,
    SURFACE_TO_STAGE,
    HomePrimaryMission,
    JourneyContext,
    JourneyProgress,
    JourneyStage,
    JourneyState,
    NextBestAction,
    empty_home_primary_mission,
    empty_journey_context,
    empty_journey_progress,
    empty_journey_state,
    empty_next_best_action,
    is_canonical_stage,
    resolve_journey_stage,
    surfaces_have_unique_stages,
)
from app.domain.student_experience.experience_workspace import ExperienceSurface


def test_canonical_stages_match_directive():
    assert tuple(stage.value for stage in CANONICAL_JOURNEY_STAGES) == (
        "onboarding",
        "planning",
        "daily_mission",
        "study_session",
        "session_reflection",
        "weekly_review",
        "revision_mode",
        "exam_readiness",
        "learning_archive",
    )


def test_stage_identifiers_are_immutable_strenum():
    assert isinstance(JourneyStage.DAILY_MISSION, str)
    assert JourneyStage.DAILY_MISSION == "daily_mission"
    assert resolve_journey_stage("exam_readiness") is JourneyStage.EXAM_READINESS
    assert is_canonical_stage("revision_mode") is True
    assert is_canonical_stage("not_a_stage") is False
    with pytest.raises(ValueError):
        resolve_journey_stage("not_a_stage")


def test_journey_state_dto_immutable():
    state = empty_journey_state("student-1")
    assert state.student_id == "student-1"
    assert state.current_stage is JourneyStage.DAILY_MISSION
    assert state.contract_version == CONTRACT_VERSION
    assert state.contract_version.startswith("p2.ms005")
    assert state.availability == AVAILABILITY_PLACEHOLDER
    with pytest.raises(FrozenInstanceError):
        state.student_id = "other"  # type: ignore[misc]


def test_journey_context_is_canonical_presentation_object():
    context = empty_journey_context()
    assert isinstance(context, JourneyContext)
    assert context.contract_version == CONTRACT_VERSION
    assert context.availability == AVAILABILITY_PLACEHOLDER
    with pytest.raises(FrozenInstanceError):
        context.mission_title = "changed"  # type: ignore[misc]
    with pytest.raises(ValueError):
        JourneyContext(source="invented_engine")
    with pytest.raises(ValueError):
        JourneyContext(completion_state="invented")
    with pytest.raises(ValueError):
        JourneyContext(urgency="critical")


def test_next_best_action_and_progress_immutable():
    action = empty_next_best_action()
    progress = empty_journey_progress()
    mission = empty_home_primary_mission()
    assert isinstance(action, NextBestAction)
    assert isinstance(progress, JourneyProgress)
    assert isinstance(mission, HomePrimaryMission)
    with pytest.raises(FrozenInstanceError):
        action.title = "changed"  # type: ignore[misc]
    with pytest.raises(FrozenInstanceError):
        progress.label = "changed"  # type: ignore[misc]
    with pytest.raises(ValueError):
        NextBestAction(source="invented_engine")
    with pytest.raises(ValueError):
        JourneyProgress(ratio=1.5)


def test_journey_state_requires_student_id():
    with pytest.raises(ValueError):
        JourneyState(student_id="")


def test_each_experience_surface_maps_to_unique_stage():
    assert surfaces_have_unique_stages() is True
    assert set(SURFACE_TO_STAGE) == set(ExperienceSurface)
    assert SURFACE_TO_STAGE[ExperienceSurface.HOME] is JourneyStage.DAILY_MISSION
    assert (
        SURFACE_TO_STAGE[ExperienceSurface.JOURNEY]
        is JourneyStage.EXAM_READINESS
    )
    assert (
        SURFACE_TO_STAGE[ExperienceSurface.REVISION]
        is JourneyStage.REVISION_MODE
    )
    assert (
        SURFACE_TO_STAGE[ExperienceSurface.HISTORY]
        is JourneyStage.LEARNING_ARCHIVE
    )
    assert SURFACE_TO_STAGE[ExperienceSurface.PROFILE] is JourneyStage.ONBOARDING


def test_primary_nav_stages_have_unique_endpoints():
    from app.application.unified_journey import endpoint_for_stage

    endpoints = [endpoint_for_stage(stage) for stage in PRIMARY_NAV_STAGES]
    assert len(endpoints) == len(set(endpoints))
