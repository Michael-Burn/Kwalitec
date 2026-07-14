"""AutomationContext — execution inputs for one workflow run."""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Any


@dataclass(frozen=True)
class AutomationContext:
    """Immutable inputs supplied to an automation workflow.

    Version 1 carries an opaque parameter map. Workflows interpret keys they
    understand; the framework does not impose domain-specific shapes.
    """

    parameters: MappingProxyType[str, Any]

    @classmethod
    def empty(cls) -> AutomationContext:
        """Return a context with no parameters."""

        return cls(parameters=MappingProxyType({}))

    @classmethod
    def from_mapping(
        cls, parameters: dict[str, Any] | None = None
    ) -> AutomationContext:
        """Build a context from a mutable mapping (copied into MappingProxyType)."""

        return cls(parameters=MappingProxyType(dict(parameters or {})))
