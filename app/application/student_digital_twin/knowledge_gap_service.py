"""Knowledge-gap generation — via KnowledgeGapDetectionRule + evidence bundle."""

from __future__ import annotations

from datetime import UTC, datetime

from app.application.curriculum_retrieval.curriculum_retrieval_service import (
    CurriculumRetrievalService,
)
from app.application.educational_reasoning.curriculum_evidence_service import (
    CurriculumEvidenceService,
)
from app.domain.educational_reasoning.gap_analysis import (
    GAP_MASTERY_THRESHOLD,
    KnowledgeGapDetectionRule,
    PrerequisiteAnalysisRule,
)
from app.domain.educational_reasoning.reasoning_context import ReasoningContext
from app.domain.student_digital_twin.knowledge_gap import KnowledgeGap
from app.domain.student_digital_twin.mastery import MasteryMap

__all__ = ["GAP_MASTERY_THRESHOLD", "KnowledgeGapService"]


class KnowledgeGapService:
    """Identify knowledge gaps using retrieval evidence only.

    Builds a CurriculumEvidenceBundle then applies gap + prerequisite rules.
    """

    def __init__(
        self,
        *,
        retrieval: CurriculumRetrievalService | None = None,
    ) -> None:
        retrieval_svc = retrieval or CurriculumRetrievalService()
        self._retrieval = retrieval_svc
        self._evidence = CurriculumEvidenceService(retrieval=retrieval_svc)

    def identify(
        self,
        *,
        twin_id: str,
        mastery: MasteryMap,
        workspace_id: str,
        subject_code: str = "",
    ) -> tuple[KnowledgeGap, ...]:
        """Return gaps for weak concepts that have retrieval-backed evidence."""
        now = datetime.now(UTC).replace(tzinfo=None)
        evidence = self._evidence.retrieve_for_reasoning(
            observations=(),
            mastery=mastery,
            workspace_id=workspace_id,
            subject_code=subject_code,
        )
        context = ReasoningContext(
            twin_id=twin_id,
            student_id=twin_id,
            workspace_id=workspace_id,
            subject_code=subject_code,
            observations=(),
            observation_ids=(),
            prior_mastery=mastery,
            curriculum_evidence=evidence,
            triggered_by="knowledge_gap_service",
            computed_at=now,
            mastery=mastery,
        )
        gap_ex = KnowledgeGapDetectionRule().apply(context)
        context = context.with_updates(gaps=gap_ex.gaps or ())
        prereq_ex = PrerequisiteAnalysisRule().apply(context)
        return prereq_ex.gaps if prereq_ex.gaps is not None else ()
