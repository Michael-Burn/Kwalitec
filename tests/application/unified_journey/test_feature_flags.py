"""Feature flag tests — ENABLE_UNIFIED_JOURNEY (P2-MS001–P2-MS004)."""

from __future__ import annotations

from app.application.config.v2_flags import resolve_v2_feature_flags
from app.application.unified_journey import (
    JourneyContextAssembler,
    JourneyCoordinator,
    SessionPhase,
)
from app.infrastructure.adapters.student_experience.composition import (
    build_production_experience,
)
from app.infrastructure.diagnostics.dual_run import build_dual_run_status
from app.presentation.student.navigation import build_navigation
from app.presentation.student.view_models import home_vm
from tests.application.unified_journey.test_home_integration import _snap


def test_unified_journey_flag_defaults_off():
    flags = resolve_v2_feature_flags(environ={})
    assert flags.ENABLE_UNIFIED_JOURNEY is False


def test_unified_journey_flag_truthy_env():
    flags = resolve_v2_feature_flags(
        environ={"KWALITEC_UNIFIED_JOURNEY": "1"}
    )
    assert flags.ENABLE_UNIFIED_JOURNEY is True


def test_unified_journey_flag_isolation_preserves_programme_i():
    flags = resolve_v2_feature_flags(
        environ={"KWALITEC_UNIFIED_JOURNEY": "1"}
    )
    assert flags.ENABLE_UNIFIED_JOURNEY is True
    assert flags.ENABLE_ADAPTIVE_ENGINE is False
    assert flags.ENABLE_DIGITAL_TWIN is False
    assert flags.ENABLE_STRATEGY_ENGINE is False
    assert flags.ENABLE_EVIDENCE_PLATFORM is False
    assert flags.ENABLE_JOURNEY_BRIDGE is False
    assert flags.ENABLE_MISSION_READ_BRIDGE is False


def test_composition_wires_coordinator_only_when_flag_on():
    flags_off = resolve_v2_feature_flags(environ={})
    composition_off, _ = build_production_experience(flags=flags_off)
    assert composition_off.journey_coordinator is None

    flags_on = resolve_v2_feature_flags(
        environ={"KWALITEC_UNIFIED_JOURNEY": "true"}
    )
    composition_on, _ = build_production_experience(flags=flags_on)
    assert composition_on.journey_coordinator is not None
    assert isinstance(composition_on.journey_coordinator, JourneyCoordinator)
    # Programme I adapters remain present; coordinator does not replace them.
    assert composition_on.adaptive is not None
    assert composition_on.twin is not None
    assert composition_on.mission is not None


def test_dual_run_status_exposes_unified_journey():
    status_off = build_dual_run_status(
        flags=resolve_v2_feature_flags(environ={})
    )
    assert status_off.unified_journey is False
    status_on = build_dual_run_status(
        flags=resolve_v2_feature_flags(
            environ={"KWALITEC_UNIFIED_JOURNEY": "yes"}
        )
    )
    assert status_on.unified_journey is True


def test_flag_off_keeps_feature_navigation():
    nav = build_navigation("home", unified_journey=False)
    assert any(item.label == "Home" for item in nav)
    assert not any(item.journey_stage for item in nav)


def test_flag_on_switches_to_journey_navigation():
    nav = build_navigation("home", unified_journey=True)
    assert any(item.label == "Today" for item in nav)
    assert any(item.journey_stage == "daily_mission" for item in nav)


def test_coordinator_available_independently_of_programme_i_engine_flags():
    """Journey orchestration works without Adaptive/Strategy/Twin/Evidence ON."""
    flags = resolve_v2_feature_flags(
        environ={"KWALITEC_UNIFIED_JOURNEY": "1"}
    )
    assert flags.ENABLE_ADAPTIVE_ENGINE is False
    assert flags.ENABLE_STRATEGY_ENGINE is False
    coordinator = JourneyCoordinator(assembler=JourneyContextAssembler())
    context = coordinator.journey_context("42")
    assert context.availability == "placeholder"
    assert context.mission_title == "Today's primary mission"
    day = coordinator.day_experience("42")
    assert day.current_phase is SessionPhase.READY
    session = coordinator.study_session("42", day=day)
    assert session.mission_title == "Today's primary mission"


def test_guided_session_fields_isolated_when_flag_off():
    vm = home_vm(_snap(), unified_journey=False)
    assert vm.guided_session_active is False
    assert vm.session_phase == ""
    assert vm.session_status == ""
    assert vm.session_control == ""
    assert vm.session_learning_objective == ""
    assert vm.reflection_available is False
    assert vm.reflection_active is False
    assert vm.reflection_prompts == ()
    assert vm.day_complete is False
