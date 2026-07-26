"""Policy Evaluation Factory (MS-006 E3).

Deterministic PolicyEvaluation construction:
validate → assess → explain → assemble → assign evaluation_id → telemetry.

Consumes immutable ExperimentObservations and registered PolicyDefinitions
only. Never mutates observations or evidence, never promotes policies, never
persists, never changes educational behaviour.
"""

from __future__ import annotations

import hashlib
import time
from collections.abc import Sequence
from dataclasses import replace

from app.infrastructure.adapters.evidence_platform.contracts import (
    EVIDENCE_VERSION_E3,
    ExperimentObservation,
    PolicyDefinition,
    PolicyEvaluation,
    serialize_canonical,
)
from app.infrastructure.adapters.evidence_platform.evaluation_assembler import (
    EvaluationAssembler,
    build_evaluation_assembler,
)
from app.infrastructure.adapters.evidence_platform.evaluation_explainability import (
    EvaluationExplainability,
    build_evaluation_explainability,
)
from app.infrastructure.adapters.evidence_platform.evaluation_telemetry import (
    emit_completed,
    emit_failed,
    emit_latency,
    emit_requested,
)
from app.infrastructure.adapters.evidence_platform.evaluation_validator import (
    EvaluationValidationError,
    EvaluationValidator,
    build_evaluation_validator,
)
from app.infrastructure.adapters.evidence_platform.evaluator import (
    PolicyEvaluator,
    build_policy_evaluator,
)
from app.infrastructure.adapters.evidence_platform.policy_registry import (
    PolicyDefinitionRegistry,
    build_policy_definition_registry,
)
from app.infrastructure.events.registry import EventRegistry


class PolicyEvaluationFactory:
    """Create immutable PolicyEvaluation artefacts (E3).

    Identical ExperimentObservations + Identical PolicyDefinition → Identical
    PolicyEvaluation every execution.
    """

    FACTORY_ID = "policy_evaluation_factory"
    FACTORY_VERSION = "1.0.0-e3"
    ENGINE_VERSION = EVIDENCE_VERSION_E3

    def __init__(
        self,
        *,
        evaluator: PolicyEvaluator | None = None,
        assembler: EvaluationAssembler | None = None,
        explainability: EvaluationExplainability | None = None,
        validator: EvaluationValidator | None = None,
        registry: PolicyDefinitionRegistry | None = None,
        events: EventRegistry | None = None,
        enabled: bool = True,
    ) -> None:
        self._validator = validator or EvaluationValidator()
        self._registry = registry or PolicyDefinitionRegistry(
            validator=self._validator
        )
        self._evaluator = evaluator or PolicyEvaluator(validator=self._validator)
        self._explainability = explainability or EvaluationExplainability()
        self._assembler = assembler or EvaluationAssembler(
            validator=self._validator
        )
        self._events = events
        self._enabled = bool(enabled)

    @property
    def factory_id(self) -> str:
        return self.FACTORY_ID

    @property
    def factory_version(self) -> str:
        return self.FACTORY_VERSION

    @property
    def registry(self) -> PolicyDefinitionRegistry:
        return self._registry

    @property
    def evaluator(self) -> PolicyEvaluator:
        return self._evaluator

    @property
    def assembler(self) -> EvaluationAssembler:
        return self._assembler

    @property
    def explainability(self) -> EvaluationExplainability:
        return self._explainability

    @property
    def validator(self) -> EvaluationValidator:
        return self._validator

    def is_enabled(self) -> bool:
        return self._enabled

    def register_definition(
        self,
        definition: PolicyDefinition,
        *,
        replace: bool = False,
    ) -> PolicyDefinition:
        """Register a policy definition in the in-memory registry."""
        self._ensure_enabled()
        return self._registry.register(definition, replace=replace)

    def evaluate(
        self,
        observations: Sequence[ExperimentObservation],
        definition: PolicyDefinition | None = None,
        *,
        policy_id: str | None = None,
        created_at: str | None = None,
    ) -> PolicyEvaluation:
        """Evaluate observations against a registered / provided definition.

        Provide either ``definition`` or ``policy_id`` (registry lookup).
        Observations and evidence are never mutated. No policy promotion.
        """
        self._ensure_enabled()
        resolved = self._resolve_definition(
            definition=definition, policy_id=policy_id
        )
        started = time.perf_counter()
        if self._events is not None:
            emit_requested(
                self._events,
                policy_id=resolved.policy_id,
                policy_version=resolved.policy_version,
                observation_count=len(tuple(observations or ())),
            )
        try:
            # Freeze input serializations to assert immutability after evaluate.
            input_snapshots = tuple(obs.serialize() for obs in observations)
            assessment = self._evaluator.assess(observations, resolved)
            explanation = self._explainability.build(
                definition=resolved,
                observations=observations,
                assessment=assessment,
            )
            # Deterministic created_at from observation material when omitted.
            resolved_created_at = created_at
            if resolved_created_at is None:
                resolved_created_at = _deterministic_created_at(observations)
            draft = self._assembler.assemble(
                definition=resolved,
                assessment=assessment,
                explanation=explanation,
                evaluation_id="",
                created_at=resolved_created_at,
            )
            evaluation_id = deterministic_evaluation_id(draft)
            evaluation = replace(draft, evaluation_id=evaluation_id)
            validated = self._validator.validate_evaluation(evaluation)

            for original, current in zip(
                input_snapshots, observations, strict=True
            ):
                if current.serialize() != original:
                    raise EvaluationValidationError(
                        "ExperimentObservation mutated during evaluation"
                    )

            if self._events is not None:
                emit_completed(
                    self._events,
                    policy_id=validated.policy_id,
                    policy_version=validated.policy_version,
                    evaluation_id=validated.evaluation_id,
                    gate_result=validated.gate_result,
                    recommendation=validated.recommendation,
                    confidence_band=validated.confidence_band,
                    experiment_refs=validated.experiment_refs,
                    evidence_refs=validated.evidence_refs,
                )
                emit_latency(
                    self._events,
                    policy_id=validated.policy_id,
                    duration_ms=round((time.perf_counter() - started) * 1000, 3),
                    ok=True,
                )
            return validated
        except Exception as exc:
            if self._events is not None:
                emit_failed(
                    self._events,
                    policy_id=resolved.policy_id,
                    policy_version=resolved.policy_version,
                    error_code=type(exc).__name__,
                    message=str(exc),
                )
                emit_latency(
                    self._events,
                    policy_id=resolved.policy_id,
                    duration_ms=round((time.perf_counter() - started) * 1000, 3),
                    ok=False,
                )
            raise

    def evaluate_registered(
        self,
        observations: Sequence[ExperimentObservation],
        policy_id: str,
        *,
        created_at: str | None = None,
    ) -> PolicyEvaluation:
        """Evaluate using a registry lookup by policy_id."""
        return self.evaluate(
            observations, policy_id=policy_id, created_at=created_at
        )

    def _resolve_definition(
        self,
        *,
        definition: PolicyDefinition | None,
        policy_id: str | None,
    ) -> PolicyDefinition:
        if definition is not None and policy_id is not None:
            if definition.policy_id != (policy_id or "").strip():
                raise EvaluationValidationError(
                    "definition.policy_id must match policy_id"
                )
        if definition is not None:
            return self._validator.validate_definition(
                definition, require_evaluable=True
            )
        key = (policy_id or "").strip()
        if not key:
            raise EvaluationValidationError("provide definition or policy_id")
        return self._validator.validate_definition(
            self._registry.require(key), require_evaluable=True
        )

    def _ensure_enabled(self) -> None:
        if not self._enabled:
            raise EvaluationValidationError(
                "PolicyEvaluationFactory is disabled (feature flag OFF)"
            )


def deterministic_evaluation_id(evaluation: PolicyEvaluation) -> str:
    """Derive evaluation_id from material fields (excludes evaluation_id)."""
    material = {
        "baseline_policy_version": evaluation.baseline_policy_version,
        "confidence_band": evaluation.confidence_band,
        "confidence_rationale": evaluation.confidence_rationale,
        "created_at": evaluation.created_at,
        "engine_version": evaluation.engine_version or EVIDENCE_VERSION_E3,
        "evaluation_version": evaluation.evaluation_version or EVIDENCE_VERSION_E3,
        "evidence_bundle_ids": list(evaluation.evidence_bundle_ids),
        "evidence_refs": list(evaluation.evidence_refs),
        "experiment_id": evaluation.experiment_id,
        "experiment_refs": list(evaluation.experiment_refs),
        "explanation": evaluation.explanation.to_canonical_dict(),
        "gate_codes": list(evaluation.gate_codes),
        "gate_result": evaluation.gate_result,
        "limitations": list(evaluation.limitations),
        "outcome_metrics": [
            metric.to_canonical_dict() for metric in evaluation.outcome_metrics
        ],
        "policy_id": evaluation.policy_id,
        "policy_version": evaluation.policy_version,
        "provenance": dict(evaluation.provenance),
        "recommendation": evaluation.recommendation,
        "statistical_summary": dict(evaluation.statistical_summary),
    }
    digest = hashlib.sha256(
        serialize_canonical(material).encode("utf-8")
    ).hexdigest()
    return f"eval-{digest[:24]}"


def _deterministic_created_at(
    observations: Sequence[ExperimentObservation],
) -> str | None:
    """Use max observation observed_at when present (no wall-clock invent)."""
    stamps = sorted(
        obs.observed_at for obs in observations if obs.observed_at
    )
    return stamps[-1] if stamps else None


def build_policy_evaluation_factory(
    *,
    enabled: bool,
    evaluator: PolicyEvaluator | None = None,
    assembler: EvaluationAssembler | None = None,
    explainability: EvaluationExplainability | None = None,
    validator: EvaluationValidator | None = None,
    registry: PolicyDefinitionRegistry | None = None,
    events: EventRegistry | None = None,
    definitions: tuple[PolicyDefinition, ...] | None = None,
) -> PolicyEvaluationFactory | None:
    """DI helper — construct PolicyEvaluationFactory only when the flag is on."""
    if not enabled:
        return None
    wired_validator = validator or build_evaluation_validator()
    wired_registry = registry or build_policy_definition_registry(
        enabled=True,
        validator=wired_validator,
        definitions=definitions,
    )
    if wired_registry is None:
        return None
    wired_evaluator = evaluator or build_policy_evaluator(
        enabled=True, validator=wired_validator
    )
    if wired_evaluator is None:
        return None
    wired_assembler = assembler or build_evaluation_assembler(
        enabled=True, validator=wired_validator
    )
    if wired_assembler is None:
        return None
    wired_explainability = explainability or build_evaluation_explainability()
    return PolicyEvaluationFactory(
        evaluator=wired_evaluator,
        assembler=wired_assembler,
        explainability=wired_explainability,
        validator=wired_validator,
        registry=wired_registry,
        events=events,
        enabled=True,
    )
