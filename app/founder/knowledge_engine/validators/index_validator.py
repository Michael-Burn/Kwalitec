"""Validate Knowledge Engine scan results (FOS-001)."""

from __future__ import annotations

from app.founder.knowledge_engine.dto.validation import (
    KnowledgeValidationIssue,
    KnowledgeValidationReport,
)
from app.founder.knowledge_engine.repository.scanner import ScanResult


class KnowledgeIndexValidator:
    """Validate scan connectivity and artefact completeness signals."""

    def validate(self, scan: ScanResult) -> KnowledgeValidationReport:
        """Build a validation report from a scan result.

        Args:
            scan: Result of ``KnowledgeRepositoryScanner.scan``.

        Returns:
            Immutable ``KnowledgeValidationReport``.
        """
        issues: list[KnowledgeValidationIssue] = list(scan.issues)
        if not scan.artefacts and not scan.missing_roots:
            issues.append(
                KnowledgeValidationIssue(
                    code="empty_index",
                    message="Repository scan completed but indexed zero artefacts.",
                )
            )
        return KnowledgeValidationReport(issues=tuple(issues))
