"""WorkflowExecutionPayload — cargo returned by AutomationTask.execute."""

from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any

from app.automation.models.result import AutomationStatus


@dataclass(frozen=True)
class WorkflowExecutionPayload:
    """Structured outcome produced by a workflow implementation.

    The executor measures timing and wraps this into AutomationResult.
    Optional ``status`` lets a workflow declare PARTIAL_SUCCESS explicitly;
    otherwise the executor derives status from errors / outputs.
    """

    outputs: MappingProxyType[str, Any] = field(
        default_factory=lambda: MappingProxyType({})
    )
    warnings: tuple[str, ...] = ()
    errors: tuple[str, ...] = ()
    status: AutomationStatus | None = None

    @classmethod
    def from_mapping(
        cls,
        outputs: dict[str, Any] | None = None,
        *,
        warnings: tuple[str, ...] = (),
        errors: tuple[str, ...] = (),
        status: AutomationStatus | None = None,
    ) -> WorkflowExecutionPayload:
        """Build a payload from a mutable outputs mapping."""

        return cls(
            outputs=MappingProxyType(dict(outputs or {})),
            warnings=warnings,
            errors=errors,
            status=status,
        )
