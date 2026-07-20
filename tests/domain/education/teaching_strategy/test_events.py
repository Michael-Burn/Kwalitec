"""Domain event tests for Teaching Strategy."""

from __future__ import annotations

import pytest

from domain.education.foundation.enums import TeachingStrategyType
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import TeachingStrategyId
from domain.education.teaching_strategy import (
    EffectivenessLevel,
    StrategyRevisionKind,
    TeachingStrategyRevised,
    TeachingStrategySelected,
)
from tests.domain.education.teaching_strategy.conftest import make_strategy


def test_select_emits_selected_event() -> None:
    strategy = make_strategy()
    strategy.select()
    events = strategy.pull_events()
    assert len(events) == 1
    event = events[0]
    assert isinstance(event, TeachingStrategySelected)
    assert event.primary_strategy is TeachingStrategyType.WORKED_EXAMPLE
    assert event.intention_count == 1
    assert event.secondary_count == 0


def test_revise_emits_revised_event() -> None:
    strategy = make_strategy(select=True)
    strategy.pull_events()
    strategy.revise(
        rationale=strategy.rationale.with_statement(
            "Updated educational justification after new evidence"
        )
    )
    events = strategy.pull_events()
    assert len(events) == 1
    assert isinstance(events[0], TeachingStrategyRevised)
    assert events[0].revision_kind is StrategyRevisionKind.RATIONALE_AMENDED


def test_selected_event_immutable_and_validated() -> None:
    event = TeachingStrategySelected(
        strategy_id=TeachingStrategyId("ts-e1"),
        student_id="student-ada",
        primary_strategy=TeachingStrategyType.ANALOGY,
        effectiveness_level=EffectivenessLevel.HIGH,
        intention_count=1,
        diagnosis_count=1,
        hypothesis_count=0,
        secondary_count=0,
    )
    assert event.primary_strategy is TeachingStrategyType.ANALOGY
    with pytest.raises(EducationalInvariantViolation):
        TeachingStrategySelected(
            strategy_id=TeachingStrategyId("ts-e2"),
            student_id="student-ada",
            primary_strategy=TeachingStrategyType.ANALOGY,
            effectiveness_level=EffectivenessLevel.HIGH,
            intention_count=0,
            diagnosis_count=1,
            hypothesis_count=0,
            secondary_count=0,
        )


def test_revised_event_requires_revision_kind() -> None:
    event = TeachingStrategyRevised(
        strategy_id=TeachingStrategyId("ts-e3"),
        student_id="student-ada",
        primary_strategy=TeachingStrategyType.WORKED_EXAMPLE,
        effectiveness_level=EffectivenessLevel.MODERATE,
        revision_kind=StrategyRevisionKind.RETIRED,
        secondary_count=2,
    )
    assert event.revision_kind is StrategyRevisionKind.RETIRED


def test_pull_events_clears_pending() -> None:
    strategy = make_strategy(select=True)
    first = strategy.pull_events()
    second = strategy.pull_events()
    assert len(first) == 1
    assert second == []


def test_compose_and_retire_emit_revised() -> None:
    strategy = make_strategy(
        primary_strategy=TeachingStrategyType.WORKED_EXAMPLE,
        intention_type=__import__(
            "domain.education.foundation.enums", fromlist=["TeachingIntentionType"]
        ).TeachingIntentionType.INCREASE_PROCEDURAL_FLUENCY,
        select=True,
    )
    strategy.pull_events()
    strategy.compose(
        (
            TeachingStrategyType.PROGRESSIVE_SCAFFOLDING,
            TeachingStrategyType.FADED_GUIDANCE,
        )
    )
    events = strategy.pull_events()
    assert events[0].revision_kind is StrategyRevisionKind.SECONDARIES_COMPOSED
    strategy.retire(reason="arc complete")
    retired = strategy.pull_events()
    assert retired[0].revision_kind is StrategyRevisionKind.RETIRED
