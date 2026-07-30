"""EI-002B — Curriculum Observatory operational analytics.

Aggregates certification trends, calibration frequency, policy warnings,
decision quality, evidence quality, and coverage metrics from the
GenerationStore (Curriculum Memory). Read-only — does not mutate chains.
"""

from __future__ import annotations

from collections import Counter
from uuid import uuid4

from app.application.curriculum_intelligence.ports.generation_store_port import (
    GenerationStorePort,
)
from app.domain.curriculum_intelligence.certified_learning import (
    CurriculumObservatoryReport,
    ObservatoryMetric,
)
from app.domain.curriculum_intelligence.generation import (
    CertificationOutcome,
    GenerationIndex,
)


class CurriculumObservatory:
    """Operational analytics surface for the Curriculum Intelligence Engine."""

    def __init__(self, store: GenerationStorePort) -> None:
        self._store = store

    def report_for_chain(self, chain_id: str) -> CurriculumObservatoryReport:
        """Build an observatory report for one generation chain."""
        chain = (chain_id or "").strip()
        if not chain:
            raise ValueError("chain_id is required")

        snapshots = self._store.list_snapshots(chain)
        certifications = []
        for snap in snapshots:
            decision = self._store.get_certification(snap.snapshot_id)
            if decision is not None:
                certifications.append((snap, decision))

        outcome_counts = Counter(
            d.outcome.value for _, d in certifications
        )
        certification_trends = tuple(
            ObservatoryMetric(
                name=f"outcome_{outcome}",
                value=float(count),
                unit="count",
                notes="certification decisions for chain",
            )
            for outcome, count in sorted(outcome_counts.items())
        ) or (
            ObservatoryMetric(
                name="outcome_none",
                value=0.0,
                unit="count",
                notes="no certification decisions recorded",
            ),
        )

        # Calibration frequency: Gen 7 re-certifications after first + profiles.
        cert_snaps = [
            s
            for s in snapshots
            if s.generation_index == int(GenerationIndex.CERTIFICATION)
        ]
        calibration_runs = max(0, len(cert_snaps) - 1) if cert_snaps else 0
        list_for_workspace = getattr(
            self._store, "list_calibration_profiles_for_workspace", None
        )
        workspace_id = ""
        get_ws = getattr(self._store, "get_workspace_id_for_chain", None)
        if callable(get_ws):
            workspace_id = str(get_ws(chain) or "")
        if not workspace_id and snapshots:
            workspace_id = str(
                getattr(snapshots[0].generation, "workspace_id", "") or ""
            )
        profile_count = 0
        if callable(list_for_workspace) and workspace_id:
            profile_count = len(list(list_for_workspace(workspace_id) or ()))
            calibration_runs = max(calibration_runs, profile_count)

        calibration_frequency = (
            ObservatoryMetric(
                name="calibration_runs",
                value=float(calibration_runs),
                unit="count",
                notes="partial regen / calibration profile applications",
            ),
            ObservatoryMetric(
                name="calibration_profiles",
                value=float(profile_count),
                unit="count",
            ),
            ObservatoryMetric(
                name="certification_snapshots",
                value=float(len(cert_snaps)),
                unit="count",
            ),
        )

        policy_warnings: list[str] = []
        decision_quality: list[ObservatoryMetric] = []
        evidence_quality: list[ObservatoryMetric] = []
        coverage_metrics: list[ObservatoryMetric] = []

        for snap, decision in certifications:
            for warning in decision.warnings or ():
                policy_warnings.append(str(warning))
            for failure in decision.hard_gate_failures or ():
                policy_warnings.append(f"hard_gate:{failure}")
            decision_quality.append(
                ObservatoryMetric(
                    name=f"decision_quality:{snap.snapshot_id}",
                    value=float(decision.decision_quality),
                    unit="score",
                    notes=decision.outcome.value,
                )
            )
            evidence_quality.append(
                ObservatoryMetric(
                    name=f"evidence_quality:{snap.snapshot_id}",
                    value=float(decision.evidence_quality),
                    unit="score",
                )
            )
            coverage_metrics.append(
                ObservatoryMetric(
                    name=f"coverage:{snap.snapshot_id}",
                    value=float(decision.coverage),
                    unit="ratio",
                    notes=decision.outcome.value,
                )
            )
            metrics = getattr(snap, "metrics", None)
            if metrics is not None:
                coverage_metrics.append(
                    ObservatoryMetric(
                        name=f"snapshot_coverage:{snap.snapshot_id}",
                        value=float(getattr(metrics, "coverage", 0.0)),
                        unit="ratio",
                    )
                )
                evidence_quality.append(
                    ObservatoryMetric(
                        name=f"snapshot_evidence:{snap.snapshot_id}",
                        value=float(getattr(metrics, "evidence_quality", 0.0)),
                        unit="score",
                    )
                )

        # Ledger-derived policy warnings.
        try:
            ledger = tuple(self._store.list_decisions(chain))
        except Exception:  # noqa: BLE001 — observatory must be best-effort
            ledger = ()
        warning_outcomes = {
            str(getattr(e.decision_outcome, "value", e.decision_outcome)).lower()
            for e in ledger
        }
        if "warning" in warning_outcomes:
            policy_warnings.append("decision_ledger_contains_warnings")
        if "rejected" in warning_outcomes:
            policy_warnings.append("decision_ledger_contains_rejections")

        certified_count = outcome_counts.get(
            CertificationOutcome.CERTIFIED.value, 0
        ) + outcome_counts.get(
            CertificationOutcome.CERTIFIED_WITH_WARNINGS.value, 0
        )
        metadata = (
            ("snapshot_count", str(len(snapshots))),
            ("certification_count", str(len(certifications))),
            ("certified_or_warnings", str(certified_count)),
            ("ledger_entries", str(len(ledger))),
        )

        return CurriculumObservatoryReport(
            report_id=f"obs_{uuid4().hex[:12]}",
            chain_id=chain,
            certification_trends=certification_trends,
            calibration_frequency=calibration_frequency,
            policy_warnings=tuple(dict.fromkeys(policy_warnings)),
            decision_quality=tuple(decision_quality),
            evidence_quality=tuple(evidence_quality),
            coverage_metrics=tuple(coverage_metrics),
            metadata=metadata,
        )

    def report_for_workspace(self, workspace_id: str) -> CurriculumObservatoryReport:
        """Resolve workspace → chain via store binding, then report."""
        wid = (workspace_id or "").strip()
        if not wid:
            raise ValueError("workspace_id is required")
        chain_id = self._store.get_chain_id_for_workspace(wid)
        if not chain_id:
            return CurriculumObservatoryReport(
                report_id=f"obs_{uuid4().hex[:12]}",
                chain_id="",
                certification_trends=(
                    ObservatoryMetric(
                        name="outcome_none",
                        value=0.0,
                        unit="count",
                        notes="workspace has no bound generation chain",
                    ),
                ),
                metadata=(("workspace_id", wid), ("bound", "false")),
            )
        report = self.report_for_chain(chain_id)
        return CurriculumObservatoryReport(
            report_id=report.report_id,
            chain_id=report.chain_id,
            certification_trends=report.certification_trends,
            calibration_frequency=report.calibration_frequency,
            policy_warnings=report.policy_warnings,
            decision_quality=report.decision_quality,
            evidence_quality=report.evidence_quality,
            coverage_metrics=report.coverage_metrics,
            metadata=report.metadata + (("workspace_id", wid), ("bound", "true")),
        )
