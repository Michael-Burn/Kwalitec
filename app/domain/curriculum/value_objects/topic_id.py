"""Canonical topic identity value object.

Structural identity only — no syllabus prose or copyrighted content.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, order=True)
class TopicId:
    """Stable curriculum topic identity.

    Attributes:
        value: Non-empty canonical topic identifier string.
    """

    value: str

    def __post_init__(self) -> None:
        if not isinstance(self.value, str):
            raise ValueError("TopicId value must be a non-empty string")
        normalized = self.value.strip()
        if not normalized:
            raise ValueError("TopicId value must be a non-empty string")
        object.__setattr__(self, "value", normalized)

    @classmethod
    def of(cls, value: str | TopicId) -> TopicId:
        """Coerce a string or TopicId to TopicId."""
        if isinstance(value, TopicId):
            return value
        return cls(value)

    def __str__(self) -> str:
        return self.value
