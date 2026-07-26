"""Experiment Framework orchestrator (MS-006 E2).

Coordinates registry lookup, validation, deterministic assignment, and
telemetry. Consumes validated EvidenceRecords and registered
ExperimentDefinitions only. Never mutates evidence, never scores
experiments, never runs policy evaluation / analytics, never persists,
never changes educational behaviour.
"""

from __future__ import annotations

import time

from app.infrastructure.adapters.evidence_platform.assigner import (
    ExperimentAssigner,
    build_experiment_assigner,
)
from app.infrastructure.adapters.evidence_platform.contracts import (
    EvidenceRecord,
    ExperimentDefinition,
    ExperimentObservation,
)
from app.infrastructure.adapters.evidence_platform.experiment_telemetry import (
    emit_completed,
    emit_failed,
    emit_latency,
    emit_requested,
)
from app.infrastructure.adapters.evidence_platform.experiment_validator import (
    ExperimentValidationError,
    ExperimentValidator,
    build_experiment_validator,
)
from app.infrastructure.adapters.evidence_platform.registry import (
    ExperimentDefinitionRegistry,
    build_experiment_definition_registry,
)
from app.infrastructure.events.registry import EventRegistry


class ExperimentFramework:
    """Deterministic experiment assignment framework (E2).

    Identical EvidenceRecord + Identical ExperimentDefinition → Identical
    ExperimentObservation every execution.
    """

    FRAMEWORK_ID = "experiment_framework"
    FRAMEWORK_VERSION = "1.0.0-e2"

    def __init__(
        self,
        *,
        registry: ExperimentDefinitionRegistry | None = None,
        assigner: ExperimentAssigner | None = None,
        validator: ExperimentValidator | None = None,
        events: EventRegistry | None = None,
        enabled: bool = True,
    ) -> None:
        self._validator = validator or ExperimentValidator()
        self._registry = registry or ExperimentDefinitionRegistry(
            validator=self._validator
        )
        self._assigner = assigner or ExperimentAssigner(validator=self._validator)
        self._events = events
        self._enabled = bool(enabled)

    @property
    def framework_id(self) -> str:
        return self.FRAMEWORK_ID

    @property
    def framework_version(self) -> str:
        return self.FRAMEWORK_VERSION

    @property
    def registry(self) -> ExperimentDefinitionRegistry:
        return self._registry

    @property
    def assigner(self) -> ExperimentAssigner:
        return self._assigner

    @property
    def validator(self) -> ExperimentValidator:
        return self._validator

    def is_enabled(self) -> bool:
        return self._enabled

    def register_definition(
        self,
        definition: ExperimentDefinition,
        *,
        replace: bool = False,
    ) -> ExperimentDefinition:
        """Register an experiment definition in the in-memory registry."""
        self._ensure_enabled()
        return self._registry.register(definition, replace=replace)

    def assign(
        self,
        record: EvidenceRecord,
        definition: ExperimentDefinition | None = None,
        *,
        experiment_id: str | None = None,
    ) -> ExperimentObservation:
        """Assign validated evidence to a registered / provided definition.

        Provide either ``definition`` or ``experiment_id`` (registry lookup).
        EvidenceRecord is never mutated.
        """
        self._ensure_enabled()
        resolved = self._resolve_definition(
            definition=definition, experiment_id=experiment_id
        )
        student_id = getattr(record, "student_id", "") or ""
        evidence_id = getattr(record, "evidence_id", "") or ""
        started = time.perf_counter()
        if self._events is not None:
            emit_requested(
                self._events,
                student_id=student_id,
                experiment_id=resolved.experiment_id,
                evidence_id=evidence_id,
            )
        try:
            observation = self._assigner.assign(record, resolved)
            if self._events is not None:
                emit_completed(
                    self._events,
                    student_id=observation.student_id,
                    experiment_id=observation.experiment_id,
                    experiment_version=observation.experiment_version,
                    arm_id=observation.arm_id,
                    cohort=observation.cohort,
                    evidence_id=observation.evidence_id,
                    observation_id=observation.observation_id,
                    assignment_mechanism=observation.assignment_mechanism,
                )
                emit_latency(
                    self._events,
                    student_id=observation.student_id,
                    experiment_id=observation.experiment_id,
                    duration_ms=round((time.perf_counter() - started) * 1000, 3),
                    ok=True,
                )
            return observation
        except Exception as exc:
            if self._events is not None:
                emit_failed(
                    self._events,
                    student_id=student_id,
                    experiment_id=resolved.experiment_id,
                    evidence_id=evidence_id,
                    error_code=type(exc).__name__,
                    message=str(exc),
                )
                emit_latency(
                    self._events,
                    student_id=student_id,
                    experiment_id=resolved.experiment_id,
                    duration_ms=round((time.perf_counter() - started) * 1000, 3),
                    ok=False,
                )
            raise

    def assign_registered(
        self,
        record: EvidenceRecord,
        experiment_id: str,
    ) -> ExperimentObservation:
        """Assign using a registry lookup by experiment_id."""
        return self.assign(record, experiment_id=experiment_id)

    def _resolve_definition(
        self,
        *,
        definition: ExperimentDefinition | None,
        experiment_id: str | None,
    ) -> ExperimentDefinition:
        if definition is not None and experiment_id is not None:
            if definition.experiment_id != (experiment_id or "").strip():
                raise ExperimentValidationError(
                    "definition.experiment_id must match experiment_id"
                )
        if definition is not None:
            return self._validator.validate_definition(
                definition, require_assignable=True
            )
        key = (experiment_id or "").strip()
        if not key:
            raise ExperimentValidationError(
                "provide definition or experiment_id"
            )
        return self._validator.validate_definition(
            self._registry.require(key), require_assignable=True
        )

    def _ensure_enabled(self) -> None:
        if not self._enabled:
            raise ExperimentValidationError(
                "ExperimentFramework is disabled (feature flag OFF)"
            )


def build_experiment_framework(
    *,
    enabled: bool,
    registry: ExperimentDefinitionRegistry | None = None,
    assigner: ExperimentAssigner | None = None,
    validator: ExperimentValidator | None = None,
    events: EventRegistry | None = None,
    definitions: tuple[ExperimentDefinition, ...] | None = None,
) -> ExperimentFramework | None:
    """DI helper — construct ExperimentFramework only when the flag is on."""
    if not enabled:
        return None
    wired_validator = validator or build_experiment_validator()
    wired_registry = registry or build_experiment_definition_registry(
        enabled=True,
        validator=wired_validator,
        definitions=definitions,
    )
    if wired_registry is None:
        return None
    wired_assigner = assigner or build_experiment_assigner(
        enabled=True, validator=wired_validator
    )
    if wired_assigner is None:
        return None
    return ExperimentFramework(
        registry=wired_registry,
        assigner=wired_assigner,
        validator=wired_validator,
        events=events,
        enabled=True,
    )
