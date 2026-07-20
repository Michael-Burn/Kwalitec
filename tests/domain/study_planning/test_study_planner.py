"""Study planning engine tests (EDU-002).

Covers: scheduling, ordering, recovery, determinism, duration allocation,
and architecture purity.
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.priority import PriorityScoreBand
from domain.education.priority.enums import UrgencyLevel
from domain.mission_generation import (
    MissionDurationBand,
    MissionPriorityBand,
    MissionSpecification,
)
from domain.mission_generation.mission_priority import MissionPriority
from domain.study_planning import (
    AvailabilityWindow,
    LearnerAvailability,
    SessionKind,
    StudyPlan,
    StudyPlanner,
    StudySchedule,
    StudySession,
    StudySessionId,
    max_session_minutes,
    recovery_minutes_for,
    review_offsets_for,
)
from tests.domain.mission_generation.conftest import (
    generate_mission,
    make_aligned_strategy,
)
from tests.domain.study_planning.conftest import (
    make_availability,
    make_planning_priority,
    make_trajectory,
    plan_study,
)

PACKAGE_ROOT = (
    Path(__file__).resolve().parents[3] / "src" / "domain" / "study_planning"
)

FORBIDDEN_MODULES = frozenset(
    {
        "flask",
        "sqlalchemy",
        "alembic",
        "jinja2",
        "wtforms",
        "requests",
        "httpx",
        "celery",
        "redis",
        "boto3",
        "openai",
        "anthropic",
        "random",
        "secrets",
        "uuid",
        "calendar",
        "zoneinfo",
    }
)

FORBIDDEN_PREFIXES = (
    "flask.",
    "sqlalchemy.",
    "app.",
    "openai.",
    "anthropic.",
)


def _imported_modules(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                names.add(alias.name)
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.add(node.module)
    return names


def test_package_exports_required_types() -> None:
    from domain import study_planning as package

    for name in (
        "StudyPlan",
        "StudySession",
        "StudyDay",
        "StudyCalendar",
        "StudyPlanner",
        "StudySchedule",
        "LearnerAvailability",
    ):
        assert hasattr(package, name), name


@pytest.mark.parametrize(
    "path",
    sorted(PACKAGE_ROOT.glob("*.py")),
    ids=lambda p: p.name,
)
def test_no_forbidden_infrastructure_or_ai_imports(path: Path) -> None:
    imported = _imported_modules(path)
    for name in imported:
        assert name not in FORBIDDEN_MODULES, f"{path.name} imports {name}"
        assert not any(
            name == prefix.rstrip(".") or name.startswith(prefix)
            for prefix in FORBIDDEN_PREFIXES
        ), f"{path.name} imports {name}"


def test_planner_source_has_no_randomness_or_calendar_apis() -> None:
    source = (PACKAGE_ROOT / "study_planner.py").read_text(encoding="utf-8")
    for token in (
        "import random",
        "from random",
        "import uuid",
        "from uuid",
        "import secrets",
        "from secrets",
        "datetime.now",
        "time.time",
        "import calendar",
        "from calendar",
        "zoneinfo",
    ):
        assert token not in source


def test_plan_returns_complete_study_plan() -> None:
    plan = plan_study()

    assert isinstance(plan, StudyPlan)
    assert plan.student_id == "student-ada"
    assert len(plan.mission_ids) == 1
    assert plan.session_count() >= 1
    assert any(s.is_work() for s in plan.ordered_sessions)
    assert plan.estimated_completion.total_work_minutes > 0
    assert len(plan.review_windows) == 2
    assert plan.priority_id.value == "prio-001"
    assert "Study plan schedules missions" in plan.educational_rationale
    assert len(plan.calendar.days) >= 1
    assert plan.schedule.length == plan.estimated_completion.session_count


def test_plan_rejects_student_mismatch() -> None:
    with pytest.raises(EducationalInvariantViolation, match="student_id"):
        StudyPlanner.plan(
            (generate_mission(),),
            make_availability(student_id="student-other"),
            make_trajectory(),
            make_planning_priority(),
        )


def test_plan_rejects_insufficient_availability() -> None:
    mission = generate_mission(with_secondaries=True)
    tiny = LearnerAvailability.of(
        "student-ada",
        AvailabilityWindow(day_index=0, available_minutes=1),
    )
    with pytest.raises(EducationalInvariantViolation, match="insufficient"):
        StudyPlanner.plan(
            (mission,),
            tiny,
            make_trajectory(),
            make_planning_priority(),
        )


def test_plan_rejects_empty_missions() -> None:
    with pytest.raises(EducationalInvariantViolation, match="at least one"):
        StudyPlanner.plan(
            (),
            make_availability(),
            make_trajectory(),
            make_planning_priority(),
        )


def test_scheduling_respects_daily_capacity() -> None:
    plan = plan_study(
        availability=make_availability(day_count=10, minutes_per_day=30)
    )
    for day in plan.calendar.days:
        assert day.allocated_minutes() <= day.available_minutes


def test_scheduling_places_sessions_on_relative_days() -> None:
    plan = plan_study()
    day_indices = [s.day_index for s in plan.ordered_sessions]
    assert day_indices == sorted(day_indices)
    assert all(day >= 0 for day in day_indices)


def test_work_sessions_precede_recovery_and_review() -> None:
    plan = plan_study(with_secondaries=True)
    kinds = [s.kind for s in plan.ordered_sessions]
    last_work = max(i for i, k in enumerate(kinds) if k is SessionKind.WORK)
    first_non_work = next(
        (i for i, k in enumerate(kinds) if k is not SessionKind.WORK),
        None,
    )
    if first_non_work is not None:
        assert last_work < first_non_work or all(
            k is SessionKind.WORK for k in kinds[: first_non_work + 1]
        )
    # Stronger: no work after the first recovery/review.
    non_work_indexes = [
        i for i, k in enumerate(kinds) if k is not SessionKind.WORK
    ]
    if non_work_indexes:
        assert all(
            kinds[i] is not SessionKind.WORK
            for i in range(non_work_indexes[0], len(kinds))
        )


def test_mission_ordering_prefers_higher_priority() -> None:
    low = generate_mission(
        strategy=make_aligned_strategy(strategy_id="ts-low", with_secondaries=False)
    )
    high = generate_mission(
        strategy=make_aligned_strategy(strategy_id="ts-high", with_secondaries=False)
    )
    # Rebuild with explicit mission priorities via object replacement is awkward;
    # generate two missions and override priority bands through MissionSpecification
    # fields by constructing plans from differently prioritised missions.
    low_mission = MissionSpecification(
        mission_id=low.mission_id,
        student_id=low.student_id,
        objective=low.objective,
        duration=low.duration,
        priority=MissionPriority.of(
            MissionPriorityBand.LOW, UrgencyLevel.ROUTINE
        ),
        sequence=low.sequence,
        success_criteria=low.success_criteria,
        completion_conditions=low.completion_conditions,
        educational_rationale=low.educational_rationale,
        twin_id=low.twin_id,
        diagnosis_id=low.diagnosis_id,
        priority_id=low.priority_id,
        strategy_id=low.strategy_id,
    )
    high_mission = MissionSpecification(
        mission_id=high.mission_id,
        student_id=high.student_id,
        objective=high.objective,
        duration=high.duration,
        priority=MissionPriority.of(
            MissionPriorityBand.CRITICAL, UrgencyLevel.IMMEDIATE
        ),
        sequence=high.sequence,
        success_criteria=high.success_criteria,
        completion_conditions=high.completion_conditions,
        educational_rationale=high.educational_rationale,
        twin_id=high.twin_id,
        diagnosis_id=high.diagnosis_id,
        priority_id=high.priority_id,
        strategy_id=high.strategy_id,
    )
    # Distinct mission ids required.
    assert low_mission.mission_id != high_mission.mission_id

    plan = plan_study(missions=(low_mission, high_mission))
    work = plan.schedule.work_sessions()
    assert work[0].mission_id == high_mission.mission_id
    assert work[-1].mission_id == low_mission.mission_id or any(
        s.mission_id == low_mission.mission_id for s in work
    )
    first_low = next(
        i for i, s in enumerate(work) if s.mission_id == low_mission.mission_id
    )
    first_high = next(
        i for i, s in enumerate(work) if s.mission_id == high_mission.mission_id
    )
    assert first_high < first_low


def test_recovery_allocated_for_medium_and_long_missions() -> None:
    plan = plan_study(with_secondaries=True)
    mission = generate_mission(with_secondaries=True)
    expected = recovery_minutes_for(mission.duration.band)
    if expected > 0:
        assert len(plan.recovery_allocations) == 1
        assert plan.recovery_allocations[0].minutes == expected
        assert plan.schedule.total_recovery_minutes() == expected
        assert any(s.is_recovery() for s in plan.ordered_sessions)
    else:
        assert plan.recovery_allocations == ()


def test_recovery_increases_after_intervention_trajectory() -> None:
    baseline = plan_study(trajectory=make_trajectory(with_intervention=False))
    boosted = plan_study(trajectory=make_trajectory(with_intervention=True))
    assert boosted.schedule.total_recovery_minutes() == (
        baseline.schedule.total_recovery_minutes() + 3
    )


def test_review_windows_follow_priority_offsets() -> None:
    priority = make_planning_priority(score_band=PriorityScoreBand.HIGH)
    plan = plan_study(priority=priority)
    offsets = review_offsets_for(PriorityScoreBand.HIGH)
    assert len(plan.review_windows) == len(offsets)
    assert tuple(w.offset_from_completion for w in plan.review_windows) == offsets
    assert len(plan.schedule.review_sessions()) == len(offsets)


def test_review_offsets_relax_for_lower_priority() -> None:
    high = review_offsets_for(PriorityScoreBand.HIGH)
    low = review_offsets_for(PriorityScoreBand.LOW)
    assert high[0] < low[0]


def test_duration_allocation_matches_mission_work_minutes() -> None:
    mission = generate_mission(with_secondaries=True)
    plan = plan_study(missions=(mission,))
    assert plan.schedule.total_work_minutes() == mission.duration.planned_minutes
    assert (
        plan.estimated_completion.total_work_minutes
        == mission.duration.planned_minutes
    )


def test_duration_allocation_respects_max_session_ceiling() -> None:
    mission = generate_mission(with_secondaries=True)
    # Force multi-session by capping daily capacity below mission total but
    # above max session... actually cap below max so chunks are smaller.
    availability = make_availability(day_count=15, minutes_per_day=20)
    plan = plan_study(missions=(mission,), availability=availability)
    for session in plan.schedule.work_sessions():
        assert session.allocated_minutes <= max_session_minutes()
        assert session.allocated_minutes <= 20


def test_work_sessions_claim_mission_tasks() -> None:
    mission = generate_mission(with_secondaries=True)
    plan = plan_study(missions=(mission,))
    claimed: list[str] = []
    for session in plan.schedule.work_sessions():
        assert session.mission_task_ids
        for task_id in session.mission_task_ids:
            claimed.append(task_id.value)
    # Every mission task should appear at least once across work sessions.
    for task in mission.sequence.tasks:
        assert task.task_id.value in claimed


def test_same_inputs_always_generate_same_plan() -> None:
    mission = generate_mission(with_secondaries=True)
    availability = make_availability()
    trajectory = make_trajectory()
    priority = make_planning_priority()

    first = StudyPlanner.plan((mission,), availability, trajectory, priority)
    second = StudyPlanner.plan((mission,), availability, trajectory, priority)

    assert first == second
    assert first.plan_id == second.plan_id
    assert first.schedule == second.schedule
    assert first.calendar == second.calendar
    assert first.estimated_completion == second.estimated_completion
    assert first.review_windows == second.review_windows
    assert first.recovery_allocations == second.recovery_allocations
    assert first.educational_rationale == second.educational_rationale


def test_repeated_planning_is_stable_across_many_runs() -> None:
    mission = generate_mission(with_secondaries=True)
    availability = make_availability()
    trajectory = make_trajectory(with_intervention=True)
    priority = make_planning_priority(score_band=PriorityScoreBand.CRITICAL)
    plans = [
        StudyPlanner.plan((mission,), availability, trajectory, priority)
        for _ in range(20)
    ]
    assert all(p == plans[0] for p in plans)


def test_plan_id_is_deterministic_from_inputs() -> None:
    plan = plan_study()
    assert plan.plan_id.value.startswith("plan-prio-001-")
    assert "avail-" in plan.plan_id.value


def test_estimated_completion_reflects_schedule() -> None:
    plan = plan_study()
    est = plan.estimated_completion
    assert est.total_minutes == (
        est.total_work_minutes
        + est.total_review_minutes
        + est.total_recovery_minutes
    )
    assert est.plan_complete_day_index >= est.work_complete_day_index
    assert est.session_count == plan.schedule.length


def test_study_schedule_rejects_gapped_indexes() -> None:
    mission = generate_mission(with_secondaries=False)
    task_id = mission.sequence.tasks[0].task_id
    with pytest.raises(EducationalInvariantViolation, match="contiguous"):
        StudySchedule.of(
            StudySession(
                session_id=StudySessionId("sess-a"),
                sequence_index=1,
                day_index=0,
                kind=SessionKind.WORK,
                mission_id=mission.mission_id,
                allocated_minutes=10,
                label="a",
                mission_task_ids=(task_id,),
            ),
            StudySession(
                session_id=StudySessionId("sess-b"),
                sequence_index=3,
                day_index=0,
                kind=SessionKind.WORK,
                mission_id=mission.mission_id,
                allocated_minutes=10,
                label="b",
                mission_task_ids=(task_id,),
            ),
        )


def test_recovery_catalogue_by_duration_band() -> None:
    assert recovery_minutes_for(MissionDurationBand.SHORT) == 0
    assert recovery_minutes_for(MissionDurationBand.MEDIUM) == 5
    assert recovery_minutes_for(MissionDurationBand.LONG) == 10
    assert recovery_minutes_for(MissionDurationBand.LONG, trajectory_bonus=3) == 13


def test_daily_schedule_exposed_on_plan() -> None:
    plan = plan_study()
    days = plan.daily_schedule()
    assert days == plan.calendar.days
    assert any(not day.is_empty() for day in days)
