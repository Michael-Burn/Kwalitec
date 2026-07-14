"""Capability Archive subsystem DTO for operational-state aggregation."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CapabilitySubsystemDTO:
    """Summary read-model from the Capability Archive (FOS-002).

    Inventory counts and identifiers only — never raw archive documents.
    """

    source_version: str
    total_count: int
    completed_count: int
    active_count: int
    archive_inconsistencies: int = 0
    current_release: str = ""
    recent_capability_ids: tuple[str, ...] = ()
