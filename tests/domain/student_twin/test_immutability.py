"""Immutability tests for student_twin domain types."""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from app.domain.student_twin.learning_history import LearningHistory
from app.domain.student_twin.mastery_state import MasteryState, TopicMasteryRecord
from app.domain.student_twin.recommendation_state import (
    Recommendation,
    RecommendationKind,
)
from app.domain.student_twin.twin_version import TwinVersion
from tests.domain.student_twin.helpers import make_event, make_twin


@pytest.mark.parametrize(
    "factory,field",
    [
        (lambda: make_twin(), "version"),
        (lambda: make_event(), "event_id"),
        (lambda: TwinVersion.initial(), "major"),
        (lambda: LearningHistory.empty(), "events"),
        (lambda: MasteryState.empty(), "overall_score"),
        (lambda: TopicMasteryRecord.create("t1", 0.5), "mastery_score"),
        (lambda: Recommendation.create(
            "r1", RecommendationKind.TAKE_BREAK
        ), "priority"),
    ],
)
def test_domain_objects_are_frozen(factory, field):
    obj = factory()
    with pytest.raises((FrozenInstanceError, AttributeError, TypeError)):
        setattr(obj, field, getattr(obj, field))


def test_history_append_does_not_mutate_original():
    h = LearningHistory.empty()
    h2 = h.append(make_event("e1"))
    assert h.event_count == 0
    assert h2.event_count == 1


def test_twin_with_evidence_preserves_prior():
    twin = make_twin()
    twin2 = twin.with_evidence(make_event("e1"))
    assert twin.history.is_empty
    assert twin2.version != twin.version
