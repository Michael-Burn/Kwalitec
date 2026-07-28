"""Request / result DTOs for Curriculum Extraction."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from app.domain.curriculum_extraction.canonical_document import CanonicalDocument
from app.domain.curriculum_extraction.provenance import ExtractionProvenance
from app.domain.curriculum_extraction.validation import ValidationReport
from app.domain.curriculum_knowledge_graph.graph.curriculum_knowledge_graph import (
    CurriculumKnowledgeGraph,
)


@dataclass(frozen=True)
class ExtractionRequest:
    """Pipeline input: Canonical CMP + Syllabus documents."""

    job_id: str
    subject_code: str
    edition_label: str
    subject_title: str
    cmp_document: CanonicalDocument
    syllabus_document: CanonicalDocument
    provider: str = "IFoA"
    persist: bool = True
    metadata: tuple[tuple[str, str], ...] = ()

    def __post_init__(self) -> None:
        if not (self.job_id or "").strip():
            raise ValueError("job_id must be non-empty")
        if not (self.subject_code or "").strip():
            raise ValueError("subject_code must be non-empty")
        if not (self.edition_label or "").strip():
            raise ValueError("edition_label must be non-empty")
        if not (self.subject_title or "").strip():
            raise ValueError("subject_title must be non-empty")


@dataclass
class ExtractionResult:
    """Pipeline outcome. Graph is present when construction succeeded."""

    job_id: str
    edition_id: str | None
    graph: CurriculumKnowledgeGraph | None
    provenance: dict[str, ExtractionProvenance]
    validation: ValidationReport
    persisted: bool
    diagnostics: list[str] = field(default_factory=list)
    stage_trace: list[str] = field(default_factory=list)

    def to_snapshot(self) -> dict[str, Any]:
        return {
            "job_id": self.job_id,
            "edition_id": self.edition_id,
            "persisted": self.persisted,
            "validation": self.validation.to_dict(),
            "node_count": len(self.graph.nodes()) if self.graph else 0,
            "edge_count": len(self.graph.edges()) if self.graph else 0,
            "provenance_count": len(self.provenance),
            "diagnostics": list(self.diagnostics),
            "stage_trace": list(self.stage_trace),
            "graph_snapshot": self.graph.to_snapshot() if self.graph else None,
        }
