"""Immutable IngestionRequest DTO — abstract document sources only."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class DocumentSourceRef:
    """Reference to an abstract curriculum document source."""

    document_id: str
    source_ref: str
    title: str
    declared_kind: str | None = None
    metadata: tuple[tuple[str, str], ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class DocumentEntryPayload:
    """Typed entry payload for an abstract document source."""

    entry_id: str
    entry_type: str
    text: str
    number: str | None = None
    parent_ref: str | None = None
    attributes: tuple[tuple[str, str], ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class DocumentPayload:
    """Full abstract document payload for ingestion."""

    document_id: str
    source_ref: str
    title: str
    entries: tuple[DocumentEntryPayload, ...] = field(default_factory=tuple)
    declared_kind: str | None = None
    metadata: tuple[tuple[str, str], ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class IngestionRequest:
    """Request to run the curriculum ingestion pipeline.

    Carries abstract document payloads only — no Flask, no uploads, no bytes.
    """

    job_id: str
    documents: tuple[DocumentPayload, ...]
    metadata: tuple[tuple[str, str], ...] = field(default_factory=tuple)
    require_pass: bool = True
