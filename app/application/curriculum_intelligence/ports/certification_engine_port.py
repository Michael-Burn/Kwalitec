"""CertificationEngine port — Gen 7 educational certification (EI-001D)."""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.domain.curriculum_intelligence.decision_ledger import DecisionLedgerEntry
from app.domain.curriculum_intelligence.generation import (
    CertificationDecision,
    CurriculumGenerationSnapshot,
    RegressionReport,
)


class CertificationEngine(ABC):
    """Produce a certification decision for a generation-7 candidate snapshot."""

    @abstractmethod
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
        """Return CERTIFIED / CERTIFIED_WITH_WARNINGS / NOT_CERTIFIED."""


class UnimplementedCertificationEngine(CertificationEngine):
    """Legacy Phase A stub — prefer DefaultCertificationEngine (EI-001D)."""

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
        _ = (
            snapshot,
            quality_history,
            regression_history,
            decision_ledger,
            created_at_iso,
            decision_id,
        )
        raise NotImplementedError(
            "Use DefaultCertificationEngine from "
            "app.application.curriculum_intelligence.certification_engine"
        )
