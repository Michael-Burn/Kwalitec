"""Volume / matrix tests for Student Experience presentation."""

from __future__ import annotations

import pytest

from app.application.student_experience.dto.explanation_snapshot import (
    ExplanationSnapshot,
)
from app.application.student_experience.dto.home_snapshot import (
    HomeSnapshot,
    StartSessionActionSnapshot,
)
from app.application.student_experience.dto.journey_snapshot import (
    JourneySnapshot,
    JourneyTopicSnapshot,
)
from app.application.student_experience.dto.revision_snapshot import (
    RevisionOptionSnapshot,
    RevisionSnapshot,
)
from app.domain.student_experience.experience_workspace import ExperienceSurface
from app.presentation.student.navigation import build_navigation
from app.presentation.student.view_models import (
    format_minutes,
    format_readiness_percent,
    home_vm,
    journey_vm,
    revision_vm,
    shell_vm,
)
from tests.application.student_experience.helpers import (
    FakeAdaptivePort,
    FakeJourneyPort,
    FakeMissionPort,
    FakeTwinPort,
)
from tests.presentation.student.helpers import STUDENT_ROUTES, wire_experience


@pytest.mark.parametrize("days", range(0, 31))
def test_home_countdown_matrix(days):
    snap = HomeSnapshot(
        student_id="s1",
        exam_countdown_days=days,
        greeting="Hi",
    )
    vm = home_vm(snap)
    assert vm.countdown.days == days
    assert vm.countdown.has_countdown is True
    assert vm.countdown.label


@pytest.mark.parametrize("pct", range(0, 101, 5))
def test_journey_progress_matrix(pct):
    snap = JourneySnapshot(
        student_id="s1",
        progress_percent=pct,
        current_topic=JourneyTopicSnapshot("t1", "Topic"),
    )
    vm = journey_vm(snap)
    assert vm.progress_percent == pct
    assert f"{pct}%" in vm.progress_label


@pytest.mark.parametrize("minutes", list(range(0, 121, 5)))
def test_format_minutes_matrix(minutes):
    label = format_minutes(minutes)
    assert isinstance(label, str)
    assert label


@pytest.mark.parametrize("ratio_i", range(0, 21))
def test_readiness_format_matrix(ratio_i):
    ratio = ratio_i / 20
    label = format_readiness_percent(ratio)
    assert label.endswith("%")


@pytest.mark.parametrize("n_alts", range(0, 8))
def test_revision_alternatives_matrix(n_alts):
    alts = tuple(
        RevisionOptionSnapshot(
            option_id=f"r{i}",
            topic_title=f"Alt {i}",
            estimated_study_minutes=10 + i,
        )
        for i in range(n_alts)
    )
    snap = RevisionSnapshot(
        student_id="s1",
        primary=RevisionOptionSnapshot(
            option_id="primary",
            topic_title="Primary",
            is_primary=True,
            estimated_study_minutes=20,
        ),
        alternatives=alts,
        has_revision=True,
        option_count=1 + n_alts,
    )
    vm = revision_vm(snap)
    assert len(vm.alternatives) == n_alts


@pytest.mark.parametrize("surface", list(ExperienceSurface))
def test_shell_surface_matrix(surface):
    shell = shell_vm(active_surface=surface.value, page_title=surface.value.title())
    assert shell.active_surface == surface.value
    assert any(item.active for item in shell.navigation)


@pytest.mark.parametrize("surface", list(ExperienceSurface))
def test_nav_matrix(surface):
    nav = build_navigation(surface)
    assert sum(1 for i in nav if i.active) == 1


@pytest.mark.parametrize(("endpoint", "path"), STUDENT_ROUTES)
@pytest.mark.parametrize("mask", [0, 1, 3, 7])
def test_routes_with_port_masks(student_client, experience_app, endpoint, path, mask):
    wire_experience(
        experience_app,
        student_twin=FakeTwinPort(available=bool(mask & 1)),
        adaptive_decision=FakeAdaptivePort(available=bool(mask & 2)),
        mission=FakeMissionPort(available=bool(mask & 4)),
        learning_journey=FakeJourneyPort(available=True),
    )
    response = student_client.get(path)
    # Even when ports fail, UI should degrade calmly (200 with flash/empty)
    assert response.status_code == 200


@pytest.mark.parametrize("can_start", [True, False])
@pytest.mark.parametrize("enabled", [True, False])
def test_home_cta_enablement_matrix(can_start, enabled):
    snap = HomeSnapshot(
        student_id="s1",
        has_recommendation=True,
        can_start_session=can_start,
        start_session=StartSessionActionSnapshot(
            enabled=enabled,
            can_start=can_start,
            mission_id="m1",
        ),
        explanation=ExplanationSnapshot(why_recommended="Because"),
    )
    vm = home_vm(snap)
    assert vm.primary_cta_enabled is (can_start and enabled)
