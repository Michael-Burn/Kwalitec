"""Curriculum edition / version metadata.

Structural versioning only — no proprietary syllabus text.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.domain.curriculum.entities._text import require_non_empty
from app.domain.curriculum.value_objects.curriculum_id import CurriculumId


@dataclass(frozen=True)
class CurriculumVersion:
    """Edition identity for a curriculum programme structure.

    Attributes:
        curriculum_id: Programme identity this edition belongs to.
        version_label: Human-readable edition label (e.g. ``2025``).
        schema_version: Structural schema integer for loaders (monotonic).
        notes: Optional operational note (not copyrighted content).
    """

    curriculum_id: CurriculumId
    version_label: str
    schema_version: int = 1
    notes: str | None = None

    @classmethod
    def create(
        cls,
        curriculum_id: str | CurriculumId,
        version_label: str,
        *,
        schema_version: int = 1,
        notes: str | None = None,
    ) -> CurriculumVersion:
        """Construct a CurriculumVersion after validating invariants.

        Raises:
            ValueError: On empty identities/labels or non-positive schema.
        """
        cid = CurriculumId.of(curriculum_id)
        label = require_non_empty(version_label, "version_label")
        if schema_version < 1:
            raise ValueError("schema_version must be >= 1")
        note = None if notes is None else require_non_empty(notes, "notes")
        return cls(
            curriculum_id=cid,
            version_label=label,
            schema_version=schema_version,
            notes=note,
        )
