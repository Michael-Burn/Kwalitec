"""GenerationOrchestrator — sequential generations, snapshots, regression, rollback.

Phase B: Agents produce Generations 1–3; RegressionGuard uses real metrics.
Phase C: Agents produce Generations 4–6 (Concept Formation, Objective
Intelligence, Educational Reconciliation) with Educational Policies.
Phase D: Generation 7 Educational Certification + Decision Ledger + Review Pack.
Never skips RegressionGuard for G≥2.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import uuid4

from app.application.curriculum_intelligence.exceptions import GenerationOrderError
from app.application.curriculum_intelligence.mock_generation_runners import (
    GenerationRunContext,
    GenerationRunner,
)
from app.application.curriculum_intelligence.ports.certification_engine_port import (
    CertificationEngine,
)
from app.application.curriculum_intelligence.ports.generation_store_port import (
    GenerationStorePort,
)
from app.application.curriculum_intelligence.regression_guard import RegressionGuard
from app.application.curriculum_intelligence.review_pack_emitter import (
    ReviewPackEmitter,
)
from app.domain.curriculum_intelligence.certification import (
    CertificationReport,
    CertifiedCurriculumSnapshot,
)
from app.domain.curriculum_intelligence.extracted_document import ExtractedDocument
from app.domain.curriculum_intelligence.generation import (
    CalibrationProfile,
    CertificationDecision,
    CurriculumGenerationSnapshot,
    SnapshotStatus,
)
from app.domain.curriculum_intelligence.review_pack import EducationalReviewPack


def _utc_now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


@dataclass(frozen=True)
class OrchestratorResult:
    """Outcome of an orchestrated generation chain (or partial run)."""

    chain_id: str
    accepted_snapshots: tuple[CurriculumGenerationSnapshot, ...]
    rejected_snapshots: tuple[CurriculumGenerationSnapshot, ...]
    active_snapshot_id: str | None
    stopped_at_index: int | None
    rolled_back: bool
    certification: CertificationDecision | None = None
    certification_report: CertificationReport | None = None
    certified_snapshot: CertifiedCurriculumSnapshot | None = None
    review_pack: EducationalReviewPack | None = None


class GenerationOrchestrator:
    """Run Agents / runners in order; checkpoint; gate; activate or rollback."""

    def __init__(
        self,
        store: GenerationStorePort,
        regression_guard: RegressionGuard,
        runners: dict[int, GenerationRunner],
        *,
        certification_engine: CertificationEngine | None = None,
        review_pack_emitter: ReviewPackEmitter | None = None,
    ) -> None:
        self._store = store
        self._guard = regression_guard
        self._runners = runners
        self._certification = certification_engine
        self._review_pack_emitter = review_pack_emitter or ReviewPackEmitter()

    def run_chain(
        self,
        *,
        chain_id: str,
        workspace_id: str,
        source_document_ids: tuple[int, ...],
        start_from: int = 1,
        through: int = 7,
        profile: CalibrationProfile | None = None,
        stop_on_regression: bool = True,
        source_documents: tuple[ExtractedDocument, ...] = (),
        subject_code: str = "CS1",
        version_label: str = "default",
        fixed_created_at_iso: str | None = None,
        emit_review_pack: bool = True,
    ) -> OrchestratorResult:
        """Execute generations ``start_from``..``through`` sequentially.

        Args:
            chain_id: Engine run / Curriculum Memory chain id.
            workspace_id: Studio workspace owning the sources.
            source_document_ids: CIP document ids feeding Gen 1.
            start_from: First generation index (inclusive).
            through: Last generation index (inclusive).
            profile: Optional calibration profile (recorded on generations).
            stop_on_regression: When True, halt after a rejected generation.
            source_documents: Normalised ExtractedDocuments for Agents.
            subject_code: Subject code for hierarchy construction.
            version_label: Version label for hierarchy mapping.
            fixed_created_at_iso: Optional frozen timestamp for reproducibility.
            emit_review_pack: When True and Gen 7 runs, emit Educational Review Pack.
        """
        if start_from < 1 or through > 7 or start_from > through:
            raise GenerationOrderError(
                f"Invalid generation range {start_from}..{through}."
            )

        accepted: list[CurriculumGenerationSnapshot] = []
        rejected: list[CurriculumGenerationSnapshot] = []
        prior = self._seed_prior_for_start(chain_id, start_from)
        if start_from > 1 and prior is None:
            raise GenerationOrderError(
                f"Cannot start from generation {start_from} without an active snapshot."
            )
        if (
            start_from > 1
            and prior is not None
            and prior.generation_index < start_from - 1
        ):
            raise GenerationOrderError(
                "Active snapshot generation "
                f"{prior.generation_index} cannot seed start_from={start_from}."
            )

        rolled_back = False
        stopped_at: int | None = None
        certification: CertificationDecision | None = None
        certification_report: CertificationReport | None = None
        certified_snapshot: CertifiedCurriculumSnapshot | None = None
        review_pack: EducationalReviewPack | None = None

        for index in range(start_from, through + 1):
            runner = self._runners.get(index)
            if runner is None:
                raise GenerationOrderError(
                    f"No runner registered for generation {index}."
                )

            pending_decisions: list = []
            history = [
                s
                for s in self._store.list_snapshots(chain_id)
                if s.status in {SnapshotStatus.ACCEPTED, SnapshotStatus.SUPERSEDED}
            ]
            history.sort(key=lambda s: s.generation_index)
            decision_ledger = tuple(self._store.list_decisions(chain_id))
            regression_history = tuple(self._store.list_regression_reports(chain_id))

            context = GenerationRunContext(
                chain_id=chain_id,
                workspace_id=workspace_id,
                source_document_ids=source_document_ids,
                prior_snapshot=prior,
                calibration_profile=profile,
                source_documents=source_documents,
                subject_code=subject_code,
                version_label=version_label,
                fixed_created_at_iso=fixed_created_at_iso,
                pending_decisions=pending_decisions,
                decision_ledger=decision_ledger,
                quality_history=tuple(history),
                regression_history=regression_history,
            )
            snapshot = runner.run(context)
            if snapshot.generation_index != index:
                raise GenerationOrderError(
                    f"Runner for {index} produced generation_index="
                    f"{snapshot.generation_index}."
                )

            # Partial regen (calibration) may reproduce deterministic snapshot
            # / decision ids from the same parent hash. Snapshots and ledger
            # entries are append-only — mint unique ids when colliding.
            if self._store.get_snapshot(snapshot.snapshot_id) is not None:
                from dataclasses import replace as dc_replace

                new_snap_id = f"snap-{uuid4().hex[:16]}"
                new_gen_id = f"gen-{uuid4().hex[:16]}"
                snapshot = dc_replace(
                    snapshot,
                    snapshot_id=new_snap_id,
                    generation=dc_replace(
                        snapshot.generation, generation_id=new_gen_id
                    ),
                    provenance_bundle_id=f"bundle-{new_snap_id}",
                )
                for i, entry in enumerate(pending_decisions):
                    pending_decisions[i] = dc_replace(
                        entry,
                        decision_id=f"{entry.decision_id}-{uuid4().hex[:6]}",
                        generation_id=new_gen_id,
                        snapshot_id=new_snap_id,
                    )

            # Persist pending acceptance; status stays accepted until guard runs.
            self._store.append_snapshot(snapshot)
            for entry in pending_decisions:
                # Bind snapshot id if agent left it empty.
                if not entry.snapshot_id:
                    from dataclasses import replace as dc_replace

                    entry = dc_replace(entry, snapshot_id=snapshot.snapshot_id)
                self._store.append_decision(entry)

            if index >= 2:
                baselines = self._validation_baselines(chain_id, prior)
                verdict = self._guard.compare(
                    snapshot.metrics,
                    tuple(b.metrics for b in baselines),
                )
                report = self._guard.build_report(
                    report_id=f"reg-{uuid4().hex[:12]}",
                    chain_id=chain_id,
                    candidate_generation_id=snapshot.generation_id,
                    candidate_snapshot_id=snapshot.snapshot_id,
                    baseline_generation_ids=tuple(b.generation_id for b in baselines),
                    verdict=verdict,
                    candidate_metrics=snapshot.metrics,
                    created_at_iso=_utc_now_iso(),
                )
                self._store.append_regression_report(report)

                if not verdict.accepted:
                    rejected_snap = self._store.update_snapshot_status(
                        snapshot.snapshot_id,
                        SnapshotStatus.REJECTED_BY_REGRESSION,
                    )
                    rejected.append(rejected_snap)
                    rolled_back = True
                    stopped_at = index
                    # Active pointer unchanged — rollback semantics.
                    if stop_on_regression:
                        break
                    continue

            # Accept: supersede previous active, activate new.
            previous_active = self._store.get_active_snapshot(chain_id)
            if (
                previous_active is not None
                and previous_active.snapshot_id != snapshot.snapshot_id
                and previous_active.status is SnapshotStatus.ACCEPTED
            ):
                self._store.update_snapshot_status(
                    previous_active.snapshot_id, SnapshotStatus.SUPERSEDED
                )
            if snapshot.status is not SnapshotStatus.ACCEPTED:
                snapshot = self._store.update_snapshot_status(
                    snapshot.snapshot_id, SnapshotStatus.ACCEPTED
                )
            self._store.set_active_snapshot(chain_id, snapshot.snapshot_id)
            accepted.append(snapshot)
            prior = snapshot

            # Generation 7 — persist certification artefacts.
            if index == 7:
                report = getattr(runner, "last_certification_report", None)
                if report is not None:
                    certification_report = report
                    certification = report.decision
                    # Ensure snapshot_id binding matches Gen 7 head.
                    if certification.snapshot_id != snapshot.snapshot_id:
                        from dataclasses import replace as dc_replace

                        certification = dc_replace(
                            certification, snapshot_id=snapshot.snapshot_id
                        )
                        certification_report = dc_replace(
                            certification_report, decision=certification
                        )
                    self._store.append_certification(certification)
                    ledger = tuple(self._store.list_decisions(chain_id))
                    certified_snapshot = CertifiedCurriculumSnapshot(
                        snapshot=snapshot,
                        certification=certification,
                        report=certification_report,
                        decision_ledger=ledger,
                    )
                    if emit_review_pack:
                        all_snaps = tuple(
                            s
                            for s in self._store.list_snapshots(chain_id)
                            if s.status
                            in {
                                SnapshotStatus.ACCEPTED,
                                SnapshotStatus.SUPERSEDED,
                            }
                        )
                        review_pack = self._review_pack_emitter.emit(
                            chain_id=chain_id,
                            workspace_id=workspace_id,
                            snapshots=all_snaps,
                            decision_ledger=ledger,
                            regression_reports=tuple(
                                self._store.list_regression_reports(chain_id)
                            ),
                            certification_report=certification_report,
                            created_at_iso=fixed_created_at_iso or _utc_now_iso(),
                        )

        active = self._store.get_active_snapshot(chain_id)
        return OrchestratorResult(
            chain_id=chain_id,
            accepted_snapshots=tuple(accepted),
            rejected_snapshots=tuple(rejected),
            active_snapshot_id=active.snapshot_id if active else None,
            stopped_at_index=stopped_at,
            rolled_back=rolled_back,
            certification=certification,
            certification_report=certification_report,
            certified_snapshot=certified_snapshot,
            review_pack=review_pack,
        )

    def run_from(
        self,
        start_index: int,
        *,
        chain_id: str,
        workspace_id: str,
        source_document_ids: tuple[int, ...],
        through: int = 7,
        profile: CalibrationProfile | None = None,
        source_documents: tuple[ExtractedDocument, ...] = (),
        subject_code: str = "CS1",
        version_label: str = "default",
        fixed_created_at_iso: str | None = None,
    ) -> OrchestratorResult:
        """Partial regeneration entry used by CalibrationRouter (Phase E)."""
        return self.run_chain(
            chain_id=chain_id,
            workspace_id=workspace_id,
            source_document_ids=source_document_ids,
            start_from=start_index,
            through=through,
            profile=profile,
            source_documents=source_documents,
            subject_code=subject_code,
            version_label=version_label,
            fixed_created_at_iso=fixed_created_at_iso,
        )

    def rollback_to_active(self, chain_id: str) -> CurriculumGenerationSnapshot | None:
        """Return the last accepted active snapshot (no content mutation)."""
        return self._store.get_active_snapshot(chain_id)

    def _seed_prior_for_start(
        self,
        chain_id: str,
        start_from: int,
    ) -> CurriculumGenerationSnapshot | None:
        """Seed partial regen from Gen(start_from-1), not a later Gen7 head.

        Calibration ``run_from(3)`` must validate Gen3 against Gen2 ceilings,
        not against the superseded Gen7 active pointer (PL-001A C4).
        """
        active = self._store.get_active_snapshot(chain_id)
        if start_from <= 1:
            return active
        history = [
            s
            for s in self._store.list_snapshots(chain_id)
            if s.status in {SnapshotStatus.ACCEPTED, SnapshotStatus.SUPERSEDED}
        ]
        parents = [
            s for s in history if s.generation_index == start_from - 1
        ]
        if parents:
            return parents[-1]
        earlier = [s for s in history if s.generation_index < start_from]
        if earlier:
            return max(earlier, key=lambda s: s.generation_index)
        return active

    def _validation_baselines(
        self,
        chain_id: str,
        prior: CurriculumGenerationSnapshot | None,
    ) -> list[CurriculumGenerationSnapshot]:
        """Multi-generation validation parents: prior + prior-of-prior + earliest."""
        history = [
            s
            for s in self._store.list_snapshots(chain_id)
            if s.status in {SnapshotStatus.ACCEPTED, SnapshotStatus.SUPERSEDED}
        ]
        history.sort(key=lambda s: s.generation_index)
        selected: list[CurriculumGenerationSnapshot] = []
        if history:
            selected.append(history[0])  # original / Gen 1 ceiling
        if prior is not None:
            selected.append(prior)
            earlier = [
                s for s in history if s.generation_index < prior.generation_index
            ]
            if earlier:
                selected.append(earlier[-1])
        # Deduplicate by snapshot_id preserving order
        seen: set[str] = set()
        unique: list[CurriculumGenerationSnapshot] = []
        for snap in selected:
            if snap.snapshot_id not in seen:
                unique.append(snap)
                seen.add(snap.snapshot_id)
        return unique
