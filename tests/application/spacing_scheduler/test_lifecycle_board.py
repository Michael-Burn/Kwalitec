"""Spacing Scheduler lifecycle output: upcoming / due / overdue as calendar data."""

from __future__ import annotations

import ast
from datetime import date
from pathlib import Path

from app.application.spacing_scheduler import (
    InMemorySpacingStateStore,
    SchedulingStatus,
    SpacingIntervalPolicy,
    SpacingSchedulerService,
)
from app.application.spacing_scheduler.board import build_revision_board

LEARNER = "lifecycle-learner"
PKG_DUE = "PKG-DUE"
PKG_OVERDUE = "PKG-OVERDUE"
PKG_UPCOMING = "PKG-UPCOMING"


def test_scheduler_reports_upcoming_due_overdue_as_pure_calendar_output():
    """Requirement 1: lifecycle states are calendar-derived; no arbitration types."""
    service = SpacingSchedulerService(store=InMemorySpacingStateStore())
    as_of = date(2026, 9, 5)

    # upcoming: completed today -> due tomorrow
    service.record_completed_exposure(
        learner_id=LEARNER,
        package_id=PKG_UPCOMING,
        completed_on=date(2026, 9, 5),
    )
    # due: completed yesterday -> due today
    service.record_completed_exposure(
        learner_id=LEARNER,
        package_id=PKG_DUE,
        completed_on=date(2026, 9, 4),
    )
    # overdue: completed three days ago -> due two days ago
    service.record_completed_exposure(
        learner_id=LEARNER,
        package_id=PKG_OVERDUE,
        completed_on=date(2026, 9, 2),
    )

    board = service.revision_board(learner_id=LEARNER, as_of=as_of)
    assert [e.package_id for e in board.upcoming] == [PKG_UPCOMING]
    assert [e.package_id for e in board.due] == [PKG_DUE]
    assert [e.package_id for e in board.overdue] == [PKG_OVERDUE]
    # due_now is overdue first, then due (backward compatible actionable list)
    assert [e.package_id for e in board.due_now] == [PKG_OVERDUE, PKG_DUE]
    assert board.due[0].decision.status is SchedulingStatus.DUE
    assert board.overdue[0].decision.status is SchedulingStatus.OVERDUE
    assert board.upcoming[0].decision.status is SchedulingStatus.NOT_DUE


def test_overdue_threshold_is_configurable_policy_not_hardcoded():
    """overdue_after_days lives on SpacingIntervalPolicy (default 1)."""
    policy = SpacingIntervalPolicy(overdue_after_days=3)
    service = SpacingSchedulerService(
        store=InMemorySpacingStateStore(),
        policy=policy,
    )
    # next_due_on = 2026-09-02; days past on 2026-09-04 = 2 < 3 → still DUE
    service.record_completed_exposure(
        learner_id=LEARNER,
        package_id=PKG_DUE,
        completed_on=date(2026, 9, 1),
    )
    still_due = service.evaluate(
        learner_id=LEARNER,
        package_id=PKG_DUE,
        as_of=date(2026, 9, 4),
    )
    assert still_due.status is SchedulingStatus.DUE

    overdue = service.evaluate(
        learner_id=LEARNER,
        package_id=PKG_DUE,
        as_of=date(2026, 9, 5),
    )
    assert overdue.status is SchedulingStatus.OVERDUE
    assert overdue.days_overdue == 3


def test_scheduler_modules_have_no_adaptive_or_arbitration_awareness():
    """Scheduler domain/application must not import adaptive arbitration."""
    roots = [
        Path("app/domain/spacing_scheduler"),
        Path("app/application/spacing_scheduler"),
    ]
    forbidden = (
        "adaptive_decision",
        "arbitration",
        "PolicyV1",
        "adaptive_review",
        "ArbitrationLabel",
    )
    for root in roots:
        for path in root.rglob("*.py"):
            source = path.read_text(encoding="utf-8")
            tree = ast.parse(source)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import | ast.ImportFrom):
                    mod = (
                        node.module
                        if isinstance(node, ast.ImportFrom)
                        else ",".join(a.name for a in node.names)
                    ) or ""
                    for name in forbidden:
                        assert name not in mod, f"{path} imports {mod}"
            for name in ("ArbitrationLabel", "arbitrate_sitting_precedence"):
                assert name not in source, f"{path} mentions {name}"


def test_build_revision_board_keeps_due_now_compatible():
    """Revision/composer can keep using due_now for both due and overdue."""
    svc = SpacingSchedulerService(store=InMemorySpacingStateStore())
    svc.record_completed_exposure(
        learner_id=LEARNER, package_id=PKG_DUE, completed_on=date(2026, 9, 4)
    )
    svc.record_completed_exposure(
        learner_id=LEARNER,
        package_id=PKG_OVERDUE,
        completed_on=date(2026, 9, 2),
    )
    board = build_revision_board(
        learner_id=LEARNER,
        as_of=date(2026, 9, 5),
        states=svc.list_states_for_learner(learner_id=LEARNER),
        evaluate=svc.evaluate,
    )
    assert board.has_due is True
    assert board.has_overdue is True
    assert {e.package_id for e in board.due_now} == {PKG_DUE, PKG_OVERDUE}
