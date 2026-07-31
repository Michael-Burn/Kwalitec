"""Exceptions for the Student Runtime Coordinator."""

from __future__ import annotations


class StudentRuntimeError(Exception):
    """Base error for Student Runtime composition failures."""


class SessionSpineUnavailable(StudentRuntimeError):  # noqa: N818
    """Session spine cannot start (flag off, missing ports, or enrol gap)."""


class MissionNotAcceptable(StudentRuntimeError):  # noqa: N818
    """Mission cannot be accepted into a Study Session."""
