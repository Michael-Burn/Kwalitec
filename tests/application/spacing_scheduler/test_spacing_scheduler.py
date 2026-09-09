"""Spacing Scheduler isolation tests (roadmap item 2).

Proves the capability correct alone: no Revision, daily composer, or UI.
"""

from __future__ import annotations

import inspect
from dataclasses import fields
from datetime import date, timedelta

import pytest

from app.application.spacing_scheduler import (
    ExposureKind,
    InMemorySpacingStateStore,
    SchedulingStatus,
    SpacingIntervalPolicy,
    SpacingSchedulerService,
    SpacingState,
    get_spacing_scheduler,
    reset_canonical_spacing_scheduler_for_tests,
)
from app.domain.spacing_scheduler.scheduler import SpacingScheduler
from app.domain.spacing_scheduler.types import (
    FORBIDDEN_SIGNAL_NAMES,
    ReviewableUnitId,
    SchedulingDecision,
)

PACKAGE_A = "CS1-EP001-PKG-1.1-PURPOSE-FUNCTION"
LEARNER = "learner-spacing-1"


@pytest.fixture
def service() -> SpacingSchedulerService:
    return SpacingSchedulerService(store=InMemorySpacingStateStore())


def test_completion_creates_correct_initial_scheduling_state(
    service: SpacingSchedulerService,
) -> None:
    """Requirement 1: first completion sets initial interval and next due."""
    completed_on = date(2026, 9, 1)
    state = service.record_completed_exposure(
        learner_id=LEARNER,
        package_id=PACKAGE_A,
        completed_on=completed_on,
    )

    assert state.unit_id == PACKAGE_A
    assert state.last_completed_on == completed_on
    assert state.current_interval_days == 1
    assert state.next_due_on == date(2026, 9, 2)
    assert state.review_cycle_count == 0
    assert state.last_exposure_kind is ExposureKind.INITIAL_COMPLETION

    decision = service.evaluate(
        learner_id=LEARNER,
        package_id=PACKAGE_A,
        as_of=date(2026, 9, 1),
    )
    assert decision.status is SchedulingStatus.NOT_DUE
    assert decision.next_due_on == date(2026, 9, 2)


def test_three_review_cycles_widen_then_shorten_after_miss(
    service: SpacingSchedulerService,
) -> None:
    """Requirement 2: three successive cycles plus late/missed behaviour."""
    day0 = date(2026, 9, 1)

    # Cycle 0: initial completion -> interval 1, due day0+1
    s0 = service.record_completed_exposure(
        learner_id=LEARNER,
        package_id=PACKAGE_A,
        completed_on=day0,
    )
    assert s0.current_interval_days == 1
    assert s0.next_due_on == day0 + timedelta(days=1)

    # Cycle 1: on-time at due -> ladder advances 1 -> 3
    day1 = s0.next_due_on
    s1 = service.record_completed_exposure(
        learner_id=LEARNER,
        package_id=PACKAGE_A,
        completed_on=day1,
    )
    assert s1.last_exposure_kind is ExposureKind.ON_TIME_REVIEW
    assert s1.current_interval_days == 3
    assert s1.next_due_on == day1 + timedelta(days=3)
    assert s1.review_cycle_count == 1

    # Cycle 2: on-time again -> ladder advances 3 -> 7
    day2 = s1.next_due_on
    s2 = service.record_completed_exposure(
        learner_id=LEARNER,
        package_id=PACKAGE_A,
        completed_on=day2,
    )
    assert s2.last_exposure_kind is ExposureKind.ON_TIME_REVIEW
    assert s2.current_interval_days == 7
    assert s2.next_due_on == day2 + timedelta(days=7)
    assert s2.review_cycle_count == 2

    # Cycle 3a: late completion after due -> ladder retreats 7 -> 3
    late_day = s2.next_due_on + timedelta(days=2)
    s_late = service.record_completed_exposure(
        learner_id=LEARNER,
        package_id=PACKAGE_A,
        completed_on=late_day,
    )
    assert s_late.last_exposure_kind is ExposureKind.LATE_REVIEW
    assert s_late.current_interval_days == 3
    assert s_late.next_due_on == late_day + timedelta(days=3)

    # Fresh unit: three on-time cycles then an explicit miss shortens interval
    pkg_b = "CS1-EP001-PKG-REV-SAMPLING-DISTRIBUTIONS"
    t0 = date(2026, 10, 1)
    service.record_completed_exposure(
        learner_id=LEARNER, package_id=pkg_b, completed_on=t0
    )
    t1 = service.get_state(learner_id=LEARNER, package_id=pkg_b).next_due_on
    service.record_completed_exposure(
        learner_id=LEARNER, package_id=pkg_b, completed_on=t1
    )
    t2 = service.get_state(learner_id=LEARNER, package_id=pkg_b).next_due_on
    service.record_completed_exposure(
        learner_id=LEARNER, package_id=pkg_b, completed_on=t2
    )
    before_miss = service.get_state(learner_id=LEARNER, package_id=pkg_b)
    assert before_miss.current_interval_days == 7
    miss_day = before_miss.next_due_on + timedelta(days=3)
    missed = service.record_missed_review(
        learner_id=LEARNER,
        package_id=pkg_b,
        as_of=miss_day,
    )
    assert missed.last_exposure_kind is ExposureKind.MISSED_REVIEW
    assert missed.current_interval_days == 3
    assert missed.next_due_on == miss_day + timedelta(days=3)
    assert missed.last_completed_on == before_miss.last_completed_on


def test_canonical_source_returns_same_state_from_any_caller() -> None:
    """Requirement 3: one canonical store queried the same way everywhere."""
    reset_canonical_spacing_scheduler_for_tests()
    try:
        from_home = get_spacing_scheduler()
        from_revision = get_spacing_scheduler()
        assert from_home is from_revision

        completed_on = date(2026, 9, 8)
        from_home.record_completed_exposure(
            learner_id=LEARNER,
            package_id=PACKAGE_A,
            completed_on=completed_on,
        )

        state_a = from_home.get_state(
            learner_id=LEARNER, package_id=PACKAGE_A
        )
        state_b = from_revision.get_state(
            learner_id=LEARNER, package_id=PACKAGE_A
        )
        decision_a = from_home.evaluate(
            learner_id=LEARNER,
            package_id=PACKAGE_A,
            as_of=completed_on + timedelta(days=1),
        )
        decision_b = from_revision.evaluate(
            learner_id=LEARNER,
            package_id=PACKAGE_A,
            as_of=completed_on + timedelta(days=1),
        )

        assert state_a == state_b
        assert decision_a == decision_b
        assert decision_a.status is SchedulingStatus.DUE
    finally:
        reset_canonical_spacing_scheduler_for_tests()


def test_interface_cannot_accept_or_produce_performance_signals(
    service: SpacingSchedulerService,
) -> None:
    """Requirement 4: structural refusal of mastery/weakness-style signals.

    Roadmap item 5 must not carve exceptions: ``confidence`` and every other
    forbidden name remain rejected on record/evaluate exactly as before.
    ``ladder_step_delta`` is a calendar-only param and is not a forbidden name.
    """
    expected_forbidden = frozenset(
        {
            "mastery",
            "mastery_score",
            "estimated_knowledge",
            "estimated_mastery",
            "weak",
            "weakness",
            "weak_score",
            "accuracy",
            "performance",
            "priority",
            "priority_score",
            "urgency",
            "confidence",
            "score",
            "roi",
        }
    )
    assert FORBIDDEN_SIGNAL_NAMES == expected_forbidden
    assert "confidence" in FORBIDDEN_SIGNAL_NAMES
    assert "ladder_step_delta" not in FORBIDDEN_SIGNAL_NAMES

    public_types = (SpacingState, SchedulingDecision, ReviewableUnitId)
    for cls in public_types:
        names = {f.name.lower() for f in fields(cls)}
        assert not (names & FORBIDDEN_SIGNAL_NAMES), cls.__name__

    for method_name in (
        "record_completed_exposure",
        "record_missed_review",
        "evaluate",
        "explain",
    ):
        method = getattr(service, method_name)
        params = set(inspect.signature(method).parameters)
        assert not (params & FORBIDDEN_SIGNAL_NAMES), method_name

    forbidden_kwargs = {
        "mastery": 0.5,
        "mastery_score": 42.0,
        "estimated_knowledge": 0.4,
        "estimated_mastery": 0.4,
        "weak": True,
        "weakness": True,
        "weak_score": 0.2,
        "accuracy": 0.9,
        "performance": 0.8,
        "priority": 1,
        "priority_score": 1.0,
        "urgency": 1,
        "confidence": 4,
        "score": 10,
        "roi": 0.1,
    }
    for name, value in forbidden_kwargs.items():
        with pytest.raises(TypeError, match="performance signals"):
            service.record_completed_exposure(
                learner_id=LEARNER,
                package_id=PACKAGE_A,
                completed_on=date(2026, 9, 1),
                **{name: value},
            )
        with pytest.raises(TypeError, match="performance signals"):
            service.evaluate(
                learner_id=LEARNER,
                package_id=PACKAGE_A,
                as_of=date(2026, 9, 1),
                **{name: value},
            )
        with pytest.raises(TypeError, match="performance signals"):
            SpacingScheduler().apply_completed_exposure(
                learner_id=LEARNER,
                unit_id=PACKAGE_A,
                completed_on=date(2026, 9, 1),
                prior=None,
                **{name: value},
            )

    # Decision payloads expose only time/interval facts.
    service.record_completed_exposure(
        learner_id=LEARNER,
        package_id=PACKAGE_A,
        completed_on=date(2026, 9, 1),
    )
    decision = service.evaluate(
        learner_id=LEARNER,
        package_id=PACKAGE_A,
        as_of=date(2026, 9, 2),
    )
    decision_fields = {f.name.lower() for f in fields(decision)}
    assert not (decision_fields & FORBIDDEN_SIGNAL_NAMES)
    assert "explanation" in decision_fields


@pytest.mark.parametrize(
    ("delta", "expected_interval"),
    [
        (-1, 1),  # initial 1, then one step shorter, clamped at min
        (0, 1),
        (1, 3),  # initial 1, then one step longer → 3
    ],
)
def test_ladder_step_delta_applies_after_exposure_kind_and_clamps(
    service: SpacingSchedulerService,
    delta: int,
    expected_interval: int,
) -> None:
    """Calendar-only nudge after normal ladder move; respects ladder bounds."""
    completed_on = date(2026, 9, 1)
    state = service.record_completed_exposure(
        learner_id=LEARNER,
        package_id=PACKAGE_A,
        completed_on=completed_on,
        ladder_step_delta=delta,
    )
    assert state.current_interval_days == expected_interval
    assert state.next_due_on == completed_on + timedelta(days=expected_interval)


def test_ladder_step_delta_clamps_at_ladder_max(
    service: SpacingSchedulerService,
) -> None:
    """+1 at the top of the ladder must not invent days beyond the ladder."""
    day = date(2026, 9, 1)
    # Climb to the top of the default ladder (1 → 3 → 7 → 14 → 30).
    for days in (0, 1, 3, 7, 14):
        service.record_completed_exposure(
            learner_id=LEARNER,
            package_id=PACKAGE_A,
            completed_on=day + timedelta(days=days),
        )
    top = service.get_state(learner_id=LEARNER, package_id=PACKAGE_A)
    assert top is not None
    assert top.current_interval_days == 30

    nudged = service.record_completed_exposure(
        learner_id=LEARNER,
        package_id=PACKAGE_A,
        completed_on=day + timedelta(days=30),
        ladder_step_delta=1,
    )
    assert nudged.current_interval_days == 30
    assert nudged.next_due_on == day + timedelta(days=60)


def test_invalid_ladder_step_delta_rejected(
    service: SpacingSchedulerService,
) -> None:
    with pytest.raises(ValueError, match="ladder_step_delta"):
        service.record_completed_exposure(
            learner_id=LEARNER,
            package_id=PACKAGE_A,
            completed_on=date(2026, 9, 1),
            ladder_step_delta=2,
        )


def test_every_scheduling_decision_explains_itself(
    service: SpacingSchedulerService,
) -> None:
    """Requirement 5: plain, specific, queryable explanations."""
    never = service.evaluate(
        learner_id=LEARNER,
        package_id=PACKAGE_A,
        as_of=date(2026, 9, 1),
    )
    assert never.status is SchedulingStatus.NEVER_SCHEDULED
    assert "not scheduled" in never.explanation
    assert PACKAGE_A in never.explanation

    service.record_completed_exposure(
        learner_id=LEARNER,
        package_id=PACKAGE_A,
        completed_on=date(2026, 9, 1),
    )

    not_due = service.evaluate(
        learner_id=LEARNER,
        package_id=PACKAGE_A,
        as_of=date(2026, 9, 1),
    )
    assert not_due.status is SchedulingStatus.NOT_DUE
    assert "not yet due, next due in 1 day" in not_due.explanation
    assert "current interval is 1 day" in not_due.explanation
    assert service.explain(
        learner_id=LEARNER,
        package_id=PACKAGE_A,
        as_of=date(2026, 9, 1),
    ) == not_due.explanation

    due = service.evaluate(
        learner_id=LEARNER,
        package_id=PACKAGE_A,
        as_of=date(2026, 9, 2),
    )
    assert due.status is SchedulingStatus.DUE
    assert (
        "due because last completed 1 day ago, current interval is 1 day"
        in due.explanation
    )

    overdue = service.evaluate(
        learner_id=LEARNER,
        package_id=PACKAGE_A,
        as_of=date(2026, 9, 5),
    )
    assert overdue.status is SchedulingStatus.OVERDUE
    assert "overdue by 3 days" in overdue.explanation
    assert "was due on 2026-09-02" in overdue.explanation


def test_policy_is_configurable_without_changing_scheduler_code() -> None:
    """Interval ladder lives in policy, not hardcoded in callers."""
    policy = SpacingIntervalPolicy(
        initial_interval_days=2,
        interval_ladder_days=(2, 5, 11),
    )
    svc = SpacingSchedulerService(
        store=InMemorySpacingStateStore(),
        policy=policy,
    )
    state = svc.record_completed_exposure(
        learner_id=LEARNER,
        package_id=PACKAGE_A,
        completed_on=date(2026, 9, 1),
    )
    assert state.current_interval_days == 2
    assert state.next_due_on == date(2026, 9, 3)

    on_time = svc.record_completed_exposure(
        learner_id=LEARNER,
        package_id=PACKAGE_A,
        completed_on=date(2026, 9, 3),
    )
    assert on_time.current_interval_days == 5
