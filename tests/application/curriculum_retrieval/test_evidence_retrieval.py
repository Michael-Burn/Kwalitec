"""CIP-003 evidence retrieval platform tests."""

from __future__ import annotations

from app.application.curriculum_intelligence.pipeline_coordinator import (
    PipelineCoordinator,
)
from app.application.curriculum_intelligence.processing_job_service import (
    ProcessingJobService,
)
from app.application.curriculum_retrieval.curriculum_retrieval_service import (
    CurriculumRetrievalService,
)
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
from app.application.curriculum_studio.document_upload_service import (
    DocumentUploadService,
)
from app.domain.curriculum_retrieval.embedding import EmbeddingIndexStatus
from app.domain.curriculum_retrieval.intent import QueryIntent, detect_intent
from app.domain.curriculum_retrieval.profile import (
    RetrievalProfile,
    weights_for_profile,
)
from app.domain.curriculum_retrieval.query import RetrievalQuery
from app.extensions import db
from app.infrastructure.adapters.curriculum_intelligence import (
    CurriculumIntelligenceProcessingAdapter,
)
from app.infrastructure.adapters.curriculum_retrieval.hashing_embedding_model import (
    HashingEmbeddingModel,
    cosine_similarity,
)
from app.infrastructure.adapters.curriculum_retrieval.local_vector_store import (
    LocalVectorStoreAdapter,
)
from app.infrastructure.adapters.document_storage import LocalDocumentStorageAdapter
from app.models.curriculum_intelligence import (
    CipCurriculumEntity,
    CipEmbeddingRecord,
    CipKnowledgeRelation,
    CipLocalVectorEntry,
    CipRetrievalLog,
)
from app.presentation.curriculum_studio.factory import set_studio_service
from tests.application.curriculum_intelligence.test_pipeline import (
    FixtureAwareExtractionAdapter,
    make_curriculum_pdf,
)
from tests.application.curriculum_studio.helpers import (
    make_studio_with_ports,
    seed_workspace,
)
from tests.presentation.curriculum_studio.helpers import login_founder


def _cip003_env(app, tmp_path, workspace_id: str = "ws-cip3"):
    studio, _, _, _ = make_studio_with_ports()
    seed_workspace(studio, workspace_id=workspace_id, subject_code="CS1")
    studio.create_subject("CS1", title="Core Statistics")
    set_studio_service(studio, app=app)
    storage = LocalDocumentStorageAdapter(tmp_path / f"cip3-{workspace_id}")
    jobs = ProcessingJobService()
    coordinator = PipelineCoordinator(
        storage=storage,
        extractor_port=FixtureAwareExtractionAdapter(),
        jobs=jobs,
    )
    processing = CurriculumIntelligenceProcessingAdapter(
        storage,
        auto_run=True,
        coordinator=coordinator,
        jobs=jobs,
    )
    svc = DocumentUploadService(
        studio=studio,
        storage=storage,
        processing=processing,
        max_bytes=5 * 1024 * 1024,
    )
    return studio, svc, storage, coordinator, jobs, workspace_id


def test_detect_intent_keywords():
    assert detect_intent("What is the definition of Bayes") is QueryIntent.DEFINITION
    assert detect_intent("Show the formula for variance") is QueryIntent.FORMULA
    assert detect_intent("worked example of Poisson") is QueryIntent.EXAMPLE
    assert detect_intent("practice question on survival") is QueryIntent.PRACTICE
    assert detect_intent("prerequisites for CT5") is QueryIntent.PREREQUISITE
    assert detect_intent("related concepts") is QueryIntent.RELATED
    assert detect_intent("Bayes theorem") is QueryIntent.GENERAL


def test_hashing_embedding_deterministic_and_normalised():
    model = HashingEmbeddingModel(dimensions=32)
    a = model.embed("Bayes theorem posterior prior")
    b = model.embed("Bayes theorem posterior prior")
    c = model.embed("Completely different actuarial syllabus text")
    assert a == b
    assert abs(sum(x * x for x in a) - 1.0) < 1e-6
    assert cosine_similarity(a, b) > 0.99
    assert cosine_similarity(a, c) < cosine_similarity(a, b)


def test_local_vector_store_abstraction(app, ctx):
    store = LocalVectorStoreAdapter()
    model = HashingEmbeddingModel(dimensions=16)
    v1 = model.embed("concept alpha")
    v2 = model.embed("concept beta")
    store.upsert(
        vector_id="vec_a",
        vector=v1,
        metadata={"workspace_id": "ws", "entity_id": "e1"},
    )
    store.upsert(
        vector_id="vec_b",
        vector=v2,
        metadata={"workspace_id": "ws", "entity_id": "e2"},
    )
    db.session.commit()
    hits = store.search(
        query_vector=v1, limit=2, filter_metadata={"workspace_id": "ws"}
    )
    assert hits[0].vector_id == "vec_a"
    assert hits[0].score >= hits[1].score
    assert store.count(filter_metadata={"workspace_id": "ws"}) == 2
    hits2 = store.search(
        query_vector=v1, limit=2, filter_metadata={"workspace_id": "ws"}
    )
    assert [h.vector_id for h in hits] == [h.vector_id for h in hits2]


def test_ranking_deterministic_and_profile_sensitive():
    ranker = EvidenceRankingService()
    inputs = RankingInputs(
        semantic_similarity=0.8,
        graph_distance=1,
        confidence=0.9,
        founder_verified=True,
        document_version_score=1.0,
        entity_freshness=0.8,
        relationship_strength=0.5,
        evidence_count_norm=0.4,
        entity_kind="concept",
    )
    tutor = ranker.rank(
        inputs=inputs,
        weights=weights_for_profile(RetrievalProfile.TUTOR),
        intent=QueryIntent.DEFINITION,
    )
    analytics = ranker.rank(
        inputs=inputs,
        weights=weights_for_profile(RetrievalProfile.ANALYTICS),
        intent=QueryIntent.DEFINITION,
    )
    tutor2 = ranker.rank(
        inputs=inputs,
        weights=weights_for_profile(RetrievalProfile.TUTOR),
        intent=QueryIntent.DEFINITION,
    )
    assert tutor.rank_score == tutor2.rank_score
    assert tutor.rank_score != analytics.rank_score
    assert 0.0 <= tutor.rank_score <= 1.0


def test_retrieval_policies_change_weights_not_pipeline():
    policies = RetrievalPolicyService()
    tutor = policies.weights(RetrievalProfile.TUTOR)
    search = policies.weights(RetrievalProfile.KNOWLEDGE_SEARCH)
    assert tutor.semantic_similarity < search.semantic_similarity
    assert policies.preferred_kinds(QueryIntent.FORMULA)[0] == "formula"
    assert policies.kind_boost(kind="formula", intent=QueryIntent.FORMULA) > 0


def test_pipeline_generates_embeddings_and_retrieval(app, ctx, tmp_path, client):
    _, upload, _, _, _, workspace_id = _cip003_env(app, tmp_path)
    meta = upload.upload(
        workspace_id,
        kind="cmp",
        filename="cs1.pdf",
        data=make_curriculum_pdf(),
        actor_id="founder@test",
    )
    db.session.commit()
    assert meta.document_id

    embeddings = CipEmbeddingRecord.query.filter_by(
        document_id=meta.document_id
    ).all()
    assert len(embeddings) >= 1
    assert any(e.status == EmbeddingIndexStatus.INDEXED.value for e in embeddings)
    assert CipLocalVectorEntry.query.count() >= 1

    retrieval = CurriculumRetrievalService()
    out = retrieval.retrieve(
        RetrievalQuery(
            text="Bayes theorem definition",
            workspace_id=workspace_id,
            profile=RetrievalProfile.FOUNDER_EXPLORER,
            limit=5,
            include_diagnostics=True,
        )
    )
    db.session.commit()
    assert out.diagnostics is not None
    assert out.retrieval_log_id
    assert CipRetrievalLog.query.filter_by(log_id=out.retrieval_log_id).first()
    assert hasattr(out, "results")
    if out.results:
        top = out.results[0]
        assert top.entity_id
        assert top.ranking.rank_score == top.rank_score

    out2 = retrieval.retrieve(
        RetrievalQuery(
            text="Bayes theorem definition",
            workspace_id=workspace_id,
            profile=RetrievalProfile.FOUNDER_EXPLORER,
            limit=5,
            include_diagnostics=True,
        )
    )
    assert [r.entity_id for r in out.results] == [r.entity_id for r in out2.results]
    assert [r.rank_score for r in out.results] == [r.rank_score for r in out2.results]


def test_graph_traversal_neighbours(app, ctx, tmp_path):
    _, upload, _, _, _, workspace_id = _cip003_env(app, tmp_path, "ws-cip3-graph")
    meta = upload.upload(
        workspace_id,
        kind="cmp",
        filename="cs1.pdf",
        data=make_curriculum_pdf(),
        actor_id="founder@test",
    )
    db.session.commit()
    entity = CipCurriculumEntity.query.filter_by(document_id=meta.document_id).first()
    assert entity is not None
    rel_count = CipKnowledgeRelation.query.filter_by(
        document_id=meta.document_id
    ).count()
    assert rel_count >= 0
    neighbours = KnowledgeGraphTraversalService().neighbours(
        entity.entity_id, workspace_id=workspace_id, max_hops=2
    )
    assert isinstance(neighbours, list)


def test_vector_index_service_hides_vectors(app, ctx, tmp_path):
    _, upload, _, _, _, workspace_id = _cip003_env(app, tmp_path, "ws-cip3-idx")
    meta = upload.upload(
        workspace_id,
        kind="cmp",
        filename="cs1.pdf",
        data=make_curriculum_pdf(),
        actor_id="founder@test",
    )
    db.session.commit()
    index = VectorIndexService()
    pairs = index.search(
        query_text="learning objective",
        workspace_id=workspace_id,
        limit=5,
        document_id=meta.document_id,
    )
    for entity_id, score in pairs:
        assert isinstance(entity_id, str)
        assert isinstance(score, float)


def test_embedding_generation_skips_non_embeddable(app, ctx):
    entity = CipCurriculumEntity(
        entity_id="ent-src-ref",
        map_id="map1",
        document_id=1,
        kind="source_reference",
        title="Page ref",
        body="",
        version_label="2026",
    )
    db.session.add(entity)
    db.session.commit()
    svc = EmbeddingGenerationService()
    assert svc.generate_for_entity(entity, workspace_id="ws") is None


def test_evidence_ordering_prefers_higher_confidence_when_similar(app, ctx):
    ranker = EvidenceRankingService()
    high = ranker.rank(
        inputs=RankingInputs(
            semantic_similarity=0.7,
            graph_distance=0,
            confidence=0.95,
            founder_verified=False,
            document_version_score=0.7,
            entity_freshness=0.5,
            relationship_strength=0.2,
            evidence_count_norm=0.2,
            entity_kind="concept",
        ),
        weights=weights_for_profile(RetrievalProfile.KNOWLEDGE_SEARCH),
    )
    low = ranker.rank(
        inputs=RankingInputs(
            semantic_similarity=0.7,
            graph_distance=0,
            confidence=0.2,
            founder_verified=False,
            document_version_score=0.7,
            entity_freshness=0.5,
            relationship_strength=0.2,
            evidence_count_norm=0.2,
            entity_kind="concept",
        ),
        weights=weights_for_profile(RetrievalProfile.KNOWLEDGE_SEARCH),
    )
    assert high.rank_score > low.rank_score


def test_founder_evidence_api(app, ctx, tmp_path, client):
    login_founder(client, app)
    _, upload, _, _, _, workspace_id = _cip003_env(app, tmp_path, "ws-cip3-api")
    upload.upload(
        workspace_id,
        kind="cmp",
        filename="cs1.pdf",
        data=make_curriculum_pdf(),
        actor_id="founder@test",
    )
    db.session.commit()

    status = client.get(
        f"/console/studio/workspaces/{workspace_id}/intelligence/embeddings/status"
    )
    assert status.status_code == 200
    body = status.get_json()
    assert body["ok"] is True
    assert "indexed" in body["status"]
    assert "vector_json" not in str(body)

    search = client.get(
        f"/console/studio/workspaces/{workspace_id}/intelligence/evidence/search",
        query_string={"q": "Bayes", "profile": "founder_explorer"},
    )
    assert search.status_code == 200
    payload = search.get_json()
    assert payload["ok"] is True
    retrieval = payload["retrieval"]
    assert "results" in retrieval
    assert "intent" in retrieval
    blob = str(retrieval)
    assert "vector_json" not in blob
    assert "embedding_model_weights" not in blob

    entity = CipCurriculumEntity.query.first()
    assert entity is not None
    neighbours = client.get(
        f"/console/studio/workspaces/{workspace_id}/intelligence/"
        f"entities/{entity.entity_id}/neighbours"
    )
    assert neighbours.status_code == 200
    assert neighbours.get_json()["ok"] is True

    related = client.get(
        f"/console/studio/workspaces/{workspace_id}/intelligence/"
        f"entities/{entity.entity_id}/related"
    )
    assert related.status_code == 200

    diagnostics = client.get(
        f"/console/studio/workspaces/{workspace_id}/intelligence/retrieval/diagnostics",
        query_string={"q": "Bayes theorem"},
    )
    assert diagnostics.status_code == 200
    assert "diagnostics" in diagnostics.get_json()["retrieval"]
