"""Provider source protocols for Founder Operational State (FOS-005).

Providers wrap subsystem public read surfaces. Sources are injectable so
operational-state tests never depend on filesystem scanning.
"""

from __future__ import annotations

from typing import Protocol

from app.founder.operational_state.dto.capability import CapabilitySubsystemDTO
from app.founder.operational_state.dto.internal_alpha import (
    InternalAlphaSubsystemDTO,
)
from app.founder.operational_state.dto.knowledge import KnowledgeSubsystemDTO


class KnowledgeSource(Protocol):
    """Public read surface for the Knowledge Engine (FOS-001)."""

    def load(self) -> KnowledgeSubsystemDTO:
        """Return a Knowledge Engine summary for aggregation."""


class CapabilitySource(Protocol):
    """Public read surface for the Capability Archive (FOS-002)."""

    def load(self) -> CapabilitySubsystemDTO:
        """Return a Capability Archive summary for aggregation."""


class InternalAlphaSource(Protocol):
    """Public read surface for Internal Alpha processed outputs (FOS-003)."""

    def load(self) -> InternalAlphaSubsystemDTO:
        """Return an Internal Alpha summary for aggregation."""
