"""Timeline evolution and comparison coverage."""

from __future__ import annotations

import pytest

from app.application.student_twin.timeline_service import TimelineService
from tests.application.student_twin.helpers import make_engine, success_events
from tests.domain.student_twin.helpers import make_event


@pytest.mark.parametrize("steps", list(range(1, 26)))
def test_timeline_event_ids_grow(steps):
    engine = make_engine()
    twin = engine.create_twin("l1", twin_id="t1")
    snaps = [engine.domain_snapshot(twin)]
    for i in range(steps):
        twin = engine.ingest_evidence(twin, make_event(f"e{i}", day=1 + (i % 28)))
        snaps.append(engine.domain_snapshot(twin))
    evolution = TimelineService.event_ids_evolution(snaps)
    assert len(evolution) == steps + 1
    assert len(evolution[-1]) == steps
    for earlier, later in zip(evolution, evolution[1:]):
        assert len(later) == len(earlier) + 1
        assert earlier == later[:-1]


@pytest.mark.parametrize("n", list(range(1, 21)))
def test_comparison_evidence_added(n):
    engine = make_engine()
    twin = engine.create_twin("l1", twin_id="t1")
    baseline = engine.domain_snapshot(twin)
    twin = engine.ingest_many(twin, success_events(n))
    current = engine.domain_snapshot(twin)
    comparison = engine.compare(baseline, current)
    assert comparison.evidence_added == n
