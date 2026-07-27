"""CurriculumRetrievalService — canonical evidence retrieval façade (CIP-003).

Every future AI capability (Student Digital Twin, Mission Engine, Tutor,
Revision Planner, Analytics, APIs) must retrieve curriculum evidence through
this service. No consumer may query the vector database directly.
"""

from __future__ import annotations

import json
import uuid
from datetime import UTC, datetime

from app.application.curriculum_retrieval.embedding_generation_service import (
    EmbeddingGenerationService,
)
from app.application.curriculum_retrieval.evidence_ranking_service import (
    EvidenceRankingService,
    RankingInputs,
)
from app.application.curriculum_retrieval.knowledge_graph_traversal_service import (
    KnowledgeGraphTraversalService,
)
from app.application.curriculum_retrieval.retrieval_policy_service import (
    RetrievalPolicyService,
)
from app.application.curriculum_retrieval.vector_index_service import VectorIndexService
from app.domain.curriculum_intelligence.confidence import confidence_band_from_score
from app.domain.curriculum_intelligence.knowledge_graph import KnowledgeRelationType
from app.domain.curriculum_intelligence.review import VerificationStatus
from app.domain.curriculum_retrieval.intent import QueryIntent, detect_intent
from app.domain.curriculum_retrieval.profile import RetrievalProfile
from app.domain.curriculum_retrieval.query import RetrievalQuery
from app.domain.curriculum_retrieval.result import (
    EvidenceItem,
    RankedEvidence,
    RetrievalDiagnostics,
    RetrievalResult,
)
from app.extensions import db
from app.models.curriculum_intelligence import (
    CipConfidenceRecord,
    CipCurriculumEntity,
    CipProvenanceEvidence,
    CipProvenanceRecord,
    CipRetrievalLog,
    CipReviewRecord,
)
from app.models.curriculum_studio_foundation import StudioFoundationDocument


def _utc_now() -> datetime:
    return datetime.now(UTC).replace(tzinfo=None)


class CurriculumRetrievalService:
    """Orchestrate the CIP-003 retrieval pipeline.

    Query → Intent → Graph Expansion → Metadata Filter → Vector Search →
    Evidence Ranking → Confidence/Provenance Weighting → Structured Evidence
    """

    def __init__(
        self,
        *,
        vector_index: VectorIndexService | None = None,
        ranking: EvidenceRankingService | None = None,
        traversal: KnowledgeGraphTraversalService | None = None,
        policies: RetrievalPolicyService | None = None,
        embeddings: EmbeddingGenerationService | None = None,
    ) -> None:
        self._policies = policies or RetrievalPolicyService()
        self._traversal = traversal or KnowledgeGraphTraversalService()
        self._ranking = ranking or EvidenceRankingService(policies=self._policies)
        self._embeddings = embeddings or EmbeddingGenerationService()
        self._index = vector_index or VectorIndexService(embeddings=self._embeddings)

    def retrieve(self, query: RetrievalQuery) -> RetrievalResult:
        """Run the full retrieval pipeline and return structured evidence."""
        profile = self._policies.resolve(query.profile)
        intent = query.intent or detect_intent(query.text)
        weights = self._policies.weights(profile)
        notes: list[str] = []

        # 1) Vector search seeds
        vector_pairs = self._index.search(
            query_text=query.text,
            workspace_id=query.workspace_id,
            limit=max(query.limit * 4, 20),
            document_id=query.document_id,
        )
        similarity_by_id = {eid: score for eid, score in vector_pairs}
        seed_ids = list(similarity_by_id.keys())
        if query.seed_entity_id:
            seed_ids = [query.seed_entity_id, *seed_ids]

        # 2) Knowledge graph expansion
        hops = max(0, int(query.expand_graph_hops))
        distances = self._traversal.expand_entity_ids(
            seed_ids,
            workspace_id=query.workspace_id,
            max_hops=hops,
        )
        for seed in seed_ids:
            distances.setdefault(seed, 0)
        graph_expanded_count = len(distances)

        # 3) Metadata filtering
        candidates = self._load_candidates(
            entity_ids=list(distances.keys()) or seed_ids,
            workspace_id=query.workspace_id,
            document_id=query.document_id,
            subject_code=query.subject_code,
            version_label=query.version_label,
            entity_kinds=query.entity_kinds,
            require_verified=query.require_verified,
            min_confidence=query.min_confidence,
        )
        metadata_filtered_count = len(candidates)

        if not candidates and query.text.strip():
            # Fallback: lexical title/body scan within workspace when index empty.
            notes.append("vector_index_sparse_fallback_lexical")
            candidates = self._lexical_fallback(query)
            metadata_filtered_count = len(candidates)
            for entity in candidates:
                distances.setdefault(entity.entity_id, 0)

        # 4–7) Rank with confidence / provenance / verification weighting
        ranked: list[RankedEvidence] = []
        for entity in candidates:
            verified = self._is_verified(entity.entity_id)
            conf_row = self._latest_confidence(entity.entity_id)
            confidence = (
                float(conf_row.score)
                if conf_row is not None
                else float(entity.confidence or 0.0)
            )
            if query.min_confidence and confidence < query.min_confidence:
                continue
            if query.require_verified and not verified:
                continue

            provenance = self._latest_provenance(entity.entity_id)
            evidence_items = self._evidence_items(provenance)
            evidence_norm = min(1.0, len(evidence_items) / 5.0)
            rel_strength = self._traversal.mean_edge_strength(
                entity.entity_id, workspace_id=query.workspace_id
            )
            version_score = self._version_score(
                entity.version_label, query.version_label
            )
            freshness = self._freshness_score(entity)
            semantic = float(similarity_by_id.get(entity.entity_id, 0.0))
            # Lexical boost when vector miss but title matches
            if semantic <= 0 and query.text.strip():
                semantic = self._lexical_similarity(query.text, entity)

            dist = distances.get(entity.entity_id)

            breakdown = self._ranking.rank(
                inputs=RankingInputs(
                    semantic_similarity=semantic,
                    graph_distance=dist,
                    confidence=confidence,
                    founder_verified=verified,
                    document_version_score=version_score,
                    entity_freshness=freshness,
                    relationship_strength=rel_strength,
                    evidence_count_norm=evidence_norm,
                    entity_kind=entity.kind,
                ),
                weights=weights,
                intent=intent,
            )

            ranked.append(
                self._build_ranked(
                    entity=entity,
                    confidence=confidence,
                    verified=verified,
                    provenance=provenance,
                    evidence_items=evidence_items,
                    breakdown=breakdown,
                    graph_distance=dist,
                )
            )

        ranked.sort(key=lambda item: (-item.rank_score, item.entity_id))
        limited = ranked[: max(1, query.limit)]

        result = self._assemble_result(
            query=query,
            intent=intent,
            profile=profile,
            ranked=limited,
            diagnostics=(
                RetrievalDiagnostics(
                    intent=intent,
                    profile=profile,
                    candidate_count=len(ranked),
                    graph_expanded_count=graph_expanded_count,
                    metadata_filtered_count=metadata_filtered_count,
                    vector_hit_count=len(vector_pairs),
                    ranked_count=len(limited),
                    seed_entity_ids=tuple(seed_ids[:20]),
                    notes=tuple(notes),
                )
                if query.include_diagnostics
                else None
            ),
        )
        log_id = self._log_retrieval(query, intent, profile, result)
        return RetrievalResult(
            query_text=result.query_text,
            intent=result.intent,
            profile=result.profile,
            results=result.results,
            concept_ids=result.concept_ids,
            learning_objective_ids=result.learning_objective_ids,
            definition_ids=result.definition_ids,
            formula_ids=result.formula_ids,
            example_ids=result.example_ids,
            practice_question_ids=result.practice_question_ids,
            prerequisite_ids=result.prerequisite_ids,
            related_concept_ids=result.related_concept_ids,
            diagnostics=result.diagnostics,
            retrieval_log_id=log_id,
        )

    def search_concepts(
        self,
        *,
        text: str,
        workspace_id: str,
        limit: int = 10,
        profile: RetrievalProfile | str = RetrievalProfile.KNOWLEDGE_SEARCH,
    ) -> RetrievalResult:
        """Concept-focused search convenience."""
        return self.retrieve(
            RetrievalQuery(
                text=text,
                workspace_id=workspace_id,
                profile=self._policies.resolve(profile),
                entity_kinds=("concept",),
                limit=limit,
                include_diagnostics=True,
            )
        )

    def neighbours(
        self,
        entity_id: str,
        *,
        workspace_id: str,
        max_hops: int = 1,
    ) -> list[dict]:
        """Knowledge graph neighbours for Founder / Twin consumers."""
        return self._traversal.neighbours(
            entity_id, workspace_id=workspace_id, max_hops=max_hops
        )

    def related_concepts(
        self,
        entity_id: str,
        *,
        workspace_id: str,
        limit: int = 20,
    ) -> list[dict]:
        """Related concepts via graph edges."""
        return self._traversal.related_concepts(
            entity_id, workspace_id=workspace_id, limit=limit
        )

    def embedding_status(self, workspace_id: str) -> dict:
        """Embedding index status (educational metadata only)."""
        return self._embeddings.status_for_workspace(workspace_id)

    def diagnostics_for_query(self, query: RetrievalQuery) -> RetrievalResult:
        """Force diagnostics inclusion for Founder Evidence Explorer."""
        return self.retrieve(
            RetrievalQuery(
                text=query.text,
                workspace_id=query.workspace_id,
                profile=query.profile,
                intent=query.intent,
                document_id=query.document_id,
                subject_code=query.subject_code,
                version_label=query.version_label,
                entity_kinds=query.entity_kinds,
                require_verified=query.require_verified,
                min_confidence=query.min_confidence,
                limit=query.limit,
                expand_graph_hops=query.expand_graph_hops,
                seed_entity_id=query.seed_entity_id,
                include_diagnostics=True,
            )
        )

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------

    def _document_ids(
        self,
        workspace_id: str,
        *,
        document_id: int | None = None,
        subject_code: str = "",
    ) -> set[int]:
        q = StudioFoundationDocument.query.filter_by(workspace_id=workspace_id)
        if document_id is not None:
            q = q.filter_by(id=document_id)
        if subject_code:
            q = q.filter_by(subject_code=subject_code)
        return {int(d.id) for d in q.all()}

    def _load_candidates(
        self,
        *,
        entity_ids: list[str],
        workspace_id: str,
        document_id: int | None,
        subject_code: str,
        version_label: str,
        entity_kinds: tuple[str, ...],
        require_verified: bool,
        min_confidence: float,
    ) -> list[CipCurriculumEntity]:
        doc_ids = self._document_ids(
            workspace_id, document_id=document_id, subject_code=subject_code
        )
        if not doc_ids:
            return []
        q = CipCurriculumEntity.query.filter(
            CipCurriculumEntity.document_id.in_(doc_ids)
        )
        if entity_ids:
            q = q.filter(CipCurriculumEntity.entity_id.in_(entity_ids))
        if entity_kinds:
            q = q.filter(CipCurriculumEntity.kind.in_(list(entity_kinds)))
        if version_label:
            q = q.filter_by(version_label=version_label)
        entities = q.all()
        if require_verified:
            entities = [e for e in entities if self._is_verified(e.entity_id)]
        if min_confidence > 0:
            filtered: list[CipCurriculumEntity] = []
            for e in entities:
                conf = self._latest_confidence(e.entity_id)
                score = float(conf.score) if conf else float(e.confidence or 0.0)
                if score >= min_confidence:
                    filtered.append(e)
            entities = filtered
        return entities

    def _lexical_fallback(self, query: RetrievalQuery) -> list[CipCurriculumEntity]:
        doc_ids = self._document_ids(
            query.workspace_id,
            document_id=query.document_id,
            subject_code=query.subject_code,
        )
        if not doc_ids:
            return []
        needle = query.text.strip().lower()
        rows = CipCurriculumEntity.query.filter(
            CipCurriculumEntity.document_id.in_(doc_ids)
        ).all()
        if query.entity_kinds:
            allowed = set(query.entity_kinds)
            rows = [r for r in rows if r.kind in allowed]
        scored: list[tuple[float, CipCurriculumEntity]] = []
        for row in rows:
            hay = f"{row.title} {row.body}".lower()
            if needle and needle in hay:
                scored.append((1.0, row))
            elif any(tok and tok in hay for tok in needle.split()):
                scored.append((0.5, row))
        scored.sort(key=lambda item: (-item[0], item[1].entity_id))
        return [row for _, row in scored[: max(query.limit * 3, 15)]]

    def _lexical_similarity(self, text: str, entity: CipCurriculumEntity) -> float:
        tokens = {t for t in text.lower().split() if len(t) > 2}
        if not tokens:
            return 0.0
        hay = f"{entity.title} {entity.body}".lower()
        hits = sum(1 for t in tokens if t in hay)
        return min(1.0, hits / max(1, len(tokens)))

    def _is_verified(self, entity_id: str) -> bool:
        row = (
            CipReviewRecord.query.filter_by(
                subject_kind="entity", subject_id=entity_id
            )
            .order_by(CipReviewRecord.id.desc())
            .first()
        )
        if row is None:
            return False
        return row.verification_status == VerificationStatus.VERIFIED.value

    def _latest_confidence(self, entity_id: str) -> CipConfidenceRecord | None:
        return (
            CipConfidenceRecord.query.filter_by(
                subject_kind="entity", subject_id=entity_id
            )
            .order_by(CipConfidenceRecord.id.desc())
            .first()
        )

    def _latest_provenance(self, entity_id: str) -> CipProvenanceRecord | None:
        return (
            CipProvenanceRecord.query.filter_by(
                subject_kind="entity", subject_id=entity_id
            )
            .order_by(CipProvenanceRecord.id.desc())
            .first()
        )

    def _evidence_items(
        self, provenance: CipProvenanceRecord | None
    ) -> tuple[EvidenceItem, ...]:
        if provenance is None:
            return ()
        rows = CipProvenanceEvidence.query.filter_by(
            provenance_id=provenance.provenance_id
        ).all()
        items: list[EvidenceItem] = []
        for row in rows:
            items.append(
                EvidenceItem(
                    evidence_id=row.evidence_id,
                    role=row.evidence_role or "source",
                    excerpt=(row.excerpt or "")[:400],
                    page_number=row.page_number,
                    provenance_id=provenance.provenance_id,
                )
            )
        return tuple(items)

    def _version_score(self, entity_version: str, preferred: str) -> float:
        if not preferred:
            return 0.7
        if (entity_version or "") == preferred:
            return 1.0
        return 0.4

    def _freshness_score(self, entity: CipCurriculumEntity) -> float:
        created = getattr(entity, "created_at", None)
        if created is None:
            return 0.5
        age_days = max(0.0, (_utc_now() - created).total_seconds() / 86400.0)
        # Newer entities score higher; 180-day half-life style decay.
        return max(0.2, min(1.0, 1.0 / (1.0 + age_days / 180.0)))

    def _build_ranked(
        self,
        *,
        entity: CipCurriculumEntity,
        confidence: float,
        verified: bool,
        provenance: CipProvenanceRecord | None,
        evidence_items: tuple[EvidenceItem, ...],
        breakdown,
        graph_distance: int | None,
    ) -> RankedEvidence:
        ws = None
        doc = db.session.get(StudioFoundationDocument, entity.document_id)
        if doc is not None:
            ws = doc.workspace_id

        prereqs = self._traversal.typed_neighbour_ids(
            entity.entity_id,
            relation_types=KnowledgeGraphTraversalService.PREREQ_TYPES,
            workspace_id=ws,
        )
        related = self._traversal.typed_neighbour_ids(
            entity.entity_id,
            relation_types=KnowledgeGraphTraversalService.RELATED_TYPES,
            workspace_id=ws,
            kind_filter="concept",
        )
        formulae = self._traversal.typed_neighbour_ids(
            entity.entity_id,
            relation_types=frozenset({KnowledgeRelationType.FORMULA_FOR.value}),
            workspace_id=ws,
        )
        # Also include child formulae via parent hierarchy scan.
        if entity.kind == "concept":
            child_formulae = [
                c.entity_id
                for c in CipCurriculumEntity.query.filter_by(
                    parent_entity_id=entity.entity_id, kind="formula"
                ).all()
            ]
            formulae = tuple(dict.fromkeys([*formulae, *child_formulae]))

        examples = self._traversal.typed_neighbour_ids(
            entity.entity_id,
            relation_types=frozenset({KnowledgeRelationType.EXAMPLE_OF.value}),
            workspace_id=ws,
        )
        child_examples = [
            c.entity_id
            for c in CipCurriculumEntity.query.filter_by(
                parent_entity_id=entity.entity_id, kind="example"
            ).all()
        ]
        examples = tuple(dict.fromkeys([*examples, *child_examples]))

        practice = [
            c.entity_id
            for c in CipCurriculumEntity.query.filter_by(
                parent_entity_id=entity.entity_id, kind="practice_question"
            ).all()
        ]
        los = self._traversal.typed_neighbour_ids(
            entity.entity_id,
            relation_types=frozenset(
                {KnowledgeRelationType.LEARNING_OBJECTIVE_OF.value}
            ),
            workspace_id=ws,
        )

        pages: tuple[int, ...] = ()
        try:
            import json as _json

            pages = tuple(_json.loads(entity.source_pages_json or "[]"))
        except (TypeError, ValueError):
            pages = ()

        band = confidence_band_from_score(confidence)
        return RankedEvidence(
            entity_id=entity.entity_id,
            kind=entity.kind,
            title=entity.title or "",
            body=entity.body or "",
            document_id=int(entity.document_id),
            version_label=entity.version_label or "",
            confidence=confidence,
            confidence_band=band.value,
            verified=verified,
            provenance_id=provenance.provenance_id if provenance else None,
            rank_score=breakdown.rank_score,
            ranking=breakdown,
            evidence=evidence_items,
            prerequisites=prereqs,
            related_concepts=related,
            supporting_formulae=formulae,
            worked_examples=examples,
            practice_questions=tuple(practice),
            learning_objectives=los,
            graph_distance=graph_distance,
            source_pages=pages if isinstance(pages, tuple) else tuple(pages),
        )

    def _assemble_result(
        self,
        *,
        query: RetrievalQuery,
        intent: QueryIntent,
        profile: RetrievalProfile,
        ranked: list[RankedEvidence],
        diagnostics: RetrievalDiagnostics | None,
    ) -> RetrievalResult:
        concepts = tuple(r.entity_id for r in ranked if r.kind == "concept")
        definitions = concepts  # concept bodies are definitional evidence
        los = tuple(r.entity_id for r in ranked if r.kind == "learning_objective")
        formulae = tuple(r.entity_id for r in ranked if r.kind == "formula")
        examples = tuple(r.entity_id for r in ranked if r.kind == "example")
        practice = tuple(r.entity_id for r in ranked if r.kind == "practice_question")
        prereq: list[str] = []
        related: list[str] = []
        for r in ranked:
            prereq.extend(r.prerequisites)
            related.extend(r.related_concepts)
        return RetrievalResult(
            query_text=query.text,
            intent=intent,
            profile=profile,
            results=tuple(ranked),
            concept_ids=concepts,
            learning_objective_ids=los,
            definition_ids=definitions,
            formula_ids=formulae,
            example_ids=examples,
            practice_question_ids=practice,
            prerequisite_ids=tuple(dict.fromkeys(prereq)),
            related_concept_ids=tuple(dict.fromkeys(related)),
            diagnostics=diagnostics,
        )

    def _log_retrieval(
        self,
        query: RetrievalQuery,
        intent: QueryIntent,
        profile: RetrievalProfile,
        result: RetrievalResult,
    ) -> str:
        log_id = f"rlog_{uuid.uuid4().hex[:20]}"
        top_ids = ",".join(r.entity_id for r in result.results[:10])
        diagnostics = {}
        if result.diagnostics is not None:
            d = result.diagnostics
            diagnostics = {
                "intent": d.intent.value,
                "profile": d.profile.value,
                "candidate_count": d.candidate_count,
                "graph_expanded_count": d.graph_expanded_count,
                "metadata_filtered_count": d.metadata_filtered_count,
                "vector_hit_count": d.vector_hit_count,
                "ranked_count": d.ranked_count,
                "seed_entity_ids": list(d.seed_entity_ids),
                "notes": list(d.notes),
            }
        row = CipRetrievalLog(
            log_id=log_id,
            workspace_id=query.workspace_id,
            profile=profile.value,
            intent=intent.value,
            query_text=query.text[:2000],
            document_id=query.document_id,
            result_count=len(result.results),
            top_entity_ids_csv=top_ids,
            diagnostics_json=json.dumps(diagnostics, separators=(",", ":")),
        )
        db.session.add(row)
        db.session.flush()
        return log_id
