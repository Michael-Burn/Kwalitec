"""RecoveryPlannerPort + feature-flag isolation tests (P2-MS010)."""

from __future__ import annotations

from app.application.config.v2_flags import resolve_v2_feature_flags
from app.infrastructure.adapters.recovery_planner import (
    DisruptionSummary,
    MissedSessionFact,
    RecoveryContext,
    RecoveryPlanCandidate,
    RecoveryPlannerPort,
    StudyCapacityFact,
    StudyRecoveryPlannerAdapter,
    build_study_recovery_planner_adapter,
)
from app.infrastructure.adapters.student_experience.composition import (
    build_production_experience,
)
from app.infrastructure.diagnostics.dual_run import build_dual_run_status
from app.services.recovery_injection import (
    RuntimeARecoveryInjection,
    build_runtime_a_recovery_injection,
)


def _context(*, student_id: str = "7") -> RecoveryContext:
    return RecoveryContext(
        recovery_id="rcv-test",
        reporting_period="this_week",
        disruption_summary=DisruptionSummary(
            summary="1 planned session was not completed.",
            disruption_kind="missed_planned_sessions",
            missed_count=1,
            source_description="Derived from recorded plan vs completion.",
        ),
        missed_sessions=(
            MissedSessionFact(
                session_ref="session-a",
                planned_at="2026-08-04T09:00:00+00:00",
                source_description="Plan ledger session-a",
            ),
        ),
        available_study_capacity=StudyCapacityFact(
            available_minutes=60,
            available_slots=1,
            source_description="Declared remaining capacity.",
        ),
        current_plan_version="plan-v1",
        evidence_provenance={"evidence_refs": ["ev-9"]},
        generated_at="2026-08-07T12:00:00+00:00",
        student_id=student_id,
    )


def test_recovery_planner_flag_defaults_off():
    flags = resolve_v2_feature_flags(environ={})
    assert flags.ENABLE_RECOVERY_PLANNER is False
    dual = build_dual_run_status(flags=flags)
    assert dual.recovery_planner is False


def test_recovery_planner_flag_enables_dual_run_field():
    flags = resolve_v2_feature_flags(
        environ={"KWALITEC_RECOVERY_PLANNER": "1"}
    )
    assert flags.ENABLE_RECOVERY_PLANNER is True
    dual = build_dual_run_status(flags=flags)
    assert dual.recovery_planner is True


def test_flag_isolation_from_all_prior_flags():
    recovery_only = resolve_v2_feature_flags(
        environ={"KWALITEC_RECOVERY_PLANNER": "1"}
    )
    assert recovery_only.ENABLE_RECOVERY_PLANNER is True
    assert recovery_only.ENABLE_EVIDENCE_ADVISORY is False
    assert recovery_only.ENABLE_EXPERIENCE_FEEDBACK is False
    assert recovery_only.ENABLE_EXPERIENCE_OBSERVATION is False
    assert recovery_only.ENABLE_EXPERIENCE_DIAGNOSTICS is False
    assert recovery_only.ENABLE_EVIDENCE_PLATFORM is False
    assert recovery_only.ENABLE_UNIFIED_JOURNEY is False
    assert recovery_only.ENABLE_STRATEGY_ENGINE is False
    assert recovery_only.ENABLE_DIGITAL_TWIN is False
    assert recovery_only.ENABLE_ADAPTIVE_ENGINE is False

    others_only = resolve_v2_feature_flags(
        environ={
            "KWALITEC_EVIDENCE_ADVISORY": "1",
            "KWALITEC_EXPERIENCE_FEEDBACK": "1",
            "KWALITEC_EXPERIENCE_OBSERVATION": "1",
            "KWALITEC_EXPERIENCE_DIAGNOSTICS": "1",
            "KWALITEC_EVIDENCE_PLATFORM": "1",
            "KWALITEC_UNIFIED_JOURNEY": "1",
            "KWALITEC_STRATEGY_ENGINE": "1",
            "KWALITEC_DIGITAL_TWIN": "1",
            "KWALITEC_ADAPTIVE_ENGINE": "1",
        }
    )
    assert others_only.ENABLE_RECOVERY_PLANNER is False


def test_adapter_implements_recovery_port():
    adapter = build_study_recovery_planner_adapter(enabled=True)
    assert adapter is not None
    assert isinstance(adapter, RecoveryPlannerPort)
    assert isinstance(adapter, StudyRecoveryPlannerAdapter)
    assert adapter.port_id == "recovery_planner_port"
    assert adapter.is_available() is True


def test_plan_recovery_returns_advisory_placeholder():
    adapter = build_study_recovery_planner_adapter(enabled=True)
    assert adapter is not None
    result = adapter.plan_recovery(_context())
    assert result.ok is True
    assert isinstance(result.value, RecoveryPlanCandidate)
    candidate = result.value
    assert candidate.advisory_only is True
    assert candidate.strategy_type == "structural_placeholder"
    assert candidate.affected_period == "this_week"
    assert candidate.provenance["source_service"] == "study_recovery_planner"
    assert candidate.provenance["evidence_provenance"]["evidence_refs"] == ["ev-9"]
    assert "session-a" in candidate.provenance["missed_session_refs"]


def test_plan_recovery_is_deterministic():
    adapter = build_study_recovery_planner_adapter(enabled=True)
    assert adapter is not None
    ctx = _context()
    first = adapter.plan_recovery(ctx)
    second = adapter.plan_recovery(ctx)
    assert first.ok and second.ok
    assert first.value is not None and second.value is not None
    assert first.value.serialize() == second.value.serialize()


def test_disabled_adapter_rejects_plan():
    adapter = StudyRecoveryPlannerAdapter(enabled=False)
    result = adapter.plan_recovery(_context())
    assert result.ok is False
    assert result.error_code == "UNAVAILABLE"


def test_composition_wires_recovery_when_flag_on():
    flags_off = resolve_v2_feature_flags(environ={})
    composition_off, _ = build_production_experience(flags=flags_off)
    assert composition_off.recovery_planner is None
    assert composition_off.recovery_injection is None

    flags_on = resolve_v2_feature_flags(
        environ={"KWALITEC_RECOVERY_PLANNER": "1"}
    )
    composition_on, _ = build_production_experience(flags=flags_on)
    assert isinstance(
        composition_on.recovery_planner, StudyRecoveryPlannerAdapter
    )
    assert isinstance(
        composition_on.recovery_injection, RuntimeARecoveryInjection
    )
    assert composition_on.recovery_injection.port is composition_on.recovery_planner


def test_build_helpers_respect_enabled_gate():
    assert build_study_recovery_planner_adapter(enabled=False) is None
    assert build_runtime_a_recovery_injection(enabled=False) is None
    adapter = build_study_recovery_planner_adapter(enabled=True)
    injection = build_runtime_a_recovery_injection(enabled=True, port=adapter)
    assert adapter is not None
    assert injection is not None
    assert injection.port is adapter
