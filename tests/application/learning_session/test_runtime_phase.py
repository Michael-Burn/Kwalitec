"""Tests for RuntimePhase vocabulary and transition helpers."""

from __future__ import annotations

from app.application.learning_session.runtime_phase import (
    RuntimePhase,
    RuntimeTransitionEvent,
    is_terminal_runtime_phase,
    next_runtime_phase,
    phase_from_session_state,
)
from app.domain.learning_journey.value_objects.session_state import SessionState


class TestRuntimePhaseTransitions:
    def test_planned_prepare_ready(self):
        assert (
            next_runtime_phase(RuntimePhase.PLANNED, RuntimeTransitionEvent.PREPARE)
            == RuntimePhase.READY
        )

    def test_planned_start_active(self):
        assert (
            next_runtime_phase(RuntimePhase.PLANNED, RuntimeTransitionEvent.START)
            == RuntimePhase.ACTIVE
        )

    def test_ready_start_active(self):
        assert (
            next_runtime_phase(RuntimePhase.READY, RuntimeTransitionEvent.START)
            == RuntimePhase.ACTIVE
        )

    def test_active_pause_paused(self):
        assert (
            next_runtime_phase(RuntimePhase.ACTIVE, RuntimeTransitionEvent.PAUSE)
            == RuntimePhase.PAUSED
        )

    def test_paused_resume_active(self):
        assert (
            next_runtime_phase(RuntimePhase.PAUSED, RuntimeTransitionEvent.RESUME)
            == RuntimePhase.ACTIVE
        )

    def test_active_complete_completed(self):
        assert (
            next_runtime_phase(RuntimePhase.ACTIVE, RuntimeTransitionEvent.COMPLETE)
            == RuntimePhase.COMPLETED
        )

    def test_paused_complete_completed(self):
        assert (
            next_runtime_phase(RuntimePhase.PAUSED, RuntimeTransitionEvent.COMPLETE)
            == RuntimePhase.COMPLETED
        )

    def test_completed_archive_archived(self):
        assert (
            next_runtime_phase(RuntimePhase.COMPLETED, RuntimeTransitionEvent.ARCHIVE)
            == RuntimePhase.ARCHIVED
        )

    def test_invalid_pause_from_planned(self):
        assert (
            next_runtime_phase(RuntimePhase.PLANNED, RuntimeTransitionEvent.PAUSE)
            is None
        )

    def test_invalid_archive_from_active(self):
        assert (
            next_runtime_phase(RuntimePhase.ACTIVE, RuntimeTransitionEvent.ARCHIVE)
            is None
        )

    def test_invalid_resume_from_active(self):
        assert (
            next_runtime_phase(RuntimePhase.ACTIVE, RuntimeTransitionEvent.RESUME)
            is None
        )

    def test_invalid_start_from_completed(self):
        assert (
            next_runtime_phase(RuntimePhase.COMPLETED, RuntimeTransitionEvent.START)
            is None
        )

    def test_invalid_prepare_from_ready(self):
        assert (
            next_runtime_phase(RuntimePhase.READY, RuntimeTransitionEvent.PREPARE)
            is None
        )

    def test_archived_is_terminal(self):
        assert is_terminal_runtime_phase(RuntimePhase.ARCHIVED)
        assert is_terminal_runtime_phase(RuntimePhase.COMPLETED)
        assert not is_terminal_runtime_phase(RuntimePhase.ACTIVE)


class TestPhaseFromSessionState:
    def test_not_started_planned(self):
        assert (
            phase_from_session_state(SessionState.NOT_STARTED)
            == RuntimePhase.PLANNED
        )

    def test_not_started_prepared_ready(self):
        assert (
            phase_from_session_state(SessionState.NOT_STARTED, prepared=True)
            == RuntimePhase.READY
        )

    def test_active(self):
        assert phase_from_session_state(SessionState.ACTIVE) == RuntimePhase.ACTIVE

    def test_paused(self):
        assert phase_from_session_state(SessionState.PAUSED) == RuntimePhase.PAUSED

    def test_completed(self):
        assert (
            phase_from_session_state(SessionState.COMPLETED) == RuntimePhase.COMPLETED
        )

    def test_completed_archived(self):
        assert (
            phase_from_session_state(SessionState.COMPLETED, archived=True)
            == RuntimePhase.ARCHIVED
        )

    def test_abandoned_maps_archived(self):
        assert (
            phase_from_session_state(SessionState.ABANDONED) == RuntimePhase.ARCHIVED
        )

    def test_skipped_maps_archived(self):
        assert phase_from_session_state(SessionState.SKIPPED) == RuntimePhase.ARCHIVED

    def test_phase_values_are_stable(self):
        assert RuntimePhase.PLANNED.value == "planned"
        assert RuntimePhase.READY.value == "ready"
        assert RuntimePhase.ARCHIVED.value == "archived"
