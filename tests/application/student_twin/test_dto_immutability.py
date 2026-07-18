"""DTO immutability for student_twin application projections."""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from app.application.student_twin.dto.comparison_snapshot import ComparisonSnapshot
from app.application.student_twin.dto.evidence_summary import EvidenceSummary
from app.application.student_twin.dto.learner_snapshot import LearnerSnapshot
from app.application.student_twin.dto.mastery_summary import MasterySummary
from app.application.student_twin.dto.readiness_summary import ReadinessSummary
from app.application.student_twin.dto.recommendation_snapshot import (
    RecommendationExplanation,
    RecommendationSnapshot,
)
from app.application.student_twin.dto.twin_snapshot import TwinSnapshotDTO
from tests.application.student_twin.helpers import make_engine, success_events


@pytest.mark.parametrize(
    "factory,field",
    [
        (lambda: EvidenceSummary(), "total_events"),
        (lambda: MasterySummary(), "overall_score"),
        (lambda: ReadinessSummary(), "readiness_score"),
        (lambda: RecommendationSnapshot(), "overall_confidence"),
        (lambda: LearnerSnapshot(learner_id="l1"), "learner_id"),
        (
            lambda: ComparisonSnapshot.create(
                twin_id="t1",
                baseline_version="1.0.0",
                current_version="1.0.1",
                mastery_delta=0.1,
                readiness_delta=0.05,
                confidence_delta=0.02,
                retention_delta=0.01,
                evidence_added=1,
            ),
            "twin_id",
        ),
        (
            lambda: RecommendationExplanation(
                recommendation_id="r1",
                kind="take_break",
                topic_id=None,
                evidence_ids=(),
                rationale="x",
                expected_benefit="y",
                confidence="low",
                priority=0.5,
            ),
            "priority",
        ),
    ],
)
def test_dto_frozen(factory, field):
    obj = factory()
    with pytest.raises((FrozenInstanceError, AttributeError, TypeError)):
        setattr(obj, field, getattr(obj, field))


def test_twin_snapshot_dto_from_engine():
    engine = make_engine()
    twin = engine.create_twin("l1", twin_id="t1")
    twin = engine.ingest_many(twin, success_events(3))
    dto = engine.snapshot(twin)
    assert isinstance(dto, TwinSnapshotDTO)
    with pytest.raises((FrozenInstanceError, AttributeError, TypeError)):
        setattr(dto, "twin_id", "mutated")
