"""Persistence port and in-memory store for Spacing Scheduler state."""

from __future__ import annotations

from typing import Protocol

from app.domain.spacing_scheduler.types import SpacingState


class SpacingStateStore(Protocol):
    """Persistence port for canonical spacing state."""

    def get(self, learner_id: str, unit_id: str) -> SpacingState | None:
        """Return stored state or None when never scheduled."""

    def put(self, state: SpacingState) -> None:
        """Upsert canonical state for the learner/unit pair."""

    def list_for_learner(self, learner_id: str) -> tuple[SpacingState, ...]:
        """Return every stored state for the learner (any order)."""


class InMemorySpacingStateStore:
    """Process-local store used until a durable adapter is wired."""

    def __init__(self) -> None:
        self._rows: dict[tuple[str, str], SpacingState] = {}

    def get(self, learner_id: str, unit_id: str) -> SpacingState | None:
        return self._rows.get((learner_id.strip(), unit_id.strip()))

    def put(self, state: SpacingState) -> None:
        self._rows[(state.learner_id, state.unit_id)] = state

    def list_for_learner(self, learner_id: str) -> tuple[SpacingState, ...]:
        lid = learner_id.strip()
        return tuple(
            state for (learner, _), state in self._rows.items() if learner == lid
        )

    def clear(self) -> None:
        self._rows.clear()
