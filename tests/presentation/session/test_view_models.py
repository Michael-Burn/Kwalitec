"""View model tests for Learning Session Experience."""

from __future__ import annotations

import pytest

from app.application.session_experience.dto.activity_snapshot import ActivitySnapshot
from app.application.session_experience.dto.completion_snapshot import (
    CompletionSnapshot,
    ReturnHomeActionSnapshot,
)
from app.application.session_experience.dto.overview_snapshot import (
    BeginSessionActionSnapshot,
    OverviewSnapshot,
)
from app.application.session_experience.dto.progress_snapshot import ProgressSnapshot
from app.application.session_experience.dto.reflection_snapshot import (
    ReflectionSnapshot,
)
from app.application.session_experience.facade import SessionFlowSnapshot
from app.domain.session_experience.session_workspace import (
    SessionSurface,
    SessionWorkspace,
)
from app.presentation.session.view_models import (
    FORBIDDEN_LEARNER_TERMS,
    activity_vm,
    completion_vm,
    contains_forbidden_terms,
    overview_vm,
    page_from_flow,
    progress_vm,
    reflection_vm,
)


def test_overview_vm_labels():
    vm = overview_vm(
        OverviewSnapshot(
            experience_session_id="es-1",
            student_id="stu-1",
            session_id="sess-1",
            objective="Strengthen equity method",
            estimated_minutes=30,
            activity_count=3,
            expected_readiness_improvement=0.03,
            can_begin=True,
            begin_action=BeginSessionActionSnapshot(
                can_begin=True, session_id="sess-1"
            ),
        )
    )
    assert "30" in vm.estimated_duration_label
    assert "3" in vm.activity_count_label
    assert vm.begin_enabled


def test_activity_vm_position():
    vm = activity_vm(
        ActivitySnapshot(
            activity_id="a1",
            session_id="sess-1",
            question="Q?",
            activity_index=2,
            activities_total=5,
        )
    )
    assert "2" in vm.position_label and "5" in vm.position_label


def test_progress_vm_percent():
    vm = progress_vm(
        ProgressSnapshot(
            session_id="sess-1",
            progress_percent=40,
            activities_total=5,
            activities_completed=2,
            activities_remaining=3,
            estimated_remaining_minutes=12,
        )
    )
    assert vm.percent == 40
    assert vm.has_progress
    assert "12" in vm.remaining_time_label


def test_reflection_vm():
    vm = reflection_vm(
        ReflectionSnapshot(
            session_id="sess-1",
            key_insight="Influence matters",
            has_insight=True,
            reflection_prompt="What remains unclear?",
        )
    )
    assert vm.has_insight
    assert vm.key_insight


def test_completion_vm():
    vm = completion_vm(
        CompletionSnapshot(
            session_id="sess-1",
            student_id="stu-1",
            time_studied_minutes=25,
            activities_completed=3,
            can_return_home=True,
            return_home=ReturnHomeActionSnapshot(),
            estimated_next_session_minutes=20,
        )
    )
    assert "25" in vm.time_studied_label
    assert "20" in vm.next_session_label


def test_page_from_flow_overview():
    ws = SessionWorkspace.create("sw-1", "stu-1", "sess-1")
    flow = SessionFlowSnapshot(
        workspace=ws,
        surface=SessionSurface.OVERVIEW.value,
        overview=OverviewSnapshot(
            experience_session_id="es-1",
            student_id="stu-1",
            session_id="sess-1",
            can_begin=True,
            begin_action=BeginSessionActionSnapshot(
                can_begin=True, session_id="sess-1", label="Begin Session"
            ),
        ),
        next_surface="activity",
    )
    page = page_from_flow(flow)
    assert page.shell.active_surface == "overview"
    assert page.primary_cta_enabled
    assert page.overview is not None


@pytest.mark.parametrize("term", FORBIDDEN_LEARNER_TERMS)
def test_forbidden_terms_detected(term):
    assert contains_forbidden_terms(f"See the {term} for details")
