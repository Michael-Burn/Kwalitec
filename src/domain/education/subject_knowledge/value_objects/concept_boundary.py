"""Concept boundary — where a teachable idea begins and ends.

Architecture Source
    CONCEPT_ARCHITECTURE.md
Concept
    Concept Boundary
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import (
    EducationalValueObject,
    require_non_empty_text,
)


@dataclass(frozen=True, slots=True)
class ConceptBoundary(EducationalValueObject):
    """Educational boundary of a concept: inclusion, exclusion, and contrast.

    Boundaries prevent overgeneralisation and support accurate classification
    under exam rewording (Concept Architecture §4.2).
    """

    inclusion: str
    exclusion: str
    key_contrast: str | None = None

    def _validate(self) -> None:
        object.__setattr__(
            self,
            "inclusion",
            require_non_empty_text(self.inclusion, "inclusion"),
        )
        object.__setattr__(
            self,
            "exclusion",
            require_non_empty_text(self.exclusion, "exclusion"),
        )
        if self.key_contrast is not None:
            object.__setattr__(
                self,
                "key_contrast",
                require_non_empty_text(self.key_contrast, "key_contrast"),
            )

    def marks_contrast(self) -> bool:
        """True when a key neighbouring contrast is recorded."""
        return self.key_contrast is not None
