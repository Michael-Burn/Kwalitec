"""IAHF-001 True Study Session Pause / Resume regression tests.

Covers active-time accumulation (excludes paused wall time), multiple
pause/resume cycles, finalize after pauses, and refresh-while-paused
restore. Does not redesign Mission lifecycle or Educational Evidence.
"""

from __future__ import annotations

from app.services.study_session_timer import (
    STATUS_COMPLETED,
    STATUS_PAUSED,
    STATUS_RUNNING,
    active_minutes_for_prefill,
    elapsed_seconds,
    finalize,
    from_dict,
    new_timer,
    pause,
    resume,
    start,
    to_dict,
)


class TestActiveTimeExcludesPausedPeriod:
    def test_start_pause_wait_resume_excludes_paused(self):
        t0 = 1_000_000
        state = start(new_timer(), now_ms=t0)
        # Study for 30s
        state = pause(state, now_ms=t0 + 30_000)
        assert state.status == STATUS_PAUSED
        assert elapsed_seconds(state, now_ms=t0 + 30_000) == 30

        # Paused for 5 minutes of wall clock — elapsed must stay frozen
        paused_later = t0 + 30_000 + 300_000
        assert elapsed_seconds(state, now_ms=paused_later) == 30

        state = resume(state, now_ms=paused_later)
        assert state.status == STATUS_RUNNING
        # Study another 20s after resume
        after = paused_later + 20_000
        assert elapsed_seconds(state, now_ms=after) == 50


class TestMultiplePauseResumeCycles:
    def test_multiple_cycles_accumulate_only_running(self):
        t0 = 5_000_000
        state = start(new_timer(), now_ms=t0)

        # Run 10s, pause
        state = pause(state, now_ms=t0 + 10_000)
        # Idle 60s wall, resume
        t1 = t0 + 10_000 + 60_000
        state = resume(state, now_ms=t1)
        # Run 15s, pause
        state = pause(state, now_ms=t1 + 15_000)
        # Idle 120s wall, resume
        t2 = t1 + 15_000 + 120_000
        state = resume(state, now_ms=t2)
        # Run 5s
        assert elapsed_seconds(state, now_ms=t2 + 5_000) == 30


class TestCompleteAfterPauses:
    def test_finalize_while_paused_keeps_active_only(self):
        t0 = 2_000_000
        state = start(new_timer(), now_ms=t0)
        state = pause(state, now_ms=t0 + 90_000)
        # Long pause before finish
        done = finalize(state, now_ms=t0 + 90_000 + 600_000)
        assert done.status == STATUS_COMPLETED
        assert done.accumulated_seconds == 90
        assert done.running_since_ms is None

    def test_finalize_while_running_folds_open_segment(self):
        t0 = 3_000_000
        state = start(new_timer(), now_ms=t0)
        state = pause(state, now_ms=t0 + 40_000)
        state = resume(state, now_ms=t0 + 100_000)
        done = finalize(state, now_ms=t0 + 100_000 + 25_000)
        assert done.status == STATUS_COMPLETED
        assert done.accumulated_seconds == 65

    def test_active_minutes_prefill_ceils(self):
        assert active_minutes_for_prefill(0) is None
        assert active_minutes_for_prefill(1) == 1
        assert active_minutes_for_prefill(60) == 1
        assert active_minutes_for_prefill(61) == 2


class TestRefreshWhilePaused:
    def test_serialize_paused_restore_elapsed_frozen(self):
        t0 = 9_000_000
        state = start(new_timer(), now_ms=t0)
        state = pause(state, now_ms=t0 + 45_000)

        payload = to_dict(state)
        restored = from_dict(payload)
        assert restored.status == STATUS_PAUSED
        # Simulated page refresh 10 minutes later
        later = t0 + 45_000 + 600_000
        assert elapsed_seconds(restored, now_ms=later) == 45

    def test_serialize_running_restore_continues_open_segment(self):
        t0 = 8_000_000
        state = start(new_timer(), now_ms=t0)
        payload = to_dict(state)
        restored = from_dict(payload)
        assert restored.status == STATUS_RUNNING
        assert elapsed_seconds(restored, now_ms=t0 + 12_000) == 12
