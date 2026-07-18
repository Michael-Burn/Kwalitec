"""Curriculum document — abstract structured source for ingestion.

Never stores PDF bytes. Never depends on Flask upload endpoints.
Content is an ordered list of typed entries that extractors consume
deterministically.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum


class DocumentKind(StrEnum):
    """Recognised curriculum document kinds (abstract sources)."""

    CMP = "cmp"
    SYLLABUS = "syllabus"
    LEARNING_OBJECTIVES = "learning_objectives"
    FORMULA_SHEET = "formula_sheet"
    SUPPORTING_DOCUMENT = "supporting_document"
    UNKNOWN = "unknown"


class DocumentEntryType(StrEnum):
    """Typed structural entry inside an abstract curriculum document."""

    SECTION = "section"
    TOPIC = "topic"
    OBJECTIVE = "objective"
    PREREQUISITE = "prerequisite"
    METADATA = "metadata"
    FORMULA = "formula"
    NOTE = "note"


def resolve_document_kind(value: DocumentKind | str) -> DocumentKind:
    """Resolve a DocumentKind from enum or string token."""
    if isinstance(value, DocumentKind):
        return value
    token = (value or "").strip().lower().replace("-", "_").replace(" ", "_")
    aliases = {
        "learning_objective": DocumentKind.LEARNING_OBJECTIVES,
        "objectives": DocumentKind.LEARNING_OBJECTIVES,
        "lo": DocumentKind.LEARNING_OBJECTIVES,
        "formula": DocumentKind.FORMULA_SHEET,
        "formulas": DocumentKind.FORMULA_SHEET,
        "supporting": DocumentKind.SUPPORTING_DOCUMENT,
        "support": DocumentKind.SUPPORTING_DOCUMENT,
        "document": DocumentKind.SUPPORTING_DOCUMENT,
        "core_maths_pack": DocumentKind.CMP,
        "core_mathematics_pack": DocumentKind.CMP,
    }
    if token in aliases:
        return aliases[token]
    try:
        return DocumentKind(token)
    except ValueError as exc:
        raise ValueError(f"Unknown document kind: {value!r}") from exc


def resolve_entry_type(value: DocumentEntryType | str) -> DocumentEntryType:
    """Resolve a DocumentEntryType from enum or string token."""
    if isinstance(value, DocumentEntryType):
        return value
    token = (value or "").strip().lower().replace("-", "_").replace(" ", "_")
    aliases = {
        "chapter": DocumentEntryType.SECTION,
        "part": DocumentEntryType.SECTION,
        "heading": DocumentEntryType.SECTION,
        "learning_objective": DocumentEntryType.OBJECTIVE,
        "lo": DocumentEntryType.OBJECTIVE,
        "prereq": DocumentEntryType.PREREQUISITE,
        "meta": DocumentEntryType.METADATA,
    }
    if token in aliases:
        return aliases[token]
    try:
        return DocumentEntryType(token)
    except ValueError as exc:
        raise ValueError(f"Unknown document entry type: {value!r}") from exc


@dataclass(frozen=True)
class DocumentEntry:
    """Single typed structural entry in an abstract curriculum document."""

    entry_id: str
    entry_type: DocumentEntryType
    text: str
    number: str | None = None
    parent_ref: str | None = None
    attributes: tuple[tuple[str, str], ...] = field(default_factory=tuple)

    @classmethod
    def create(
        cls,
        entry_id: str,
        entry_type: DocumentEntryType | str,
        text: str,
        *,
        number: str | None = None,
        parent_ref: str | None = None,
        attributes: list[tuple[str, str]]
        | tuple[tuple[str, str], ...]
        | None = None,
    ) -> DocumentEntry:
        """Construct a DocumentEntry after validating invariants."""
        eid = _require_non_empty(entry_id, "entry_id")
        body = _require_non_empty(text, "text")
        num = None if number is None else _require_non_empty(number, "number")
        parent = (
            None
            if parent_ref is None
            else _require_non_empty(parent_ref, "parent_ref")
        )
        attrs = tuple(attributes or ())
        for key, value in attrs:
            _require_non_empty(key, "attribute key")
            if not isinstance(value, str):
                raise ValueError("attribute value must be a string")
        return cls(
            entry_id=eid,
            entry_type=resolve_entry_type(entry_type),
            text=body,
            number=num,
            parent_ref=parent,
            attributes=attrs,
        )

    def attribute(self, key: str, default: str | None = None) -> str | None:
        """Return the first attribute value for ``key``, or ``default``."""
        token = (key or "").strip().lower()
        for attr_key, attr_value in self.attributes:
            if attr_key.strip().lower() == token:
                return attr_value
        return default


@dataclass(frozen=True)
class CurriculumDocument:
    """Abstract curriculum document source for deterministic ingestion.

    Stores references and typed entries only — never PDF content, never bytes.
    """

    document_id: str
    source_ref: str
    title: str
    entries: tuple[DocumentEntry, ...] = field(default_factory=tuple)
    declared_kind: DocumentKind | None = None
    metadata: tuple[tuple[str, str], ...] = field(default_factory=tuple)

    @classmethod
    def create(
        cls,
        document_id: str,
        source_ref: str,
        title: str,
        *,
        entries: list[DocumentEntry] | tuple[DocumentEntry, ...] | None = None,
        declared_kind: DocumentKind | str | None = None,
        metadata: list[tuple[str, str]]
        | tuple[tuple[str, str], ...]
        | None = None,
    ) -> CurriculumDocument:
        """Construct a CurriculumDocument after validating invariants.

        Raises:
            ValueError: On empty identity/reference/title, or content-like refs.
        """
        did = _require_non_empty(document_id, "document_id")
        ref = _require_non_empty(source_ref, "source_ref")
        name = _require_non_empty(title, "title")
        _reject_embedded_content(ref)
        entries_t = tuple(entries or ())
        seen: set[str] = set()
        for entry in entries_t:
            if entry.entry_id in seen:
                raise ValueError(f"duplicate entry_id: {entry.entry_id!r}")
            seen.add(entry.entry_id)
        kind = (
            None
            if declared_kind is None
            else resolve_document_kind(declared_kind)
        )
        meta = tuple(metadata or ())
        for key, value in meta:
            _require_non_empty(key, "metadata key")
            if not isinstance(value, str):
                raise ValueError("metadata value must be a string")
        return cls(
            document_id=did,
            source_ref=ref,
            title=name,
            entries=entries_t,
            declared_kind=kind,
            metadata=meta,
        )

    @property
    def entry_count(self) -> int:
        """Number of structural entries."""
        return len(self.entries)

    def entries_of_type(
        self, entry_type: DocumentEntryType | str
    ) -> tuple[DocumentEntry, ...]:
        """Return entries matching ``entry_type``."""
        resolved = resolve_entry_type(entry_type)
        return tuple(e for e in self.entries if e.entry_type is resolved)

    def metadata_value(self, key: str, default: str | None = None) -> str | None:
        """Return the first metadata value for ``key``, or ``default``."""
        token = (key or "").strip().lower()
        for meta_key, meta_value in self.metadata:
            if meta_key.strip().lower() == token:
                return meta_value
        return default

    def with_entries(
        self, entries: list[DocumentEntry] | tuple[DocumentEntry, ...]
    ) -> CurriculumDocument:
        """Return a document with replaced entries."""
        return CurriculumDocument.create(
            self.document_id,
            self.source_ref,
            self.title,
            entries=entries,
            declared_kind=self.declared_kind,
            metadata=self.metadata,
        )


def _require_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a non-empty string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized


def _reject_embedded_content(reference: str) -> None:
    """Reject obvious embedded payloads (data URIs / raw PDF markers)."""
    lowered = reference.lower()
    if lowered.startswith("data:"):
        raise ValueError("source_ref must not embed content (data URI)")
    if "%pdf-" in lowered or lowered.startswith("%pdf"):
        raise ValueError("source_ref must not embed PDF content")
