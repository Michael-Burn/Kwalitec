"""Explainability Gate for AdaptiveOutputBundle (MS-003 A3).

Quality validator only:
  PASS → eligible for future authority (observational marker)
  FAIL → remain observational / shadow-only

Does not alter recommendations, grant authority, write Runtime A, or
change Experience behaviour.
"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass
from typing import Any

from app.infrastructure.adapters.adaptive_engine import gate_telemetry as telemetry
from app.infrastructure.adapters.adaptive_engine.contracts import (
    EXPLAINABILITY_INCOMPLETE,
    AdaptiveOutputBundle,
)
from app.infrastructure.adapters.adaptive_engine.quality_rules import (
    QualityViolation,
    evaluate_quality_rules,
)
from app.infrastructure.events.registry import EventRegistry

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class ExplainabilityGateResult:
    """Outcome of an Explainability Gate evaluation.

    The AdaptiveOutputBundle is never mutated. Eligibility is a marker for
    future cutover (A4+) — A3 does not grant Experience authority.
    """

    passed: bool
    eligible_for_future_authority: bool
    observational_only: bool
    violations: tuple[QualityViolation, ...]
    decision_id: str = ""
    error_code: str | None = None

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "decision_id": self.decision_id,
            "eligible_for_future_authority": self.eligible_for_future_authority,
            "error_code": self.error_code,
            "observational_only": self.observational_only,
            "passed": self.passed,
            "violations": [v.to_canonical_dict() for v in self.violations],
        }


class ExplainabilityGate:
    """Validate AdaptiveOutputBundle explainability without mutation.

    Executes only when constructed/enabled under Adaptive Engine + Shadow flags.
    """

    GATE_ID = "explainability_gate"
    GATE_VERSION = "1.0.0-a3"

    def __init__(
        self,
        *,
        events: EventRegistry | None = None,
        enabled: bool = True,
    ) -> None:
        self._events = events or EventRegistry()
        self._enabled = bool(enabled)

    @property
    def gate_id(self) -> str:
        return self.GATE_ID

    @property
    def gate_version(self) -> str:
        return self.GATE_VERSION

    def is_enabled(self) -> bool:
        return self._enabled

    def validate(
        self,
        output: AdaptiveOutputBundle,
        *,
        student_id: str | None = None,
    ) -> ExplainabilityGateResult:
        """Validate ``output`` and emit observational gate telemetry.

        Returns a gate result. Never mutates ``output``. Failed bundles remain
        observational only (shadow-only eligibility).
        """
        if not isinstance(output, AdaptiveOutputBundle):
            raise TypeError("output must be an AdaptiveOutputBundle")

        sid = (student_id or "").strip()
        decision_id = output.decision_id or ""

        if not self._enabled:
            # Disabled gate: treat as observational; no authority eligibility.
            return ExplainabilityGateResult(
                passed=False,
                eligible_for_future_authority=False,
                observational_only=True,
                violations=(
                    QualityViolation(
                        rule_id="explainability.gate_disabled",
                        message="Explainability Gate is disabled (feature flags OFF)",
                    ),
                ),
                decision_id=decision_id,
                error_code="UNAVAILABLE",
            )

        telemetry.emit_requested(
            self._events,
            student_id=sid,
            decision_id=decision_id,
        )
        started = time.perf_counter()
        passed = False
        try:
            # Snapshot identity before validation to prove non-mutation in tests.
            before = output.serialize()
            violations = evaluate_quality_rules(output)
            after = output.serialize()
            if before != after:
                # Defensive: quality rules must never mutate; log if violated.
                logger.error(
                    "explainability gate detected output mutation decision_id=%s",
                    decision_id,
                )
                violations = violations + (
                    QualityViolation(
                        rule_id="explainability.mutation_forbidden",
                        message="AdaptiveOutputBundle mutated during gate validation",
                    ),
                )

            passed = len(violations) == 0
            if passed:
                result = ExplainabilityGateResult(
                    passed=True,
                    eligible_for_future_authority=True,
                    observational_only=True,  # A3: no Experience cutover yet
                    violations=(),
                    decision_id=decision_id,
                    error_code=None,
                )
                telemetry.emit_passed(
                    self._events,
                    student_id=sid,
                    decision_id=decision_id,
                    topic_code=output.recommendation.topic_code,
                    decision_kind=output.recommendation.decision_kind,
                    confidence_band=output.confidence.band,
                )
            else:
                result = ExplainabilityGateResult(
                    passed=False,
                    eligible_for_future_authority=False,
                    observational_only=True,
                    violations=violations,
                    decision_id=decision_id,
                    error_code=EXPLAINABILITY_INCOMPLETE,
                )
                telemetry.emit_failed(
                    self._events,
                    student_id=sid,
                    decision_id=decision_id,
                    error_code=EXPLAINABILITY_INCOMPLETE,
                    violation_rule_ids=tuple(v.rule_id for v in violations),
                    message="; ".join(v.message for v in violations),
                )
            return result
        finally:
            latency_ms = (time.perf_counter() - started) * 1000.0
            telemetry.emit_latency(
                self._events,
                student_id=sid,
                decision_id=decision_id,
                latency_ms=latency_ms,
                passed=passed,
            )


def build_explainability_gate(
    *,
    enabled: bool,
    events: EventRegistry | None = None,
) -> ExplainabilityGate | None:
    """DI helper — construct gate only when Engine + Shadow flags are on."""
    if not enabled:
        return None
    return ExplainabilityGate(events=events, enabled=True)


__all__ = [
    "ExplainabilityGate",
    "ExplainabilityGateResult",
    "QualityViolation",
    "build_explainability_gate",
    "evaluate_quality_rules",
]
