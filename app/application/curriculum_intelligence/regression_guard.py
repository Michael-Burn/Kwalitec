"""RegressionGuard — lexicographic gates over EQ-001-derived QualitySnapshots.

Hard gates protect coverage, noise, hierarchy, granularity, evidence quality,
and confidence. Soft notes remain for informational preference messaging.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.domain.curriculum_intelligence.generation import (
    QualitySnapshot,
    RegressionPolicy,
    RegressionReport,
)


@dataclass(frozen=True)
class RegressionVerdict:
    """Outcome of comparing a candidate quality vector to baselines."""

    accepted: bool
    reason: str
    gate_failures: tuple[str, ...]
    baseline_metrics: QualitySnapshot


class RegressionGuard:
    """Lexicographic hard gates over real educational quality vectors."""

    def __init__(self, policy: RegressionPolicy | None = None) -> None:
        self._policy = policy or RegressionPolicy()

    @property
    def policy(self) -> RegressionPolicy:
        return self._policy

    def compare(
        self,
        candidate: QualitySnapshot,
        baselines: tuple[QualitySnapshot, ...],
        *,
        policy: RegressionPolicy | None = None,
    ) -> RegressionVerdict:
        """Compare candidate against the educational ceiling of baselines.

        Hard gates (in order):
        1. coverage must not decrease beyond ε
        2. noise must not increase beyond ε
        3. hierarchy must not decrease beyond ε
        4. granularity must not decrease beyond ε (Phase C)
        5. evidence_quality must not decrease beyond ε (Phase C)
        6. confidence must not decrease beyond ε (Phase C)

        Soft preference notes remain when dimensions improve or stay level.
        """
        active_policy = policy or self._policy
        if not baselines:
            return RegressionVerdict(
                accepted=True,
                reason="no_baselines",
                gate_failures=(),
                baseline_metrics=candidate,
            )

        ceiling = _ceiling(baselines)
        failures: list[str] = []

        if candidate.coverage + active_policy.coverage_epsilon < ceiling.coverage:
            failures.append(
                f"coverage:{candidate.coverage:.4f}<{ceiling.coverage:.4f}"
            )
        if candidate.noise - active_policy.noise_epsilon > ceiling.noise:
            failures.append(f"noise:{candidate.noise:.4f}>{ceiling.noise:.4f}")
        if candidate.hierarchy + active_policy.hierarchy_epsilon < ceiling.hierarchy:
            failures.append(
                f"hierarchy:{candidate.hierarchy:.4f}<{ceiling.hierarchy:.4f}"
            )
        if (
            active_policy.reject_on_granularity
            and candidate.granularity + active_policy.granularity_epsilon
            < ceiling.granularity
        ):
            failures.append(
                f"granularity:{candidate.granularity:.4f}<{ceiling.granularity:.4f}"
            )
        if (
            active_policy.reject_on_evidence_quality
            and candidate.evidence_quality + active_policy.evidence_quality_epsilon
            < ceiling.evidence_quality
        ):
            failures.append(
                "evidence_quality:"
                f"{candidate.evidence_quality:.4f}<{ceiling.evidence_quality:.4f}"
            )
        if (
            active_policy.reject_on_confidence
            and candidate.confidence + active_policy.confidence_epsilon
            < ceiling.confidence
        ):
            failures.append(
                f"confidence:{candidate.confidence:.4f}<{ceiling.confidence:.4f}"
            )

        if failures:
            return RegressionVerdict(
                accepted=False,
                reason="regression_gates_failed",
                gate_failures=tuple(failures),
                baseline_metrics=ceiling,
            )

        soft_notes: list[str] = []
        if (
            active_policy.prefer_granularity
            and candidate.granularity < ceiling.granularity
        ):
            soft_notes.append("granularity_below_ceiling")
        if (
            active_policy.prefer_confidence
            and candidate.confidence < ceiling.confidence
        ):
            soft_notes.append("confidence_below_ceiling")

        reason = "accepted"
        if soft_notes:
            reason = "accepted_with_soft_notes:" + ",".join(soft_notes)

        return RegressionVerdict(
            accepted=True,
            reason=reason,
            gate_failures=(),
            baseline_metrics=ceiling,
        )

    def build_report(
        self,
        *,
        report_id: str,
        chain_id: str,
        candidate_generation_id: str,
        candidate_snapshot_id: str,
        baseline_generation_ids: tuple[str, ...],
        verdict: RegressionVerdict,
        candidate_metrics: QualitySnapshot,
        created_at_iso: str,
    ) -> RegressionReport:
        """Materialise a durable RegressionReport from a verdict."""
        return RegressionReport(
            report_id=report_id,
            chain_id=chain_id,
            candidate_generation_id=candidate_generation_id,
            candidate_snapshot_id=candidate_snapshot_id,
            baseline_generation_ids=baseline_generation_ids,
            accepted=verdict.accepted,
            reason=verdict.reason,
            candidate_metrics=candidate_metrics,
            baseline_metrics=verdict.baseline_metrics,
            gate_failures=verdict.gate_failures,
            created_at_iso=created_at_iso,
        )


def _ceiling(baselines: tuple[QualitySnapshot, ...]) -> QualitySnapshot:
    """Educational ceiling: best coverage/hierarchy/granularity/confidence/
    evidence_quality; worst (lowest) duplicates and noise among baselines.
    """
    return QualitySnapshot(
        coverage=max(b.coverage for b in baselines),
        hierarchy=max(b.hierarchy for b in baselines),
        duplicates=min(b.duplicates for b in baselines),
        noise=min(b.noise for b in baselines),
        granularity=max(b.granularity for b in baselines),
        confidence=max(b.confidence for b in baselines),
        active_node_count=max(b.active_node_count for b in baselines),
        rejected_node_count=max(b.rejected_node_count for b in baselines),
        low_confidence_share=min(b.low_confidence_share for b in baselines),
        chapters=max(b.chapters for b in baselines),
        sections=max(b.sections for b in baselines),
        topics=max(b.topics for b in baselines),
        objectives=max(b.objectives for b in baselines),
        evidence_quality=max(b.evidence_quality for b in baselines),
    )
