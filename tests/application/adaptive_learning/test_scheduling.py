"""Revision scheduling and urgency matrices."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest

from app.application.adaptive_learning.revision_scheduler import RevisionScheduler
from app.domain.adaptive_learning.revision_window import RevisionUrgency
from tests.domain.adaptive_learning.helpers import make_candidate

PRIORITIES = [i / 10 for i in range(11)]
EXAMS = [0.0, 0.5, 1.0]
AS_OF = datetime(2026, 7, 18, 12, 0, tzinfo=UTC)


@pytest.mark.parametrize("priority", PRIORITIES)
@pytest.mark.parametrize("exam", EXAMS)
def test_urgency_mapping_stable(priority, exam):
    a = RevisionScheduler.urgency_for(priority, exam_proximity=exam)
    b = RevisionScheduler.urgency_for(priority, exam_proximity=exam)
    assert a is b
    assert isinstance(a, RevisionUrgency)


@pytest.mark.parametrize("n", range(1, 8))
def test_schedule_respects_max_windows(n):
    candidates = [
        make_candidate(f"t{i}", priority=0.9 - i * 0.05, retention=0.2)
        for i in range(6)
    ]
    windows = RevisionScheduler.schedule(
        candidates,
        as_of=AS_OF,
        exam_proximity=0.5,
        max_windows=n,
    )
    assert len(windows) == min(n, len(candidates))


@pytest.mark.parametrize("exam", EXAMS)
def test_schedule_orders_by_priority(exam):
    candidates = [
        make_candidate("low", priority=0.3, retention=0.7),
        make_candidate("high", priority=0.9, retention=0.1),
        make_candidate("mid", priority=0.55, retention=0.4),
    ]
    windows = RevisionScheduler.schedule(
        candidates,
        as_of=AS_OF,
        exam_proximity=exam,
        max_windows=3,
    )
    assert windows[0].topic_id == "high"
    assert windows[0].priority_score >= windows[-1].priority_score


@pytest.mark.parametrize("urgency", list(RevisionUrgency))
def test_urgency_offset_non_negative(urgency):
    assert RevisionScheduler.URGENCY_OFFSET_HOURS[urgency] >= 0.0


@pytest.mark.parametrize("priority", [0.2, 0.5, 0.85, 0.95])
def test_window_start_after_or_at_as_of(priority):
    candidates = [make_candidate("t1", priority=priority, retention=0.2)]
    windows = RevisionScheduler.schedule(candidates, as_of=AS_OF, max_windows=1)
    assert windows[0].suggested_start >= AS_OF
    assert windows[0].suggested_end > windows[0].suggested_start


@pytest.mark.parametrize("day_offset", range(0, 14))
def test_schedule_uses_as_of_clock(day_offset):
    when = AS_OF + timedelta(days=day_offset)
    candidates = [make_candidate("t1", priority=0.9, retention=0.1)]
    windows = RevisionScheduler.schedule(candidates, as_of=when, max_windows=1)
    assert windows[0].suggested_start >= when
