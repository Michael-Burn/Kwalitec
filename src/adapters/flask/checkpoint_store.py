"""Session Runtime checkpoint serialization (Flask-free).

Stores lifecycle events as plain dicts so adapters can persist checkpoints in
HTTP sessions or in-memory test doubles. Never contains educational logic.
"""

from __future__ import annotations

from collections.abc import MutableMapping
from typing import Protocol

from application.session_runtime import SessionEvent, SessionEventKind, SessionRuntime


class CheckpointStore(Protocol):
    """Load / save serialized session event logs by session identity."""

    def load(self, session_id: str) -> list[dict[str, object]] | None: ...

    def save(self, session_id: str, events: list[dict[str, object]]) -> None: ...

    def clear(self, session_id: str) -> None: ...


class InMemoryCheckpointStore:
    """Process-local checkpoint store for tests and single-worker demos."""

    def __init__(self) -> None:
        self._data: dict[str, list[dict[str, object]]] = {}

    def load(self, session_id: str) -> list[dict[str, object]] | None:
        key = (session_id or "").strip()
        if not key:
            return None
        payload = self._data.get(key)
        return None if payload is None else [dict(item) for item in payload]

    def save(self, session_id: str, events: list[dict[str, object]]) -> None:
        key = (session_id or "").strip()
        if not key:
            return
        self._data[key] = [dict(item) for item in events]

    def clear(self, session_id: str) -> None:
        key = (session_id or "").strip()
        if key:
            self._data.pop(key, None)


class MappingCheckpointStore:
    """Checkpoint store backed by any mutable mapping (e.g. Flask session)."""

    def __init__(
        self,
        mapping: MutableMapping[str, object],
        *,
        prefix: str = "eos_session_events:",
    ) -> None:
        self._mapping = mapping
        self._prefix = prefix

    def _key(self, session_id: str) -> str:
        return f"{self._prefix}{(session_id or '').strip()}"

    def load(self, session_id: str) -> list[dict[str, object]] | None:
        key = self._key(session_id)
        if not (session_id or "").strip():
            return None
        payload = self._mapping.get(key)
        if not isinstance(payload, list):
            return None
        return [dict(item) for item in payload if isinstance(item, dict)]

    def save(self, session_id: str, events: list[dict[str, object]]) -> None:
        if not (session_id or "").strip():
            return
        self._mapping[self._key(session_id)] = [dict(item) for item in events]

    def clear(self, session_id: str) -> None:
        if (session_id or "").strip():
            self._mapping.pop(self._key(session_id), None)


def events_to_dicts(
    events: tuple[SessionEvent, ...] | list[SessionEvent],
) -> list[dict[str, object]]:
    """Serialize runtime events to JSON-friendly dicts."""
    return [
        {
            "kind": event.kind.value,
            "sequence": event.sequence,
            "from_stage": event.from_stage,
            "to_stage": event.to_stage,
            "paused_after": event.paused_after,
            "cancelled_after": event.cancelled_after,
        }
        for event in events
    ]


def dicts_to_events(
    payload: list[dict[str, object]] | None,
) -> tuple[SessionEvent, ...]:
    """Deserialize event dicts into ``SessionEvent`` tuples."""
    if not payload:
        return ()
    events: list[SessionEvent] = []
    for item in payload:
        events.append(
            SessionEvent(
                kind=SessionEventKind(str(item["kind"])),
                sequence=int(item["sequence"]),  # type: ignore[arg-type]
                from_stage=str(item["from_stage"]),
                to_stage=str(item["to_stage"]),
                paused_after=bool(item.get("paused_after", False)),
                cancelled_after=bool(item.get("cancelled_after", False)),
            )
        )
    return tuple(events)


def restore_runtime(
    runtime: SessionRuntime,
    store: CheckpointStore,
    session_id: str,
) -> SessionRuntime:
    """Replay stored events onto a fresh runtime when a checkpoint exists."""
    payload = store.load(session_id)
    events = dicts_to_events(payload)
    if not events:
        return runtime
    return SessionRuntime.replay(
        runtime.view_model,
        events,
        session_id=session_id,
    )
