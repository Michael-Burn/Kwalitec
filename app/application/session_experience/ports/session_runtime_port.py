"""Session Runtime port — Learning Session execution collaboration.

Session Experience never imports Learning Session Runtime packages.
"""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class SessionRuntimePort(Protocol):
    """Structural contract for Learning Session Runtime collaboration.

    Experience may present overview / progress / completion and request
    lifecycle transitions. It must never compute educational closure law.
    """

    @property
    def component_id(self) -> str:
        """Stable component identity."""

    @property
    def component_version(self) -> str:
        """Version string for health / diagnostics."""

    def is_available(self) -> bool:
        """True when the Session Runtime port can accept work."""

    def get_session_overview(
        self, student_id: str, *, session_id: str
    ) -> dict[str, Any] | None:
        """Return opaque session overview facts."""

    def begin_session(
        self, student_id: str, *, session_id: str
    ) -> dict[str, Any]:
        """Request session begin; return opaque runtime status."""

    def get_runtime_snapshot(
        self, student_id: str, *, session_id: str
    ) -> dict[str, Any] | None:
        """Return opaque runtime snapshot for progress projection."""

    def record_response(
        self,
        student_id: str,
        *,
        session_id: str,
        activity_id: str,
        response: str,
    ) -> dict[str, Any]:
        """Hand response to the educational kernel; return opaque result.

        Evidence recording remains invisible to presentation.
        """

    def complete_session(
        self, student_id: str, *, session_id: str
    ) -> dict[str, Any]:
        """Request session educational close; return opaque completion."""

    def get_reflection(
        self, student_id: str, *, session_id: str
    ) -> dict[str, Any] | None:
        """Return opaque reflection guidance facts."""

    def get_completion_summary(
        self, student_id: str, *, session_id: str
    ) -> dict[str, Any] | None:
        """Return opaque session summary / completion facts."""
