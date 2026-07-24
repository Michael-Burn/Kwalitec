"""Correlation ID generation for analytics event linkage."""

from __future__ import annotations

from uuid import uuid4


def new_correlation_id() -> str:
    """Allocate a new analytics correlation id (hex UUID)."""
    return uuid4().hex
