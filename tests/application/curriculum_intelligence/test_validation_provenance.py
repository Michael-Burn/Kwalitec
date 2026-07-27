"""CIP-002 validation, provenance, confidence, review, and audit tests."""

from __future__ import annotations

from app.application.curriculum_intelligence.audit_service import AuditService
from app.application.curriculum_intelligence.confidence_scoring_service import (
    ConfidenceScoringService,
)
from app.application.curriculum_intelligence.founder_review_service import (
    FounderReviewService,
)
from app.application.curriculum_intelligence.graph_validation_service import (
    GraphValidationService,
)
from app.application.curriculum_intelligence.pipeline_coordinator import (
    PipelineCoordinator,
)
from app.application.curriculum_intelligence.pipeline_metrics_service import (
    PipelineMetricsService,
)
from app.application.curriculum_intelligence.processing_job_service import (
    ProcessingJobService,
)
from app.application.curriculum_intelligence.provenance_service import ProvenanceService
from app.application.curriculum_studio.document_upload_service import (
    DocumentUploadService,
)
from app.domain.curriculum_intelligence.audit import AuditAction
from app.domain.curriculum_intelligence.confidence import confidence_band_from_score
from app.domain.curriculum_intelligence.curriculum_entity import (
    CurriculumEntityKind,
    CurriculumKnowledgeEntity,
)
from app.domain.curriculum_intelligence.knowledge_graph import (
    KnowledgeGraph,
    KnowledgeRelation,
    KnowledgeRelationType,
)
from app.domain.curriculum_intelligence.provenance import (
    PARSER_VERSION,
    ProvenanceSubjectKind,
)
from app.domain.curriculum_intelligence.review import ReviewStatus
from app.domain.curriculum_intelligence.validation_report import ValidationIssueKind
from app.extensions import db
from app.infrastructure.adapters.curriculum_intelligence import (
    CurriculumIntelligenceProcessingAdapter,
)
from app.infrastructure.adapters.document_storage import LocalDocumentStorageAdapter
from app.models.curriculum_intelligence import (
    CipAuditEvent,
    CipConfidenceRecord,
    CipCurriculumEntity,
    CipProvenanceRecord,
    CipQualityMetrics,
    CipReviewRecord,
    CipValidationReport,
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


def _cip002_env(app, tmp_path, workspace_id: str = "ws-cip2"):
    studio, _, _, _ = make_studio_with_ports()
    seed_workspace(studio, workspace_id=workspace_id, subject_code="CS1")
    studio.create_subject("CS1", title="Core Statistics")
    set_studio_service(studio, app=app)
    storage = LocalDocumentStorageAdapter(tmp_path / f"cip2-{workspace_id}")
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


def test_confidence_band_boundaries():
    assert confidence_band_from_score(0.9).value == "high"
    assert confidence_band_from_score(0.7).value == "medium"
    assert confidence_band_from_score(0.5).value == "low"
    assert confidence_band_from_score(0.2).value == "very_low"


def test_confidence_scoring_produces_reason_and_factors(app, ctx):
    entity = CurriculumKnowledgeEntity(
        entity_id="ent-test01",
        kind=CurriculumEntityKind.CONCEPT,
        title="Bayes Theorem",
        body="Posterior proportional to likelihood times prior.",
        parent_id=None,
        child_ids=(),
        source_document_id=1,
        source_pages=(214,),
        version_label="2026",
        confidence=0.98,
        needs_review=False,
    )
    record = ConfidenceScoringService().score_entity(entity, document_id=1)
    db.session.commit()
    assert 0.0 <= record.score <= 1.0
    assert record.reason
    assert record.factors
    assert record.subject_id == "ent-test01"
    stored = CipConfidenceRecord.query.filter_by(subject_id="ent-test01").one()
    assert stored.reason == record.reason
    assert list(stored.factors)


def test_provenance_chain_and_immutability(app, ctx):
    entity = CurriculumKnowledgeEntity(
        entity_id="ent-prov01",
        kind=CurriculumEntityKind.FORMULA,
        title="Bayes",
        body="P(A|B)=P(B|A)P(A)/P(B)",
        parent_id=None,
        child_ids=(),
        source_document_id=42,
        source_pages=(10, 11),
        version_label="2026.1",
        confidence=0.9,
        needs_review=False,
    )
    svc = ProvenanceService()
    first = svc.record_entity(
        entity,
        pipeline_job_id="job-1",
        extraction_id="ext-1",
        parse_id="parse-1",
        map_id="map-1",
        graph_id="graph-1",
        version_label="2026.1",
    )
    db.session.commit()
    assert first.parser_version == PARSER_VERSION
    assert first.source_pages == (10, 11)
    chain = svc.chain_for_entity("ent-prov01")
    assert [c["stage"] for c in chain] == [
        "document",
        "extraction",
        "parser",
        "curriculum_mapping",
        "knowledge_graph",
    ]
    second = svc.record_entity(
        entity,
        pipeline_job_id="job-2",
        extraction_id="ext-2",
        parse_id="parse-2",
        map_id="map-2",
        graph_id="graph-2",
    )
    db.session.commit()
    assert CipProvenanceRecord.query.filter_by(subject_id="ent-prov01").count() == 2
    assert first.provenance_id != second.provenance_id


def test_review_workflow_preserves_provenance(app, ctx, tmp_path):
    _, svc, _, _, _, workspace_id = _cip002_env(app, tmp_path, "ws-rev1")
    meta = svc.upload(
        workspace_id,
        kind="cmp",
        filename="cs1-cmp.pdf",
        data=make_curriculum_pdf(),
        actor_id="founder-1",
    )
    entity = CipCurriculumEntity.query.filter_by(document_id=meta.document_id).first()
    assert entity is not None
    prov_before = ProvenanceService().get_for_subject(
        subject_kind=ProvenanceSubjectKind.ENTITY.value, subject_id=entity.entity_id
    )
    assert prov_before is not None
    review = FounderReviewService()
    approved = review.approve(
        entity_id=entity.entity_id,
        actor_id="founder-1",
        workspace_id=workspace_id,
        reason="Looks correct",
    )
    db.session.commit()
    assert approved.review_status is ReviewStatus.APPROVED
    prov_after = ProvenanceService().get_for_subject(
        subject_kind=ProvenanceSubjectKind.ENTITY.value, subject_id=entity.entity_id
    )
    assert prov_after is not None
    assert prov_after.provenance_id == prov_before.provenance_id
    history = review.history_for_entity(entity.entity_id)
    assert len(history) == 1
    assert CipReviewRecord.query.filter_by(subject_id=entity.entity_id).count() == 1
    assert (
        CipAuditEvent.query.filter_by(
            subject_id=entity.entity_id, action=AuditAction.ENTITY_APPROVED.value
        ).count()
        >= 1
    )


def test_reject_and_remap_append_only(app, ctx, tmp_path):
    _, svc, _, _, _, workspace_id = _cip002_env(app, tmp_path, "ws-rev2")
    meta = svc.upload(
        workspace_id,
        kind="cmp",
        filename="cs2-cmp.pdf",
        data=make_curriculum_pdf(),
        actor_id="founder-1",
    )
    entity = CipCurriculumEntity.query.filter_by(document_id=meta.document_id).first()
    assert entity is not None
    review = FounderReviewService()
    review.reject(
        entity_id=entity.entity_id,
        actor_id="founder-1",
        workspace_id=workspace_id,
        reason="Wrong mapping",
    )
    review.remap(
        entity_id=entity.entity_id,
        actor_id="founder-1",
        workspace_id=workspace_id,
        remap_target_id="B3.2",
        reason="Should map to B3.2",
    )
    db.session.commit()
    assert CipReviewRecord.query.filter_by(subject_id=entity.entity_id).count() == 2
    assert (
        review.current_status(
            subject_kind=ProvenanceSubjectKind.ENTITY.value,
            subject_id=entity.entity_id,
        )
        is ReviewStatus.REMAPPED
    )


def test_graph_validation_rules(app, ctx):
    doc_id = 9001
    db.session.add_all(
        [
            CipCurriculumEntity(
                entity_id="ent-a",
                map_id="map-x",
                document_id=doc_id,
                kind=CurriculumEntityKind.TOPIC.value,
                title="Topic A",
                body="",
                version_label="2026",
                confidence=0.9,
            ),
            CipCurriculumEntity(
                entity_id="ent-b",
                map_id="map-x",
                document_id=doc_id,
                kind=CurriculumEntityKind.CONCEPT.value,
                title="Bayes",
                body="",
                version_label="2025",
                confidence=0.5,
                parent_entity_id=None,
            ),
            CipCurriculumEntity(
                entity_id="ent-c",
                map_id="map-x",
                document_id=doc_id,
                kind=CurriculumEntityKind.CONCEPT.value,
                title="Bayes",
                body="",
                version_label="2026",
                confidence=0.5,
                parent_entity_id="ent-a",
            ),
        ]
    )
    db.session.flush()
    graph = KnowledgeGraph(
        graph_id="graph-x",
        document_id=doc_id,
        map_id="map-x",
        entity_ids=("ent-a", "ent-b", "ent-c"),
        relations=(
            KnowledgeRelation(
                relation_id="rel-1",
                relation_type=KnowledgeRelationType.DEPENDS_ON,
                from_entity_id="ent-a",
                to_entity_id="ent-b",
                source_document_id=doc_id,
                confidence=0.5,
            ),
            KnowledgeRelation(
                relation_id="rel-2",
                relation_type=KnowledgeRelationType.DEPENDS_ON,
                from_entity_id="ent-b",
                to_entity_id="ent-a",
                source_document_id=doc_id,
                confidence=0.5,
            ),
            KnowledgeRelation(
                relation_id="rel-broken",
                relation_type=KnowledgeRelationType.SUPPORTS,
                from_entity_id="ent-a",
                to_entity_id="ent-missing",
                source_document_id=doc_id,
                confidence=0.5,
            ),
        ),
    )
    report = GraphValidationService().validate_document(
        document_id=doc_id, graph=graph, pipeline_job_id="job-x"
    )
    db.session.commit()
    kinds = {i.kind for i in report.issues}
    assert ValidationIssueKind.ORPHAN_CONCEPT in kinds
    assert ValidationIssueKind.DUPLICATE_CONCEPT in kinds
    assert ValidationIssueKind.MISSING_LEARNING_OBJECTIVE in kinds
    assert ValidationIssueKind.VERSION_INCONSISTENCY in kinds
    assert ValidationIssueKind.INVALID_GRAPH_EDGE in kinds
    assert ValidationIssueKind.CIRCULAR_PREREQUISITE in kinds
    assert ValidationIssueKind.BROKEN_DOCUMENT_REFERENCE in kinds
    assert report.passed is False
    assert CipValidationReport.query.filter_by(document_id=doc_id).count() == 1


def test_audit_logging_and_metrics_on_pipeline(app, ctx, tmp_path):
    _, svc, _, _, _, workspace_id = _cip002_env(app, tmp_path, "ws-met1")
    meta = svc.upload(
        workspace_id,
        kind="cmp",
        filename="cs3-cmp.pdf",
        data=make_curriculum_pdf(),
        actor_id="founder-1",
    )
    assert (
        CipProvenanceRecord.query.filter_by(
            source_document_id=meta.document_id
        ).count()
        >= 1
    )
    assert (
        CipConfidenceRecord.query.filter_by(document_id=meta.document_id).count() >= 1
    )
    assert (
        CipValidationReport.query.filter_by(document_id=meta.document_id).count() == 1
    )
    assert CipQualityMetrics.query.filter_by(document_id=meta.document_id).count() >= 1
    assert (
        CipAuditEvent.query.filter_by(
            workspace_id=workspace_id,
            action=AuditAction.PIPELINE_COMPLETED.value,
        ).count()
        >= 1
    )
    metrics = PipelineMetricsService().latest_for_document(meta.document_id)
    assert metrics is not None
    assert metrics.entity_count >= 1
    summary = PipelineMetricsService().workspace_summary(workspace_id)
    assert summary["document_count"] >= 1


def test_retry_regenerates_validation_without_losing_audit(app, ctx, tmp_path):
    from app.domain.curriculum_intelligence.pipeline_stage import PipelineStage

    _, svc, storage, coordinator, jobs, workspace_id = _cip002_env(
        app, tmp_path, "ws-retry1"
    )
    meta = svc.upload(
        workspace_id,
        kind="cmp",
        filename="cs4-cmp.pdf",
        data=make_curriculum_pdf(),
        actor_id="founder-1",
    )
    audits_before = CipAuditEvent.query.filter_by(workspace_id=workspace_id).count()
    reports_before = CipValidationReport.query.filter_by(
        document_id=meta.document_id
    ).count()
    job = jobs.get_latest_for_document(meta.document_id)
    assert job is not None
    jobs.mark_failed(job, stage=PipelineStage.VERIFIED, error="simulated failure")
    db.session.commit()
    storage.put(storage_key=job.storage_key, data=make_curriculum_pdf())
    coordinator.retry(job.job_id, from_scratch=True)
    assert (
        CipValidationReport.query.filter_by(document_id=meta.document_id).count()
        > reports_before
    )
    assert (
        CipAuditEvent.query.filter_by(workspace_id=workspace_id).count() > audits_before
    )


def test_review_queue_lists_items(app, ctx, tmp_path):
    _, svc, _, _, _, workspace_id = _cip002_env(app, tmp_path, "ws-queue1")
    svc.upload(
        workspace_id,
        kind="cmp",
        filename="cs5-cmp.pdf",
        data=make_curriculum_pdf(),
        actor_id="founder-1",
    )
    items = FounderReviewService().review_queue(workspace_id=workspace_id)
    assert isinstance(items, list)
    for item in items:
        assert "entity_id" in item
        assert "confidence" in item
        assert "title" in item


def test_intelligence_api_endpoints(app, client, ctx, tmp_path):
    _, svc, _, _, _, workspace_id = _cip002_env(app, tmp_path, "ws-api1")
    meta = svc.upload(
        workspace_id,
        kind="cmp",
        filename="cs6-cmp.pdf",
        data=make_curriculum_pdf(),
        actor_id="founder-1",
    )
    login_founder(client, app)
    base = f"/console/studio/workspaces/{workspace_id}/intelligence"
    assert client.get(f"{base}/overview").status_code == 200
    assert client.get(f"{base}/validation").status_code == 200
    assert client.get(f"{base}/review-queue").status_code == 200
    assert client.get(f"{base}/metrics").status_code == 200
    assert client.get(f"{base}/audit").status_code == 200
    assert client.get(f"{base}/knowledge-graph").status_code == 200
    entity = CipCurriculumEntity.query.filter_by(document_id=meta.document_id).first()
    assert entity is not None
    detail = client.get(f"{base}/entities/{entity.entity_id}")
    assert detail.status_code == 200
    assert detail.get_json()["ok"] is True
    prov = client.get(f"{base}/entities/{entity.entity_id}/provenance")
    assert prov.status_code == 200
    approve = client.post(
        f"{base}/entities/{entity.entity_id}/approve",
        json={"reason": "Verified"},
    )
    assert approve.status_code == 200
    assert approve.get_json()["status"] == "approved"


def test_full_pipeline_still_reaches_ready(app, ctx, tmp_path):
    """Regression: CIP-002 bridge must not break CIP-001 ready stage."""
    _, svc, _, _, jobs, workspace_id = _cip002_env(app, tmp_path, "ws-ready1")
    meta = svc.upload(
        workspace_id,
        kind="cmp",
        filename="cs7-cmp.pdf",
        data=make_curriculum_pdf(),
        actor_id="founder-1",
    )
    job = jobs.get_latest_for_document(meta.document_id)
    assert job is not None
    assert job.status == "ready_for_embeddings"


def test_audit_service_history(app, ctx):
    svc = AuditService()
    svc.record(
        action=AuditAction.ENTITY_CREATED,
        actor_id="system",
        subject_kind="entity",
        subject_id="ent-hist",
        message="created",
        workspace_id="ws-hist",
        document_id=1,
        pipeline_job_id="job-hist",
        document_version="2026",
    )
    db.session.commit()
    history = svc.history_for_subject(subject_kind="entity", subject_id="ent-hist")
    assert len(history) == 1
    assert history[0].action is AuditAction.ENTITY_CREATED
    workspace = svc.history_for_workspace(workspace_id="ws-hist")
    assert len(workspace) == 1
