"""Intermediate parse / segment models shared across extraction stages."""

from __future__ import annotations

from dataclasses import dataclass, field

from app.domain.curriculum_extraction.canonical_document import (
    DocumentKind,
    StructuralLocator,
)
from app.domain.curriculum_extraction.provenance import ExtractionMethod


@dataclass(frozen=True)
class ParsedHeading:
    """Numbered heading discovered during structural parsing."""

    number: str
    title: str
    depth: int
    locator: StructuralLocator
    document_kind: DocumentKind
    raw_text: str


@dataclass(frozen=True)
class ParsedObjectCue:
    """Educational object cue (definition, formula, …) from CMP/syllabus."""

    object_kind: str
    title: str
    body: str
    locator: StructuralLocator
    document_kind: DocumentKind
    confidence: int
    extraction_method: ExtractionMethod
    attributes: tuple[tuple[str, str], ...] = ()


@dataclass(frozen=True)
class ParsedPrerequisiteCue:
    """Explicit prerequisite cue between numbered units."""

    from_number: str
    to_number: str
    locator: StructuralLocator
    document_kind: DocumentKind


@dataclass(frozen=True)
class ParsedCrossReferenceCue:
    """Soft cross-reference cue."""

    from_number: str
    to_number: str
    locator: StructuralLocator
    document_kind: DocumentKind


@dataclass
class StructuralParseResult:
    """Output of the structural parsing stage for one document."""

    document_id: str
    document_kind: DocumentKind
    headings: list[ParsedHeading] = field(default_factory=list)
    object_cues: list[ParsedObjectCue] = field(default_factory=list)
    prerequisite_cues: list[ParsedPrerequisiteCue] = field(default_factory=list)
    cross_reference_cues: list[ParsedCrossReferenceCue] = field(
        default_factory=list
    )
    diagnostics: list[str] = field(default_factory=list)


@dataclass
class SegmentNode:
    """Curriculum segment before CKG entity materialisation."""

    kind: str  # topic | section | subsection | learning_objective
    number: str
    title: str
    locator: StructuralLocator
    document_kind: DocumentKind
    confidence: int
    extraction_method: ExtractionMethod
    children: list[SegmentNode] = field(default_factory=list)
    estimated_study_minutes: int = 0
    difficulty: str = "foundational"
    cognitive_level: str = "understand"
    learning_type: str = "concept"
    parent_number: str | None = None


@dataclass
class CurriculumSegmentTree:
    """Subject-scoped segment tree from CMP + Syllabus fusion."""

    subject_code: str
    edition_label: str
    subject_title: str
    provider: str
    topics: list[SegmentNode] = field(default_factory=list)
    object_cues: list[ParsedObjectCue] = field(default_factory=list)
    prerequisite_cues: list[ParsedPrerequisiteCue] = field(default_factory=list)
    cross_reference_cues: list[ParsedCrossReferenceCue] = field(
        default_factory=list
    )
    diagnostics: list[str] = field(default_factory=list)
    subject_locator: StructuralLocator | None = None
