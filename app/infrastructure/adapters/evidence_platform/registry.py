"""Experiment definition registry (MS-006 E2).

In-memory registry of immutable ExperimentDefinition instances. No persistence.
Definitions are validated on register; Evidence Records are never stored or
mutated here.
"""

from __future__ import annotations

from app.infrastructure.adapters.evidence_platform.contracts import (
    ExperimentDefinition,
)
from app.infrastructure.adapters.evidence_platform.experiment_validator import (
    ExperimentValidationError,
    ExperimentValidator,
)


class ExperimentDefinitionRegistry:
    """Register and look up ExperimentDefinition protocols (in-memory only)."""

    REGISTRY_ID = "experiment_definition_registry"
    REGISTRY_VERSION = "1.0.0-e2"

    def __init__(
        self,
        *,
        validator: ExperimentValidator | None = None,
        definitions: tuple[ExperimentDefinition, ...] | None = None,
    ) -> None:
        self._validator = validator or ExperimentValidator()
        self._definitions: dict[str, ExperimentDefinition] = {}
        for definition in definitions or ():
            self.register(definition)

    @property
    def registry_id(self) -> str:
        return self.REGISTRY_ID

    @property
    def registry_version(self) -> str:
        return self.REGISTRY_VERSION

    @property
    def validator(self) -> ExperimentValidator:
        return self._validator

    def register(
        self,
        definition: ExperimentDefinition,
        *,
        replace: bool = False,
    ) -> ExperimentDefinition:
        """Validate and register a definition. Raises on duplicate unless replace."""
        validated = self._validator.validate_definition(definition)
        experiment_id = validated.experiment_id
        if experiment_id in self._definitions and not replace:
            raise ExperimentValidationError(
                f"experiment already registered: {experiment_id}"
            )
        self._definitions[experiment_id] = validated
        return validated

    def get(self, experiment_id: str) -> ExperimentDefinition | None:
        """Return registered definition or None."""
        key = (experiment_id or "").strip()
        if not key:
            return None
        return self._definitions.get(key)

    def require(self, experiment_id: str) -> ExperimentDefinition:
        """Return registered definition or raise."""
        definition = self.get(experiment_id)
        if definition is None:
            raise ExperimentValidationError(
                f"experiment not registered: {(experiment_id or '').strip()}"
            )
        return definition

    def contains(self, experiment_id: str) -> bool:
        """True when experiment_id is registered."""
        return self.get(experiment_id) is not None

    def list_ids(self) -> tuple[str, ...]:
        """Deterministic sorted experiment ids."""
        return tuple(sorted(self._definitions.keys()))

    def list_definitions(self) -> tuple[ExperimentDefinition, ...]:
        """Deterministic sorted definitions by experiment_id."""
        return tuple(
            self._definitions[key] for key in sorted(self._definitions.keys())
        )

    def unregister(self, experiment_id: str) -> bool:
        """Remove a definition if present. Returns True when removed."""
        key = (experiment_id or "").strip()
        if key in self._definitions:
            del self._definitions[key]
            return True
        return False

    def clear(self) -> None:
        """Remove all registered definitions."""
        self._definitions.clear()

    def __len__(self) -> int:
        return len(self._definitions)

    def __contains__(self, experiment_id: object) -> bool:
        if not isinstance(experiment_id, str):
            return False
        return self.contains(experiment_id)


def build_experiment_definition_registry(
    *,
    enabled: bool,
    validator: ExperimentValidator | None = None,
    definitions: tuple[ExperimentDefinition, ...] | None = None,
) -> ExperimentDefinitionRegistry | None:
    """DI helper — construct registry only when the feature flag is on."""
    if not enabled:
        return None
    return ExperimentDefinitionRegistry(
        validator=validator,
        definitions=definitions,
    )
