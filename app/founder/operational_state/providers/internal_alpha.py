"""Internal Alpha Provider — wraps FOS-003 processed outputs (FOS-005).

Read-only. Does not run the pipeline or read filesystem week folders.
"""

from __future__ import annotations

from types import MappingProxyType

from app.founder.operational_state.dto.internal_alpha import (
    InternalAlphaSubsystemDTO,
)

DEFAULT_INTERNAL_ALPHA_SOURCE_VERSION = "unwired"


class StaticInternalAlphaSource:
    """Injectable Internal Alpha source for tests and defaults."""

    def __init__(self, dto: InternalAlphaSubsystemDTO | None = None) -> None:
        self._dto = dto or InternalAlphaSubsystemDTO(
            source_version=DEFAULT_INTERNAL_ALPHA_SOURCE_VERSION,
            current_week="",
            feedback_count=0,
            duplicate_count=0,
            category_counts=MappingProxyType({}),
            recent_week_labels=(),
        )

    def load(self) -> InternalAlphaSubsystemDTO:
        return self._dto


class InternalAlphaProvider:
    """Retrieve Internal Alpha summary for operational-state aggregation.

    Aggregation input only. Pipeline ownership remains with FOS-003.
    """

    def __init__(self, source: StaticInternalAlphaSource | None = None) -> None:
        self._source = source or StaticInternalAlphaSource()

    def get(self) -> InternalAlphaSubsystemDTO:
        """Return the Internal Alpha DTO from the wrapped source."""
        return self._source.load()
