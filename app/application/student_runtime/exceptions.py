"""Exceptions for the Student Runtime Coordinator."""

from __future__ import annotations


class StudentRuntimeError(Exception):
    """Base error for Student Runtime composition failures."""


class SessionSpineUnavailable(StudentRuntimeError):  # noqa: N818
    """Session spine cannot start (flag off, missing ports, or enrol gap)."""


class MissionNotAcceptable(StudentRuntimeError):  # noqa: N818
    """Mission cannot be accepted into a Study Session."""


class TopicNotReached(StudentRuntimeError):  # noqa: N818
    """Topic is not yet introduced on the student's sequential path."""


class OpenSessionReplacementRequired(StudentRuntimeError):  # noqa: N818
    """Starting a new sitting would replace the single open-session pointer."""

    def __init__(
        self,
        message: str = "",
        *,
        session_id: str = "",
        topic_id: str = "",
    ) -> None:
        super().__init__(
            message or "unfinished session would be replaced"
        )
        self.session_id = session_id
        self.topic_id = topic_id
