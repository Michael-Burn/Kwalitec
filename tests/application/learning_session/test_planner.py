"""Tests for LearningSessionPlanner."""

from __future__ import annotations

import pytest

from app.application.learning_session.exceptions import PlanningError
from app.application.learning_session.planner import LearningSessionPlanner
from app.domain.learning_journey.entities.learning_objective import ObjectiveKind
from app.domain.learning_journey.value_objects.effort_estimate import EffortEstimate
from app.domain.learning_journey.value_objects.session_state import SessionState
from tests.application.learning_session.helpers import (
    make_evidence,
    make_journey,
    make_objective,
    make_session,
)


class TestLearningSessionPlanner:
    def test_plan_basic(self):
        planner = LearningSessionPlanner(id_factory=lambda: "abc")
        journey = make_journey(objectives=[make_objective()])
        plan = planner.plan(journey=journey, objectives=list(journey.objectives))
        assert plan.session_id == "sess-abc"
        assert plan.journey_id == journey.journey_id
        assert plan.topic_id == "topic-a"
        assert plan.objective_ids == ("obj-1",)
        assert plan.sequence_index == 0
        assert "no_mastery_claim" in plan.rationale_tags

    def test_plan_uses_explicit_session_id(self):
        planner = LearningSessionPlanner()
        plan = planner.plan(
            journey=make_journey(),
            session_id="custom-sess",
            objectives=[make_objective()],
        )
        assert plan.session_id == "custom-sess"

    def test_plan_next_sequence_after_existing(self):
        planner = LearningSessionPlanner(id_factory=lambda: "n")
        journey = make_journey(
            sessions=[
                make_session("s0", sequence_index=0),
                make_session("s1", sequence_index=2, state=SessionState.COMPLETED),
            ]
        )
        plan = planner.plan(journey=journey)
        assert plan.sequence_index == 3

    def test_plan_explicit_sequence(self):
        planner = LearningSessionPlanner(id_factory=lambda: "n")
        plan = planner.plan(journey=make_journey(), sequence_index=5)
        assert plan.sequence_index == 5

    def test_plan_rejects_negative_sequence(self):
        planner = LearningSessionPlanner()
        with pytest.raises(PlanningError):
            planner.plan(journey=make_journey(), sequence_index=-1)

    def test_plan_requires_topic(self):
        planner = LearningSessionPlanner()
        journey = make_journey(topic_id="topic-a")
        # Force empty topic via override
        with pytest.raises(PlanningError):
            planner.plan(journey=journey, topic_id="  ")

    def test_plan_effort_override(self):
        planner = LearningSessionPlanner(id_factory=lambda: "e")
        plan = planner.plan(
            journey=make_journey(),
            estimated_effort=EffortEstimate.EXTENSIVE,
        )
        assert plan.estimated_effort == EffortEstimate.EXTENSIVE

    def test_plan_activities_from_objective_kind(self):
        planner = LearningSessionPlanner(id_factory=lambda: "a")
        plan = planner.plan(
            journey=make_journey(),
            objectives=[make_objective(kind=ObjectiveKind.APPLY)],
        )
        assert "worked_example" in plan.recommended_activities

    def test_plan_counts_previous_evidence(self):
        planner = LearningSessionPlanner(id_factory=lambda: "p")
        prior = [make_evidence("je-1"), make_evidence("je-2", evidence_id="ev-2")]
        plan = planner.plan(journey=make_journey(), previous_evidence=prior)
        assert plan.previous_evidence_count == 2

    def test_plan_uses_journey_evidence_when_none_supplied(self):
        planner = LearningSessionPlanner(id_factory=lambda: "j")
        journey = make_journey(evidence=[make_evidence()])
        plan = planner.plan(journey=journey, previous_evidence=None)
        assert plan.previous_evidence_count == 1

    def test_plan_from_session(self):
        planner = LearningSessionPlanner()
        session = make_session(effort=EffortEstimate.HIGH)
        plan = planner.plan_from_session(
            session,
            topic_id="topic-a",
            objectives=[make_objective()],
        )
        assert plan.session_id == session.session_id
        assert plan.estimated_effort == EffortEstimate.HIGH
        assert plan.topic_id == "topic-a"

    def test_plan_from_session_without_objectives_uses_session_objective(self):
        planner = LearningSessionPlanner()
        session = make_session(objective_id="obj-9")
        plan = planner.plan_from_session(session, topic_id="topic-a")
        assert plan.objective_ids == ("obj-9",)

    def test_plan_topic_override(self):
        planner = LearningSessionPlanner(id_factory=lambda: "t")
        plan = planner.plan(journey=make_journey(), topic_id="topic-b")
        assert plan.topic_id == "topic-b"

    def test_plan_immutable(self):
        planner = LearningSessionPlanner(id_factory=lambda: "i")
        plan = planner.plan(journey=make_journey())
        with pytest.raises(Exception):
            plan.session_id = "mutated"  # type: ignore[misc]
