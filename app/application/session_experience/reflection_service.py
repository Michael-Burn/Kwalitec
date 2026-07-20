"""ReflectionService — reflection checkpoint projection."""

from __future__ import annotations

from app.application.session_experience._registry import SessionExperienceRegistry
from app.application.session_experience._snapshots import reflection_snapshot
from app.application.session_experience.dto.reflection_snapshot import (
    ReflectionSnapshot,
)
from app.application.session_experience.exceptions import (
    PortUnavailable,
    ReflectionError,
)
from app.application.session_experience.ports.session_runtime_port import (
    SessionRuntimePort,
)
from app.domain.session_experience.reflection_projection import ReflectionProjection
from app.domain.session_experience.session_workspace import SessionSurface


class ReflectionService:
    """Project reflection guidance from Session Runtime port.

    No scoring language. Educational guidance only.
    """

    def __init__(
        self,
        *,
        session_runtime: SessionRuntimePort | None = None,
        registry: SessionExperienceRegistry | None = None,
    ) -> None:
        self._runtime = session_runtime
        self._registry = registry

    def reflection(
        self, student_id: str, *, session_id: str
    ) -> ReflectionSnapshot:
        """Build the reflection projection for ``session_id``."""
        sid = _require_id(student_id)
        sess = _require_id(session_id, field="session_id")
        runtime = self._require_runtime()
        opaque = runtime.get_reflection(sid, session_id=sess) or {}
        try:
            domain = ReflectionProjection.create(
                sess,
                key_insight=str(
                    opaque.get("key_insight") or opaque.get("insight") or ""
                ),
                concept_confidence=str(
                    opaque.get("concept_confidence")
                    or opaque.get("confidence_label")
                    or ""
                ),
                suggested_improvement=str(
                    opaque.get("suggested_improvement")
                    or opaque.get("improvement")
                    or ""
                ),
                reflection_prompt=str(
                    opaque.get("reflection_prompt") or opaque.get("prompt") or ""
                ),
                topic_title=str(opaque.get("topic_title") or opaque.get("topic") or ""),
                next_action_label=str(
                    opaque.get("next_action_label") or "Continue to Summary"
                ),
            )
        except ValueError as exc:
            raise ReflectionError(str(exc)) from exc
        if self._registry is not None:
            workspace = self._registry.get_workspace_for_session(sess)
            if workspace is not None and not workspace.is_on(SessionSurface.REFLECTION):
                self._registry.put_workspace(
                    workspace.navigate_to(SessionSurface.REFLECTION)
                )
        return reflection_snapshot(domain)

    def continue_to_summary(
        self, student_id: str, *, session_id: str
    ) -> ReflectionSnapshot:
        """Acknowledge reflection and move workspace to Summary."""
        snap = self.reflection(student_id, session_id=session_id)
        if self._registry is not None:
            workspace = self._registry.get_workspace_for_session(session_id)
            if workspace is not None:
                self._registry.put_workspace(
                    workspace.navigate_to(SessionSurface.SUMMARY)
                )
        return snap

    def _require_runtime(self) -> SessionRuntimePort:
        if self._runtime is None or not self._runtime.is_available():
            raise PortUnavailable("session_runtime port unavailable")
        return self._runtime


def _require_id(value: str, field: str = "student_id") -> str:
    if not isinstance(value, str) or not value.strip():
        raise ReflectionError(f"{field} must be a non-empty string")
    return value.strip()
