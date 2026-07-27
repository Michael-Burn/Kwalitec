"""Graph and mapping validation contracts (CIP-002)."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class ValidationIssueKind(StrEnum):
    """Deterministic validation failure categories."""

    ORPHAN_CONCEPT = "orphan_concept"
    CIRCULAR_PREREQUISITE = "circular_prerequisite"
    DUPLICATE_CONCEPT = "duplicate_concept"
    MISSING_LEARNING_OBJECTIVE = "missing_learning_objective"
    BROKEN_DOCUMENT_REFERENCE = "broken_document_reference"
    INVALID_GRAPH_EDGE = "invalid_graph_edge"
    VERSION_INCONSISTENCY = "version_inconsistency"
    LOW_CONFIDENCE_CLUSTER = "low_confidence_cluster"


class ValidationSeverity(StrEnum):
    """Issue severity for Founder triage."""

    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


@dataclass(frozen=True)
class ValidationIssue:
    """One validation finding against the curriculum knowledge graph."""

    issue_id: str
    kind: ValidationIssueKind
    severity: ValidationSeverity
    message: str
    subject_kind: str
    subject_id: str
    related_ids: tuple[str, ...] = ()
    document_id: int | None = None


@dataclass(frozen=True)
class ValidationReport:
    """Validation snapshot for one document / graph."""

    report_id: str
    document_id: int
    graph_id: str
    map_id: str
    pipeline_job_id: str
    issue_count: int
    error_count: int
    warning_count: int
    passed: bool
    issues: tuple[ValidationIssue, ...]
    created_at_iso: str
