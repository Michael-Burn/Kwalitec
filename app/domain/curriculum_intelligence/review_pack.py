"""Educational Review Pack contracts (EI-001D).

Generated for every engine run that reaches Generation 7 certification.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.domain.curriculum_intelligence.certification import CertificationReport
from app.domain.curriculum_intelligence.decision_ledger import DecisionLedgerSummary
from app.domain.curriculum_intelligence.generation import (
    QualitySnapshot,
    RegressionReport,
)


@dataclass(frozen=True)
class GenerationComparisonRow:
    """One generation's quality vector for comparison reports."""

    generation_index: int
    generation_id: str
    purpose: str
    metrics: QualitySnapshot
    active_nodes: int
    rejected_nodes: int
    generation_hash: str = ""


@dataclass(frozen=True)
class EducationalReviewPack:
    """Full Educational Review Pack for a certified (or attempted) run."""

    pack_id: str
    chain_id: str
    workspace_id: str
    created_at_iso: str
    generation_comparison: tuple[GenerationComparisonRow, ...]
    decision_summary: DecisionLedgerSummary
    coverage_matrix: dict[str, object]
    hierarchy_report: dict[str, object]
    evidence_report: dict[str, object]
    decision_ledger_summary: DecisionLedgerSummary
    regression_report: tuple[RegressionReport, ...]
    certification_report: CertificationReport | None
    artefacts_markdown: dict[str, str]

    @property
    def artefact_names(self) -> tuple[str, ...]:
        return tuple(sorted(self.artefacts_markdown.keys()))
