"""Navigation integration tests — Unified Student Journey (P2-MS001)."""

from __future__ import annotations

from app.application.unified_journey import (
    PRIMARY_NAV_STAGES,
    JourneyStage,
    stage_for_surface,
)
from app.domain.student_experience.experience_workspace import ExperienceSurface
from app.presentation.student.navigation import (
    build_navigation,
    endpoint_for,
)


def test_feature_navigation_unchanged_when_flag_off():
    nav = build_navigation("home", unified_journey=False)
    assert len(nav) == 7
    labels = [item.label for item in nav]
    assert labels == [
        "Home",
        "Syllabus",
        "Revision",
        "History",
        "Settings",
        "Choose Exam",
        "Help",
    ]
    assert all(item.journey_stage == "" for item in nav)


def test_unified_navigation_reflects_journey_stages():
    nav = build_navigation("home", unified_journey=True)
    labels = [item.label for item in nav]
    assert labels == [
        "Today",
        "Planning",
        "Exam Readiness",
        "Revision",
        "Archive",
        "Onboarding",
        "Help",
    ]
    stage_items = [item for item in nav if item.journey_stage]
    assert len(stage_items) == len(PRIMARY_NAV_STAGES)
    assert {item.journey_stage for item in stage_items} == {
        stage.value for stage in PRIMARY_NAV_STAGES
    }
    # Study Plan is absorbed into Planning — not a competing product link.
    assert "Study Plan" not in labels


def test_unified_navigation_active_stage_from_surface():
    nav = build_navigation(
        ExperienceSurface.REVISION,
        unified_journey=True,
    )
    active = [item for item in nav if item.active]
    assert len(active) == 1
    assert active[0].journey_stage == JourneyStage.REVISION_MODE.value
    assert active[0].endpoint == "student.revision"


def test_unified_navigation_active_stage_from_endpoint():
    nav = build_navigation(
        unified_journey=True,
        active_endpoint="study_plan.index",
    )
    active = [item for item in nav if item.active]
    assert len(active) == 1
    assert active[0].journey_stage == JourneyStage.PLANNING.value


def test_every_major_surface_belongs_to_exactly_one_stage():
    seen: set[JourneyStage] = set()
    for surface in ExperienceSurface:
        stage = stage_for_surface(surface)
        assert stage not in seen
        seen.add(stage)
        # Feature endpoints remain stable for compatibility.
        assert endpoint_for(surface).startswith("student.")


def test_unified_nav_without_system_items():
    nav = build_navigation("home", unified_journey=True, include_system=False)
    assert len(nav) == len(PRIMARY_NAV_STAGES)
    assert all(item.journey_stage for item in nav)
