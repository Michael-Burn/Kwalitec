"""Session-length learning-objective batching."""

from __future__ import annotations

from app.application.curriculum_intelligence.objective_chunk import (
    select_objectives_for_session,
)
from app.domain.educational_runtime_engine.student_facing_identity import (
    format_learning_objective_label,
)


def test_select_objectives_fits_sixty_minute_budget():
    ids = [f"obj-{i}" for i in range(1, 11)]
    selected = select_objectives_for_session(ids, session_minutes=60)
    assert 1 <= len(selected) <= 3
    assert selected == tuple(ids[: len(selected)])


def test_select_objectives_one_lo_when_estimates_exceed_budget():
    ids = ["a", "b", "c"]
    selected = select_objectives_for_session(
        ids,
        session_minutes=60,
        objective_minutes={"a": 180, "b": 180, "c": 180},
    )
    assert selected == ("a",)


def test_select_objectives_always_returns_at_least_one():
    assert select_objectives_for_session(["only"], session_minutes=15) == ("only",)
    assert select_objectives_for_session([], session_minutes=60) == ()


def test_format_learning_objective_label_dedupes_code_prefix():
    assert (
        format_learning_objective_label(
            code="4.2.1",
            text="4.2.1 Variables, factors taking categorical values",
        )
        == "4.2.1 Variables, factors taking categorical values"
    )
    assert (
        format_learning_objective_label(
            code="4.2.1",
            text="Variables, factors taking categorical values",
        )
        == "4.2.1 Variables, factors taking categorical values"
    )
    assert not format_learning_objective_label(
        code="4.2.1",
        text="4.2.1 Variables",
    ).startswith("4.2.1: 4.2.1")
