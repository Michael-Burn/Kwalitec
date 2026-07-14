"""Capability Archive (FOS-002).

Repository-backed capability inventory. Public API:
``CapabilityArchiveQueryService`` — the only surface other Founder
components may use.

No Flask, no persistence, no AI.
"""

from __future__ import annotations

from app.founder.capability_archive.config import (
    CapabilityArchiveConfig,
    default_config,
    discover_repo_root,
)
from app.founder.capability_archive.dto import (
    ArchiveValidationIssue,
    ArchiveValidationReport,
    CapabilityArchiveSummaryDTO,
    CapabilityRecordDTO,
)
from app.founder.capability_archive.services import CapabilityArchiveQueryService

__all__ = [
    "ArchiveValidationIssue",
    "ArchiveValidationReport",
    "CapabilityArchiveConfig",
    "CapabilityArchiveQueryService",
    "CapabilityArchiveSummaryDTO",
    "CapabilityRecordDTO",
    "default_config",
    "discover_repo_root",
]
