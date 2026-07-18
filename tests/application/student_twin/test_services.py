"""Service unit tests for student_twin calculators and estimators."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from app.application.student_twin.confidence_calculator import ConfidenceCalculator
from app.application.student_twin.evidence_aggregator import EvidenceAggregator
from app.application.student_twin.learning_velocity_service import (
    LearningVelocityService,
)
from app.application.student_twin.mastery_calculator import MasteryCalculator
from app.application.student_twin.readiness_estimator import ReadinessEstimator
from app.application.student_twin.recommendation_service import RecommendationService
from app.application.student_twin.retention_estimator import RetentionEstimator
from app.application.student_twin.weakness_analyser import WeaknessAnalyser
from tests.application.student_twin.helpers import mixed_events, success_events
from tests.domain.student_twin.helpers import make_event, make_events

AS_OF = datetime(2026, 7, 18, tzinfo=UTC)


def test_evidence_aggregator_counts():
    events = success_events(5) + mixed_events()
    profile = EvidenceAggregator.aggregate(events)
    assert profile.total_events == len(events)
    assert profile.topic_count >= 1


def test_mastery_calculator_positive_path():
    mastery = MasteryCalculator.calculate(success_events(8))
    assert mastery.overall_score > 0
    assert mastery.record_for("topic-1") is not None


def test_mastery_calculator_negative_path():
    events = make_events(5, outcome="fail")
    mastery = MasteryCalculator.calculate(events)
    # starting at 0 with negative deltas stays at 0
    assert mastery.overall_score == 0.0


def test_confidence_increases_with_volume():
    low = ConfidenceCalculator.calculate(success_events(2))
    high = ConfidenceCalculator.calculate(success_events(12))
    assert high.overall_score >= low.overall_score


def test_retention_decays_with_time():
    events = success_events(5)
    mastery = MasteryCalculator.calculate(events)
    recent = RetentionEstimator.calculate(
        events, mastery, as_of=datetime(2026, 7, 10, tzinfo=UTC)
    )
    later = RetentionEstimator.calculate(
        events, mastery, as_of=datetime(2026, 9, 1, tzinfo=UTC)
    )
    assert later.overall_score <= recent.overall_score


def test_readiness_blend():
    events = success_events(10)
    mastery = MasteryCalculator.calculate(events)
    confidence = ConfidenceCalculator.calculate(events)
    retention = RetentionEstimator.calculate(events, mastery, as_of=AS_OF)
    readiness = ReadinessEstimator.calculate(mastery, retention, confidence)
    assert 0.0 <= readiness.readiness_score <= 1.0


def test_weakness_and_recommendations():
    events = [
        make_event("w1", outcome="fail", score=0.1, day=1),
        make_event("w2", outcome="fail", score=0.2, day=2),
    ]
    mastery = MasteryCalculator.calculate(events)
    confidence = ConfidenceCalculator.calculate(events)
    retention = RetentionEstimator.calculate(events, mastery, as_of=AS_OF)
    weaknesses = WeaknessAnalyser.analyse(mastery, retention, confidence)
    velocity = LearningVelocityService.calculate(events, as_of=AS_OF)
    readiness = ReadinessEstimator.calculate(mastery, retention, confidence)
    recs = RecommendationService.recommend(
        mastery, retention, readiness, weaknesses, velocity
    )
    assert not recs.is_empty
    primary = recs.primary
    assert primary.rationale
    assert primary.expected_benefit
    assert primary.evidence_ids


@pytest.mark.parametrize("window", [1.0, 3.0, 7.0, 14.0, 30.0])
def test_velocity_windows(window):
    events = success_events(5)
    velocity = LearningVelocityService.calculate(
        events, as_of=AS_OF, window_days=window
    )
    assert velocity.window_days == window
