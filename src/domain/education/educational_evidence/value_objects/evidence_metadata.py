"""Evidence metadata — constrained, immutable key/value detail.

Architecture Source
    STUDENT_DIGITAL_TWIN.md (Learning Evidence Model)
Concept
    Evidence Metadata
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import EducationalValueObject
from domain.education.foundation.errors import EducationalInvariantViolation

Primitive = str | int | float | bool | None


@dataclass(frozen=True, slots=True)
class EvidenceMetadata(EducationalValueObject):
    """Immutable, canonically-ordered bag of type-specific evidence detail.

    Values are restricted to educational primitives (``str``/``int``/
    ``float``/``bool``/``None``) so this value object cannot smuggle nested
    structures, DTOs, or opaque blobs into the domain model. Entries are
    always stored sorted by key so two metadata bags built from the same
    content compare equal regardless of construction order — this is the
    canonical (normalised) form.
    """

    entries: tuple[tuple[str, Primitive], ...] = ()

    def _validate(self) -> None:
        seen: set[str] = set()
        for key, value in self.entries:
            if not isinstance(key, str) or not key.strip():
                raise EducationalInvariantViolation(
                    "metadata keys must be non-empty strings",
                    invariant="EvidenceMetadata.key.non_empty",
                )
            if key in seen:
                raise EducationalInvariantViolation(
                    f"duplicate metadata key: {key}",
                    invariant="EvidenceMetadata.key.unique",
                )
            if value is not None and not isinstance(value, str | int | float | bool):
                raise EducationalInvariantViolation(
                    f"metadata value for {key!r} must be a primitive "
                    "(str, int, float, bool, or None)",
                    invariant="EvidenceMetadata.value.type",
                )
            seen.add(key)
        object.__setattr__(
            self, "entries", tuple(sorted(self.entries, key=lambda pair: pair[0]))
        )

    @classmethod
    def of(cls, **kwargs: Primitive) -> EvidenceMetadata:
        return cls(entries=tuple(kwargs.items()))

    @classmethod
    def empty(cls) -> EvidenceMetadata:
        return cls()

    def get(self, key: str, default: Primitive = None) -> Primitive:
        for existing_key, value in self.entries:
            if existing_key == key:
                return value
        return default

    def has(self, key: str) -> bool:
        return any(existing_key == key for existing_key, _ in self.entries)

    def as_dict(self) -> dict[str, Primitive]:
        return dict(self.entries)

    def is_empty(self) -> bool:
        return not self.entries

    def with_entry(self, key: str, value: Primitive) -> EvidenceMetadata:
        remaining = tuple((k, v) for k, v in self.entries if k != key)
        return EvidenceMetadata(entries=(*remaining, (key, value)))

    def __len__(self) -> int:
        return len(self.entries)
