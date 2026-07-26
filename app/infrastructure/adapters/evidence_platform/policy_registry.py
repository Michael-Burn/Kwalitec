"""Policy definition registry (MS-006 E3).

In-memory registry of immutable PolicyDefinition instances. No persistence.
Definitions are validated on register; ExperimentObservations are never stored
or mutated here.
"""

from __future__ import annotations

from app.infrastructure.adapters.evidence_platform.contracts import (
    PolicyDefinition,
)
from app.infrastructure.adapters.evidence_platform.evaluation_validator import (
    EvaluationValidationError,
    EvaluationValidator,
)


class PolicyDefinitionRegistry:
    """Register and look up PolicyDefinition protocols (in-memory only)."""

    REGISTRY_ID = "policy_definition_registry"
    REGISTRY_VERSION = "1.0.0-e3"

    def __init__(
        self,
        *,
        validator: EvaluationValidator | None = None,
        definitions: tuple[PolicyDefinition, ...] | None = None,
    ) -> None:
        self._validator = validator or EvaluationValidator()
        self._definitions: dict[str, PolicyDefinition] = {}
        for definition in definitions or ():
            self.register(definition)

    @property
    def registry_id(self) -> str:
        return self.REGISTRY_ID

    @property
    def registry_version(self) -> str:
        return self.REGISTRY_VERSION

    @property
    def validator(self) -> EvaluationValidator:
        return self._validator

    def register(
        self,
        definition: PolicyDefinition,
        *,
        replace: bool = False,
    ) -> PolicyDefinition:
        """Validate and register a definition. Raises on duplicate unless replace."""
        validated = self._validator.validate_definition(definition)
        policy_id = validated.policy_id
        if policy_id in self._definitions and not replace:
            raise EvaluationValidationError(
                f"policy already registered: {policy_id}"
            )
        self._definitions[policy_id] = validated
        return validated

    def get(self, policy_id: str) -> PolicyDefinition | None:
        """Return registered definition or None."""
        key = (policy_id or "").strip()
        if not key:
            return None
        return self._definitions.get(key)

    def require(self, policy_id: str) -> PolicyDefinition:
        """Return registered definition or raise."""
        definition = self.get(policy_id)
        if definition is None:
            raise EvaluationValidationError(
                f"policy not registered: {(policy_id or '').strip()}"
            )
        return definition

    def contains(self, policy_id: str) -> bool:
        """True when policy_id is registered."""
        return self.get(policy_id) is not None

    def list_ids(self) -> tuple[str, ...]:
        """Deterministic sorted policy ids."""
        return tuple(sorted(self._definitions.keys()))

    def list_definitions(self) -> tuple[PolicyDefinition, ...]:
        """Deterministic sorted definitions by policy_id."""
        return tuple(
            self._definitions[key] for key in sorted(self._definitions.keys())
        )

    def unregister(self, policy_id: str) -> bool:
        """Remove a definition if present. Returns True when removed."""
        key = (policy_id or "").strip()
        if key in self._definitions:
            del self._definitions[key]
            return True
        return False

    def clear(self) -> None:
        """Remove all registered definitions."""
        self._definitions.clear()

    def __len__(self) -> int:
        return len(self._definitions)

    def __contains__(self, policy_id: object) -> bool:
        if not isinstance(policy_id, str):
            return False
        return self.contains(policy_id)


def build_policy_definition_registry(
    *,
    enabled: bool,
    validator: EvaluationValidator | None = None,
    definitions: tuple[PolicyDefinition, ...] | None = None,
) -> PolicyDefinitionRegistry | None:
    """DI helper — construct registry only when the feature flag is on."""
    if not enabled:
        return None
    return PolicyDefinitionRegistry(
        validator=validator,
        definitions=definitions,
    )
