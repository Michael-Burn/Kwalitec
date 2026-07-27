"""Exceptions for the Founder → Student bridge (PI-002A)."""

from __future__ import annotations


class PlatformIntegrationError(Exception):
    """Base error for PI-002A bridge operations."""


class PublishedSubjectNotDiscoverable(PlatformIntegrationError):  # noqa: N818
    """Published subject is not available in student discovery."""


class BridgeEnrolmentBlocked(PlatformIntegrationError):  # noqa: N818
    """Enrolment was refused by bridge policy or flags."""
