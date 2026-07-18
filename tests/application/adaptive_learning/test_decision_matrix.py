"""Large decision consistency matrix across Twin topic configurations."""

from __future__ import annotations

import pytest

from tests.application.adaptive_learning.helpers import (
    make_curriculum,
    make_engine,
    make_journey,
    make_snapshot,
)

MASTERY = [0.1, 0.5, 0.9]
RETENTION = [0.1, 0.5, 0.9]
IMPORTANCE = [0.2, 0.9]
EXAM = [0.0, 1.0]


@pytest.mark.parametrize("mastery", MASTERY)
@pytest.mark.parametrize("retention", RETENTION)
def test_decide_is_deterministic_for_topic_scores(mastery, retention):
    engine = make_engine(seed="d")
    snap = make_snapshot(
        topics=[
            {
                "id": "topic-1",
                "mastery": mastery,
                "retention": retention,
                "knowledge": (mastery + retention) / 2,
                "confidence": 0.4,
                "severity": max(0.1, 1.0 - min(mastery, retention)),
            }
        ]
    )
    a = engine.decide(
        snap,
        journey_position=make_journey(),
        curriculum_context=make_curriculum(),
    )
    b = engine.decide(
        snap,
        journey_position=make_journey(),
        curriculum_context=make_curriculum(),
    )
    assert a.priority_score == b.priority_score
    assert a.primary_topic_id == b.primary_topic_id
    assert a.estimated_study_minutes == b.estimated_study_minutes
    assert a.explanation.rationale == b.explanation.rationale
    assert a.roi == b.roi


@pytest.mark.parametrize("importance", IMPORTANCE)
@pytest.mark.parametrize("exam", EXAM)
@pytest.mark.parametrize("retention", [0.2, 0.5, 0.8])
def test_curriculum_context_determinism(importance, exam, retention):
    engine = make_engine(seed="c")
    snap = make_snapshot(
        topics=[
            {
                "id": "topic-1",
                "mastery": 0.35,
                "retention": retention,
                "knowledge": 0.4,
                "confidence": 0.35,
                "severity": 0.6,
            }
        ]
    )
    ctx = make_curriculum(
        importance={"topic-1": importance},
        exam_proximity=exam,
        struggle={"topic-1": 0.4},
    )
    a = engine.decide(snap, curriculum_context=ctx)
    b = engine.decide(snap, curriculum_context=ctx)
    assert a.priority_score == b.priority_score
    assert a.revision_plan.plan_id  # non-empty


@pytest.mark.parametrize("n_topics", range(1, 6))
@pytest.mark.parametrize("events_per_day", [0.0, 1.0, 3.0, 8.0])
def test_multi_topic_decisions(n_topics, events_per_day):
    engine = make_engine(seed="m")
    topics = [
        {
            "id": f"topic-{i}",
            "mastery": 0.2 + i * 0.1,
            "retention": 0.15 + i * 0.1,
            "knowledge": 0.25,
            "confidence": 0.3,
            "severity": 0.7 - i * 0.05,
        }
        for i in range(n_topics)
    ]
    snap = make_snapshot(topics=topics, events_per_day=events_per_day)
    decision = engine.decide(
        snap,
        journey_position=make_journey(topics[0]["id"]),
        curriculum_context=make_curriculum(
            importance={t["id"]: 0.5 + i * 0.05 for i, t in enumerate(topics)}
        ),
    )
    assert decision.intervention_type.value == "revision"
    if decision.has_intervention:
        assert decision.primary_topic_id in {t["id"] for t in topics}
        assert decision.explanation.has_evidence or decision.evidence_ids


@pytest.mark.parametrize("progress", [0.0, 0.25, 0.5, 0.75, 1.0])
def test_journey_progress_accepted(progress):
    from app.application.adaptive_learning.decision_engine import JourneyPositionInput

    journey = JourneyPositionInput.create(
        journey_id="j1",
        current_topic_id="topic-1",
        progress_ratio=progress,
    )
    engine = make_engine()
    decision = engine.decide(make_snapshot(), journey_position=journey)
    assert decision.learner_id == "learner-1"
