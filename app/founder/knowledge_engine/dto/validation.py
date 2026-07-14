"""Validation cargo for Knowledge Engine scans (FOS-001)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class KnowledgeValidationIssue:
    """One deterministic Knowledge Engine validation finding."""

    code: str
    message: str
    artefact_id: str = ""


@dataclass(frozen=True)
class KnowledgeValidationReport:
    """Immutable report of Knowledge Engine scan validation."""

    issues: tuple[KnowledgeValidationIssue, ...]

    @property
    def ok(self) -> bool:
        return len(self.issues) == 0

    @property
    def error_count(self) -> int:
        return len(self.issues)
