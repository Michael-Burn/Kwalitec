"""Application-layer exceptions for Mission Engine 2.0.

Framework-independent. Raised when mission lifecycle, scheduling,
validation, workload, or dispatch rules are violated.
"""

from __future__ import annotations


class MissionEngineV2Error(Exception):
    """Base exception for Mission Engine 2.0 failures."""


class MissionNotFound(MissionEngineV2Error):  # noqa: N818
    """No mission exists for the requested identity."""


class DuplicateMission(MissionEngineV2Error):  # noqa: N818
    """A mission for the same learner / date / session already exists."""


class ActiveMissionExists(MissionEngineV2Error):  # noqa: N818
    """Learner already has one active mission; another cannot be activated."""


class InvalidMissionState(MissionEngineV2Error):  # noqa: N818
    """Operation is unlawful for the mission's current lifecycle state."""


class MissionAlreadyCompleted(MissionEngineV2Error):  # noqa: N818
    """Mission has already reached a completed outcome."""


class MissionAlreadyArchived(MissionEngineV2Error):  # noqa: N818
    """Mission has been archived and no longer accepts lifecycle changes."""


class InvalidSessionReference(MissionEngineV2Error):  # noqa: N818
    """Mission references a session that is missing or inconsistent."""


class InvalidJourneyReference(MissionEngineV2Error):  # noqa: N818
    """Mission references a journey that is missing or in an unlawful state."""


class TopicUnavailable(MissionEngineV2Error):  # noqa: N818
    """Curriculum topic referenced by the mission is not available."""


class SchedulingError(MissionEngineV2Error):  # noqa: N818
    """Mission could not be scheduled under current deterministic rules."""


class WorkloadExceeded(MissionEngineV2Error):  # noqa: N818
    """Scheduling would violate structural workload limits."""


class DispatchError(MissionEngineV2Error):  # noqa: N818
    """Dispatch payload could not be produced for the mission."""


class MissionFactoryError(MissionEngineV2Error):  # noqa: N818
    """Daily mission could not be composed from upstream educational inputs."""
