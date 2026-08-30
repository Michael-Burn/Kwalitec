"""ADR-027 M0 / Phase 3 Adaptive Decision package.

SittingDecisionOrchestrator coordinates Policy V0 or Policy V1 decisions and
Runtime C materialisation. Runtime C must not import this package.
"""

from __future__ import annotations

from app.application.adaptive_decision.orchestrator import (
    SittingDecisionOrchestrator,
)
from app.application.adaptive_decision.policy_v0 import (
    PolicyV0AdaptiveDecisionEngine,
)
from app.application.adaptive_decision.policy_v1 import (
    PolicyV1AdaptiveDecisionEngine,
)
from app.application.adaptive_decision.types import (
    DailySittingRequest,
    DecisionOutcome,
    SittingDecision,
)

__all__ = [
    "DailySittingRequest",
    "DecisionOutcome",
    "PolicyV0AdaptiveDecisionEngine",
    "PolicyV1AdaptiveDecisionEngine",
    "SittingDecision",
    "SittingDecisionOrchestrator",
]
