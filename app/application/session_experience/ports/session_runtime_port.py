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

    def pause_session(
        self, student_id: str, *, session_id: str
    ) -> dict[str, Any]:
        """Request session pause; return opaque runtime status."""

    def resume_session(
        self, student_id: str, *, session_id: str
    ) -> dict[str, Any]:
        """Request session resume; return opaque runtime status."""

    def request_finish(
        self, student_id: str, *, session_id: str
    ) -> dict[str, Any]:
        """Enter Ready to Finish (Finish Review) without completing."""

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
        scored_correct: bool | None = None,
        structured: bool = False,
        score_payload: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Hand response to the educational kernel; return opaque result.

        Evidence recording remains invisible to presentation.
        Optional ``scored_correct`` / ``structured`` come from the activity
        layer (KWP-004) — this port does not score.
        """

    def update_checklist(
        self,
        student_id: str,
        *,
        session_id: str,
        item_id: str,
        done: bool,
    ) -> dict[str, Any]:
        """Update a plan-checklist item; return opaque progress facts."""

    def save_surface(
        self,
        student_id: str,
        *,
        session_id: str,
        surface: str,
    ) -> dict[str, Any]:
        """Persist the active workspace surface for recovery."""

    def complete_session(
        self,
        student_id: str,
        *,
        session_id: str,
        finish_verdict: str | None = None,
        finish_notes: str | None = None,
    ) -> dict[str, Any]:
        """Request session educational close; return opaque completion.

        When finish review is required, ``finish_verdict`` must be
        yes / partially / no. Never silently completes.
        """

    def get_reflection(
        self, student_id: str, *, session_id: str
    ) -> dict[str, Any] | None:
        """Return opaque reflection guidance facts."""

    def record_reflection_note(
        self,
        student_id: str,
        *,
        session_id: str,
        note: str,
        confidence_rating: int | None = None,
    ) -> dict[str, Any]:
        """Persist the student's free-text reflection note onto the session record.

        Optional ``confidence_rating`` (1-5) is stored beside the note on the
        same opaque session document for session-local display only.

        Returns an opaque acknowledgement. Never scores or interprets the note.
        """

    def get_completion_summary(
        self, student_id: str, *, session_id: str
    ) -> dict[str, Any] | None:
        """Return opaque session summary / completion facts."""
