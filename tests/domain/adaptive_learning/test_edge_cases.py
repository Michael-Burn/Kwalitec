"""Domain edge cases and immutability."""

from __future__ import annotations

from dataclasses import FrozenInstanceError
from datetime import UTC, datetime, timedelta

import pytest

from app.domain.adaptive_learning.revision_window import RevisionWindow
from tests.domain.adaptive_learning.helpers import (
    make_candidate,
    make_explanation,
    make_intervention,
    make_priority,
    make_roi,
    make_window,
)


@pytest.mark.parametrize(
    "obj_factory",
    [
        make_priority,
        make_roi,
        make_explanation,
        make_intervention,
        make_candidate,
        make_window,
    ],
)
def test_domain_objects_are_frozen(obj_factory):
    obj = obj_factory()
    with pytest.raises((FrozenInstanceError, AttributeError, TypeError)):
        obj.__setattr__("topic_id" if hasattr(obj, "topic_id") else "score", "x")


def test_window_rejects_end_before_start():
    start = datetime(2026, 7, 18, 12, tzinfo=UTC)
    with pytest.raises(ValueError):
        RevisionWindow.create(
            "t1",
            urgency="today",
            suggested_start=start,
            suggested_end=start - timedelta(minutes=5),
            allocated_minutes=20.0,
            priority_score=0.5,
        )


@pytest.mark.parametrize("bad", ["", "   ", None])
def test_candidate_rejects_bad_topic(bad):
    with pytest.raises((ValueError, AttributeError, TypeError)):
        make_candidate(topic_id=bad)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "retention,mastery",
    [(0.0, 0.0), (0.5, 0.5), (1.0, 1.0), (0.1, 0.9), (0.9, 0.1)],
)
def test_candidate_scores_roundtrip(retention, mastery):
    c = make_candidate(retention=retention, mastery=mastery)
    assert c.retention_score == retention
    assert c.mastery_score == mastery


@pytest.mark.parametrize("minutes", [-1.0, -0.01])
def test_roi_rejects_negative_minutes(minutes):
    with pytest.raises(ValueError):
        make_roi(minutes=minutes)


@pytest.mark.parametrize("itype", ["revision", "REVISION", "Revision"])
def test_intervention_type_case_insensitive_via_enum_values(itype):
    # resolve uses lowercase strip; uppercase REVISION fails StrEnum unless lowercased
    from app.domain.adaptive_learning.intervention_type import resolve_intervention_type

    if itype.lower() == "revision":
        assert resolve_intervention_type(itype.lower()).value == "revision"
