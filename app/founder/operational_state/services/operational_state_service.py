"""FounderOperationalStateService — aggregation coordinator (FOS-005).

Responsibilities:
1. Query providers
2. Build state
3. Validate state
4. Return immutable snapshot

No AI, recommendations, scoring, or release decisions.
"""

from __future__ import annotations

from collections.abc import Callable
from datetime import datetime
from typing import Protocol

from app.founder.operational_state.builders import OperationalStateBuilder
from app.founder.operational_state.dto.capability import CapabilitySubsystemDTO
from app.founder.operational_state.dto.internal_alpha import (
    InternalAlphaSubsystemDTO,
)
from app.founder.operational_state.dto.knowledge import KnowledgeSubsystemDTO
from app.founder.operational_state.models import FounderOperationalState
from app.founder.operational_state.providers import (
    CapabilityArchiveProvider,
    InternalAlphaProvider,
    KnowledgeQueryProvider,
)
from app.founder.operational_state.validators import OperationalStateValidator


class KnowledgeGate(Protocol):
    """Anything that can supply a KnowledgeSubsystemDTO."""

    def get(self) -> KnowledgeSubsystemDTO:
        """Return a Knowledge Engine summary."""


class CapabilityGate(Protocol):
    """Anything that can supply a CapabilitySubsystemDTO."""

    def get(self) -> CapabilitySubsystemDTO:
        """Return a Capability Archive summary."""


class InternalAlphaGate(Protocol):
    """Anything that can supply an InternalAlphaSubsystemDTO."""

    def get(self) -> InternalAlphaSubsystemDTO:
        """Return an Internal Alpha summary."""


class FounderOperationalStateService:
    """Query subsystem providers and return an immutable operational snapshot."""

    def __init__(
        self,
        *,
        knowledge: KnowledgeGate | None = None,
        capability: CapabilityGate | None = None,
        internal_alpha: InternalAlphaGate | None = None,
        builder: OperationalStateBuilder | None = None,
        validator: OperationalStateValidator | None = None,
        clock: Callable[[], datetime] | None = None,
    ) -> None:
        # FSI-001: defaults are live repository-backed providers.
        # Tests inject Static* sources via KnowledgeProvider / CapabilityProvider.
        self._knowledge: KnowledgeGate = knowledge or KnowledgeQueryProvider()
        self._capability: CapabilityGate = capability or CapabilityArchiveProvider()
        self._internal_alpha: InternalAlphaGate = (
            internal_alpha or InternalAlphaProvider()
        )
        resolved_validator = validator or OperationalStateValidator()
        self._builder = builder or OperationalStateBuilder(
            validator=resolved_validator,
            clock=clock,
        )

    def get_state(
        self, *, generated_at: datetime | None = None
    ) -> FounderOperationalState:
        """Build and validate the current Founder Operational State.

        Args:
            generated_at: Optional fixed timestamp for deterministic tests.

        Returns:
            Immutable FounderOperationalState.

        Raises:
            OperationalStateValidationError: When the assembled snapshot
                fails completeness validation.
        """
        knowledge = self._knowledge.get()
        capability = self._capability.get()
        internal_alpha = self._internal_alpha.get()
        return self._builder.build(
            knowledge,
            capability,
            internal_alpha,
            generated_at=generated_at,
            validate=True,
        )
