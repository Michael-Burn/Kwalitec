"""Unit tests for Preferred Authority routing (RI-001)."""

from __future__ import annotations

from types import SimpleNamespace

from app.application.runtime_integration.dto import FallbackReason
from app.application.runtime_integration.routing import decide_authority


def test_disabled_flag_forces_fallback() -> None:
    decision = decide_authority(
        integration_enabled=False,
        instance=SimpleNamespace(instance_id="sci-1", subject_code="CS1"),
        decision_count=3,
    )
    assert decision.use_educational_intelligence is False
    assert decision.fallback_reason is FallbackReason.RUNTIME_INTEGRATION_DISABLED


def test_no_sci_falls_back() -> None:
    decision = decide_authority(
        integration_enabled=True,
        instance=None,
        decision_count=0,
        preferred_subject="CS1",
    )
    assert decision.use_educational_intelligence is False
    assert decision.fallback_reason is FallbackReason.NO_ACTIVE_SCI
    assert decision.missing_prerequisite == "active_student_curriculum_instance"


def test_empty_decisions_fall_back() -> None:
    instance = SimpleNamespace(instance_id="sci-1", subject_code="CS1")
    decision = decide_authority(
        integration_enabled=True,
        instance=instance,
        decision_count=0,
    )
    assert decision.use_educational_intelligence is False
    assert decision.fallback_reason is FallbackReason.NO_EDUCATIONAL_DECISIONS
    assert decision.instance_id == "sci-1"


def test_sci_and_decisions_select_educational_intelligence() -> None:
    instance = SimpleNamespace(instance_id="sci-1", subject_code="CS1")
    decision = decide_authority(
        integration_enabled=True,
        instance=instance,
        decision_count=2,
    )
    assert decision.use_educational_intelligence is True
    assert decision.fallback_reason is None
    assert decision.instance_id == "sci-1"
    assert decision.subject_code == "CS1"
