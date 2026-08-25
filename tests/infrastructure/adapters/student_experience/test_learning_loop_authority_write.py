"""Defensive learning-loop Twin write path (Authority read-only).

When Session Completion Bridge is absent and ``composition.twin`` is the
Foundation Authority port (no ``apply_session_outcome``), the loop must
skip the Twin write gracefully — Runtime A owns session writes.
"""

from __future__ import annotations

from unittest import mock

from app.infrastructure.adapters.digital_twin.authority import (
    StudentTwinFoundationAuthorityPort,
)
from app.infrastructure.adapters.digital_twin.foundation import (
    StudentDigitalTwinFoundation,
)
from app.infrastructure.adapters.student_experience.composition import (
    StudentExperienceComposition,
)
from app.infrastructure.adapters.student_twin.experience_adapter import (
    ExperienceTwinAdapter,
)


def test_learning_loop_skips_apply_when_twin_is_authority_port():
    composition = StudentExperienceComposition(
        seed_demo_learners=False,
        enable_learning_loop=False,
        session_completion=None,
    )
    foundation = StudentDigitalTwinFoundation(enabled=True)
    composition.twin = StudentTwinFoundationAuthorityPort(
        foundation=foundation,
        fallback=None,
        enabled=True,
    )
    assert not hasattr(composition.twin, "apply_session_outcome")

    completed = {
        "session_id": "sess-1",
        "topic_title": "Probability",
        "estimated_minutes": 25,
    }
    with (
        mock.patch.object(
            composition.mission,
            "complete_session",
            return_value=completed,
        ) as complete,
        mock.patch.object(
            composition.adaptive,
            "recalculate_from_twin",
            return_value=None,
        ) as recalc,
        mock.patch.object(
            composition.adaptive,
            "get_todays_recommendation",
            return_value={},
        ),
        mock.patch.object(
            composition.adaptive,
            "accept_recommendation",
            return_value={},
        ),
        mock.patch.object(
            composition.orchestrator,
            "set_activity_status",
            return_value=None,
        ),
    ):
        # Must not raise AttributeError on Authority port.
        composition._run_learning_loop(
            "42",
            {
                "session_id": "sess-1",
                "mission_id": "m-1",
                "topic_title": "Probability",
                "estimated_minutes": 25,
            },
        )

    complete.assert_called_once()
    recalc.assert_called_once()
    twin_payload = recalc.call_args.kwargs["twin_payload"]
    # Empty ack from skipped write — still merged into recalculate payload.
    assert isinstance(twin_payload, dict)


def test_learning_loop_still_applies_on_experience_twin_adapter():
    composition = StudentExperienceComposition(
        seed_demo_learners=False,
        enable_learning_loop=False,
        session_completion=None,
    )
    assert isinstance(composition.twin, ExperienceTwinAdapter)

    completed = {
        "session_id": "sess-2",
        "topic_title": "Statistics",
        "estimated_minutes": 30,
    }
    with (
        mock.patch.object(
            composition.mission,
            "complete_session",
            return_value=completed,
        ),
        mock.patch.object(
            composition.twin,
            "apply_session_outcome",
            wraps=composition.twin.apply_session_outcome,
        ) as apply,
        mock.patch.object(
            composition.adaptive,
            "recalculate_from_twin",
            return_value=None,
        ),
        mock.patch.object(
            composition.adaptive,
            "get_todays_recommendation",
            return_value={},
        ),
        mock.patch.object(
            composition.adaptive,
            "accept_recommendation",
            return_value={},
        ),
        mock.patch.object(
            composition.orchestrator,
            "set_activity_status",
            return_value=None,
        ),
    ):
        composition._run_learning_loop(
            "99",
            {
                "session_id": "sess-2",
                "mission_id": "m-2",
                "topic_title": "Statistics",
                "estimated_minutes": 30,
            },
        )

    apply.assert_called_once()
    assert apply.call_args.kwargs["session_payload"] == completed


def test_learning_loop_early_returns_when_session_completion_wired():
    """Bridge path must not call apply_session_outcome (Authority-safe)."""
    bridge = mock.Mock()
    composition = StudentExperienceComposition(
        seed_demo_learners=False,
        enable_learning_loop=False,
        session_completion=bridge,
    )
    composition.twin = StudentTwinFoundationAuthorityPort(
        foundation=StudentDigitalTwinFoundation(enabled=True),
        fallback=None,
        enabled=True,
    )
    with (
        mock.patch.object(
            composition.mission,
            "complete_session",
        ) as complete,
        mock.patch.object(
            composition.orchestrator,
            "set_activity_status",
            return_value=None,
        ),
    ):
        composition._run_learning_loop(
            "7",
            {"session_id": "s", "mission_id": "m"},
        )

    complete.assert_not_called()
