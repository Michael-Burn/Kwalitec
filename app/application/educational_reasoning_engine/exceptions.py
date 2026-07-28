"""Exceptions for Educational Reasoning Engine application services (EI-007)."""

from __future__ import annotations


class EducationalReasoningError(Exception):
    """Base error for educational reasoning services."""


class InstanceNotFoundError(EducationalReasoningError):
    """Requested Student Curriculum Instance does not exist."""


class DecisionNotFoundError(EducationalReasoningError):
    """Requested educational decision does not exist."""
