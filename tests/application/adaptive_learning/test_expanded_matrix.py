"""Expanded priority × ROI × context matrices to harden determinism."""

from __future__ import annotations

import pytest

from app.application.adaptive_learning.priority_calculator import PriorityCalculator
from app.application.adaptive_learning.revision_planner import RevisionPlanner
from app.application.adaptive_learning.roi_estimator import ROIEstimator
from tests.application.adaptive_learning.helpers import (
    make_curriculum,
    make_engine,
    make_journey,
    make_snapshot,
)

RET = [round(i * 0.1, 2) for i in range(11)]  # 0.0 .. 1.0
MAST = [0.0, 0.5, 1.0]
IMP = [0.0, 0.5, 1.0]
EXAM = [0.0, 1.0]


@pytest.mark.parametrize("retention", RET)
@pytest.mark.parametrize("mastery", MAST)
def test_priority_grid_retention_mastery(retention, mastery):
    p = PriorityCalculator.calculate(
        retention_score=retention,
        mastery_score=mastery,
        confidence=0.45,
        curriculum_importance=0.5,
        exam_proximity=0.25,
    )
    assert 0.0 <= p.score <= 1.0
    roi = ROIEstimator.estimate(
        priority=p,
        retention_risk=p.retention_risk,
        mastery_gap=p.mastery_gap,
        curriculum_importance=0.5,
    )
    assert roi.estimated_study_minutes >= 10.0


@pytest.mark.parametrize("importance", IMP)
@pytest.mark.parametrize("exam", EXAM)
@pytest.mark.parametrize("struggle", IMP)
@pytest.mark.parametrize("prereq", IMP)
def test_priority_context_grid(importance, exam, struggle, prereq):
    p = PriorityCalculator.calculate(
        retention_score=0.35,
        mastery_score=0.4,
        confidence=0.35,
        curriculum_importance=importance,
        prerequisite_criticality=prereq,
        historical_struggle=struggle,
        exam_proximity=exam,
        events_per_day=2.0,
        mastery_delta=-0.2,
    )
    q = PriorityCalculator.calculate(
        retention_score=0.35,
        mastery_score=0.4,
        confidence=0.35,
        curriculum_importance=importance,
        prerequisite_criticality=prereq,
        historical_struggle=struggle,
        exam_proximity=exam,
        events_per_day=2.0,
        mastery_delta=-0.2,
    )
    assert p == q


@pytest.mark.parametrize("retention", [0.1, 0.3, 0.5, 0.7, 0.9])
@pytest.mark.parametrize("mastery", [0.1, 0.3, 0.5, 0.7, 0.9])
@pytest.mark.parametrize("importance", [0.2, 0.6, 1.0])
def test_engine_grid_decisions(retention, mastery, importance):
    engine = make_engine(seed="g")
    snap = make_snapshot(
        topics=[
            {
                "id": "topic-1",
                "mastery": mastery,
                "retention": retention,
                "knowledge": (mastery + retention) / 2,
                "confidence": 0.4,
                "severity": max(0.05, 1 - min(mastery, retention)),
            }
        ]
    )
    ctx = make_curriculum(importance={"topic-1": importance}, exam_proximity=0.4)
    d1 = engine.decide(snap, journey_position=make_journey(), curriculum_context=ctx)
    d2 = engine.decide(snap, journey_position=make_journey(), curriculum_context=ctx)
    assert d1.priority_score == d2.priority_score
    assert d1.estimated_study_minutes == d2.estimated_study_minutes
    assert d1.explanation.expected_educational_benefit
    assert d1.intervention_type.value == "revision"


@pytest.mark.parametrize("topic_count", range(1, 7))
@pytest.mark.parametrize("exam", [0.0, 0.3, 0.7, 1.0])
def test_planner_candidate_counts(topic_count, exam):
    topics = [
        {
            "id": f"t{i}",
            "mastery": 0.15 + (i % 5) * 0.1,
            "retention": 0.1 + (i % 4) * 0.1,
            "knowledge": 0.2,
            "confidence": 0.3,
            "severity": 0.75,
        }
        for i in range(topic_count)
    ]
    snap = make_snapshot(topics=topics)
    candidates = RevisionPlanner.build_candidates(
        knowledge=snap.knowledge,
        mastery=snap.mastery,
        retention=snap.retention,
        confidence=snap.confidence,
        weaknesses=snap.weaknesses,
        velocity=snap.velocity,
        topic_importance={t["id"]: 0.6 for t in topics},
        exam_proximity=exam,
        current_topic_id=topics[0]["id"],
    )
    assert len(candidates) <= topic_count
    # ranking stable
    scores = [c.priority.score for c in candidates]
    assert scores == sorted(scores, reverse=True)
