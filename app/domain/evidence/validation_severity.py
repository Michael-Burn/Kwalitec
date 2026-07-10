"""Severity levels for Evidence Candidate validation messages.

Severity is structural signalling only — not educational weight, mastery
impact, or Twin-update priority.
"""

from __future__ import annotations

from enum import Enum


class ValidationSeverity(str, Enum):
    """How strongly a validation message affects acceptance.

    Values are stable snake_case identifiers. ``ERROR`` rejects a candidate;
    ``WARNING`` and ``INFO`` do not.
    """

    ERROR = "error"
    WARNING = "warning"
    INFO = "info"
