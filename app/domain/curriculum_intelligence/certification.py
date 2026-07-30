"""Generation 7 certification contracts (EI-001D).

CertifiedCurriculumSnapshot is the only artefact Founder Preview may consume.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.domain.curriculum_intelligence.decision_ledger import DecisionLedgerEntry
from app.domain.curriculum_intelligence.generation import (
    CertificationDecision,
    CertificationOutcome,
    CurriculumGenerationSnapshot,
    QualitySnapshot,
)


@dataclass(frozen=True)
class CertificationPolicy:
    """Hard / soft gates for Generation 7 Educational Certification."""

    coverage_floor: float = 0.90
    hierarchy_floor: float = 0.50
    granularity_floor: float = 0.40
    confidence_floor: float = 0.60
    evidence_quality_floor: float = 0.50
    decision_quality_floor: float = 0.55
    max_noise: float = 0.0
    max_low_confidence_share_warning: float = 0.25
    require_syllabus_refs_on_objectives: bool = True
    require_no_active_regression_head: bool = True


@dataclass(frozen=True)
class DecisionQualityScores:
    """Explainable decision-quality dimensions for Gen 7."""

    merge_quality: float
    split_quality: float
    objective_quality: float
    coverage_quality: float
    hierarchy_quality: float
    policy_consistency: float
    evidence_quality: float
    aggregate: float

    def as_vector(self) -> dict[str, float]:
        return {
            "merge_quality": self.merge_quality,
            "split_quality": self.split_quality,
            "objective_quality": self.objective_quality,
            "coverage_quality": self.coverage_quality,
            "hierarchy_quality": self.hierarchy_quality,
            "policy_consistency": self.policy_consistency,
            "evidence_quality": self.evidence_quality,
            "aggregate": self.aggregate,
        }


@dataclass(frozen=True)
class CertificationReport:
    """Full Gen 7 certification artefact (scores + decision + reasons)."""

    decision: CertificationDecision
    decision_quality: DecisionQualityScores
    quality_vector: QualitySnapshot
    hard_gate_failures: tuple[str, ...]
    warnings: tuple[str, ...]
    reasons: tuple[str, ...]
    ledger_entry_ids: tuple[str, ...] = ()

    @property
    def outcome(self) -> CertificationOutcome:
        return self.decision.outcome

    @property
    def certification_status(self) -> CertificationOutcome:
        return self.decision.outcome


@dataclass(frozen=True)
class CertifiedCurriculumSnapshot:
    """Immutable certified head for Founder Preview / future publication.

    Preview consumes certified snapshots only — never raw Gen 1–6 heads.
    """

    snapshot: CurriculumGenerationSnapshot
    certification: CertificationDecision
    report: CertificationReport
    decision_ledger: tuple[DecisionLedgerEntry, ...] = ()

    @property
    def chain_id(self) -> str:
        return self.snapshot.chain_id

    @property
    def snapshot_id(self) -> str:
        return self.snapshot.snapshot_id

    @property
    def outcome(self) -> CertificationOutcome:
        return self.certification.outcome

    @property
    def is_preview_eligible(self) -> bool:
        """CERTIFIED or CERTIFIED_WITH_WARNINGS may enter Founder Preview."""
        return self.outcome in {
            CertificationOutcome.CERTIFIED,
            CertificationOutcome.CERTIFIED_WITH_WARNINGS,
        }
