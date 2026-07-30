"""CertificationEngine — Generation 7 educational certification (EI-001D)."""

from __future__ import annotations

from uuid import uuid4

from app.application.curriculum_intelligence.decision_quality import (
    compute_decision_quality,
)
from app.application.curriculum_intelligence.ports.certification_engine_port import (
    CertificationEngine,
)
from app.domain.curriculum_intelligence.certification import (
    CertificationPolicy,
    CertificationReport,
    DecisionQualityScores,
)
from app.domain.curriculum_intelligence.content_role import NON_CURRICULUM_ROLES
from app.domain.curriculum_intelligence.decision_ledger import DecisionLedgerEntry
from app.domain.curriculum_intelligence.generation import (
    CertificationDecision,
    CertificationOutcome,
    CurriculumGenerationSnapshot,
    RegressionReport,
    SnapshotStatus,
)

_OBJECTIVE_KINDS = frozenset({"learning_objective", "objective"})
_NOISE_ROLES = frozenset(r.value for r in NON_CURRICULUM_ROLES)

# Quality Score weights (normative blend → 0–100).
_W_COVERAGE = 0.30
_W_HIERARCHY = 0.20
_W_GRANULARITY = 0.15
_W_NOISE_INV = 0.15
_W_CONFIDENCE = 0.10
_W_EVIDENCE = 0.10


class DefaultCertificationEngine(CertificationEngine):
    """Score Gen 6 (+ history) and emit CERTIFIED / WARNINGS / NOT_CERTIFIED."""

    def __init__(self, policy: CertificationPolicy | None = None) -> None:
        self._policy = policy or CertificationPolicy()

    def certify(
        self,
        snapshot: CurriculumGenerationSnapshot,
        *,
        quality_history: tuple[CurriculumGenerationSnapshot, ...],
        regression_history: tuple[RegressionReport, ...],
        decision_ledger: tuple[DecisionLedgerEntry, ...] = (),
        created_at_iso: str = "",
        decision_id: str | None = None,
    ) -> CertificationDecision:
        """Return certification decision; prefer ``certify_report``."""
        report = self.certify_report(
            snapshot,
            quality_history=quality_history,
            regression_history=regression_history,
            decision_ledger=decision_ledger,
            created_at_iso=created_at_iso,
            decision_id=decision_id,
        )
        return report.decision

    def certify_report(
        self,
        snapshot: CurriculumGenerationSnapshot,
        *,
        quality_history: tuple[CurriculumGenerationSnapshot, ...],
        regression_history: tuple[RegressionReport, ...],
        decision_ledger: tuple[DecisionLedgerEntry, ...] = (),
        created_at_iso: str = "",
        decision_id: str | None = None,
    ) -> CertificationReport:
        """Full Gen 7 certification with scores, gates, and reasons."""
        _ = quality_history  # available for Review Pack / future diet checks
        metrics = snapshot.metrics
        decision_quality = compute_decision_quality(
            decision_ledger, snapshot=snapshot, metrics=metrics
        )
        hard_failures, warnings, reasons = self._evaluate_gates(
            snapshot,
            regression_history=regression_history,
            decision_quality=decision_quality,
        )

        quality_score = self._quality_score(metrics)
        reasoning_confidence = self._reasoning_confidence(
            decision_ledger, metrics.confidence
        )

        if hard_failures:
            outcome = CertificationOutcome.NOT_CERTIFIED
        elif warnings:
            outcome = CertificationOutcome.CERTIFIED_WITH_WARNINGS
        else:
            outcome = CertificationOutcome.CERTIFIED

        ts = created_at_iso or snapshot.created_at_iso
        decision = CertificationDecision(
            decision_id=decision_id or f"cert-{uuid4().hex[:12]}",
            chain_id=snapshot.chain_id,
            snapshot_id=snapshot.snapshot_id,
            outcome=outcome,
            quality_score=quality_score,
            confidence=round(metrics.confidence, 4),
            coverage=round(metrics.coverage, 4),
            hierarchy_score=round(metrics.hierarchy, 4),
            granularity_score=round(metrics.granularity, 4),
            warnings=tuple(warnings),
            hard_gate_failures=tuple(hard_failures),
            created_at_iso=ts,
            evidence_quality=round(metrics.evidence_quality, 4),
            reasoning_confidence=reasoning_confidence,
            decision_quality=decision_quality.aggregate,
            failure_reasons=tuple(hard_failures),
        )
        return CertificationReport(
            decision=decision,
            decision_quality=decision_quality,
            quality_vector=metrics,
            hard_gate_failures=tuple(hard_failures),
            warnings=tuple(warnings),
            reasons=tuple(reasons),
            ledger_entry_ids=tuple(e.decision_id for e in decision_ledger),
        )

    def _quality_score(self, metrics) -> float:
        noise_inv = max(0.0, 1.0 - metrics.noise)
        blended = (
            _W_COVERAGE * metrics.coverage
            + _W_HIERARCHY * metrics.hierarchy
            + _W_GRANULARITY * metrics.granularity
            + _W_NOISE_INV * noise_inv
            + _W_CONFIDENCE * metrics.confidence
            + _W_EVIDENCE * metrics.evidence_quality
        )
        return round(100.0 * blended, 2)

    def _reasoning_confidence(
        self,
        entries: tuple[DecisionLedgerEntry, ...],
        fallback: float,
    ) -> float:
        if not entries:
            return round(fallback, 4)
        return round(
            sum(e.reasoning_confidence for e in entries) / len(entries),
            4,
        )

    def _evaluate_gates(
        self,
        snapshot: CurriculumGenerationSnapshot,
        *,
        regression_history: tuple[RegressionReport, ...],
        decision_quality: DecisionQualityScores,
    ) -> tuple[list[str], list[str], list[str]]:
        policy = self._policy
        metrics = snapshot.metrics
        hard: list[str] = []
        soft: list[str] = []
        reasons: list[str] = []

        active = snapshot.active_nodes()
        contaminated = [
            n for n in active if (n.role or "") in _NOISE_ROLES
        ]
        if contaminated or metrics.noise > policy.max_noise:
            hard.append(
                "front_matter_contamination: "
                f"noise={metrics.noise:.4f} exceeds max={policy.max_noise:.4f} "
                f"({len(contaminated)} active non-curriculum nodes)"
            )

        if metrics.coverage < policy.coverage_floor:
            hard.append(
                "coverage_floor: "
                f"coverage={metrics.coverage:.4f} < floor={policy.coverage_floor:.4f}"
            )

        if metrics.hierarchy < policy.hierarchy_floor:
            hard.append(
                "hierarchy_floor: "
                f"hierarchy={metrics.hierarchy:.4f} "
                f"< floor={policy.hierarchy_floor:.4f}"
            )

        if metrics.granularity < policy.granularity_floor:
            soft.append(
                "granularity_soft: "
                f"granularity={metrics.granularity:.4f} "
                f"< floor={policy.granularity_floor:.4f}"
            )

        if metrics.confidence < policy.confidence_floor:
            hard.append(
                "confidence_floor: "
                f"confidence={metrics.confidence:.4f} "
                f"< floor={policy.confidence_floor:.4f}"
            )

        if metrics.evidence_quality < policy.evidence_quality_floor:
            hard.append(
                "evidence_quality_floor: "
                f"evidence_quality={metrics.evidence_quality:.4f} "
                f"< floor={policy.evidence_quality_floor:.4f}"
            )

        if decision_quality.aggregate < policy.decision_quality_floor:
            soft.append(
                "decision_quality_soft: "
                f"decision_quality={decision_quality.aggregate:.4f} "
                f"< floor={policy.decision_quality_floor:.4f}"
            )

        if policy.require_no_active_regression_head:
            if snapshot.status is SnapshotStatus.REJECTED_BY_REGRESSION:
                hard.append(
                    "regression_head: active snapshot was rejected by RegressionGuard"
                )
            # If the latest regression for this snapshot failed, block.
            for report in regression_history:
                if (
                    report.candidate_snapshot_id == snapshot.snapshot_id
                    and not report.accepted
                ):
                    hard.append(
                        "regression_rejected: "
                        f"snapshot {snapshot.snapshot_id} failed regression "
                        f"({report.reason})"
                    )
                    break

        if policy.require_syllabus_refs_on_objectives:
            objectives = [n for n in active if n.kind in _OBJECTIVE_KINDS]
            missing_ref = []
            for node in objectives:
                has_syllabus = bool(node.lineage.syllabus_refs)
                attrs = dict(node.attributes)
                cmp_only = attrs.get("cmp_only_support", "").lower() in {
                    "1",
                    "true",
                    "yes",
                }
                if not has_syllabus and not cmp_only:
                    missing_ref.append(node.node_id)
            if missing_ref:
                # Soft when few; hard when majority lack authority.
                share = len(missing_ref) / max(len(objectives), 1)
                msg = (
                    "objective_syllabus_refs: "
                    f"{len(missing_ref)}/{len(objectives)} active LOs lack "
                    "syllabus ref or cmp_only_support flag"
                )
                if share > 0.5:
                    hard.append(msg)
                else:
                    soft.append(msg)

        if metrics.low_confidence_share > policy.max_low_confidence_share_warning:
            soft.append(
                "low_confidence_share: "
                f"{metrics.low_confidence_share:.4f} > "
                f"{policy.max_low_confidence_share_warning:.4f}"
            )

        # Cross-diet / partial coverage warning when coverage is below perfect
        # but still above the hard floor (EQ-001 2019 CMP vs 2026 syllabus).
        if policy.coverage_floor <= metrics.coverage < 1.0:
            soft.append(
                "partial_coverage: "
                f"coverage={metrics.coverage:.4f} — cross-diet or incomplete "
                "syllabus alignment may remain"
            )

        if hard:
            reasons.append("Hard certification gates failed.")
            reasons.extend(hard)
        elif soft:
            reasons.append("Hard gates passed; soft warnings remain.")
            reasons.extend(soft)
        else:
            reasons.append("All hard and soft certification gates passed.")

        return hard, soft, reasons
