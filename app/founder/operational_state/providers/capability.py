"""Capability Provider — wraps Capability Archive public reads (FOS-005)."""

from __future__ import annotations

from app.founder.operational_state.dto.capability import CapabilitySubsystemDTO

DEFAULT_CAPABILITY_SOURCE_VERSION = "unwired"


class StaticCapabilitySource:
    """Injectable Capability Archive source for tests and defaults."""

    def __init__(self, dto: CapabilitySubsystemDTO | None = None) -> None:
        self._dto = dto or CapabilitySubsystemDTO(
            source_version=DEFAULT_CAPABILITY_SOURCE_VERSION,
            total_count=0,
            completed_count=0,
            active_count=0,
        )

    def load(self) -> CapabilitySubsystemDTO:
        return self._dto


class CapabilityProvider:
    """Retrieve Capability Archive summary for operational-state aggregation.

    Does not mutate archives. Does not evaluate capabilities.
    """

    def __init__(self, source: StaticCapabilitySource | None = None) -> None:
        self._source = source or StaticCapabilitySource()

    def get(self) -> CapabilitySubsystemDTO:
        """Return the Capability Archive DTO from the wrapped source."""
        return self._source.load()
