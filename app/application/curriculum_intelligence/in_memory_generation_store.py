"""In-memory Generation Store — append-only Curriculum Memory for tests / Phase A."""

from __future__ import annotations

from copy import deepcopy

from app.application.curriculum_intelligence.exceptions import (
    LineageAppendError,
    SnapshotImmutableError,
    SnapshotNotFoundError,
)
from app.application.curriculum_intelligence.ports.generation_store_port import (
    GenerationStorePort,
)
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


class InMemoryGenerationStore(GenerationStorePort):
    """Process-local append-only store. Snapshots cannot be rewritten."""

    def __init__(self) -> None:
        self._snapshots: dict[str, CurriculumGenerationSnapshot] = {}
        self._active: dict[str, str] = {}
        self._lineage_ops: dict[tuple[str, str], list[LineageOperation]] = {}
        self._lineage_seed: dict[tuple[str, str], LineageRecord] = {}
        self._regression: dict[str, list[RegressionReport]] = {}
        self._certifications: dict[str, CertificationDecision] = {}
        self._calibration: dict[str, CalibrationProfile] = {}
        self._decisions: dict[str, list[DecisionLedgerEntry]] = {}
        self._decision_ids: set[str] = set()
        self._workspace_chains: dict[str, str] = {}
        self._chain_workspaces: dict[str, str] = {}

    def append_snapshot(self, snapshot: CurriculumGenerationSnapshot) -> None:
        if snapshot.snapshot_id in self._snapshots:
            raise SnapshotImmutableError(
                f"Snapshot {snapshot.snapshot_id!r} already exists "
                "and cannot be rewritten."
            )
        frozen = deepcopy(snapshot)
        self._snapshots[frozen.snapshot_id] = frozen
        if frozen.generation.workspace_id:
            self._workspace_chains[frozen.generation.workspace_id] = frozen.chain_id
            self._chain_workspaces[frozen.chain_id] = frozen.generation.workspace_id
        for node in frozen.nodes:
            key = (frozen.chain_id, node.node_id)
            if key not in self._lineage_seed:
                self._lineage_seed[key] = node.lineage
                self._lineage_ops[key] = list(node.lineage.operations)
            else:
                known_ids = {op.operation_id for op in self._lineage_ops[key]}
                for op in node.lineage.operations:
                    if op.operation_id not in known_ids:
                        self._lineage_ops[key].append(op)
                        known_ids.add(op.operation_id)

    def get_snapshot(self, snapshot_id: str) -> CurriculumGenerationSnapshot | None:
        snap = self._snapshots.get(snapshot_id)
        return deepcopy(snap) if snap is not None else None

    def get_generation(self, generation_id: str) -> Generation | None:
        for snap in self._snapshots.values():
            if snap.generation_id == generation_id:
                return deepcopy(snap.generation)
        return None

    def list_snapshots(self, chain_id: str) -> list[CurriculumGenerationSnapshot]:
        items = [s for s in self._snapshots.values() if s.chain_id == chain_id]
        items.sort(key=lambda s: (s.generation_index, s.created_at_iso, s.snapshot_id))
        return [deepcopy(s) for s in items]

    def get_active_snapshot(self, chain_id: str) -> CurriculumGenerationSnapshot | None:
        snapshot_id = self._active.get(chain_id)
        if snapshot_id is None:
            return None
        return self.get_snapshot(snapshot_id)

    def set_active_snapshot(self, chain_id: str, snapshot_id: str) -> None:
        snap = self._snapshots.get(snapshot_id)
        if snap is None:
            raise SnapshotNotFoundError(f"Snapshot {snapshot_id!r} not found.")
        if snap.chain_id != chain_id:
            raise SnapshotNotFoundError(
                f"Snapshot {snapshot_id!r} does not belong to chain {chain_id!r}."
            )
        if snap.status is not SnapshotStatus.ACCEPTED:
            raise SnapshotImmutableError(
                "Only accepted snapshots may become the active head."
            )
        self._active[chain_id] = snapshot_id

    def update_snapshot_status(
        self, snapshot_id: str, status: SnapshotStatus
    ) -> CurriculumGenerationSnapshot:
        snap = self._snapshots.get(snapshot_id)
        if snap is None:
            raise SnapshotNotFoundError(f"Snapshot {snapshot_id!r} not found.")
        updated = snap.with_status(status)
        self._snapshots[snapshot_id] = updated
        return deepcopy(updated)

    def append_lineage_operation(
        self,
        *,
        chain_id: str,
        node_id: str,
        operation: LineageOperation,
    ) -> None:
        key = (chain_id, node_id)
        ops = self._lineage_ops.setdefault(key, [])
        if any(existing.operation_id == operation.operation_id for existing in ops):
            raise LineageAppendError(
                f"Lineage operation {operation.operation_id!r} already recorded."
            )
        ops.append(operation)
        seed = self._lineage_seed.get(key)
        if seed is None:
            self._lineage_seed[key] = LineageRecord(
                created_generation=operation.generation_id,
                created_generation_index=operation.generation_index,
                last_modified_generation=operation.generation_id,
                last_modified_generation_index=operation.generation_index,
                operations=(operation,),
            )
        else:
            self._lineage_seed[key] = seed.with_appended(operation)

    def get_lineage_for_node(
        self, *, chain_id: str, node_id: str
    ) -> LineageRecord | None:
        key = (chain_id, node_id)
        seed = self._lineage_seed.get(key)
        if seed is None:
            return None
        ops = tuple(self._lineage_ops.get(key, []))
        return LineageRecord(
            created_generation=seed.created_generation,
            created_generation_index=seed.created_generation_index,
            last_modified_generation=(
                ops[-1].generation_id if ops else seed.last_modified_generation
            ),
            last_modified_generation_index=(
                ops[-1].generation_index
                if ops
                else seed.last_modified_generation_index
            ),
            operations=ops,
            related_node_ids=seed.related_node_ids,
            syllabus_refs=seed.syllabus_refs,
            cmp_evidence=seed.cmp_evidence,
            parent_history=seed.parent_history,
            merged_from=seed.merged_from,
            split_into=seed.split_into,
            rejection_reason_code=seed.rejection_reason_code,
            rejection_reason_label=seed.rejection_reason_label,
        )

    def append_regression_report(self, report: RegressionReport) -> None:
        self._regression.setdefault(report.chain_id, []).append(deepcopy(report))

    def list_regression_reports(self, chain_id: str) -> list[RegressionReport]:
        return [deepcopy(r) for r in self._regression.get(chain_id, [])]

    def append_certification(self, decision: CertificationDecision) -> None:
        self._certifications[decision.snapshot_id] = deepcopy(decision)

    def get_certification(self, snapshot_id: str) -> CertificationDecision | None:
        decision = self._certifications.get(snapshot_id)
        return deepcopy(decision) if decision is not None else None

    def append_decision(self, entry: DecisionLedgerEntry) -> None:
        if entry.decision_id in self._decision_ids:
            raise LineageAppendError(
                f"Decision {entry.decision_id!r} already recorded on the ledger."
            )
        self._decision_ids.add(entry.decision_id)
        self._decisions.setdefault(entry.chain_id, []).append(deepcopy(entry))

    def list_decisions(self, chain_id: str) -> list[DecisionLedgerEntry]:
        return [deepcopy(e) for e in self._decisions.get(chain_id, [])]

    def save_calibration_profile(self, profile: CalibrationProfile) -> None:
        self._calibration[profile.profile_id] = deepcopy(profile)

    def get_calibration_profile(self, profile_id: str) -> CalibrationProfile | None:
        profile = self._calibration.get(profile_id)
        return deepcopy(profile) if profile is not None else None

    def list_calibration_profiles_for_workspace(
        self, workspace_id: str
    ) -> list[CalibrationProfile]:
        wid = (workspace_id or "").strip()
        return [
            deepcopy(p)
            for p in self._calibration.values()
            if p.workspace_id == wid
        ]

    def get_workspace_id_for_chain(self, chain_id: str) -> str | None:
        return self._chain_workspaces.get(chain_id)

    def ensure_chain(self, chain_id: str, workspace_id: str) -> str:
        self._workspace_chains[workspace_id] = chain_id
        self._chain_workspaces[chain_id] = workspace_id
        return chain_id

    def get_chain_id_for_workspace(self, workspace_id: str) -> str | None:
        return self._workspace_chains.get(workspace_id)

    def bind_workspace_chain(self, workspace_id: str, chain_id: str) -> None:
        self.ensure_chain(chain_id, workspace_id)
