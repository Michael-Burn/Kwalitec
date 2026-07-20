"""Shared helpers for Learning Session Experience domain tests."""

from __future__ import annotations

from app.domain.session_experience.activity_projection import ActivityProjection
from app.domain.session_experience.completion_projection import CompletionProjection
from app.domain.session_experience.learning_session import (
    BeginSessionAction,
    LearningSession,
)
from app.domain.session_experience.reflection_projection import ReflectionProjection
from app.domain.session_experience.session_progress import SessionProgress
from app.domain.session_experience.session_workspace import SessionWorkspace


def make_workspace(**kwargs):
    return SessionWorkspace.create(
        kwargs.pop("workspace_id", "sw-1"),
        kwargs.pop("student_id", "stu-1"),
        kwargs.pop("session_id", "sess-1"),
        **kwargs,
    )


def make_session(**kwargs):
    return LearningSession.create(
        kwargs.pop("experience_session_id", "es-1"),
        kwargs.pop("student_id", "stu-1"),
        kwargs.pop("session_id", "sess-1"),
        **kwargs,
    )


def make_begin_action(**kwargs):
    return BeginSessionAction.create(**kwargs)


def make_progress(**kwargs):
    return SessionProgress.create(kwargs.pop("session_id", "sess-1"), **kwargs)


def make_activity(**kwargs):
    return ActivityProjection.create(
        kwargs.pop("activity_id", "act-1"),
        kwargs.pop("session_id", "sess-1"),
        **kwargs,
    )


def make_reflection(**kwargs):
    return ReflectionProjection.create(kwargs.pop("session_id", "sess-1"), **kwargs)


def make_completion(**kwargs):
    return CompletionProjection.create(
        kwargs.pop("session_id", "sess-1"),
        kwargs.pop("student_id", "stu-1"),
        **kwargs,
    )
