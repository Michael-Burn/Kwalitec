"""Unit tests for educational foundation identity value objects."""

from __future__ import annotations

import pytest

from domain.education.foundation import (
    ConceptId,
    DecisionId,
    DiagnosisId,
    DigitalTwinId,
    EducationalInvariantViolation,
    EvidenceId,
    HypothesisId,
    LearningEpisodeId,
    LearningObjectiveId,
    MisconceptionId,
    OrchestratorId,
    PriorityId,
    ReflectionId,
    StudentKnowledgeId,
    TeachingIntentionId,
    TeachingStrategyId,
)

_ID_TYPES = (
    LearningObjectiveId,
    ConceptId,
    LearningEpisodeId,
    TeachingStrategyId,
    TeachingIntentionId,
    DiagnosisId,
    HypothesisId,
    PriorityId,
    DecisionId,
    OrchestratorId,
    DigitalTwinId,
    EvidenceId,
    ReflectionId,
    StudentKnowledgeId,
    MisconceptionId,
)


@pytest.mark.parametrize("id_cls", _ID_TYPES)
def test_identity_accepts_valid_token(id_cls: type) -> None:
    identity = id_cls("obj-001")
    assert identity.value == "obj-001"
    assert str(identity) == "obj-001"


@pytest.mark.parametrize("id_cls", _ID_TYPES)
def test_identity_strips_outer_whitespace(id_cls: type) -> None:
    identity = id_cls("  obj-001  ")
    assert identity.value == "obj-001"


@pytest.mark.parametrize("id_cls", _ID_TYPES)
@pytest.mark.parametrize("raw", ["", "   ", None])
def test_identity_rejects_blank(id_cls: type, raw: str | None) -> None:
    with pytest.raises(EducationalInvariantViolation):
        id_cls(raw)  # type: ignore[arg-type]


@pytest.mark.parametrize("id_cls", _ID_TYPES)
def test_identity_rejects_interior_whitespace(id_cls: type) -> None:
    with pytest.raises(EducationalInvariantViolation) as exc_info:
        id_cls("obj 001")
    assert exc_info.value.invariant is not None
    assert "whitespace" in (exc_info.value.invariant or "")


@pytest.mark.parametrize("id_cls", _ID_TYPES)
def test_identity_equality_and_hash(id_cls: type) -> None:
    left = id_cls("same-id")
    right = id_cls("same-id")
    other = id_cls("other-id")
    assert left == right
    assert left != other
    assert hash(left) == hash(right)
    assert {left, right, other} == {left, other}


@pytest.mark.parametrize("id_cls", _ID_TYPES)
def test_identity_is_immutable(id_cls: type) -> None:
    identity = id_cls("frozen-id")
    with pytest.raises(AttributeError):
        identity.value = "mutated"  # type: ignore[misc]


def test_distinct_identity_types_are_not_equal() -> None:
    assert LearningObjectiveId("x") != ConceptId("x")
    assert EvidenceId("e1") != ReflectionId("e1")
