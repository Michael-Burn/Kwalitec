"""Large parametrized matrix for Student Digital Twin application."""

from __future__ import annotations

import pytest

from app.application.student_twin.mastery_calculator import MasteryCalculator
from app.application.student_twin.policies.mastery_policy import MasteryPolicy
from app.domain.student_twin.evidence_type import EvidenceType
from tests.application.student_twin.helpers import make_engine, success_events
from tests.domain.student_twin.helpers import make_event

TOPICS = [f"topic-{i}" for i in range(1, 41)]
EVIDENCE_TYPES = [
    "activity_completed",
    "assessment_outcome",
    "practice_result",
    "reflection",
    "self_assessment",
    "recall_performance",
    "confidence_rating",
    "time_on_task",
    "session_completion",
    "mission_completion",
    "revision_outcome",
]
SCORES = [i / 10 for i in range(0, 11)]
DAYS = list(range(1, 29))
SUBJECTS = [
    "CS1", "CM1", "CB2", "FS1", "FM1", "CP1", "CP2", "SA1", "SA2", "CB1",
] * 5


@pytest.mark.parametrize("topic_id", TOPICS)
def test_engine_ingests_topic(topic_id):
    engine = make_engine()
    twin = engine.create_twin("l1", twin_id=f"t-{topic_id}")
    event = make_event("e1", topic_id=topic_id, outcome="success", score=0.8)
    twin = engine.ingest_evidence(twin, event)
    assert twin.mastery.record_for(topic_id) is not None


@pytest.mark.parametrize("etype", EVIDENCE_TYPES)
def test_engine_ingests_each_evidence_type(etype):
    engine = make_engine()
    twin = engine.create_twin("l1", twin_id=f"t-{etype}")
    topic = None if etype in {"session_completion", "time_on_task"} else "topic-1"
    event = make_event("e1", etype, topic_id=topic, outcome="success")
    twin = engine.ingest_evidence(twin, event)
    assert twin.event_count == 1


@pytest.mark.parametrize("score", SCORES)
def test_mastery_delta_with_scores(score):
    event = make_event(
        "e1",
        EvidenceType.ASSESSMENT_OUTCOME,
        score=score,
        outcome=None,
    )
    delta = MasteryPolicy.delta_for(event)
    assert isinstance(delta, float)


@pytest.mark.parametrize("day", DAYS)
def test_events_across_calendar_days(day):
    event = make_event("e1", day=day)
    assert event.occurred_at is not None
    mastery = MasteryCalculator.calculate([event])
    assert mastery.topic_count in (0, 1)


@pytest.mark.parametrize("n", list(range(1, 51)))
def test_success_streak_mastery_monotonic(n):
    events = success_events(n)
    mastery = MasteryCalculator.calculate(events)
    assert 0.0 <= mastery.overall_score <= 1.0
    if n >= 2:
        prev = MasteryCalculator.calculate(events[:-1]).overall_score
        assert mastery.overall_score >= prev - 1e-12
        assert mastery.overall_score <= 1.0


@pytest.mark.parametrize(
    "learner_id,subject",
    [(f"L{i}", code) for i, code in enumerate(SUBJECTS, start=1)],
)
def test_create_twins_many_subjects(learner_id, subject):
    engine = make_engine()
    twin = engine.create_twin(
        learner_id,
        twin_id=f"twin-{learner_id}",
        subject_code=subject,
    )
    assert twin.identity.subject_code == subject
    dto = engine.snapshot(twin)
    assert dto.subject_code == subject


@pytest.mark.parametrize("n", list(range(0, 21)))
def test_empty_and_growing_snapshots(n):
    engine = make_engine()
    twin = engine.create_twin("l1", twin_id="t1")
    if n:
        twin = engine.ingest_many(twin, success_events(n))
    dto = engine.snapshot(twin)
    assert dto.evidence.total_events == n
    assert len(dto.history_event_ids) == n


@pytest.mark.parametrize(
    "outcome",
    [
        "pass",
        "fail",
        "success",
        "incorrect",
        "partial",
        "strong",
        "weak",
        "high",
        "low",
    ],
)
def test_recommendation_always_explainable(outcome):
    engine = make_engine()
    twin = engine.create_twin("l1", twin_id="t1")
    twin = engine.ingest_evidence(
        twin,
        make_event(
            "e1",
            EvidenceType.ASSESSMENT_OUTCOME,
            outcome=outcome,
            score=None,
        ),
    )
    for rec in twin.recommendations.recommendations:
        assert rec.rationale is not None
        assert rec.expected_benefit
        assert rec.confidence is not None
