"""Framework-level AutomationContext structural checks."""

from __future__ import annotations

from types import MappingProxyType

from app.automation.dto.validation import ValidationIssue, ValidationReport
from app.automation.models.context import AutomationContext


class AutomationContextValidator:
    """Validate that a context is structurally usable by the framework."""

    def validate(self, context: AutomationContext | None) -> ValidationReport:
        """Return ok=False when ``context`` is missing or malformed."""

        issues: list[ValidationIssue] = []
        if context is None:
            issues.append(
                ValidationIssue(
                    code="missing_context",
                    message="AutomationContext is required",
                    field="context",
                )
            )
            return ValidationReport(ok=False, issues=tuple(issues))

        if not isinstance(context, AutomationContext):
            issues.append(
                ValidationIssue(
                    code="invalid_context_type",
                    message="context must be an AutomationContext instance",
                    field="context",
                )
            )
            return ValidationReport(ok=False, issues=tuple(issues))

        parameters = context.parameters
        if not isinstance(parameters, MappingProxyType):
            issues.append(
                ValidationIssue(
                    code="invalid_parameters_type",
                    message="context.parameters must be a MappingProxyType",
                    field="context.parameters",
                )
            )
        else:
            for key in parameters:
                if not isinstance(key, str) or not key.strip():
                    issues.append(
                        ValidationIssue(
                            code="invalid_parameter_key",
                            message="parameter keys must be non-empty strings",
                            field="context.parameters",
                        )
                    )
                    break

        return ValidationReport(ok=len(issues) == 0, issues=tuple(issues))
