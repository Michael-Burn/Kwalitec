"""CapabilityArchiveQueryService — public query API (FOS-002).

This service is the only public API exposed by the Capability Archive.
Consumers must not access the repository scanner or filesystem paths.
"""

from __future__ import annotations

from pathlib import Path

from app.founder.capability_archive.config import (
    CapabilityArchiveConfig,
    default_config,
    discover_repo_root,
)
from app.founder.capability_archive.dto.record import CapabilityRecordDTO
from app.founder.capability_archive.dto.summary import CapabilityArchiveSummaryDTO
from app.founder.capability_archive.dto.validation import (
    ArchiveValidationIssue,
    ArchiveValidationReport,
)
from app.founder.capability_archive.repository import CapabilityArchiveScanner
from app.founder.capability_archive.validators import CapabilityArchiveValidator


class CapabilityArchiveQueryService:
    """Query Capability Archive records from a repository-backed store.

    Integration only — no AI, no persistence, no capability evaluation.
    """

    def __init__(
        self,
        *,
        repo_root: Path | None = None,
        config: CapabilityArchiveConfig | None = None,
        validator: CapabilityArchiveValidator | None = None,
    ) -> None:
        self._root = (repo_root or discover_repo_root()).resolve()
        self._config = config or default_config()
        self._validator = validator or CapabilityArchiveValidator()
        self._scanner = CapabilityArchiveScanner(
            repo_root=self._root,
            config=self._config,
        )
        self._records: tuple[CapabilityRecordDTO, ...] | None = None
        self._report: ArchiveValidationReport | None = None

    def refresh(self) -> None:
        """Re-scan the archive and replace the in-memory inventory."""
        scan = self._scanner.scan()
        self._records = scan.records
        self._report = self._validator.validate(scan)

    def list_capabilities(self) -> tuple[CapabilityRecordDTO, ...]:
        """Return all archived capability records (immutable DTOs)."""
        return self._ensure_index()

    def get_capability(self, capability_id: str) -> CapabilityRecordDTO | None:
        """Return one capability by id, or None when absent."""
        needle = capability_id.strip()
        for record in self._ensure_index():
            if record.capability_id == needle:
                return record
        return None

    def get_summary(self) -> CapabilityArchiveSummaryDTO:
        """Return aggregated archive inventory for consumers."""
        records = self._ensure_index()
        report = self._report or ArchiveValidationReport(issues=())
        completed = sum(
            1
            for r in records
            if r.status.lower() in self._config.completed_statuses
        )
        active = sum(
            1 for r in records if r.status.lower() in self._config.active_statuses
        )
        recent = tuple(
            r.capability_id for r in records[: self._config.recent_limit]
        )
        release = self._derive_release(records)
        return CapabilityArchiveSummaryDTO(
            source_version=self._config.source_version,
            total_count=len(records),
            completed_count=completed,
            active_count=active,
            archive_inconsistencies=report.error_count,
            current_release=release,
            recent_capability_ids=recent,
            missing_artefacts=report.missing_artefacts,
            duplicate_capability_ids=report.duplicate_capability_ids,
        )

    def list_validation_issues(self) -> tuple[ArchiveValidationIssue, ...]:
        """Return validation issues (missing fields, duplicates, etc.)."""
        self._ensure_index()
        assert self._report is not None
        return self._report.issues

    def _ensure_index(self) -> tuple[CapabilityRecordDTO, ...]:
        if self._records is None:
            self.refresh()
        assert self._records is not None
        return self._records

    def _derive_release(self, records: tuple[CapabilityRecordDTO, ...]) -> str:
        versions = [r.version for r in records if r.version]
        if not versions:
            return self._config.default_release
        # Deterministic: lexicographic max among non-empty version labels.
        return max(versions)
