"""Immutable AdapterRequest — input to every Mission Adapter operation."""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType


@dataclass(frozen=True)
class AdapterRequest:
    """Caller context for a mission adapter invocation.

    Contains stable internal identifiers only — no PII beyond ids the
    product already treats as internal keys. Educational reasoning is
    never performed from these fields by the adapter itself.
    """

    operation: str
    learner_id: str
    mission_id: str | None = None
    journey_id: str | None = None
    topic_id: str | None = None
    session_id: str | None = None
    organisation_id: str | None = None
    cohort_id: str | None = None
    environment: str = "production"
    correlation_id: str | None = None
    context: MappingProxyType | None = None

    def __post_init__(self) -> None:
        if self.context is None:
            object.__setattr__(self, "context", MappingProxyType({}))
        elif not isinstance(self.context, MappingProxyType):
            object.__setattr__(
                self,
                "context",
                MappingProxyType(dict(self.context)),
            )
