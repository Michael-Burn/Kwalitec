"""Certified snapshot loader for Curriculum Studio workspaces (EI-002A)."""

from __future__ import annotations

from app.application.curriculum_intelligence.founder_preview import (
    CertifiedSnapshotLoader,
)
from app.application.curriculum_intelligence.ports.generation_store_port import (
    GenerationStorePort,
)
from app.domain.curriculum_intelligence.certification import (
    CertificationReport,
    CertifiedCurriculumSnapshot,
    DecisionQualityScores,
)
from app.domain.curriculum_intelligence.generation import (
    CertificationOutcome,
    GenerationIndex,
    QualitySnapshot,
)


class StoreCertifiedSnapshotLoader(CertifiedSnapshotLoader):
    """Load CertifiedCurriculumSnapshot from GenerationStorePort by workspace."""

    def __init__(self, store: GenerationStorePort) -> None:
        self._store = store

    def load_for_workspace(
        self, workspace_id: str
    ) -> CertifiedCurriculumSnapshot | None:
        chain_id = self._store.get_chain_id_for_workspace(workspace_id)
        if not chain_id:
            return None
        active = self._store.get_active_snapshot(chain_id)
        if active is None:
            return None
        # Prefer Gen 7 certified head; fall back to active if it is Gen 7.
        certified_snap = active
        if active.generation_index != int(GenerationIndex.CERTIFICATION):
            snaps = [
                s
                for s in self._store.list_snapshots(chain_id)
                if s.generation_index == int(GenerationIndex.CERTIFICATION)
            ]
            if not snaps:
                return None
            certified_snap = snaps[-1]
        decision = self._store.get_certification(certified_snap.snapshot_id)
        if decision is None:
            return None
        if decision.outcome is CertificationOutcome.NOT_CERTIFIED:
            # Loader still returns the artefact; PreviewService filters eligibility.
            pass
        ledger = tuple(self._store.list_decisions(chain_id))
        report = CertificationReport(
            decision=decision,
            decision_quality=DecisionQualityScores(
                merge_quality=0.0,
                split_quality=0.0,
                objective_quality=0.0,
                coverage_quality=decision.coverage,
                hierarchy_quality=decision.hierarchy_score,
                policy_consistency=0.0,
                evidence_quality=decision.evidence_quality,
                aggregate=decision.decision_quality,
            ),
            quality_vector=certified_snap.metrics
            if hasattr(certified_snap.metrics, "as_vector")
            else QualitySnapshot(
                coverage=decision.coverage,
                hierarchy=decision.hierarchy_score,
                duplicates=0.0,
                noise=0.0,
                granularity=decision.granularity_score,
                confidence=decision.confidence,
                evidence_quality=decision.evidence_quality,
            ),
            hard_gate_failures=decision.hard_gate_failures,
            warnings=decision.warnings,
            reasons=decision.failure_reasons,
            ledger_entry_ids=tuple(e.decision_id for e in ledger),
        )
        return CertifiedCurriculumSnapshot(
            snapshot=certified_snap,
            certification=decision,
            report=report,
            decision_ledger=ledger,
        )
