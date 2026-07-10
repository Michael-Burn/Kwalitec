"""Individual validation finding for an Evidence Candidate.

Messages are immutable diagnostic records. They never mutate the candidate
and never encode scores or Twin-update instructions.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.domain.evidence.validation_severity import ValidationSeverity


@dataclass(frozen=True)
class ValidationMessage:
    """One structural validation finding.

    Attributes:
        code: Stable machine-readable identifier (e.g. ``missing_identifier``).
        message: Human-readable explanation of the finding.
        severity: Whether the finding rejects, warns, or informs.
        field: Optional candidate attribute the finding relates to.
    """

    code: str
    message: str
    severity: ValidationSeverity
    field: str | None = None
