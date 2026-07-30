"""EI-002A — Founder integration: workspace binding, calibration, certified publish."""

from __future__ import annotations

from app.application.curriculum_intelligence.agents import default_phase_d_runners
from app.application.curriculum_intelligence.calibration_service import (
    FounderCalibrationService,
)
from app.application.curriculum_intelligence.certification_engine import (
    DefaultCertificationEngine,
)
from app.application.curriculum_intelligence.founder_preview import (
    CertifiedSnapshotPreviewService,
)
from app.application.curriculum_intelligence.generation_orchestrator import (
    GenerationOrchestrator,
)
from app.application.curriculum_intelligence.in_memory_generation_store import (
    InMemoryGenerationStore,
)
from app.application.curriculum_intelligence.ports.calibration_router_port import (
    DefaultCalibrationRouter,
)
from app.application.curriculum_intelligence.regression_guard import RegressionGuard
from app.application.curriculum_intelligence.review_pack_emitter import (
    ReviewPackEmitter,
)
from app.application.curriculum_intelligence.workspace_generation_service import (
    WorkspaceGenerationService,
)
from app.application.curriculum_studio.exceptions import PublicationError
from app.application.curriculum_studio_foundation.authority import (
    PublishedCurriculumAuthority,
)
from app.domain.curriculum_intelligence.generation import (
    DifficultyBiasStyle,
    GenerationIndex,
    GranularityStyle,
    HierarchyStyle,
    TopicDensityStyle,
)
from app.domain.curriculum_intelligence.workspace_binding import (
    META_CHAIN_ID,
    WorkspaceGenerationBinding,
    chain_id_for_workspace,
)
from app.domain.curriculum_studio.publication_checklist import (
    ChecklistItemCode,
    PublicationChecklist,
)
from app.infrastructure.adapters.curriculum_intelligence.certified_snapshot_loader import (  # noqa: E501
    StoreCertifiedSnapshotLoader,
)
from tests.application.curriculum_intelligence.test_ei001d_educational_certification import (  # noqa: E501
    _syllabus_doc,
)
from tests.application.curriculum_studio.helpers import (
    make_ready_facts,
    seed_publishable,
    seed_workspace,
)


def _orchestrator(store: InMemoryGenerationStore) -> GenerationOrchestrator:
    return GenerationOrchestrator(
        store,
        RegressionGuard(),
        default_phase_d_runners(),
        certification_engine=DefaultCertificationEngine(),
        review_pack_emitter=ReviewPackEmitter(),
    )


def test_workspace_binds_to_exactly_one_generation_chain():
    store = InMemoryGenerationStore()
    studio = seed_workspace()
    service = WorkspaceGenerationService(
        store, registry=studio.registry, orchestrator=_orchestrator(store)
    )
    first = service.ensure_binding("ws-1")
    second = service.ensure_binding("ws-1")
    assert first.chain_id == second.chain_id == chain_id_for_workspace("ws-1")
    assert store.get_chain_id_for_workspace("ws-1") == first.chain_id
    workspace = studio.registry.get_workspace("ws-1")
    assert workspace is not None
    assert dict(workspace.metadata)[META_CHAIN_ID] == first.chain_id


def test_initial_pipeline_sets_intelligence_certified_and_review_pack():
    store = InMemoryGenerationStore()
    studio = seed_workspace()
    service = WorkspaceGenerationService(
        store, registry=studio.registry, orchestrator=_orchestrator(store)
    )
    result = service.run_initial_pipeline(
        "ws-1",
        source_document_ids=(101,),
        source_documents=(_syllabus_doc(),),
        fixed_created_at_iso="2026-07-30T12:00:00Z",
    )
    assert result.intelligence_certified is True
    assert result.binding.certified_snapshot_id
    assert result.binding.review_pack_ref
    assert result.orchestrator.review_pack is not None
    workspace = studio.registry.get_workspace("ws-1")
    assert workspace is not None
    assert workspace.facts.intelligence_certified is True
    checklist = PublicationChecklist.compute(workspace.facts)
    assert (
        checklist.item(ChecklistItemCode.INTELLIGENCE_CERTIFIED).satisfied is True
    )


def test_calibration_reruns_topic_density_from_gen4():
    store = InMemoryGenerationStore()
    studio = seed_workspace()
    orch = _orchestrator(store)
    workspace_service = WorkspaceGenerationService(
        store, registry=studio.registry, orchestrator=orch
    )
    workspace_service.run_initial_pipeline(
        "ws-1",
        source_document_ids=(101,),
        source_documents=(_syllabus_doc(),),
        fixed_created_at_iso="2026-07-30T12:00:00Z",
    )
    calibration = FounderCalibrationService(
        store,
        registry=studio.registry,
        orchestrator=orch,
        router=DefaultCalibrationRouter(),
        workspace_service=workspace_service,
    )
    # Seed an initial balanced profile so subsequent style deltas are partial.
    calibration.apply(
        "ws-1",
        granularity=GranularityStyle.BALANCED,
        hierarchy=HierarchyStyle.BALANCED,
        topic_density=TopicDensityStyle.BALANCED,
        difficulty_bias=DifficultyBiasStyle.BALANCED,
        source_document_ids=(101,),
        source_documents=(_syllabus_doc(),),
        fixed_created_at_iso="2026-07-30T12:02:00Z",
    )
    result = calibration.apply(
        "ws-1",
        granularity=GranularityStyle.BALANCED,
        hierarchy=HierarchyStyle.BALANCED,
        topic_density=TopicDensityStyle.CONSOLIDATED,
        difficulty_bias=DifficultyBiasStyle.BALANCED,
        source_document_ids=(101,),
        source_documents=(_syllabus_doc(),),
        fixed_created_at_iso="2026-07-30T12:05:00Z",
    )
    assert result.generations_rerun[0] == int(GenerationIndex.CONCEPT_FORMATION)
    assert int(GenerationIndex.CERTIFICATION) in result.generations_rerun
    assert result.intelligence_certified is True
    assert result.orchestrator.certification is not None
    workspace = studio.registry.get_workspace("ws-1")
    assert workspace is not None
    assert workspace.facts.calibration_applied is True
    assert workspace.facts.intelligence_certified is True
    assert calibration.current_profile("ws-1") is not None


def test_calibration_profile_seed_preserves_certification():
    """First apply of balanced defaults seeds profile without clearing cert."""
    store = InMemoryGenerationStore()
    studio = seed_workspace()
    orch = _orchestrator(store)
    workspace_service = WorkspaceGenerationService(
        store, registry=studio.registry, orchestrator=orch
    )
    workspace_service.run_initial_pipeline(
        "ws-1",
        source_document_ids=(101,),
        source_documents=(_syllabus_doc(),),
        fixed_created_at_iso="2026-07-30T12:00:00Z",
    )
    calibration = FounderCalibrationService(
        store,
        registry=studio.registry,
        orchestrator=orch,
        router=DefaultCalibrationRouter(),
        workspace_service=workspace_service,
    )
    result = calibration.apply(
        "ws-1",
        granularity=GranularityStyle.BALANCED,
        hierarchy=HierarchyStyle.BALANCED,
        topic_density=TopicDensityStyle.BALANCED,
        difficulty_bias=DifficultyBiasStyle.BALANCED,
        source_document_ids=(101,),
        source_documents=(_syllabus_doc(),),
        fixed_created_at_iso="2026-07-30T12:02:00Z",
    )
    assert result.generations_rerun == ()
    assert result.intelligence_certified is True
    workspace = studio.registry.get_workspace("ws-1")
    assert workspace is not None
    assert workspace.facts.intelligence_certified is True


def test_certified_preview_loader_projects_structure():
    store = InMemoryGenerationStore()
    studio = seed_workspace()
    service = WorkspaceGenerationService(
        store, registry=studio.registry, orchestrator=_orchestrator(store)
    )
    service.run_initial_pipeline(
        "ws-1",
        source_document_ids=(101,),
        source_documents=(_syllabus_doc(),),
        fixed_created_at_iso="2026-07-30T12:00:00Z",
    )
    preview = CertifiedSnapshotPreviewService(
        loader=StoreCertifiedSnapshotLoader(store)
    )
    certified = preview.get_certified_for_workspace("ws-1")
    assert certified is not None
    projected = preview.project(certified)
    assert projected.source == "certified_snapshot"
    assert projected.preview_eligible is True


def test_publication_requires_certified_or_legacy_fallback():
    studio = seed_publishable()
    studio.publication.update_facts("ws-1", intelligence_certified=False)
    try:
        studio.publication.publish("ws-1")
        raised = False
    except PublicationError as exc:
        raised = True
        assert "certified" in str(exc).lower()
    assert raised is True

    studio.publication.update_facts(
        "ws-1",
        intelligence_certified=False,
        legacy_publish_fallback=True,
    )
    pub = studio.publication.publish("ws-1")
    assert pub.lifecycle_status == "published"


def test_publication_succeeds_when_intelligence_certified():
    studio = seed_publishable()
    assert studio.registry.get_workspace("ws-1").facts.intelligence_certified is True
    pub = studio.publication.publish("ws-1")
    assert pub.lifecycle_status == "published"


def test_runtime_authority_accepts_certified_and_legacy_packages():
    authority = PublishedCurriculumAuthority()
    assert authority._runtime_accepts(  # noqa: SLF001
        {"certification": {"authority": "certified_snapshot", "status": "certified"}}
    )
    assert authority._runtime_accepts(  # noqa: SLF001
        {"certification": {"authority": "legacy_cip_fallback"}}
    )
    assert authority._runtime_accepts({"structure": {}})  # noqa: SLF001 — pre-EI
    assert (
        authority._runtime_accepts(  # noqa: SLF001
            {"certification": {"authority": "raw_parser_output"}}
        )
        is False
    )


def test_migration_marks_legacy_fallback_for_uncertified_workspace():
    store = InMemoryGenerationStore()
    studio = seed_workspace()
    service = WorkspaceGenerationService(
        store, registry=studio.registry, orchestrator=_orchestrator(store)
    )
    binding = service.mark_legacy_fallback("ws-1")
    assert binding.legacy_fallback is True
    workspace = studio.registry.get_workspace("ws-1")
    assert workspace is not None
    assert workspace.facts.legacy_publish_fallback is True
    checklist = PublicationChecklist.compute(workspace.facts)
    # Legacy counts toward intelligence checklist satisfaction for migration.
    assert (
        checklist.item(ChecklistItemCode.INTELLIGENCE_CERTIFIED).satisfied is True
    )


def test_ready_facts_include_intelligence_certified():
    facts = make_ready_facts()
    assert facts.intelligence_certified is True
    assert PublicationChecklist.compute(facts).ready_to_publish is True


def test_workspace_binding_round_trip_metadata():
    binding = WorkspaceGenerationBinding(
        workspace_id="ws-x",
        chain_id="ei-chain-ws-x",
        certified_snapshot_id="snap-1",
        calibration_profile_id="cal-1",
        review_pack_ref="review-pack:ei-chain-ws-x:pack-1",
    )
    restored = WorkspaceGenerationBinding.from_metadata(
        "ws-x", binding.as_metadata()
    )
    assert restored is not None
    assert restored.chain_id == binding.chain_id
    assert restored.certified_snapshot_id == "snap-1"
