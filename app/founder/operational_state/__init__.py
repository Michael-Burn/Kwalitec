"""Founder Operational State Service (FOS-005).

Aggregates Knowledge Engine, Capability Archive, and Internal Alpha
summaries into one immutable operational snapshot.

Aggregation only — no AI, recommendations, scoring, or release decisions.
"""

from __future__ import annotations

from app.founder.operational_state.models import FounderOperationalState
from app.founder.operational_state.services import FounderOperationalStateService

__all__ = [
    "FounderOperationalState",
    "FounderOperationalStateService",
]
