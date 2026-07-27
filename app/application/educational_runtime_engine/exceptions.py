"""Application exceptions for Educational Runtime Engine (PI-001C)."""

from __future__ import annotations


class EducationalRuntimeError(Exception):
    """Base exception for curriculum-driven runtime failures."""


class PublishedCurriculumUnavailable(EducationalRuntimeError):  # noqa: N818
    """No active published curriculum package for the subject."""


class EnrolmentNotFound(EducationalRuntimeError):  # noqa: N818
    """Student enrolment was not found."""


class EnrolmentAlreadyExists(EducationalRuntimeError):  # noqa: N818
    """Student is already enrolled for this curriculum identity."""


class StudyPlanInstanceNotFound(EducationalRuntimeError):  # noqa: N818
    """Study plan instance was not found."""


class MissionInstanceNotFound(EducationalRuntimeError):  # noqa: N818
    """Mission instance was not found."""


class MissionAlreadyCompleted(EducationalRuntimeError):  # noqa: N818
    """Mission instance is already completed."""


class SyllabusAlreadyComplete(EducationalRuntimeError):  # noqa: N818
    """No further learning missions remain for this plan."""


class IllegalRuntimeState(EducationalRuntimeError):  # noqa: N818
    """Requested runtime operation violates state rules."""
