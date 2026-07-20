"""Unit tests for educational foundation bases, errors, and results."""

from __future__ import annotations

from dataclasses import dataclass

import pytest

from domain.education.foundation import (
    ConceptId,
    EducationalDomainError,
    EducationalEntity,
    EducationalInvariantViolation,
    EducationalResult,
    EducationalValueObject,
    LearningObjectiveId,
    require_identity_value,
    require_non_empty_text,
)


@dataclass(frozen=True, slots=True, eq=False)
class _ProbeEntity(EducationalEntity):
    """Minimal concrete entity for identity-equality tests."""

    identity: ConceptId
    note: str

    @property
    def entity_id(self) -> EducationalValueObject:
        return self.identity

    def _validate(self) -> None:
        if not isinstance(self.identity, ConceptId):
            raise EducationalInvariantViolation(
                "identity must be a ConceptId",
                invariant="ProbeEntity.identity.type",
            )
        if not self.note.strip():
            raise EducationalInvariantViolation(
                "note must be non-empty",
                invariant="ProbeEntity.note.non_empty",
            )


def test_domain_error_requires_message() -> None:
    err = EducationalDomainError("diagnosis requires evidence")
    assert str(err) == "diagnosis requires evidence"
    assert err.message == "diagnosis requires evidence"
    blank = EducationalDomainError("   ")
    assert blank.message == "educational domain error"


def test_invariant_violation_carries_invariant_code() -> None:
    err = EducationalInvariantViolation(
        "empty id",
        invariant="LearningObjectiveId.non_empty",
    )
    assert isinstance(err, EducationalDomainError)
    assert err.invariant == "LearningObjectiveId.non_empty"


def test_require_helpers() -> None:
    assert require_non_empty_text("  hello  ", "label") == "hello"
    assert require_identity_value("id-1", "ConceptId") == "id-1"
    with pytest.raises(EducationalInvariantViolation):
        require_non_empty_text("", "label")
    with pytest.raises(EducationalInvariantViolation):
        require_identity_value("has space", "ConceptId")


def test_entity_equality_is_identity_based() -> None:
    left = _ProbeEntity(ConceptId("c1"), note="first")
    right = _ProbeEntity(ConceptId("c1"), note="different note")
    other = _ProbeEntity(ConceptId("c2"), note="first")
    assert left == right
    assert left != other
    assert left.same_identity(right)
    assert not left.same_identity(other)
    assert hash(left) == hash(right)
    assert {left, right, other} == {left, other}


def test_entity_rejects_invalid_construction() -> None:
    with pytest.raises(EducationalInvariantViolation):
        _ProbeEntity(ConceptId("c1"), note="   ")


def test_entity_immutability() -> None:
    entity = _ProbeEntity(ConceptId("c1"), note="stable")
    with pytest.raises(AttributeError):
        entity.note = "changed"  # type: ignore[misc]


def test_result_ok_and_fail() -> None:
    ok = EducationalResult.ok(LearningObjectiveId("lo-1"))
    assert ok.is_success
    assert not ok.is_failure
    assert ok.value == LearningObjectiveId("lo-1")
    assert ok.value_or(LearningObjectiveId("fallback")) == LearningObjectiveId(
        "lo-1"
    )

    fail = EducationalResult[LearningObjectiveId].fail(
        EducationalInvariantViolation("nope", invariant="test")
    )
    assert fail.is_failure
    assert fail.error.message == "nope"
    assert fail.value_or(LearningObjectiveId("fallback")) == LearningObjectiveId(
        "fallback"
    )


def test_result_value_and_error_guards() -> None:
    ok = EducationalResult.ok(42)
    with pytest.raises(EducationalDomainError):
        _ = ok.error

    fail = EducationalResult[int].fail("blocked")
    with pytest.raises(EducationalDomainError):
        _ = fail.value


def test_result_map() -> None:
    ok = EducationalResult.ok(2).map(lambda n: n * 3)
    assert ok.is_success
    assert ok.value == 6

    fail = EducationalResult[int].fail("x").map(lambda n: n * 3)
    assert fail.is_failure
    assert fail.error.message == "x"


def test_result_fail_from_string() -> None:
    fail = EducationalResult[str].fail("thin evidence")
    assert isinstance(fail.error, EducationalDomainError)
    assert fail.error.message == "thin evidence"


def test_value_object_cannot_be_instantiated_directly() -> None:
    with pytest.raises(TypeError):
        EducationalValueObject()  # type: ignore[misc]


def test_entity_cannot_be_instantiated_directly() -> None:
    with pytest.raises(TypeError):
        EducationalEntity()  # type: ignore[misc]
