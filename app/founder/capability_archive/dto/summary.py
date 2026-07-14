"""Capability Archive inventory summary DTO (FOS-002)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CapabilityArchiveSummaryDTO:
    """Aggregated Capability Archive inventory for consumers."""

    source_version: str
    total_count: int
    completed_count: int
    active_count: int
    archive_inconsistencies: int = 0
    current_release: str = ""
    recent_capability_ids: tuple[str, ...] = ()
    missing_artefacts: tuple[str, ...] = ()
    duplicate_capability_ids: tuple[str, ...] = ()
