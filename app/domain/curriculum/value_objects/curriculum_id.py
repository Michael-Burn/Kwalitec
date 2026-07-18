"""Canonical curriculum identity value object.

Names a programme structure (e.g. paper code), not proprietary content.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, order=True)
class CurriculumId:
    """Stable curriculum / programme identity.

    Attributes:
        value: Non-empty canonical curriculum identifier string.
    """

    value: str

    def __post_init__(self) -> None:
        if not isinstance(self.value, str):
            raise ValueError("CurriculumId value must be a non-empty string")
        normalized = self.value.strip()
        if not normalized:
            raise ValueError("CurriculumId value must be a non-empty string")
        object.__setattr__(self, "value", normalized)

    @classmethod
    def of(cls, value: str | CurriculumId) -> CurriculumId:
        """Coerce a string or CurriculumId to CurriculumId."""
        if isinstance(value, CurriculumId):
            return value
        return cls(value)

    def __str__(self) -> str:
        return self.value
