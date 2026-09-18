"""Canonical coverage reconciliation (dual-source eligibility)."""

from app.application.coverage_reconciliation.acceptance import (
    LegacyAcceptanceResult,
    LegacyCompletionCandidate,
    accept_legacy_completion,
)
from app.application.coverage_reconciliation.constants import (
    CATEGORY_AMBIGUOUS_HISTORICAL_ACTIVITY,
    CATEGORY_CONFIRMED_COVERED,
    CATEGORY_HISTORICALLY_COMPLETED,
    CATEGORY_NOT_COVERED,
    COVERED_FOR_DISPLAY,
    EVIDENCE_LEGACY_COMPLETION,
    EVIDENCE_VERIFIED_COMPLETION,
)
from app.application.coverage_reconciliation.service import (
    CoverageReconciliationService,
)
from app.application.coverage_reconciliation.types import (
    CanonicalCoverageVerdict,
    CoverageDisplay,
    LearnerCoverageReconciliation,
    UnmappedHistoricalActivity,
)

__all__ = [
    "CATEGORY_AMBIGUOUS_HISTORICAL_ACTIVITY",
    "CATEGORY_CONFIRMED_COVERED",
    "CATEGORY_HISTORICALLY_COMPLETED",
    "CATEGORY_NOT_COVERED",
    "COVERED_FOR_DISPLAY",
    "CoverageDisplay",
    "CoverageReconciliationService",
    "CanonicalCoverageVerdict",
    "EVIDENCE_LEGACY_COMPLETION",
    "EVIDENCE_VERIFIED_COMPLETION",
    "LearnerCoverageReconciliation",
    "LegacyAcceptanceResult",
    "LegacyCompletionCandidate",
    "UnmappedHistoricalActivity",
    "accept_legacy_completion",
]
