"""Retrieve supporting curriculum evidence before educational rules execute.

Stage 2 of the educational pipeline. Uses CurriculumRetrievalService only —
never VectorStore, Knowledge Graph, or embeddings directly.
"""

from __future__ import annotations

import logging

from app.application.curriculum_retrieval.curriculum_retrieval_service import (
    CurriculumRetrievalService,
)
from app.domain.curriculum_retrieval.profile import RetrievalProfile
from app.domain.curriculum_retrieval.query import RetrievalQuery
from app.domain.curriculum_retrieval.result import RetrievalResult
from app.domain.educational_reasoning.reasoning_context import CurriculumEvidenceBundle
from app.domain.student_digital_twin.mastery import MasteryMap
from app.domain.student_digital_twin.observation import Observation

logger = logging.getLogger(__name__)

# Align with gap detection threshold — only fetch evidence for weak concepts.
_CANDIDATE_MASTERY_THRESHOLD = 0.55


class CurriculumEvidenceService:
    """Build a CurriculumEvidenceBundle for a Twin reasoning cycle."""

    def __init__(
        self,
        *,
        retrieval: CurriculumRetrievalService | None = None,
    ) -> None:
        self._retrieval = retrieval or CurriculumRetrievalService()

    def retrieve_for_reasoning(
        self,
        *,
        observations: tuple[Observation, ...],
        mastery: MasteryMap,
        workspace_id: str,
        subject_code: str = "",
    ) -> CurriculumEvidenceBundle:
        """Retrieve curriculum evidence for concepts needing educational support.

        Evidence is keyed by concept_id. Concepts without retrieval hits are
        omitted — downstream gap rules will not create unsupported gaps.
        Retrieval failures are treated as empty evidence (no gaps), never as
        opaque educational decisions.
        """
        if not (workspace_id or "").strip():
            return CurriculumEvidenceBundle.empty()

        concept_ids = _candidate_concepts(observations, mastery)
        by_concept: dict[str, RetrievalResult] = {}
        all_evidence_ids: list[str] = []
        retrieval_log_ids: list[str] = []

        for concept_id in concept_ids:
            title = _concept_title(concept_id, mastery, observations)
            query_text = title or concept_id
            try:
                result = self._retrieval.retrieve(
                    RetrievalQuery(
                        text=query_text,
                        workspace_id=workspace_id,
                        profile=RetrievalProfile.STUDENT_DIGITAL_TWIN,
                        subject_code=subject_code,
                        seed_entity_id=concept_id,
                        limit=5,
                        expand_graph_hops=1,
                        include_diagnostics=True,
                    )
                )
            except Exception:
                logger.warning(
                    "curriculum evidence retrieval failed for concept=%s "
                    "workspace=%s; continuing without evidence",
                    concept_id,
                    workspace_id,
                    exc_info=True,
                )
                continue
            if not result.results:
                continue
            by_concept[concept_id] = result
            if result.retrieval_log_id:
                retrieval_log_ids.append(result.retrieval_log_id)
            for ranked in result.results:
                for item in ranked.evidence:
                    if item.evidence_id:
                        all_evidence_ids.append(item.evidence_id)
                all_evidence_ids.append(f"ranked:{ranked.entity_id}")

        return CurriculumEvidenceBundle(
            by_concept=by_concept,
            all_evidence_ids=tuple(dict.fromkeys(all_evidence_ids)),
            retrieval_log_ids=tuple(dict.fromkeys(retrieval_log_ids)),
        )


def _candidate_concepts(
    observations: tuple[Observation, ...],
    mastery: MasteryMap,
) -> list[str]:
    """Concepts referenced by observations or below mastery threshold."""
    ids: set[str] = set()
    for obs in observations:
        concept = (obs.curriculum_entity_id or "").strip()
        if concept:
            ids.add(concept)
    for record in mastery.records:
        if (
            record.mastery_score < _CANDIDATE_MASTERY_THRESHOLD
            and record.evidence_count > 0
        ):
            ids.add(record.concept_id)
    return sorted(ids)


def _concept_title(
    concept_id: str,
    mastery: MasteryMap,
    observations: tuple[Observation, ...],
) -> str:
    record = mastery.get(concept_id)
    if record is not None and record.concept_title:
        return record.concept_title
    for obs in observations:
        if obs.curriculum_entity_id == concept_id:
            title = str(obs.metadata.get("concept_title") or "")
            if title:
                return title
    return ""
