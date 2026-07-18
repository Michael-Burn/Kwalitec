"""Application-layer exceptions for the Mission Adapter.

Framework-independent. Raised when routing, comparison, migration,
engine availability, or audit rules are violated.
"""

from __future__ import annotations


class MissionAdapterError(Exception):
    """Base exception for Mission Adapter failures."""


class RoutingError(MissionAdapterError):
    """Routing decision could not be produced under current policy."""


class ComparisonFailure(MissionAdapterError):  # noqa: N818
    """Parallel / shadow comparison could not be completed safely."""


class MigrationStateError(MissionAdapterError):
    """Requested migration transition is unlawful."""


class EngineUnavailable(MissionAdapterError):  # noqa: N818
    """A required mission engine port is missing or unhealthy."""


class AuditFailure(MissionAdapterError):  # noqa: N818
    """An immutable audit record could not be generated."""
