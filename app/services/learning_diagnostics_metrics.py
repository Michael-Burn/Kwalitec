"""Learning Diagnostics metrics for Founder observability (KWP-008).

Aggregates deterministic diagnostic reports over persisted Evidence Packages.
Does not change Evidence Authority, Twin, Progress, Strategy, or Session runtime.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from typing import Any

from app.application.learning_diagnostics.dto import DiagnosticCategory
from app.application.learning_diagnostics.engine import LearningDiagnosticsEngine


@dataclass(frozen=True)
class LearningDiagnosticsMetricsSnapshot:
    """Founder-facing diagnostic category distribution and trend rates."""

    sittings_evaluated: int = 0
    category_counts: dict[str, int] = field(default_factory=dict)
    conceptual_misunderstanding_rate: float = 0.0
    prerequisite_weakness_rate: float = 0.0
    formula_recall_rate: float = 0.0
    calculation_accuracy_rate: float = 0.0
    reading_interpretation_rate: float = 0.0
    exam_technique_rate: float = 0.0
    confidence_mismatch_rate: float = 0.0
    retention_decay_rate: float = 0.0
    inconsistent_practice_rate: float = 0.0
    improving_understanding_rate: float = 0.0
    strong_performance_rate: float = 0.0
    # Supporting-cause frequencies (any finding, not only primary).
    supporting_category_counts: dict[str, int] = field(default_factory=dict)

    def to_opaque(self) -> dict[str, Any]:
        return {
            "sittings_evaluated": self.sittings_evaluated,
            "category_counts": dict(self.category_counts),
            "conceptual_misunderstanding_rate": round(
                self.conceptual_misunderstanding_rate, 4
            ),
            "prerequisite_weakness_rate": round(self.prerequisite_weakness_rate, 4),
            "formula_recall_rate": round(self.formula_recall_rate, 4),
            "calculation_accuracy_rate": round(self.calculation_accuracy_rate, 4),
            "reading_interpretation_rate": round(
                self.reading_interpretation_rate, 4
            ),
            "exam_technique_rate": round(self.exam_technique_rate, 4),
            "confidence_mismatch_rate": round(self.confidence_mismatch_rate, 4),
            "retention_decay_rate": round(self.retention_decay_rate, 4),
            "inconsistent_practice_rate": round(
                self.inconsistent_practice_rate, 4
            ),
            "improving_understanding_rate": round(
                self.improving_understanding_rate, 4
            ),
            "strong_performance_rate": round(self.strong_performance_rate, 4),
            "supporting_category_counts": dict(self.supporting_category_counts),
        }


class LearningDiagnosticsMetrics:
    """Compute diagnostic trends from persisted sitting packages."""

    @staticmethod
    def from_packages(
        packages: list[dict[str, Any]] | tuple[dict[str, Any], ...],
        *,
        engine: LearningDiagnosticsEngine | None = None,
    ) -> LearningDiagnosticsMetricsSnapshot:
        diagnostics_engine = engine or LearningDiagnosticsEngine()
        primary_counts: Counter[str] = Counter()
        any_counts: Counter[str] = Counter()
        evaluated = 0

        for raw in packages:
            if not isinstance(raw, dict):
                continue
            report = diagnostics_engine.evaluate_opaque(raw)
            evaluated += 1
            primary_counts[report.primary.category.value] += 1
            for finding in report.findings:
                any_counts[finding.category.value] += 1

        if evaluated == 0:
            return LearningDiagnosticsMetricsSnapshot()

        def _rate(category: DiagnosticCategory) -> float:
            return primary_counts.get(category.value, 0) / evaluated

        return LearningDiagnosticsMetricsSnapshot(
            sittings_evaluated=evaluated,
            category_counts=dict(primary_counts),
            conceptual_misunderstanding_rate=_rate(
                DiagnosticCategory.CONCEPTUAL_MISUNDERSTANDING
            ),
            prerequisite_weakness_rate=_rate(
                DiagnosticCategory.PREREQUISITE_WEAKNESS
            ),
            formula_recall_rate=_rate(
                DiagnosticCategory.FORMULA_RECALL_WEAKNESS
            ),
            calculation_accuracy_rate=_rate(
                DiagnosticCategory.CALCULATION_ACCURACY
            ),
            reading_interpretation_rate=_rate(
                DiagnosticCategory.READING_INTERPRETATION
            ),
            exam_technique_rate=_rate(DiagnosticCategory.EXAM_TECHNIQUE),
            confidence_mismatch_rate=_rate(
                DiagnosticCategory.CONFIDENCE_MISMATCH
            ),
            retention_decay_rate=_rate(DiagnosticCategory.RETENTION_DECAY),
            inconsistent_practice_rate=_rate(
                DiagnosticCategory.INCONSISTENT_PRACTICE
            ),
            improving_understanding_rate=_rate(
                DiagnosticCategory.IMPROVING_UNDERSTANDING
            ),
            strong_performance_rate=_rate(
                DiagnosticCategory.STRONG_PERFORMANCE
            ),
            supporting_category_counts=dict(any_counts),
        )

    @classmethod
    def from_store(cls, store: Any) -> LearningDiagnosticsMetricsSnapshot:
        packages: list[dict[str, Any]] = []
        list_fn = getattr(store, "list_evidence_packages", None)
        if callable(list_fn):
            raw_list = list_fn()
            if isinstance(raw_list, list | tuple):
                packages = [p for p in raw_list if isinstance(p, dict)]
        elif hasattr(store, "evidence_packages"):
            raw_list = store.evidence_packages
            if isinstance(raw_list, list | tuple):
                packages = [p for p in raw_list if isinstance(p, dict)]
        return cls.from_packages(packages)
