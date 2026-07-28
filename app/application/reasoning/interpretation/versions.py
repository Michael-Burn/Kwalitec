"""Interpretation version constants for the application layer."""

from __future__ import annotations

from app.domain.reasoning.interpretation.version import INTERPRETATION_VERSION

# Packaging versions accepted for interpretation (aligned with AP-002D1 ingress).
SUPPORTED_PACKAGING_VERSIONS: frozenset[str] = frozenset({"AP-002C.1"})

INTERPRETATION_PROVENANCE_PREFIX = "reasoning:interpretation:evidence_bundle"

__all__ = [
    "INTERPRETATION_PROVENANCE_PREFIX",
    "INTERPRETATION_VERSION",
    "SUPPORTED_PACKAGING_VERSIONS",
]
