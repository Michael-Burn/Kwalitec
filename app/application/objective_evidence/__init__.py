"""Objective Evidence Architecture (Phase 1-2).

Canonical LO identity and append-only Assessment Evidence recording.
Does not interpret mastery, EK, or strength. Does not notify Twin,
Spacing Scheduler, Policy V1, Decision Engine, or Progress paths.
"""

from app.application.objective_evidence.canonical_objective_id import (
    CanonicalObjectiveId,
)
from app.application.objective_evidence.recorder import (
    ObjectiveAssessmentEvidenceRecorder,
)
from app.application.objective_evidence.records import AssessmentEvidenceRecord
from app.application.objective_evidence.store import (
    ObjectiveAssessmentEvidenceStore,
    get_objective_assessment_evidence_store,
    reset_objective_assessment_evidence_store,
)

__all__ = (
    "AssessmentEvidenceRecord",
    "CanonicalObjectiveId",
    "ObjectiveAssessmentEvidenceRecorder",
    "ObjectiveAssessmentEvidenceStore",
    "get_objective_assessment_evidence_store",
    "reset_objective_assessment_evidence_store",
)
