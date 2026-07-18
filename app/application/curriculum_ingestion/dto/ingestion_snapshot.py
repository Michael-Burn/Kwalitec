"""Immutable IngestionSnapshot and package preview DTOs."""

from __future__ import annotations

from dataclasses import dataclass, field

from app.application.curriculum_ingestion.dto.extraction_snapshot import (
    ExtractionSnapshot,
)
from app.application.curriculum_ingestion.dto.normalization_snapshot import (
    NormalizationSnapshot,
)
from app.application.curriculum_ingestion.dto.validation_snapshot import (
    ValidationSnapshot,
)


@dataclass(frozen=True)
class CurriculumPackagePreview:
    """Normalised curriculum package preview (handoff shape only).

    Not a Curriculum Management entity. No persistence. No teaching content.
    """

    package_id: str
    job_id: str
    document_refs: tuple[tuple[str, str, str], ...] = field(default_factory=tuple)
    section_ids: tuple[str, ...] = field(default_factory=tuple)
    topic_ids: tuple[str, ...] = field(default_factory=tuple)
    objective_ids: tuple[str, ...] = field(default_factory=tuple)
    prerequisite_edges: tuple[tuple[str, str], ...] = field(default_factory=tuple)
    metadata: tuple[tuple[str, str], ...] = field(default_factory=tuple)
    ready: bool = False


@dataclass(frozen=True)
class IngestionSnapshot:
    """Read-only view of a completed or in-progress ingestion job."""

    job_id: str
    state: str
    document_count: int
    classified_kinds: tuple[tuple[str, str], ...] = field(default_factory=tuple)
    extraction: ExtractionSnapshot | None = None
    normalization: NormalizationSnapshot | None = None
    validation: ValidationSnapshot | None = None
    package: CurriculumPackagePreview | None = None
    failure_reason: str | None = None
    metadata: tuple[tuple[str, str], ...] = field(default_factory=tuple)
    passed: bool = False
