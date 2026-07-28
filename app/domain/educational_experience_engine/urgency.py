"""Urgency catalogue for Educational Experience Engine (EX-001).

Urgency is a presentation signal derived from educational decision priority
and type. It never alters the underlying Educational Decision.
"""

from __future__ import annotations

from enum import StrEnum


class UrgencyLevel(StrEnum):
    """Student-facing urgency bands for experience presentation."""

    CRITICAL = "critical"
    HIGH = "high"
    MODERATE = "moderate"
    LOW = "low"
