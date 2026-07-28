"""Exceptions for Twin Inference Engine application services (EI-006)."""

from __future__ import annotations


class TwinInferenceError(Exception):
    """Base error for twin inference services."""


class InstanceNotFoundError(TwinInferenceError):
    """Requested Student Curriculum Instance does not exist."""


class NodeNotFoundError(TwinInferenceError):
    """Requested curriculum node is not part of the SCI."""


class BeliefNotFoundError(TwinInferenceError):
    """Requested Twin belief does not exist."""
