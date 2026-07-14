"""Capability Archive snapshot DTOs for Founder Dashboard (FOS-004 / FSI-002)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CapabilityEntry:
    """One Capability Archive row for display.

    Retained for compatibility; FSI-002 projects Operational State
    ``recent_capability_ids`` rather than full archive rows.
    """

    capability_id: str
    title: str
    status: str
    version: str
    completion_date: str


@dataclass(frozen=True)
class CapabilitySnapshot:
    """Immutable Capability Archive summary for the dashboard."""

    entries: tuple[CapabilityEntry, ...]
    total_count: int
    completed_count: int
    active_count: int
    archive_inconsistencies: int = 0
    current_release: str = ""
    recent_completed_ids: tuple[str, ...] = ()


@dataclass(frozen=True)
class CapabilitySection:
    """Capability Archive panel for the Founder Dashboard."""

    entries: tuple[CapabilityEntry, ...]
    total_count: int
    completed_count: int
    active_count: int
    recent_capability_ids: tuple[str, ...] = ()
    archive_inconsistencies: int = 0
