"""State machine matrix expansion for Curriculum Ingestion domain."""

from __future__ import annotations

import pytest

from app.domain.curriculum_ingestion.ingestion_state import (
    LAWFUL_INGESTION_TRANSITIONS,
    IngestionState,
    IngestionTransitionEvent,
    has_reached,
    is_terminal_ingestion_state,
    next_ingestion_state,
    pipeline_index,
)


@pytest.mark.parametrize(
    "start,event,end",
    [(s, e, t) for (s, e), t in LAWFUL_INGESTION_TRANSITIONS.items()],
)
def test_all_lawful_transitions(start, event, end):
    assert next_ingestion_state(start, event) is end
    assert next_ingestion_state(start.value, event.value) is end


@pytest.mark.parametrize("state", list(IngestionState))
@pytest.mark.parametrize("event", list(IngestionTransitionEvent))
def test_illegal_combinations_raise_or_succeed(state, event):
    key = (state, event)
    if key in LAWFUL_INGESTION_TRANSITIONS:
        assert next_ingestion_state(state, event) is LAWFUL_INGESTION_TRANSITIONS[key]
    else:
        with pytest.raises(ValueError):
            next_ingestion_state(state, event)


@pytest.mark.parametrize(
    "current,milestone,expected",
    [
        (IngestionState.COMPLETED, IngestionState.RECEIVED, True),
        (IngestionState.RECEIVED, IngestionState.COMPLETED, False),
        (IngestionState.VALIDATED, IngestionState.VALIDATED, True),
        (IngestionState.FAILED, IngestionState.RECEIVED, False),
        (IngestionState.PREVIEW_READY, IngestionState.NORMALIZED, True),
        (IngestionState.EXTRACTED, IngestionState.PREVIEW_READY, False),
    ],
)
def test_has_reached_matrix(current, milestone, expected):
    assert has_reached(current, milestone) is expected


@pytest.mark.parametrize("state", list(IngestionState))
def test_pipeline_index_bounds(state):
    idx = pipeline_index(state)
    if state is IngestionState.FAILED:
        assert idx == -1
    else:
        assert idx >= 0


@pytest.mark.parametrize("state", list(IngestionState))
def test_terminal_flags(state):
    terminal = is_terminal_ingestion_state(state)
    assert terminal is (state in {IngestionState.COMPLETED, IngestionState.FAILED})
