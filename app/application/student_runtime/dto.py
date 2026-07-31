"""DTOs for Student Runtime Coordinator session binding."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SessionBindingResult:
    """Handle returned after Mission Accepted ≡ Study Session start/resume.

    Presentation redirects to ``/session/<session_id>/*``. Educational
    substance is intentionally thin in P1 — spine only.
    """

    session_id: str
    mission_instance_id: str
    student_id: str
    topic_title: str
    topic_id: str
    estimated_minutes: int | None
    resumed: bool
    phase: str
    authority: str = "learning_session_runtime"
