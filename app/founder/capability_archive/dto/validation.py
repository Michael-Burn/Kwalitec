"""Validation cargo for Capability Archive scans (FOS-002)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ArchiveValidationIssue:
    """One deterministic Capability Archive validation finding."""

    code: str
    message: str
    capability_id: str = ""


@dataclass(frozen=True)
class ArchiveValidationReport:
    """Immutable report of Capability Archive validation."""

    issues: tuple[ArchiveValidationIssue, ...]

    @property
    def ok(self) -> bool:
        return len(self.issues) == 0

    @property
    def error_count(self) -> int:
        return len(self.issues)

    @property
    def missing_artefacts(self) -> tuple[str, ...]:
        missing_codes = {
            "missing_field",
            "missing_archive_root",
            "missing_entries_dir",
        }
        return tuple(i.message for i in self.issues if i.code in missing_codes)

    @property
    def duplicate_capability_ids(self) -> tuple[str, ...]:
        return tuple(
            sorted(
                {
                    i.capability_id
                    for i in self.issues
                    if i.code == "duplicate_capability_id" and i.capability_id
                }
            )
        )
