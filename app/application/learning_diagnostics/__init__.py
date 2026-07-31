"""Learning Diagnostics Engine — Educational Intelligence Phase 2 (KWP-008).

Answers *why* a learner is struggling or succeeding from existing evidence.
Composes with Learning Strategy (WHAT) without redesigning Strategy, Evidence,
Progress, Twin, Runtime, or Mission Runtime.
"""

from __future__ import annotations

from app.application.learning_diagnostics.dto import (
    DIAGNOSTIC_CATEGORY_LABELS,
    DiagnosticCategory,
    DiagnosticEvidenceInput,
    DiagnosticFinding,
    LearningDiagnosticsReport,
)
from app.application.learning_diagnostics.engine import (
    LearningDiagnosticsEngine,
    get_learning_diagnostics_engine,
)

__all__ = [
    "DIAGNOSTIC_CATEGORY_LABELS",
    "DiagnosticCategory",
    "DiagnosticEvidenceInput",
    "DiagnosticFinding",
    "LearningDiagnosticsEngine",
    "LearningDiagnosticsReport",
    "get_learning_diagnostics_engine",
]
