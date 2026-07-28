"""DTOs for Founder curriculum publishing services (EI-003)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class EditionSummary:
    """Compact edition listing row for Founder review queues."""

    edition_id: str
    subject_code: str
    edition_label: str
    title: str
    publication_state: str
    validation_status: str
    review_status: str
    provider: str = "IFoA"
    published_at: str | None = None
    approved_by: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "edition_id": self.edition_id,
            "subject_code": self.subject_code,
            "edition_label": self.edition_label,
            "title": self.title,
            "publication_state": self.publication_state,
            "validation_status": self.validation_status,
            "review_status": self.review_status,
            "provider": self.provider,
            "published_at": self.published_at,
            "approved_by": self.approved_by,
        }


@dataclass(frozen=True)
class NodeInspection:
    """Single node view for Founder inspection."""

    stable_id: str
    kind: str
    title: str
    metadata: dict[str, Any] = field(default_factory=dict)
    review_status: str = "pending"
    confidence: int | None = None
    provenance: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "stable_id": self.stable_id,
            "kind": self.kind,
            "title": self.title,
            "metadata": dict(self.metadata),
            "review_status": self.review_status,
            "confidence": self.confidence,
            "provenance": self.provenance,
        }


@dataclass(frozen=True)
class HierarchyNode:
    """Tree node for hierarchy navigation."""

    stable_id: str
    kind: str
    title: str
    children: tuple[HierarchyNode, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "stable_id": self.stable_id,
            "kind": self.kind,
            "title": self.title,
            "children": [c.to_dict() for c in self.children],
        }


@dataclass(frozen=True)
class EditionInspection:
    """Full Founder inspection payload for one edition."""

    edition: EditionSummary
    hierarchy: HierarchyNode | None
    node_count: int
    edge_count: int
    validation_report: dict[str, Any] | None
    review_summary: dict[str, int]
    source_cmp_ref: str | None = None
    source_syllabus_ref: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "edition": self.edition.to_dict(),
            "hierarchy": self.hierarchy.to_dict() if self.hierarchy else None,
            "node_count": self.node_count,
            "edge_count": self.edge_count,
            "validation_report": self.validation_report,
            "review_summary": dict(self.review_summary),
            "source_cmp_ref": self.source_cmp_ref,
            "source_syllabus_ref": self.source_syllabus_ref,
        }


@dataclass(frozen=True)
class MetadataEdit:
    """Allowed educational metadata fields for editorial edit."""

    title: str | None = None
    statement: str | None = None
    difficulty: str | None = None
    estimated_study_minutes: int | None = None
    cognitive_level: str | None = None
    learning_type: str | None = None
    body: str | None = None
    notation: str | None = None
    summary: str | None = None

    def as_changes(self) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for key in (
            "title",
            "statement",
            "difficulty",
            "estimated_study_minutes",
            "cognitive_level",
            "learning_type",
            "body",
            "notation",
            "summary",
        ):
            value = getattr(self, key)
            if value is not None:
                out[key] = value
        return out


@dataclass(frozen=True)
class ComparisonChange:
    """One structured difference between two editions."""

    category: str
    change_type: str
    stable_id: str | None
    detail: str
    before: Any = None
    after: Any = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "category": self.category,
            "change_type": self.change_type,
            "stable_id": self.stable_id,
            "detail": self.detail,
            "before": self.before,
            "after": self.after,
        }


@dataclass(frozen=True)
class EditionComparison:
    """Structured comparison suitable for future Founder UI."""

    left_edition_id: str
    right_edition_id: str
    hierarchy_changes: tuple[ComparisonChange, ...] = ()
    learning_objective_changes: tuple[ComparisonChange, ...] = ()
    prerequisite_changes: tuple[ComparisonChange, ...] = ()
    educational_object_changes: tuple[ComparisonChange, ...] = ()
    metadata_changes: tuple[ComparisonChange, ...] = ()

    @property
    def change_count(self) -> int:
        return (
            len(self.hierarchy_changes)
            + len(self.learning_objective_changes)
            + len(self.prerequisite_changes)
            + len(self.educational_object_changes)
            + len(self.metadata_changes)
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "left_edition_id": self.left_edition_id,
            "right_edition_id": self.right_edition_id,
            "change_count": self.change_count,
            "hierarchy_changes": [c.to_dict() for c in self.hierarchy_changes],
            "learning_objective_changes": [
                c.to_dict() for c in self.learning_objective_changes
            ],
            "prerequisite_changes": [
                c.to_dict() for c in self.prerequisite_changes
            ],
            "educational_object_changes": [
                c.to_dict() for c in self.educational_object_changes
            ],
            "metadata_changes": [c.to_dict() for c in self.metadata_changes],
        }


@dataclass(frozen=True)
class PublicationResult:
    """Outcome of a successful publication."""

    edition_id: str
    subject_code: str
    publication_record_id: str
    snapshot_id: str
    previous_edition_id: str | None
    published_at: str
    publisher: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "edition_id": self.edition_id,
            "subject_code": self.subject_code,
            "publication_record_id": self.publication_record_id,
            "snapshot_id": self.snapshot_id,
            "previous_edition_id": self.previous_edition_id,
            "published_at": self.published_at,
            "publisher": self.publisher,
        }
