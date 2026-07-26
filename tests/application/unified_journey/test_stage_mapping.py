"""Stage → Programme I capability mapping tests (P2-MS002)."""

from __future__ import annotations

import pytest

from app.application.unified_journey import (
    CANONICAL_JOURNEY_STAGES,
    SOURCE_ADAPTIVE,
    SOURCE_EVIDENCE,
    SOURCE_RUNTIME_A,
    SOURCE_STRATEGY,
    JourneyStage,
    all_stages_mapped,
    mapping_for_stage,
    primary_subsystem_for_stage,
    stage_mapping_table,
)


def test_every_canonical_stage_is_mapped():
    assert all_stages_mapped() is True
    assert len(stage_mapping_table()) == len(CANONICAL_JOURNEY_STAGES)


def test_daily_mission_maps_to_runtime_a():
    mapping = mapping_for_stage(JourneyStage.DAILY_MISSION)
    assert mapping.primary_subsystem == SOURCE_RUNTIME_A
    capability = mapping.capability.lower()
    assert "mission" in capability or "recommendation" in capability


def test_revision_maps_to_adaptive():
    assert primary_subsystem_for_stage(JourneyStage.REVISION_MODE) == SOURCE_ADAPTIVE


def test_exam_readiness_maps_to_strategy():
    assert primary_subsystem_for_stage(JourneyStage.EXAM_READINESS) == SOURCE_STRATEGY


def test_archive_and_weekly_review_map_to_evidence():
    assert primary_subsystem_for_stage(JourneyStage.LEARNING_ARCHIVE) == SOURCE_EVIDENCE
    assert primary_subsystem_for_stage(JourneyStage.WEEKLY_REVIEW) == SOURCE_EVIDENCE


def test_planning_and_session_map_to_runtime_a():
    assert primary_subsystem_for_stage(JourneyStage.PLANNING) == SOURCE_RUNTIME_A
    assert primary_subsystem_for_stage(JourneyStage.STUDY_SESSION) == SOURCE_RUNTIME_A
    assert (
        primary_subsystem_for_stage(JourneyStage.SESSION_REFLECTION)
        == SOURCE_RUNTIME_A
    )
    assert primary_subsystem_for_stage(JourneyStage.ONBOARDING) == SOURCE_RUNTIME_A


def test_mapping_has_no_duplicate_primary_ownership_confusion():
    """Each stage has exactly one primary subsystem (no dual authority)."""
    for stage in CANONICAL_JOURNEY_STAGES:
        mapping = mapping_for_stage(stage)
        assert mapping.primary_subsystem
        assert mapping.primary_subsystem not in mapping.supporting_subsystems


def test_unknown_stage_raises():
    with pytest.raises(ValueError):
        mapping_for_stage("not_a_stage")
