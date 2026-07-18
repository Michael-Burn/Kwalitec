"""Validation summary — Founder-facing validation posture for Studio.

Represents detected structure, warnings, errors, and readiness.
Does not perform ingestion or mutate Curriculum Management.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum


class ValidationReadiness(StrEnum):
    """Overall validation readiness for publication gating."""

    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    PASSED = "passed"
    FAILED = "failed"
    BLOCKED = "blocked"


class ValidationFindingSeverity(StrEnum):
    """Severity of a Studio validation finding."""

    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    BLOCKING = "blocking"


@dataclass(frozen=True)
class ValidationFinding:
    """Single immutable validation finding for Studio review."""

    code: str
    message: str
    severity: ValidationFindingSeverity = ValidationFindingSeverity.WARNING
    section_id: str | None = None
    topic_id: str | None = None

    @classmethod
    def create(
        cls,
        code: str,
        message: str,
        *,
        severity: ValidationFindingSeverity | str = ValidationFindingSeverity.WARNING,
        section_id: str | None = None,
        topic_id: str | None = None,
    ) -> ValidationFinding:
        """Construct a finding after validating invariants."""
        resolved = (
            severity
            if isinstance(severity, ValidationFindingSeverity)
            else ValidationFindingSeverity(str(severity).strip().lower())
        )
        return cls(
            code=_require_non_empty(code, "code"),
            message=_require_non_empty(message, "message"),
            severity=resolved,
            section_id=(
                None
                if section_id is None
                else _require_non_empty(section_id, "section_id")
            ),
            topic_id=(
                None if topic_id is None else _require_non_empty(topic_id, "topic_id")
            ),
        )

    @property
    def is_blocking(self) -> bool:
        """True when this finding blocks readiness."""
        return self.severity in {
            ValidationFindingSeverity.ERROR,
            ValidationFindingSeverity.BLOCKING,
        }


@dataclass(frozen=True)
class ValidationSummary:
    """Immutable Founder-facing validation summary.

    Captures detected sections / objectives / prerequisites plus findings.
    """

    summary_id: str
    workspace_id: str
    detected_sections: tuple[str, ...] = field(default_factory=tuple)
    detected_objectives: tuple[str, ...] = field(default_factory=tuple)
    detected_prerequisites: tuple[tuple[str, str], ...] = field(default_factory=tuple)
    warnings: tuple[ValidationFinding, ...] = field(default_factory=tuple)
    errors: tuple[ValidationFinding, ...] = field(default_factory=tuple)
    readiness: ValidationReadiness = ValidationReadiness.NOT_STARTED
    passed: bool = False

    @classmethod
    def create(
        cls,
        summary_id: str,
        workspace_id: str,
        *,
        detected_sections: list[str] | tuple[str, ...] | None = None,
        detected_objectives: list[str] | tuple[str, ...] | None = None,
        detected_prerequisites: (
            list[tuple[str, str]] | tuple[tuple[str, str], ...] | None
        ) = None,
        warnings: list[ValidationFinding] | tuple[ValidationFinding, ...] | None = None,
        errors: list[ValidationFinding] | tuple[ValidationFinding, ...] | None = None,
        readiness: ValidationReadiness | str | None = None,
    ) -> ValidationSummary:
        """Construct a ValidationSummary; readiness/passed derived when omitted."""
        sid = _require_non_empty(summary_id, "summary_id")
        wid = _require_non_empty(workspace_id, "workspace_id")
        sections = tuple(detected_sections or ())
        objectives = tuple(detected_objectives or ())
        prereqs = tuple(detected_prerequisites or ())
        warn_t = tuple(warnings or ())
        err_t = tuple(errors or ())
        blocking = any(e.is_blocking for e in err_t) or any(
            w.severity is ValidationFindingSeverity.BLOCKING for w in warn_t
        )
        if readiness is None:
            if err_t or blocking:
                resolved_readiness = ValidationReadiness.FAILED
            elif sections or objectives:
                resolved_readiness = ValidationReadiness.PASSED
            else:
                resolved_readiness = ValidationReadiness.NOT_STARTED
        else:
            resolved_readiness = (
                readiness
                if isinstance(readiness, ValidationReadiness)
                else ValidationReadiness(str(readiness).strip().lower())
            )
        passed = (
            resolved_readiness is ValidationReadiness.PASSED and not blocking
        )
        return cls(
            summary_id=sid,
            workspace_id=wid,
            detected_sections=sections,
            detected_objectives=objectives,
            detected_prerequisites=prereqs,
            warnings=warn_t,
            errors=err_t,
            readiness=resolved_readiness,
            passed=passed,
        )

    @property
    def section_count(self) -> int:
        """Number of detected sections."""
        return len(self.detected_sections)

    @property
    def objective_count(self) -> int:
        """Number of detected objectives."""
        return len(self.detected_objectives)

    @property
    def prerequisite_count(self) -> int:
        """Number of detected prerequisite edges."""
        return len(self.detected_prerequisites)

    @property
    def warning_count(self) -> int:
        """Number of warning findings."""
        return len(self.warnings)

    @property
    def error_count(self) -> int:
        """Number of error findings."""
        return len(self.errors)

    @property
    def blocks_publication(self) -> bool:
        """True when validation must block publication."""
        return not self.passed


def _require_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a non-empty string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized
