"""Extraction result — immutable capture of raw extracted structures."""

from __future__ import annotations

from dataclasses import dataclass, field

from app.domain.curriculum_ingestion.curriculum_document import DocumentKind
from app.domain.curriculum_ingestion.extracted_objective import ExtractedObjective
from app.domain.curriculum_ingestion.extracted_section import ExtractedSection
from app.domain.curriculum_ingestion.extracted_topic import ExtractedTopic


@dataclass(frozen=True)
class ExtractionResult:
    """Immutable extraction output for one or more documents.

    Contains only structural candidates — never sessions, activities, or missions.
    """

    result_id: str
    document_ids: tuple[str, ...]
    document_kinds: tuple[tuple[str, DocumentKind], ...] = field(
        default_factory=tuple
    )
    sections: tuple[ExtractedSection, ...] = field(default_factory=tuple)
    topics: tuple[ExtractedTopic, ...] = field(default_factory=tuple)
    objectives: tuple[ExtractedObjective, ...] = field(default_factory=tuple)
    prerequisite_refs: tuple[tuple[str, str], ...] = field(default_factory=tuple)
    metadata: tuple[tuple[str, str], ...] = field(default_factory=tuple)
    notes: tuple[str, ...] = field(default_factory=tuple)

    @classmethod
    def create(
        cls,
        result_id: str,
        document_ids: list[str] | tuple[str, ...],
        *,
        document_kinds: list[tuple[str, DocumentKind]]
        | tuple[tuple[str, DocumentKind], ...]
        | None = None,
        sections: list[ExtractedSection]
        | tuple[ExtractedSection, ...]
        | None = None,
        topics: list[ExtractedTopic] | tuple[ExtractedTopic, ...] | None = None,
        objectives: list[ExtractedObjective]
        | tuple[ExtractedObjective, ...]
        | None = None,
        prerequisite_refs: list[tuple[str, str]]
        | tuple[tuple[str, str], ...]
        | None = None,
        metadata: list[tuple[str, str]]
        | tuple[tuple[str, str], ...]
        | None = None,
        notes: list[str] | tuple[str, ...] | None = None,
    ) -> ExtractionResult:
        """Construct an ExtractionResult after validating invariants."""
        rid = _require_non_empty(result_id, "result_id")
        docs = tuple(_require_non_empty(d, "document_id") for d in document_ids)
        if not docs:
            raise ValueError("document_ids must not be empty")
        return cls(
            result_id=rid,
            document_ids=docs,
            document_kinds=tuple(document_kinds or ()),
            sections=tuple(sections or ()),
            topics=tuple(topics or ()),
            objectives=tuple(objectives or ()),
            prerequisite_refs=tuple(prerequisite_refs or ()),
            metadata=tuple(metadata or ()),
            notes=tuple(notes or ()),
        )

    @property
    def section_count(self) -> int:
        """Number of extracted sections."""
        return len(self.sections)

    @property
    def topic_count(self) -> int:
        """Number of extracted topics."""
        return len(self.topics)

    @property
    def objective_count(self) -> int:
        """Number of extracted objectives."""
        return len(self.objectives)

    def kind_for(self, document_id: str) -> DocumentKind | None:
        """Return classified kind for ``document_id``, if recorded."""
        token = (document_id or "").strip()
        for did, kind in self.document_kinds:
            if did == token:
                return kind
        return None


def _require_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a non-empty string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized
