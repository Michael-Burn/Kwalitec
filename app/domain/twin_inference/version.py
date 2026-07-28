"""Inference rule-set version for Twin Inference Engine (EI-006).

Beliefs always carry the version of the deterministic rule pack that produced
them so recalculations remain auditable and comparable.
"""

from __future__ import annotations

# Bump when rule weights, aggregation, or learning-state thresholds change.
INFERENCE_VERSION = "tie.v1"
"""Stable identifier for the EI-006 deterministic inference pack."""
