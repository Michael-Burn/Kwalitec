"""Exceptions for Runtime Integration (RI-001).

RIS never invents educational recommendations. Failures are orchestration /
prerequisite gaps — not educational reasoning errors.
"""

from __future__ import annotations


class RuntimeIntegrationError(Exception):
    """Base error for Runtime Integration orchestration."""


class IntegrationUnavailableError(RuntimeIntegrationError):
    """Preferred authority and compatibility path both failed to produce output."""
