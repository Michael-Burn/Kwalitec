"""Preview summary — student-visible curriculum projection for Studio review.

Preview never publishes. Preview never mutates publication state.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum


class PreviewReadiness(StrEnum):
    """Preview readiness for Founder approval gating."""

    NOT_READY = "not_ready"
    READY_FOR_REVIEW = "ready_for_review"
    APPROVED = "approved"
    REJECTED = "rejected"


@dataclass(frozen=True)
class PreviewNode:
    """Single node in the student-visible curriculum hierarchy."""

    node_id: str
    title: str
    kind: str = "topic"
    parent_id: str | None = None
    order_index: int = 0

    @classmethod
    def create(
        cls,
        node_id: str,
        title: str,
        *,
        kind: str = "topic",
        parent_id: str | None = None,
        order_index: int = 0,
    ) -> PreviewNode:
        """Construct a PreviewNode after validating invariants."""
        if order_index < 0:
            raise ValueError("order_index must be non-negative")
        return cls(
            node_id=_require_non_empty(node_id, "node_id"),
            title=_require_non_empty(title, "title"),
            kind=_require_non_empty(kind, "kind"),
            parent_id=(
                None
                if parent_id is None
                else _require_non_empty(parent_id, "parent_id")
            ),
            order_index=int(order_index),
        )


@dataclass(frozen=True)
class PreviewSummary:
    """Immutable student-visible curriculum preview for Founder review.

    Includes hierarchy, objectives, prerequisites, workload, and readiness.
    """

    preview_id: str
    workspace_id: str
    hierarchy: tuple[PreviewNode, ...] = field(default_factory=tuple)
    objectives: tuple[str, ...] = field(default_factory=tuple)
    prerequisites: tuple[tuple[str, str], ...] = field(default_factory=tuple)
    estimated_workload_hours: float | None = None
    validation_passed: bool = False
    publication_ready: bool = False
    readiness: PreviewReadiness = PreviewReadiness.NOT_READY
    subject_code: str = ""
    version_label: str = ""

    @classmethod
    def create(
        cls,
        preview_id: str,
        workspace_id: str,
        *,
        hierarchy: list[PreviewNode] | tuple[PreviewNode, ...] | None = None,
        objectives: list[str] | tuple[str, ...] | None = None,
        prerequisites: (
            list[tuple[str, str]] | tuple[tuple[str, str], ...] | None
        ) = None,
        estimated_workload_hours: float | None = None,
        validation_passed: bool = False,
        publication_ready: bool = False,
        readiness: PreviewReadiness | str | None = None,
        subject_code: str = "",
        version_label: str = "",
    ) -> PreviewSummary:
        """Construct a PreviewSummary after validating invariants."""
        pid = _require_non_empty(preview_id, "preview_id")
        wid = _require_non_empty(workspace_id, "workspace_id")
        nodes = tuple(hierarchy or ())
        objs = tuple(objectives or ())
        prereqs = tuple(prerequisites or ())
        hours = estimated_workload_hours
        if hours is not None and hours < 0:
            raise ValueError("estimated_workload_hours must be non-negative")
        if readiness is None:
            if publication_ready and validation_passed and nodes:
                resolved = PreviewReadiness.READY_FOR_REVIEW
            elif nodes and validation_passed:
                resolved = PreviewReadiness.READY_FOR_REVIEW
            else:
                resolved = PreviewReadiness.NOT_READY
        else:
            resolved = (
                readiness
                if isinstance(readiness, PreviewReadiness)
                else PreviewReadiness(str(readiness).strip().lower())
            )
        return cls(
            preview_id=pid,
            workspace_id=wid,
            hierarchy=nodes,
            objectives=objs,
            prerequisites=prereqs,
            estimated_workload_hours=hours,
            validation_passed=bool(validation_passed),
            publication_ready=bool(publication_ready),
            readiness=resolved,
            subject_code=(subject_code or "").strip().upper(),
            version_label=(version_label or "").strip(),
        )

    @property
    def node_count(self) -> int:
        """Number of hierarchy nodes."""
        return len(self.hierarchy)

    @property
    def objective_count(self) -> int:
        """Number of objectives."""
        return len(self.objectives)

    @property
    def prerequisite_count(self) -> int:
        """Number of prerequisite edges."""
        return len(self.prerequisites)

    @property
    def is_approved(self) -> bool:
        """True when preview readiness is APPROVED."""
        return self.readiness is PreviewReadiness.APPROVED

    def with_readiness(self, readiness: PreviewReadiness | str) -> PreviewSummary:
        """Return a copy with updated readiness."""
        resolved = (
            readiness
            if isinstance(readiness, PreviewReadiness)
            else PreviewReadiness(str(readiness).strip().lower())
        )
        return PreviewSummary(
            preview_id=self.preview_id,
            workspace_id=self.workspace_id,
            hierarchy=self.hierarchy,
            objectives=self.objectives,
            prerequisites=self.prerequisites,
            estimated_workload_hours=self.estimated_workload_hours,
            validation_passed=self.validation_passed,
            publication_ready=self.publication_ready,
            readiness=resolved,
            subject_code=self.subject_code,
            version_label=self.version_label,
        )


def _require_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a non-empty string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized
