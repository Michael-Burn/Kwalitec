"""Performance smoke checks for student-flow page rendering (V4-004)."""

from __future__ import annotations

import time


def test_dashboard_render_budget(client) -> None:
    # Warm Jinja / presenter caches.
    client.get("/eos/dashboard/?student_id=student-ada")

    started = time.perf_counter()
    response = client.get("/eos/dashboard/?student_id=student-ada")
    elapsed_ms = (time.perf_counter() - started) * 1000

    assert response.status_code == 200
    assert elapsed_ms < 750, f"dashboard took {elapsed_ms:.1f}ms"


def test_session_action_budget(client) -> None:
    started = time.perf_counter()
    response = client.post(
        "/eos/session/action",
        data={
            "student_id": "student-ada",
            "session_id": "perf-session",
            "action": "start",
        },
    )
    elapsed_ms = (time.perf_counter() - started) * 1000

    assert response.status_code == 200
    assert elapsed_ms < 750, f"session action took {elapsed_ms:.1f}ms"
