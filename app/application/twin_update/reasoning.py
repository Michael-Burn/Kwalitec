"""ReasoningTrace — Strategy explainability cargo (Capability 4.9.9).

Audit-facing educational statement for how a Domain Strategy Output was
attributed. Not student UX. No confidence scores, probabilities, readiness,
or predictions.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ReasoningTrace:
    """Immutable explainability statement for one Strategy interpretation.

    Attributes:
        statement: Human-readable attribution of preservation or update —
            observational warrant only; never a readiness or forecast claim.
    """

    statement: str

    @classmethod
    def create(cls, statement: str) -> ReasoningTrace:
        """Construct a ReasoningTrace.

        Raises:
            ValueError: If ``statement`` is blank or not a string.
        """
        text = statement.strip() if isinstance(statement, str) else ""
        if not text:
            raise ValueError("reasoning statement must be a non-empty string")
        return cls(statement=text)

    def __str__(self) -> str:
        return self.statement
