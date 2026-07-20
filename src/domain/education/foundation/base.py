"""Shared educational domain primitives: value objects and entities.

Pure educational abstractions. No persistence, Flask, SQLAlchemy, or
serialization concerns.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from domain.education.foundation.errors import EducationalInvariantViolation


def require_non_empty_text(value: str | None, field_name: str) -> str:
    """Normalize and require a non-empty educational text field.

    Args:
        value: Raw text candidate.
        field_name: Field name for invariant messaging.

    Returns:
        Stripped non-empty string.

    Raises:
        EducationalInvariantViolation: When value is missing or blank.
    """
    if value is None:
        raise EducationalInvariantViolation(
            f"{field_name} is required",
            invariant=f"{field_name}.required",
        )
    cleaned = value.strip()
    if not cleaned:
        raise EducationalInvariantViolation(
            f"{field_name} must be non-empty",
            invariant=f"{field_name}.non_empty",
        )
    return cleaned


def require_identity_value(value: str | None, type_name: str) -> str:
    """Validate a stable educational identity token.

    Args:
        value: Raw identity candidate.
        type_name: Human-readable identity type (for error messages).

    Returns:
        Stripped non-empty identity string.

    Raises:
        EducationalInvariantViolation: When the identity is blank or contains
            interior whitespace (identities are opaque tokens, not phrases).
    """
    cleaned = require_non_empty_text(value, type_name)
    if any(ch.isspace() for ch in cleaned):
        raise EducationalInvariantViolation(
            f"{type_name} must not contain whitespace",
            invariant=f"{type_name}.no_whitespace",
        )
    return cleaned


@dataclass(frozen=True, slots=True)
class EducationalValueObject(ABC):
    """Immutable educational value object.

    Equality is structural (dataclass field equality). Subclasses must remain
    frozen and must enforce invariants in ``_validate``.
    """

    def __post_init__(self) -> None:
        self._validate()

    @abstractmethod
    def _validate(self) -> None:
        """Enforce value-object invariants after construction."""


@dataclass(frozen=True, slots=True, eq=False)
class EducationalEntity(ABC):
    """Educational entity with identity-based equality.

    Two entities are equal when their educational identities are equal,
    regardless of other attribute differences. Subclasses must expose a
    stable identity via ``entity_id``.
    """

    def __post_init__(self) -> None:
        self._validate()

    @property
    @abstractmethod
    def entity_id(self) -> EducationalValueObject:
        """Stable educational identity for this entity."""

    @abstractmethod
    def _validate(self) -> None:
        """Enforce entity invariants after construction."""

    def __eq__(self, other: object) -> bool:
        if other is self:
            return True
        if not isinstance(other, EducationalEntity):
            return NotImplemented
        if type(self) is not type(other):
            return False
        return self.entity_id == other.entity_id

    def __hash__(self) -> int:
        return hash((type(self), self.entity_id))

    def same_identity(self, other: Any) -> bool:
        """Return True when ``other`` shares this entity's educational identity."""
        if not isinstance(other, EducationalEntity):
            return False
        if type(self) is not type(other):
            return False
        return self.entity_id == other.entity_id
