"""Learning Diagnostics Engine — Educational Intelligence Phase 2 (KWP-008).

Deterministic cause diagnosis over existing sitting / Progress / Twin /
cadence signals. Produces student guidance + cause WHY — never category
labels, never AI, never scores as product.

MUST NOT redesign Learning Strategy, LearningSessionRuntime,
EducationalEvidenceAuthority, StudentTwinEngine, ProgressEngine,
Mission Runtime, Commercial Loop, or Session FSM.
"""

from __future__ import annotations

import logging
from typing import Any

from app.application.learning_diagnostics.dto import (
    DiagnosticEvidenceInput,
    LearningDiagnosticsReport,
)
from app.application.learning_diagnostics.rules import (
    diagnose,
    finding_from_decision,
)

logger = logging.getLogger(__name__)


class LearningDiagnosticsEngine:
    """Identify probable learning causes from existing evidence outputs."""

    AUTHORITY_ID = "learning_diagnostics_engine"

    def evaluate(
        self,
        evidence: DiagnosticEvidenceInput | dict[str, Any] | None = None,
        *,
        opaque: dict[str, Any] | None = None,
        metadata: dict[str, Any] | None = None,
        twin_signals: dict[str, Any] | None = None,
        cadence: dict[str, Any] | None = None,
    ) -> LearningDiagnosticsReport:
        """Return a deterministic LearningDiagnosticsReport.

        Args:
            evidence: Pre-built DiagnosticEvidenceInput, or omit to build
                from opaque sitting facts.
            opaque: Sitting / completion opaque summary.
            metadata: Completion metadata pairs / dict.
            twin_signals: Optional Twin-derived enrichments (read-only).
            cadence: Optional streak / session-count enrichments.

        Returns:
            LearningDiagnosticsReport with student-safe guidance + WHY.
        """
        if isinstance(evidence, DiagnosticEvidenceInput):
            inputs = evidence
        else:
            merged_opaque = dict(opaque or {})
            if isinstance(evidence, dict):
                merged_opaque = {**merged_opaque, **evidence}
            inputs = DiagnosticEvidenceInput.from_opaque(
                merged_opaque,
                metadata=metadata,
                twin_signals=twin_signals,
                cadence=cadence,
            )

        decisions = diagnose(inputs)
        findings = tuple(
            finding_from_decision(decision, inputs) for decision in decisions
        )
        primary = findings[0]
        supporting = findings[1:4]
        report = LearningDiagnosticsReport(
            primary=primary,
            supporting=supporting,
            metadata=(
                ("authority", self.AUTHORITY_ID),
                ("rule_id", primary.rule_id),
                ("category", primary.category.value),
            ),
        )
        logger.debug(
            "learning_diagnostics rule=%s category=%s topic=%r",
            primary.rule_id,
            primary.category.value,
            inputs.topic_title,
        )
        return report

    def evaluate_opaque(
        self,
        opaque_summary: dict[str, Any] | None,
        *,
        metadata: dict[str, Any] | None = None,
        twin_signals: dict[str, Any] | None = None,
        cadence: dict[str, Any] | None = None,
    ) -> LearningDiagnosticsReport:
        """Convenience wrapper for Sitting Report / founder projectors."""
        return self.evaluate(
            opaque=opaque_summary,
            metadata=metadata,
            twin_signals=twin_signals,
            cadence=cadence,
        )


_DEFAULT_ENGINE: LearningDiagnosticsEngine | None = None


def get_learning_diagnostics_engine() -> LearningDiagnosticsEngine:
    """Process-scoped default engine instance."""
    global _DEFAULT_ENGINE
    if _DEFAULT_ENGINE is None:
        _DEFAULT_ENGINE = LearningDiagnosticsEngine()
    return _DEFAULT_ENGINE
