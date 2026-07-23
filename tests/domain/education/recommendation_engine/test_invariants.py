"""Invariant and immutability tests for Recommendation Engine."""

from __future__ import annotations

from dataclasses import FrozenInstanceError
from datetime import UTC, datetime

import pytest

from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.recommendation_engine import (
    RecommendationCategory,
    RecommendationEngine,
    RecommendationPriority,
    RecommendationSet,
    RecommendationSetId,
    RecommendationTarget,
    SubjectId,
)
from tests.domain.education.recommendation_engine.conftest import (
    make_competency_assessment,
    make_knowledge_graph,
    make_mastery_assessment,
    make_student_state,
)

AS_OF = datetime(2026, 7, 23, 12, 0, 0, tzinfo=UTC)


def test_recommendation_set_collections_are_tuples() -> None:
    state = make_student_state()
    assessment = make_mastery_assessment(
        competencies=(make_competency_assessment(mastery_magnitude=0.4),),
        assessed_at=AS_OF,
    )
    result = RecommendationEngine.recommend(
        state,
        assessment,
        (),
        make_knowledge_graph(),
        set_id=RecommendationSetId("set-inv-001"),
        recommended_at=AS_OF,
    )
    assert isinstance(result.recommendations, tuple)
    assert isinstance(result.constraints, tuple)
    with pytest.raises((TypeError, AttributeError)):
        result.recommendations.append(None)  # type: ignore[attr-defined]


def test_value_object_immutability() -> None:
    target = RecommendationTarget(subject_id=SubjectId("algebra"))
    with pytest.raises(FrozenInstanceError):
        target.subject_id = SubjectId("calculus")  # type: ignore[misc]


def test_priority_rejects_bool() -> None:
    with pytest.raises(EducationalInvariantViolation):
        RecommendationPriority(True)  # noqa: FBT003


def test_aggregate_rejects_bad_student_id() -> None:
    with pytest.raises(EducationalInvariantViolation):
        RecommendationSet(
            RecommendationSetId("set-001"),
            " ",
            AS_OF,
        )


def test_aggregate_rejects_non_datetime() -> None:
    with pytest.raises(EducationalInvariantViolation):
        RecommendationSet(
            RecommendationSetId("set-001"),
            "student-001",
            "not-a-datetime",  # type: ignore[arg-type]
        )


def test_all_categories_are_educational_intent() -> None:
    values = {category.value for category in RecommendationCategory}
    assert "review_concept" in values
    assert "study_prerequisite" in values
    assert "attempt_checkpoint" in values
    assert "strengthen_weak_area" in values
    assert "delay_advanced_topic" in values
    assert "continue_current_mission" in values
    assert "increase_revision_frequency" in values
    assert "reduce_revision_frequency" in values
    assert "revisit_foundation" in values
    assert "maintain_mastery" in values
    assert "focus_competency" in values
    assert "prepare_assessment" in values
    assert "consolidate_knowledge" in values
