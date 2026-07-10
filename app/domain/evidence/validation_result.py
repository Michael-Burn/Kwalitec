"""Aggregate outcome of Evidence Candidate validation.

A ValidationResult is the sole output of the Evidence Validation Stage. It
does not transform, score, persist, or update Twin state.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, field

from app.domain.evidence.validation_message import ValidationMessage
from app.domain.evidence.validation_severity import ValidationSeverity


@dataclass(frozen=True)
class ValidationResult:
    """Outcome of validating one Evidence Candidate.

    Attributes:
        accepted: True when no ``ERROR`` messages were produced.
        messages: All findings in validator registration order.
    """

    accepted: bool
    messages: tuple[ValidationMessage, ...] = field(default_factory=tuple)

    @classmethod
    def from_messages(
        cls,
        messages: Sequence[ValidationMessage] | Iterable[ValidationMessage],
    ) -> ValidationResult:
        """Build a result from collected messages.

        Args:
            messages: Findings from one or more validators.

        Returns:
            Result with ``accepted`` False if any message is an ERROR.
        """
        collected = tuple(messages)
        accepted = not any(
            message.severity is ValidationSeverity.ERROR for message in collected
        )
        return cls(accepted=accepted, messages=collected)

    @property
    def errors(self) -> tuple[ValidationMessage, ...]:
        """Messages with ERROR severity."""
        return tuple(
            message
            for message in self.messages
            if message.severity is ValidationSeverity.ERROR
        )

    @property
    def warnings(self) -> tuple[ValidationMessage, ...]:
        """Messages with WARNING severity."""
        return tuple(
            message
            for message in self.messages
            if message.severity is ValidationSeverity.WARNING
        )

    @property
    def infos(self) -> tuple[ValidationMessage, ...]:
        """Messages with INFO severity."""
        return tuple(
            message
            for message in self.messages
            if message.severity is ValidationSeverity.INFO
        )

    @property
    def severity_summary(self) -> Mapping[ValidationSeverity, int]:
        """Count of messages per severity level (all severities present)."""
        counts = {severity: 0 for severity in ValidationSeverity}
        for message in self.messages:
            counts[message.severity] += 1
        return counts
