"""Shared helpers for Student Experience domain tests."""

from __future__ import annotations

from app.domain.student_experience.experience_session import (
    ExperienceSession,
    StartSessionAction,
)
from app.domain.student_experience.experience_workspace import (
    ExperienceWorkspace,
)
from app.domain.student_experience.recommendation_explanation import (
    build_explanation,
)


def make_workspace(**kwargs):
    return ExperienceWorkspace.create(
        kwargs.pop("workspace_id", "ws-1"),
        kwargs.pop("student_id", "stu-1"),
        **kwargs,
    )


def make_session(**kwargs):
    return ExperienceSession.create(
        kwargs.pop("experience_session_id", "es-1"),
        kwargs.pop("student_id", "stu-1"),
        **kwargs,
    )


def make_start_action(**kwargs):
    return StartSessionAction.create(**kwargs)


def make_explanation(**kwargs):
    return build_explanation(**kwargs)
