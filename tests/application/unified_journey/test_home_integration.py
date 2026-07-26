"""Home integration tests — Daily Mission Experience (P2-MS002 / P2-MS003)."""

from __future__ import annotations

from app.application.student_experience.dto.explanation_snapshot import (
    ExplanationSnapshot,
)
from app.application.student_experience.dto.home_snapshot import (
    HomeSnapshot,
    StartSessionActionSnapshot,
)
from app.application.unified_journey import (
    COMPLETION_COMPLETE,
    COMPLETION_IN_PROGRESS,
    JourneyContext,
    JourneyCoordinator,
    JourneyStage,
    JourneySubsystemInputs,
)
from app.presentation.student.view_models import home_vm


def _snap(**overrides) -> HomeSnapshot:
    base = dict(
        student_id="s1",
        greeting="Hello",
        recommendation_title="Revise equity",
        recommendation_summary="Focus on equity today",
        has_recommendation=True,
        can_start_session=True,
        estimated_study_minutes=25,
        expected_readiness_improvement=0.03,
        start_session=StartSessionActionSnapshot(
            label="Start Today's Session",
            enabled=True,
            can_start=True,
            mission_id="m1",
        ),
        explanation=ExplanationSnapshot(
            why_recommended="High educational return",
            expected_benefit="Strengthen readiness",
            confidence_label="Strong",
            is_complete=True,
        ),
    )
    base.update(overrides)
    return HomeSnapshot(**base)


def test_home_uses_journey_context_when_flag_on():
    vm = home_vm(_snap(), unified_journey=True)
    assert vm.unified_journey_enabled is True
    assert vm.journey_stage == "daily_mission"
    assert vm.primary_mission_title == "Revise equity"
    assert vm.why_it_matters == "High educational return"
    assert "25" in vm.estimated_duration_label
    assert vm.expected_outcome
    assert vm.primary_cta_enabled is True
    assert vm.completion_status == "not_started"
    assert vm.completion_status_label == "Not Started"
    assert vm.mission_summary
    assert len(vm.timeline_steps) == 4
    assert vm.timeline_steps[0].key == "mission"
    assert vm.timeline_steps[0].status == "current"
    # P2-MS004 guided session on Home when mission is active.
    assert vm.guided_session_active is True
    assert vm.session_phase == "ready"
    assert vm.session_status == "Ready"
    assert vm.session_learning_objective
    assert vm.session_control == "start"
    assert vm.session_control_label == "Start"


def test_home_guided_session_when_continue_cta():
    """Continue CTA maps onto Studying presentation phase (no education)."""
    snap = _snap(
        start_session=StartSessionActionSnapshot(
            label="Continue Mission",
            enabled=True,
            can_start=True,
            mission_id="m1",
        ),
    )
    vm = home_vm(snap, unified_journey=True)
    assert vm.guided_session_active is True
    assert vm.session_phase == "studying"
    assert vm.session_status == "Studying"
    assert vm.session_control == "finish"
    assert vm.session_control_label == "Finish"
    assert vm.session_elapsed_state == "in_progress"


def test_home_placeholders_when_no_recommendation():
    snap = _snap(
        recommendation_title="",
        has_recommendation=False,
        can_start_session=False,
        start_session=None,
        explanation=None,
    )
    vm = home_vm(snap, unified_journey=True)
    assert vm.unified_journey_enabled is True
    assert vm.journey_stage == "daily_mission"
    assert vm.primary_mission_title == "Today's primary mission"
    assert vm.why_it_matters == ""
    assert vm.expected_outcome == ""
    assert len(vm.timeline_steps) == 4
    assert vm.guided_session_active is False
    assert vm.session_control == ""


def test_home_ignores_journey_context_fields_when_flag_off():
    vm = home_vm(_snap(), unified_journey=False)
    assert vm.unified_journey_enabled is False
    assert vm.journey_stage == ""
    assert vm.primary_mission_title == ""
    assert vm.why_it_matters == ""
    assert vm.estimated_duration_label == ""
    assert vm.expected_outcome == ""
    assert vm.completion_status == ""
    assert vm.completion_status_label == ""
    assert vm.timeline_steps == ()
    assert vm.mission_summary == ""
    assert vm.guided_session_active is False
    assert vm.session_phase == ""
    assert vm.session_control == ""
    # Existing recommendation card still populated from Runtime A snapshot.
    assert vm.recommendation.title == "Revise equity"


def test_home_partial_runtime_a_fields():
    snap = _snap(
        recommendation_title="Topic only",
        recommendation_summary="",
        explanation=None,
        expected_readiness_improvement=None,
        estimated_study_minutes=None,
    )
    vm = home_vm(snap, unified_journey=True)
    assert vm.primary_mission_title == "Topic only"
    assert vm.estimated_duration_label == ""
    assert vm.why_it_matters == ""


def test_home_mission_completion_states_via_context():
    """Completion is UI state projected from JourneyContext — no education."""
    coordinator = JourneyCoordinator()

    in_progress_ctx = JourneyContext(
        stage=JourneyStage.DAILY_MISSION,
        mission_title="Continue equity",
        mission_reason="Keep going",
        estimated_duration="20 minutes",
        expected_outcome="Build fluency",
        completion_state=COMPLETION_IN_PROGRESS,
        cta_label="Continue Mission",
        cta_enabled=True,
        endpoint="student.start_session",
        source="runtime_a",
        availability="available",
        unavailable_reason="",
    )
    mission = coordinator.daily_mission(
        "s1",
        inputs=JourneySubsystemInputs(journey_context=in_progress_ctx),
    )
    assert mission.completion_status == COMPLETION_IN_PROGRESS
    assert mission.start_action.enabled is True

    done_ctx = JourneyContext(
        stage=JourneyStage.DAILY_MISSION,
        mission_title="Equity done",
        completion_state=COMPLETION_COMPLETE,
        cta_enabled=False,
        source="runtime_a",
        availability="available",
        unavailable_reason="",
    )
    done = coordinator.daily_mission(
        "s1",
        inputs=JourneySubsystemInputs(journey_context=done_ctx),
    )
    assert done.is_completed
    assert done.start_action.enabled is False
    timeline = coordinator.experience_timeline(
        "s1",
        inputs=JourneySubsystemInputs(journey_context=done_ctx),
    )
    assert timeline.steps[-1].status == "complete"


def test_home_presents_reflection_after_completed_mission():
    """After session completion, Home presents Guided Reflection first."""
    from app.application.unified_journey import (
        DailyMission,
        DayExperienceAssembler,
        MissionStartAction,
        ReflectionState,
        SessionPhase,
    )
    from app.presentation.student import view_models as vm_mod

    mission = DailyMission(
        title="Revise equity",
        reason="High educational return",
        estimated_duration="25 minutes",
        expected_outcome="Strengthen readiness",
        completion_status=COMPLETION_COMPLETE,
        start_action=MissionStartAction(enabled=False, label="Start"),
        mission_summary="High educational return",
        metadata=(("availability", "available"),),
    )
    day = DayExperienceAssembler().assemble(
        mission,
        phase=SessionPhase.COMPLETE,
    )
    assert day.reflection_state is ReflectionState.AVAILABLE
    assert day.reflection_active is True
    assert day.session_outcome is not None

    day_from_home = vm_mod._home_day_experience(
        mission,
        enabled=True,
        cta_label="Start",
    )
    assert day_from_home.reflection_active is True
    reflection = vm_mod._home_reflection(day_from_home, enabled=True)
    assert reflection.is_active
    assert len(reflection.prompts) == 3
    assert reflection.headline


def test_home_reflection_fields_isolated_when_flag_off():
    vm = home_vm(_snap(), unified_journey=False)
    assert vm.reflection_active is False
    assert vm.reflection_state == ""
    assert vm.reflection_prompts == ()
    assert vm.session_outcome_summary == ""
    assert vm.day_complete is False
