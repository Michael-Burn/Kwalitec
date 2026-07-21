"""SessionController — HTTP orchestration for the Study Session Runner.

Thin application-adapter controller. Invokes the session presenter and session
runtime. No educational decisions, persistence, or AI.
"""

from __future__ import annotations

from dataclasses import dataclass

from adapters.flask.checkpoint_store import (
    CheckpointStore,
    events_to_dicts,
    restore_runtime,
)
from adapters.flask.dashboard.dependency_provider import AdapterDependencies
from adapters.flask.navigation import REFLECTION_PATH, with_query
from application.session_runtime import (
    InvalidSessionTransitionError,
    SessionAction,
    SessionRuntime,
    SessionStage,
    SessionState,
)
from presentation.study_session import SessionPresenter, StudySessionViewModel

_ACTIONS: dict[str, SessionAction] = {
    "start": SessionAction.START,
    "advance": SessionAction.ADVANCE,
    "pause": SessionAction.PAUSE,
    "resume": SessionAction.RESUME,
    "complete": SessionAction.COMPLETE,
    "cancel": SessionAction.CANCEL,
}


@dataclass(frozen=True, slots=True)
class SessionActionResult:
    """Outcome of one session lifecycle HTTP action."""

    view_model: StudySessionViewModel
    state: SessionState
    redirect_path: str | None = None
    error: str = ""


class SessionController:
    """Present and drive one guided study session for HTTP handlers."""

    def __init__(self, dependencies: AdapterDependencies) -> None:
        self._dependencies = dependencies

    def show(
        self,
        student_id: str | None = None,
        *,
        session_id: str | None = None,
    ) -> StudySessionViewModel:
        """Load pipeline display cargo and present the study-session view model."""
        resolved_id = self._resolve_student(student_id)
        result = self._dependencies.load_pipeline_result(resolved_id)
        return SessionPresenter.present(result)

    def open_runtime(
        self,
        view_model: StudySessionViewModel,
        *,
        session_id: str | None = None,
    ) -> SessionRuntime:
        """Create an in-memory session runtime bound to a view model."""
        return SessionRuntime(view_model, session_id=session_id)

    def current_state(self, runtime: SessionRuntime) -> SessionState:
        """Return the current lifecycle state from a session runtime."""
        return runtime.state

    def load_runtime(
        self,
        student_id: str | None = None,
        *,
        session_id: str | None = None,
        store: CheckpointStore | None = None,
    ) -> SessionRuntime:
        """Open a runtime and restore any stored checkpoint events."""
        view = self.show(student_id, session_id=session_id)
        identity = (session_id or "").strip() or None
        runtime = self.open_runtime(view, session_id=identity)
        active_store = store or self._dependencies.checkpoint_store
        if active_store is None or runtime.state.session_id == "":
            return runtime
        return restore_runtime(runtime, active_store, runtime.state.session_id)

    def apply_action(
        self,
        action: str,
        student_id: str | None = None,
        *,
        session_id: str | None = None,
        store: CheckpointStore | None = None,
    ) -> SessionActionResult:
        """Apply a named lifecycle action and optionally persist a checkpoint."""
        active_store = store or self._dependencies.checkpoint_store
        runtime = self.load_runtime(
            student_id, session_id=session_id, store=active_store
        )
        key = (action or "").strip().lower()
        mapped = _ACTIONS.get(key)
        if mapped is None:
            return SessionActionResult(
                view_model=runtime.view_model,
                state=runtime.state,
                error=f"Unknown action: {action!r}",
            )
        try:
            self._dispatch(runtime, mapped)
        except InvalidSessionTransitionError as exc:
            return SessionActionResult(
                view_model=runtime.view_model,
                state=runtime.state,
                error=str(exc),
            )

        if active_store is not None:
            active_store.save(
                runtime.state.session_id,
                events_to_dicts(runtime.events),
            )

        redirect_path = None
        if runtime.state.stage in {SessionStage.REFLECTION, SessionStage.COMPLETED}:
            redirect_path = with_query(
                REFLECTION_PATH,
                student_id=self._resolve_student(student_id) or None,
                session_id=runtime.state.session_id or None,
            )
        return SessionActionResult(
            view_model=runtime.view_model,
            state=runtime.state,
            redirect_path=redirect_path,
        )

    def _resolve_student(self, student_id: str | None) -> str:
        resolved = (student_id or "").strip()
        if not resolved:
            resolved = self._dependencies.student_id_resolver()
        return resolved

    @staticmethod
    def _dispatch(runtime: SessionRuntime, action: SessionAction) -> SessionState:
        if action is SessionAction.START:
            return runtime.start()
        if action is SessionAction.ADVANCE:
            return runtime.advance()
        if action is SessionAction.PAUSE:
            return runtime.pause()
        if action is SessionAction.RESUME:
            return runtime.resume()
        if action is SessionAction.COMPLETE:
            return runtime.complete()
        return runtime.cancel()
