"""Reasoning rule-set version for Educational Reasoning Engine (EI-007).

Decisions always carry the version of the deterministic rule pack that
produced them so rebuilds remain auditable and comparable.
"""

from __future__ import annotations

# Bump when rule weights, thresholds, prioritisation, or decision types change.
REASONING_VERSION = "ere.v1"
"""Stable identifier for the EI-007 deterministic reasoning pack."""
