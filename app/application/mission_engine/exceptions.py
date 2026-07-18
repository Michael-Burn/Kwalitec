"""Application-layer exceptions for Mission Engine 2.0.

Framework-independent. Raised when mission lifecycle, scheduling,
validation, or delivery rules are violated.
"""

from __future__ import annotations


class MissionEngineError(Exception):
    """Base exception for Mission Engine 2.0 failures."""


class MissionNotFound(MissionEngineError):  # noqa: N818
    """No mission exists for the requested identity."""


class DuplicateMission(MissionEngineError):  # noqa: N818
    """A mission for the same learner / date / session already exists."""


class ActiveMissionExists(MissionEngineError):  # noqa: N818
    """Learner already has one active mission; another cannot be activated."""


class InvalidMissionState(MissionEngineError):  # noqa: N818
    """Operation is unlawful for the mission's current lifecycle state."""


class MissionAlreadyCompleted(MissionEngineError):  # noqa: N818
    """Mission has already reached a completed outcome."""


class MissionAlreadyArchived(MissionEngineError):  # noqa: N818
    """Mission has been archived and no longer accepts lifecycle changes."""


class InvalidSessionReference(MissionEngineError):  # noqa: N818
    """Mission references a session that is missing or inconsistent."""


class InvalidJourneyReference(MissionEngineError):  # noqa: N818
    """Mission references a journey that is missing or in an unlawful state."""


class SchedulingError(MissionEngineError):  # noqa: N818
    """Mission could not be scheduled under current deterministic rules."""


class WorkloadExceeded(MissionEngineError):  # noqa: N818
    """Scheduling would violate workload limits (e.g. more than one active)."""


class DeliveryError(MissionEngineError):  # noqa: N818
    """Delivery payload could not be produced for the mission."""


class MissionBuildError(MissionEngineError):  # noqa: N818
    """Daily mission could not be built from journey / runtime inputs."""
