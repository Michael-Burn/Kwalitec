"""Comparison service and policy tests."""

from __future__ import annotations

from types import MappingProxyType

import pytest

from app.application.mission_adapter.comparison_service import ComparisonService
from app.application.mission_adapter.dto.mission_snapshot import MissionSnapshot
from app.application.mission_adapter.exceptions import ComparisonFailure
from app.application.mission_adapter.policies.comparison_policy import (
    ComparisonPolicy,
)


def _snap(**overrides) -> MissionSnapshot:
    base = dict(
        mission_id="m1",
        learner_id="l1",
        journey_id="j1",
        topic_id="t1",
        session_id="s1",
        effort="medium",
        mission_type="today",
        is_revision=False,
        sequence_index=0,
        explanation_keys=("why", "what"),
        engine_id="v1",
        engine_version="1",
    )
    base.update(overrides)
    return MissionSnapshot(**base)


def test_compare_identical():
    svc = ComparisonService(id_factory=lambda: "cmp-1")
    result = svc.compare(_snap(), _snap(engine_id="v2"))
    assert result.matched is True
    assert result.comparison_id == "cmp-1"
    assert result.divergence_count == 0
    assert len(result.dimensions) == len(ComparisonPolicy.DIMENSIONS)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("journey_id", "other-j"),
        ("topic_id", "other-t"),
        ("session_id", "other-s"),
        ("effort", "high"),
        ("mission_type", "resume"),
        ("is_revision", True),
        ("sequence_index", 3),
        ("explanation_keys", ("only",)),
    ],
)
def test_compare_divergence_per_dimension(field, value):
    svc = ComparisonService()
    result = svc.compare(_snap(), _snap(**{field: value}))
    assert result.matched is False
    assert result.divergence_count >= 1


def test_compare_requires_both():
    svc = ComparisonService()
    with pytest.raises(ComparisonFailure):
        svc.compare(_snap(), None)
    with pytest.raises(ComparisonFailure):
        svc.compare(None, _snap())


def test_refuse_forbidden_metadata():
    svc = ComparisonService()
    bad = _snap(metadata=MappingProxyType({"title": "secret content"}))
    with pytest.raises(ComparisonFailure, match="educational"):
        svc.compare(bad, _snap(engine_id="v2"))


@pytest.mark.parametrize(
    "name",
    ["title", "body", "content", "explanation_text", "study_content", "generated_text"],
)
def test_forbidden_fields(name):
    assert ComparisonPolicy.is_forbidden_field(name) is True
    assert ComparisonPolicy.is_forbidden_field(name.upper()) is True


def test_allowed_structural_field_not_forbidden():
    assert ComparisonPolicy.is_forbidden_field("journey_id") is False


def test_extract_values():
    values = ComparisonPolicy.extract_values(_snap())
    assert values["journey_selected"] == "j1"
    assert values["revision_recommendation"] == "false"
    assert "why" in values["explanation_metadata"]


def test_history_and_summary():
    svc = ComparisonService()
    svc.compare(_snap(), _snap(engine_id="v2"))
    svc.compare(_snap(), _snap(topic_id="x", engine_id="v2"))
    summary = svc.summary()
    assert summary["total"] == 2
    assert summary["matched"] == 1
    assert summary["diverged"] == 1
    assert summary["match_rate"] == 0.5


def test_empty_summary():
    svc = ComparisonService()
    assert svc.summary()["total"] == 0
    assert svc.summary()["match_rate"] == 0.0


def test_clear_history():
    svc = ComparisonService()
    svc.compare(_snap(), _snap(engine_id="v2"))
    svc.clear_history()
    assert svc.history == ()


def test_dimension_match_immutable():
    svc = ComparisonService()
    result = svc.compare(_snap(), _snap(engine_id="v2"))
    with pytest.raises(Exception):
        result.matched = False  # type: ignore[misc]


def test_all_dimensions_listed():
    assert "journey_selected" in ComparisonPolicy.DIMENSIONS
    assert "topic_selected" in ComparisonPolicy.DIMENSIONS
    assert "session_selected" in ComparisonPolicy.DIMENSIONS
    assert "estimated_effort" in ComparisonPolicy.DIMENSIONS
    assert "mission_type" in ComparisonPolicy.DIMENSIONS
    assert "revision_recommendation" in ComparisonPolicy.DIMENSIONS
    assert "ordering" in ComparisonPolicy.DIMENSIONS
    assert "explanation_metadata" in ComparisonPolicy.DIMENSIONS


def test_explanation_keys_order_independent():
    a = _snap(explanation_keys=("b", "a"))
    b = _snap(explanation_keys=("a", "b"), engine_id="v2")
    dims = ComparisonPolicy.compare_dimensions(a, b)
    meta = next(d for d in dims if d.name == "explanation_metadata")
    assert meta.matched is True
