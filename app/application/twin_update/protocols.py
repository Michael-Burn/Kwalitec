"""Twin Update Coordinator dependency Protocols (Capability 4.9.7).

Closed Application Layer invocation boundaries for Strategy, Composer, and
Repository. Implementations are injected — the Coordinator never embeds
educational interpretation, composition math, or persistence technology.
"""

from __future__ import annotations

from typing import Any, Protocol

from app.application.twin_repository.types import (
    PersistAcknowledgement,
    TwinPersistenceFailure,
    TwinScope,
)
from app.application.twin_update.evidence import EducationalEvidencePackage
from app.application.twin_update.outputs import DomainStrategyOutput
from app.application.twin_update.result import TwinUpdateResult
from app.domain.twin.digital_twin import DigitalTwin


class TwinUpdateStrategyProtocol(Protocol):
    """Twin Update Strategy — interpret Current Twin + Evidence for one domain."""

    @property
    def strategy_identity(self) -> str:
        """Named Strategy identity for operational tracing."""

    def interpret(
        self,
        current_twin: DigitalTwin,
        evidence: EducationalEvidencePackage,
    ) -> DomainStrategyOutput:
        """Author a Domain Strategy Output without mutating inputs."""


class TwinComposerProtocol(Protocol):
    """Twin Composer — assemble Current Twin + Domain Strategy Outputs."""

    def compose(
        self,
        current_twin: DigitalTwin,
        outputs: tuple[DomainStrategyOutput, ...],
    ) -> DigitalTwin:
        """Author one immutable Successor Twin. Assembles only — never interprets."""


class TwinSuccessorRepositoryProtocol(Protocol):
    """Twin Repository successor persist surface used by the Coordinator."""

    def persist_successor_twin(
        self,
        twin: DigitalTwin,
        *,
        scope: TwinScope | None = None,
        snapshot_id: str | None = None,
        expected_current_snapshot_id: str | None = None,
        provenance: dict[str, Any] | None = None,
    ) -> PersistAcknowledgement | TwinPersistenceFailure:
        """Persist a complete Successor Twin. Never orchestrates Strategies."""


class TwinUpdateCoordinatorProtocol(Protocol):
    """Coordinator interface — Application Layer write-path orchestration."""

    def update(
        self,
        current_twin: DigitalTwin | None,
        evidence: EducationalEvidencePackage | None,
        *,
        scope: TwinScope | None = None,
    ) -> TwinUpdateResult:
        """Orchestrate Strategy → Composer → Repository for Twin succession."""
