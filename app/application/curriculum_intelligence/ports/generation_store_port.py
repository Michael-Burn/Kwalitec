"""GenerationStorePort — durable append-only Curriculum Memory.

Snapshots are immutable after append. Only status transitions and
append-only lineage / regression / certification records may be written.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.domain.curriculum_intelligence.decision_ledger import DecisionLedgerEntry
from app.domain.curriculum_intelligence.generation import (
    CalibrationProfile,
    CertificationDecision,
    CurriculumGenerationSnapshot,
    Generation,
    LineageOperation,
    LineageRecord,
    RegressionReport,
    SnapshotStatus,
)


class GenerationStorePort(ABC):
    """Append-only store for EI-001 generation artefacts."""

    @abstractmethod
    def append_snapshot(self, snapshot: CurriculumGenerationSnapshot) -> None:
        """Persist a new immutable snapshot. Raises if snapshot_id exists."""

    @abstractmethod
    def get_snapshot(self, snapshot_id: str) -> CurriculumGenerationSnapshot | None:
        """Load one snapshot by id."""

    @abstractmethod
    def get_generation(self, generation_id: str) -> Generation | None:
        """Load generation metadata by id."""

    @abstractmethod
    def list_snapshots(self, chain_id: str) -> list[CurriculumGenerationSnapshot]:
        """Return snapshots for a chain ordered by generation_index, created_at."""

    @abstractmethod
    def get_active_snapshot(self, chain_id: str) -> CurriculumGenerationSnapshot | None:
        """Return the currently active accepted snapshot for a chain."""

    @abstractmethod
    def set_active_snapshot(self, chain_id: str, snapshot_id: str) -> None:
        """Point the chain active pointer at an accepted snapshot."""

    @abstractmethod
    def update_snapshot_status(
        self, snapshot_id: str, status: SnapshotStatus
    ) -> CurriculumGenerationSnapshot:
        """Lifecycle status transition only — never mutates snapshot content."""

    @abstractmethod
    def append_lineage_operation(
        self,
        *,
        chain_id: str,
        node_id: str,
        operation: LineageOperation,
    ) -> None:
        """Append one lineage operation to Curriculum Memory."""

    @abstractmethod
    def get_lineage_for_node(
        self, *, chain_id: str, node_id: str
    ) -> LineageRecord | None:
        """Return accumulated lineage for a stable node id within a chain."""

    @abstractmethod
    def append_regression_report(self, report: RegressionReport) -> None:
        """Persist a regression accept/reject report."""

    @abstractmethod
    def list_regression_reports(self, chain_id: str) -> list[RegressionReport]:
        """Return regression reports for a chain in append order."""

    @abstractmethod
    def append_certification(self, decision: CertificationDecision) -> None:
        """Persist a certification decision record."""

    @abstractmethod
    def get_certification(self, snapshot_id: str) -> CertificationDecision | None:
        """Load certification for a snapshot, if any."""

    @abstractmethod
    def append_decision(self, entry: DecisionLedgerEntry) -> None:
        """Append one Decision Ledger entry (append-only; duplicate id rejected)."""

    @abstractmethod
    def list_decisions(self, chain_id: str) -> list[DecisionLedgerEntry]:
        """Return Decision Ledger entries for a chain in append order."""

    @abstractmethod
    def save_calibration_profile(self, profile: CalibrationProfile) -> None:
        """Persist a Founder calibration profile (append / replace by id)."""

    @abstractmethod
    def get_calibration_profile(self, profile_id: str) -> CalibrationProfile | None:
        """Load a calibration profile by id."""

    def ensure_chain(self, chain_id: str, workspace_id: str) -> str:
        """Ensure a generation chain exists and is bound to ``workspace_id``.

        Default no-op for stores that track chains only via snapshots.
        Returns the active chain_id.
        """
        _ = workspace_id
        return chain_id

    def get_chain_id_for_workspace(self, workspace_id: str) -> str | None:
        """Return the active chain id bound to a workspace, if any."""
        _ = workspace_id
        return None

    def bind_workspace_chain(self, workspace_id: str, chain_id: str) -> None:
        """Bind ``workspace_id`` to ``chain_id`` as the active chain."""
        self.ensure_chain(chain_id, workspace_id)
