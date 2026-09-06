"""Read-only ports for the Study Curriculum assembler.

Mirrors LearnerTwinQueryPort: application protocols only. Infrastructure
adapters wire Runtime C ``get_study_progress`` and published artefacts.
"""

from __future__ import annotations

from typing import Protocol

from app.application.educational_engine_foundation.dto import (
    EducationalArtefactSnapshot,
)
from app.application.progress_engine.dto import StudyProgress


class StudyProgressQueryPort(Protocol):
    """Bulk Study Progress reader (one call per subject, never per topic)."""

    def get_study_progress(
        self, *, user_id: int, subject_code: str
    ) -> StudyProgress:
        """Return the full Study Progress snapshot for a learner/subject."""
        ...


class SyllabusStructurePort(Protocol):
    """Published syllabus structure for section membership (one load)."""

    def artefact_snapshot(
        self, *, subject_code: str
    ) -> EducationalArtefactSnapshot | None:
        """Return published artefacts, or None when no active curriculum."""
        ...
