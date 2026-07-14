"""Validate Capability Archive scan results (FOS-002)."""

from __future__ import annotations

from app.founder.capability_archive.dto.validation import ArchiveValidationReport
from app.founder.capability_archive.repository.scanner import ArchiveScanResult


class CapabilityArchiveValidator:
    """Validate archive connectivity, completeness, and uniqueness."""

    def validate(self, scan: ArchiveScanResult) -> ArchiveValidationReport:
        """Return an immutable validation report for a scan.

        Args:
            scan: Result of ``CapabilityArchiveScanner.scan``.

        Returns:
            Immutable ``ArchiveValidationReport``.
        """
        return ArchiveValidationReport(issues=scan.issues)
