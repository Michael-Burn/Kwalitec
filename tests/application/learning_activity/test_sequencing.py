"""Activity sequencing, planner, and sequence builder tests."""

from __future__ import annotations

import pytest

from app.application.learning_activity.dto.activity_plan import ActivityPlanItem
from app.application.learning_activity.exceptions import PlanningError
from app.application.learning_activity.planner import ActivityPlanner
from app.application.learning_activity.policies.sequencing_policy import (
    SequencingPolicy,
)
from app.application.learning_activity.sequence_builder import SequenceBuilder
from app.domain.learning_activity.value_objects.activity_state import ActivityState
from app.domain.learning_activity.value_objects.activity_type import ActivityType
from tests.application.learning_activity.helpers import make_engine, make_plan


class TestSequencingPolicy:
    def test_default_types_arc(self):
        types = SequencingPolicy.default_types()
        assert types[0] is ActivityType.INTRODUCTION
        assert ActivityType.REFLECTION in types
        assert ActivityType.SUMMARY in types

    def test_rejects_content_and_ai(self):
        assert SequencingPolicy.rejects_content_generation() is True
        assert SequencingPolicy.rejects_ai() is True

    @pytest.mark.parametrize(
        ("tag", "expected"),
        [
            ("worked_example", ActivityType.WORKED_EXAMPLE),
            ("guided_practice", ActivityType.GUIDED_PRACTICE),
            ("independent_attempt", ActivityType.INDEPENDENT_PRACTICE),
            ("spaced_review", ActivityType.SPACED_RECALL),
            ("brief_reflection_prep", ActivityType.REFLECTION),
            ("summary_recall", ActivityType.SUMMARY),
            ("unknown_tag_xyz", ActivityType.CUSTOM),
            ("", ActivityType.CUSTOM),
        ],
    )
    def test_type_from_tag(self, tag, expected):
        assert SequencingPolicy.type_from_tag(tag) is expected

    def test_types_from_tags_dedupes_preserving_order(self):
        types = SequencingPolicy.types_from_tags(
            ("worked_example", "guided_practice", "worked_example")
        )
        assert types == (
            ActivityType.WORKED_EXAMPLE,
            ActivityType.GUIDED_PRACTICE,
        )

    def test_types_from_empty_tags_uses_default(self):
        defaults = SequencingPolicy.default_types()
        assert SequencingPolicy.types_from_tags(None) == defaults
        assert SequencingPolicy.types_from_tags(()) == defaults

    def test_order_types_preserve_input(self):
        types = (
            ActivityType.SUMMARY,
            ActivityType.INTRODUCTION,
        )
        assert SequencingPolicy.order_types(types) == types

    def test_order_types_by_priority(self):
        types = (
            ActivityType.SUMMARY,
            ActivityType.INTRODUCTION,
            ActivityType.CUSTOM,
        )
        ordered = SequencingPolicy.order_types(types, preserve_input_order=False)
        assert ordered[0] is ActivityType.INTRODUCTION
        assert ordered[-1] is ActivityType.SUMMARY

    def test_order_types_empty_uses_default(self):
        assert SequencingPolicy.order_types(None) == SequencingPolicy.default_types()

    def test_ensure_bookends(self):
        types = SequencingPolicy.ensure_bookends(
            (ActivityType.CONCEPT_LEARNING,),
            require_introduction=True,
            require_summary=True,
            require_reflection=True,
        )
        assert types[0] is ActivityType.INTRODUCTION
        assert ActivityType.REFLECTION in types
        assert types[-1] is ActivityType.SUMMARY

    def test_ensure_bookends_does_not_duplicate(self):
        types = SequencingPolicy.ensure_bookends(
            (ActivityType.INTRODUCTION, ActivityType.SUMMARY),
            require_introduction=True,
            require_summary=True,
        )
        assert types.count(ActivityType.INTRODUCTION) == 1
        assert types.count(ActivityType.SUMMARY) == 1

    @pytest.mark.parametrize("activity_type", list(ActivityType))
    def test_priority_defined_for_all_types(self, activity_type):
        assert isinstance(SequencingPolicy.priority(activity_type), int)


class TestActivityPlanner:
    def test_plan_requires_session_id(self):
        with pytest.raises(PlanningError, match="session_id"):
            ActivityPlanner().plan(session_id="")

    def test_plan_default_arc(self):
        plan = ActivityPlanner().plan(session_id="sess-1")
        assert len(plan.items) == len(SequencingPolicy.default_types())
        assert "source=default_arc" in plan.rationale_tags

    def test_plan_from_explicit_types(self):
        plan = ActivityPlanner().plan(
            session_id="sess-1",
            activity_types=(ActivityType.REVIEW, "spaced_recall"),
        )
        assert [i.activity_type for i in plan.items] == [
            ActivityType.REVIEW,
            ActivityType.SPACED_RECALL,
        ]
        assert "source=explicit_types" in plan.rationale_tags

    def test_plan_from_tags(self):
        plan = ActivityPlanner().plan(
            session_id="sess-1",
            activity_tags=("worked_example", "guided_practice"),
        )
        assert plan.items[0].activity_type is ActivityType.WORKED_EXAMPLE
        assert "source=activity_tags" in plan.rationale_tags

    def test_plan_from_items(self):
        items = (
            ActivityPlanItem(
                activity_type=ActivityType.CUSTOM,
                title="Lab",
                requested_id="custom-1",
            ),
        )
        plan = ActivityPlanner().plan(session_id="sess-1", items=items)
        assert plan.items[0].requested_id == "custom-1"
        assert "source=explicit_items" in plan.rationale_tags

    def test_plan_rejects_empty_items(self):
        with pytest.raises(PlanningError, match="empty"):
            ActivityPlanner().plan(session_id="sess-1", items=())

    def test_plan_with_bookends(self):
        plan = ActivityPlanner().plan(
            session_id="sess-1",
            activity_types=(ActivityType.CONCEPT_LEARNING,),
            require_introduction=True,
            require_summary=True,
            require_reflection=True,
        )
        types = [i.activity_type for i in plan.items]
        assert types[0] is ActivityType.INTRODUCTION
        assert ActivityType.REFLECTION in types
        assert ActivityType.SUMMARY in types

    def test_plan_frozen(self):
        plan = ActivityPlanner().plan(session_id="sess-1")
        with pytest.raises(Exception):
            plan.session_id = "x"  # type: ignore[misc]


class TestSequenceBuilder:
    def test_build_orders_by_plan(self):
        plan = make_plan(
            types=(
                ActivityType.INTRODUCTION,
                ActivityType.KNOWLEDGE_CHECK,
                ActivityType.SUMMARY,
            )
        )
        sequence = SequenceBuilder(id_factory=lambda: "x").build(plan)
        assert sequence.length == 3
        assert sequence.activities[0].activity_type is ActivityType.INTRODUCTION
        assert sequence.activities[1].sequence_index == 1
        assert all(a.state is ActivityState.NOT_STARTED for a in sequence.activities)

    def test_build_rejects_empty_plan(self):
        from app.application.learning_activity.dto.activity_plan import ActivityPlan

        plan = ActivityPlan(
            session_id="s", journey_id=None, items=(), rationale_tags=()
        )
        with pytest.raises(PlanningError, match="empty"):
            SequenceBuilder().build(plan)

    def test_build_rejects_duplicate_requested_ids(self):
        plan = make_plan(types=(ActivityType.REVIEW, ActivityType.SUMMARY))
        # Rebuild with duplicate requested ids via items
        from app.application.learning_activity.dto.activity_plan import ActivityPlan

        items = (
            ActivityPlanItem(
                activity_type=ActivityType.REVIEW, requested_id="dup"
            ),
            ActivityPlanItem(
                activity_type=ActivityType.SUMMARY, requested_id="dup"
            ),
        )
        plan = ActivityPlan(
            session_id="sess-1",
            journey_id=None,
            items=items,
            rationale_tags=(),
        )
        with pytest.raises(PlanningError, match="duplicate"):
            SequenceBuilder().build(plan)

    def test_build_uses_requested_ids(self):
        from app.application.learning_activity.dto.activity_plan import ActivityPlan

        items = (
            ActivityPlanItem(
                activity_type=ActivityType.INTRODUCTION, requested_id="intro-1"
            ),
        )
        plan = ActivityPlan(
            session_id="sess-1",
            journey_id=None,
            items=items,
            rationale_tags=(),
        )
        sequence = SequenceBuilder().build(plan)
        assert sequence.activities[0].activity_id == "intro-1"

    def test_sequence_activity_by_id(self):
        sequence = SequenceBuilder(id_factory=lambda: "x").build(make_plan())
        first = sequence.activities[0]
        assert sequence.activity_by_id(first.activity_id) is first
        assert sequence.activity_by_id("missing") is None

    def test_sequence_activity_at(self):
        sequence = SequenceBuilder(id_factory=lambda: "x").build(make_plan())
        assert sequence.activity_at(0) is sequence.activities[0]
        assert sequence.activity_at(-1) is None
        assert sequence.activity_at(99) is None

    def test_sequence_with_activity(self):
        sequence = SequenceBuilder(id_factory=lambda: "x").build(make_plan())
        first = sequence.activities[0].apply_transition(
            __import__(
                "app.domain.learning_activity.value_objects.activity_state",
                fromlist=["ActivityTransitionEvent"],
            ).ActivityTransitionEvent.START
        )
        updated = sequence.with_activity(first)
        assert updated.activities[0].state is ActivityState.ACTIVE
        assert sequence.activities[0].state is ActivityState.NOT_STARTED

    def test_sequence_with_activity_unknown_raises(self):
        sequence = SequenceBuilder(id_factory=lambda: "x").build(make_plan())
        foreign = __import__(
            "tests.application.learning_activity.helpers",
            fromlist=["make_activity"],
        ).make_activity("foreign")
        with pytest.raises(ValueError, match="not in sequence"):
            sequence.with_activity(foreign)

    def test_engine_create_sequence_deterministic(self):
        engine = make_engine()
        a = engine.create_sequence(
            session_id="sess-1",
            activity_types=(ActivityType.REVIEW, ActivityType.SUMMARY),
            sequence_id="seq-a",
        )
        b = engine.create_sequence(
            session_id="sess-1",
            activity_types=(ActivityType.REVIEW, ActivityType.SUMMARY),
            sequence_id="seq-b",
        )
        assert [x.activity_type for x in a.sequence.activities] == [
            x.activity_type for x in b.sequence.activities
        ]
