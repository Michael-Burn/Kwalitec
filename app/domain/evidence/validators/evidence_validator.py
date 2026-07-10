"""Evidence Validation Stage coordinator.

Receives one Evidence Candidate and returns one ValidationResult by
delegating to registered validators. Does not transform, score, persist, or
update the Student Digital Twin. Never mutates the candidate.
"""

from __future__ import annotations

from app.domain.evidence.evidence_candidate import EvidenceCandidate
from app.domain.evidence.validation_message import ValidationMessage
from app.domain.evidence.validation_result import ValidationResult
from app.domain.evidence.validators.base_validator import BaseValidator
from app.domain.evidence.validators.structural import default_structural_validators


class EvidenceValidator:
    """Registry-backed coordinator that invokes registered validators.

    Additional validators are registered without modifying this class
    (open for extension). Invocation order follows registration order.
    All registered validators run for every candidate; findings are merged.
    """

    def __init__(self, validators: list[BaseValidator] | None = None) -> None:
        """Initialise with an optional initial validator list.

        Args:
            validators: Validators to register at construction time.
        """
        self._validators: list[BaseValidator] = list(validators or [])

    @classmethod
    def with_structural_rules(cls) -> EvidenceValidator:
        """Build a validator pre-loaded with structural presence checks.

        Returns:
            EvidenceValidator configured with the default structural set.
        """
        return cls(default_structural_validators())

    def register(self, validator: BaseValidator) -> None:
        """Register a validator for future invocations.

        Args:
            validator: Strategy implementation to add to the registry.
        """
        self._validators.append(validator)

    @property
    def validators(self) -> tuple[BaseValidator, ...]:
        """Return a snapshot of registered validators (registration order)."""
        return tuple(self._validators)

    def validate(self, candidate: EvidenceCandidate) -> ValidationResult:
        """Run all registered validators against ``candidate``.

        Args:
            candidate: Immutable Evidence Candidate to inspect. Not mutated.

        Returns:
            Aggregated ValidationResult. ``accepted`` is False when any
            validator emits an ERROR. Does not transform, score, persist, or
            mutate Twin state.
        """
        messages: list[ValidationMessage] = []
        for validator in self._validators:
            messages.extend(validator.validate(candidate))
        return ValidationResult.from_messages(messages)
