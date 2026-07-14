"""Immutable Capability Archive record DTOs (FOS-002)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CapabilityRecordDTO:
    """One Capability Archive entry.

    Related documents are logical document identifiers — never paths.
    """

    capability_id: str
    status: str
    version: str
    completion_date: str
    programme: str
    subsystem: str
    related_documents: tuple[str, ...]
    title: str = ""
