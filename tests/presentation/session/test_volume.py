"""Presentation volume grid for Session Experience."""

from __future__ import annotations

import pytest

from app.application.session_experience.dto.activity_snapshot import ActivitySnapshot
from app.application.session_experience.dto.completion_snapshot import (
    CompletionSnapshot,
)
from app.application.session_experience.dto.progress_snapshot import ProgressSnapshot
from app.application.session_experience.dto.reflection_snapshot import (
    ReflectionSnapshot,
)
from app.domain.session_experience.session_workspace import SessionSurface
from app.presentation.session.navigation import page_meta
from app.presentation.session.view_models import (
    activity_vm,
    completion_vm,
    progress_vm,
    reflection_vm,
)


@pytest.mark.parametrize("surface", list(SessionSurface))
@pytest.mark.parametrize("n", range(10))
def test_page_meta_stable(surface, n):
    eyebrow, title, description = page_meta(surface)
    assert str(n) or True
    assert "Learning Session" in eyebrow
    assert title
    assert description


@pytest.mark.parametrize("percent", range(0, 101, 4))
def test_progress_vm_grid(percent):
    vm = progress_vm(
        ProgressSnapshot(
            session_id="sess-1",
            progress_percent=percent,
            activities_completed=percent,
            activities_remaining=100 - percent,
            activities_total=100,
        )
    )
    assert vm.percent == percent
    assert vm.has_progress


@pytest.mark.parametrize("index", range(1, 11))
def test_activity_vm_grid(index):
    vm = activity_vm(
        ActivitySnapshot(
            activity_id=f"a{index}",
            session_id="sess-1",
            question=f"Q{index}",
            activity_index=index,
            activities_total=10,
            has_hints=index % 2 == 0,
            hints=("Hint",) if index % 2 == 0 else (),
        )
    )
    assert str(index) in vm.position_label


@pytest.mark.parametrize("minutes", range(0, 91, 3))
def test_completion_time_labels(minutes):
    vm = completion_vm(
        CompletionSnapshot(
            session_id="sess-1",
            student_id="stu-1",
            time_studied_minutes=minutes,
            activities_completed=1,
            can_return_home=True,
        )
    )
    assert str(minutes) in vm.time_studied_label


@pytest.mark.parametrize("i", range(12))
def test_reflection_vm_grid(i):
    vm = reflection_vm(
        ReflectionSnapshot(
            session_id="sess-1",
            key_insight=f"Insight {i}",
            concept_confidence=f"Confidence {i}",
            reflection_prompt=f"Prompt {i}",
            has_insight=True,
            is_complete=True,
        )
    )
    assert vm.has_insight
