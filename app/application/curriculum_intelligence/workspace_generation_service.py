"""Workspace ↔ Generation Chain integration (EI-002A).

Binds Curriculum Studio workspaces to Generation Chains, runs the EI
pipeline, and syncs publication facts / metadata from orchestrator results.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import uuid4

from app.application.curriculum_intelligence.agents import (
    default_phase_d_runners,
)
from app.application.curriculum_intelligence.certification_engine import (
    DefaultCertificationEngine,
)
from app.application.curriculum_intelligence.generation_orchestrator import (
    GenerationOrchestrator,
    OrchestratorResult,
)
from app.application.curriculum_intelligence.ports.generation_store_port import (
    GenerationStorePort,
)
from app.application.curriculum_intelligence.regression_guard import RegressionGuard
from app.application.curriculum_intelligence.review_pack_emitter import (
    ReviewPackEmitter,
)
from app.application.curriculum_studio._registry import StudioRegistry
from app.application.curriculum_studio.fact_updates import copy_publication_facts
from app.domain.curriculum_intelligence.extracted_document import ExtractedDocument
from app.domain.curriculum_intelligence.generation import (
    CalibrationProfile,
    CertificationOutcome,
)
from app.domain.curriculum_intelligence.workspace_binding import (
    LEGACY_FALLBACK_VALUE,
    META_CALIBRATION_PROFILE_ID,
    META_CERTIFICATION_STATUS,
    META_CERTIFIED_SNAPSHOT_ID,
    META_CHAIN_ID,
    META_LEGACY_FALLBACK,
    META_REVIEW_PACK_REF,
    WorkspaceGenerationBinding,
    chain_id_for_workspace,
)

logger = logging.getLogger(__name__)


def _utc_now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


@dataclass(frozen=True)
class WorkspacePipelineResult:
    """Result of binding + running the EI pipeline for a workspace."""

    binding: WorkspaceGenerationBinding
    orchestrator: OrchestratorResult
    intelligence_certified: bool


def build_default_orchestrator(
    store: GenerationStorePort,
) -> GenerationOrchestrator:
    """Construct a production-shaped G1–G7 orchestrator."""
    return GenerationOrchestrator(
        store,
        RegressionGuard(),
        default_phase_d_runners(),
        certification_engine=DefaultCertificationEngine(),
        review_pack_emitter=ReviewPackEmitter(),
    )


class WorkspaceGenerationService:
    """Own the Studio workspace ↔ Generation Chain binding lifecycle."""

    def __init__(
        self,
        store: GenerationStorePort,
        *,
        registry: StudioRegistry | None = None,
        orchestrator: GenerationOrchestrator | None = None,
    ) -> None:
        self._store = store
        self._registry = registry
        self._orchestrator = orchestrator or build_default_orchestrator(store)

    def ensure_binding(self, workspace_id: str) -> WorkspaceGenerationBinding:
        """Ensure the workspace has exactly one active Generation Chain."""
        existing = self._store.get_chain_id_for_workspace(workspace_id)
        chain_id = existing or chain_id_for_workspace(workspace_id)
        self._store.ensure_chain(chain_id, workspace_id)
        active = self._store.get_active_snapshot(chain_id)
        certification = None
        certified_snapshot_id = None
        if active is not None:
            decision = self._store.get_certification(active.snapshot_id)
            if decision is None and active.generation_index == 7:
                decision = self._store.get_certification(active.snapshot_id)
            if decision is not None:
                certification = decision.outcome
                if decision.outcome is not CertificationOutcome.NOT_CERTIFIED:
                    certified_snapshot_id = decision.snapshot_id
            elif active.generation_index == 7:
                certified_snapshot_id = active.snapshot_id
        binding = WorkspaceGenerationBinding(
            workspace_id=workspace_id,
            chain_id=chain_id,
            active_snapshot_id=active.snapshot_id if active else None,
            certified_snapshot_id=certified_snapshot_id,
            certification_status=certification,
        )
        self._persist_binding_metadata(binding)
        return binding

    def get_binding(self, workspace_id: str) -> WorkspaceGenerationBinding | None:
        """Return binding from registry metadata or store, if present."""
        if self._registry is not None:
            workspace = self._registry.get_workspace(workspace_id)
            if workspace is not None:
                from_meta = WorkspaceGenerationBinding.from_metadata(
                    workspace_id, workspace.metadata
                )
                if from_meta is not None:
                    return from_meta
        chain_id = self._store.get_chain_id_for_workspace(workspace_id)
        if not chain_id:
            return None
        return self.ensure_binding(workspace_id)

    def run_initial_pipeline(
        self,
        workspace_id: str,
        *,
        source_document_ids: tuple[int, ...] = (),
        source_documents: tuple[ExtractedDocument, ...] = (),
        subject_code: str = "CS1",
        version_label: str = "default",
        profile: CalibrationProfile | None = None,
        fixed_created_at_iso: str | None = None,
    ) -> WorkspacePipelineResult:
        """Run Generations 1–7 for a workspace and sync Studio facts."""
        binding = self.ensure_binding(workspace_id)
        result = self._orchestrator.run_chain(
            chain_id=binding.chain_id,
            workspace_id=workspace_id,
            source_document_ids=source_document_ids,
            start_from=1,
            through=7,
            profile=profile,
            source_documents=source_documents,
            subject_code=subject_code,
            version_label=version_label,
            fixed_created_at_iso=fixed_created_at_iso,
        )
        updated = self.sync_from_orchestrator(workspace_id, result, profile=profile)
        certified = updated.is_certified
        return WorkspacePipelineResult(
            binding=updated,
            orchestrator=result,
            intelligence_certified=certified,
        )

    def sync_from_orchestrator(
        self,
        workspace_id: str,
        result: OrchestratorResult,
        *,
        profile: CalibrationProfile | None = None,
        calibration_applied: bool | None = None,
        review_pack_ref: str | None = None,
    ) -> WorkspaceGenerationBinding:
        """Update store binding + Studio facts/metadata from an orchestrator run."""
        self._store.bind_workspace_chain(workspace_id, result.chain_id)
        certified = result.certified_snapshot
        status = None
        certified_id = None
        if result.certification is not None:
            status = result.certification.outcome
            if status is not CertificationOutcome.NOT_CERTIFIED:
                certified_id = result.certification.snapshot_id
        elif certified is not None:
            status = certified.outcome
            if certified.is_preview_eligible:
                certified_id = certified.snapshot_id
        else:
            # Partial regen / profile-seed / early stop: preserve certification
            # already bound to the still-active snapshot (PL-001A C4).
            active_id = result.active_snapshot_id
            if active_id:
                prior_decision = self._store.get_certification(active_id)
                if prior_decision is not None:
                    status = prior_decision.outcome
                    if status is not CertificationOutcome.NOT_CERTIFIED:
                        certified_id = prior_decision.snapshot_id
            if status is None:
                existing = self.get_binding(workspace_id)
                if existing is not None and existing.certification_status is not None:
                    status = existing.certification_status
                    certified_id = existing.certified_snapshot_id
        pack_ref = review_pack_ref
        if pack_ref is None and result.review_pack is not None:
            pack_ref = f"review-pack:{result.chain_id}:{result.review_pack.pack_id}"
        if pack_ref is None:
            existing_binding = self.get_binding(workspace_id)
            if existing_binding is not None:
                pack_ref = existing_binding.review_pack_ref
        binding = WorkspaceGenerationBinding(
            workspace_id=workspace_id,
            chain_id=result.chain_id,
            active_snapshot_id=result.active_snapshot_id,
            certified_snapshot_id=certified_id,
            calibration_profile_id=profile.profile_id if profile else None,
            certification_status=status,
            review_pack_ref=pack_ref,
        )
        intelligence_ok = binding.is_certified
        applied = (
            bool(calibration_applied)
            if calibration_applied is not None
            else profile is not None
        )
        self._persist_binding_metadata(binding)
        self._sync_workspace_facts(
            workspace_id,
            intelligence_certified=intelligence_ok,
            calibration_applied=applied if profile is not None else None,
        )
        return binding

    def mark_legacy_fallback(self, workspace_id: str) -> WorkspaceGenerationBinding:
        """Mark a pre-EI workspace for legacy CIP publish during migration."""
        binding = WorkspaceGenerationBinding(
            workspace_id=workspace_id,
            chain_id=chain_id_for_workspace(workspace_id),
            legacy_fallback=True,
        )
        self._store.ensure_chain(binding.chain_id, workspace_id)
        self._persist_binding_metadata(binding)
        self._sync_workspace_facts(
            workspace_id,
            intelligence_certified=False,
            legacy_publish_fallback=True,
        )
        return binding

    def _persist_binding_metadata(self, binding: WorkspaceGenerationBinding) -> None:
        if self._registry is None:
            return
        workspace = self._registry.get_workspace(binding.workspace_id)
        if workspace is None:
            return
        meta = dict(workspace.metadata)
        meta[META_CHAIN_ID] = binding.chain_id
        if binding.active_snapshot_id:
            meta["ei_active_snapshot_id"] = binding.active_snapshot_id
        if binding.certified_snapshot_id:
            meta[META_CERTIFIED_SNAPSHOT_ID] = binding.certified_snapshot_id
        if binding.calibration_profile_id:
            meta[META_CALIBRATION_PROFILE_ID] = binding.calibration_profile_id
        if binding.certification_status is not None:
            meta[META_CERTIFICATION_STATUS] = binding.certification_status.value
        if binding.review_pack_ref:
            meta[META_REVIEW_PACK_REF] = binding.review_pack_ref
        if binding.legacy_fallback:
            meta[META_LEGACY_FALLBACK] = LEGACY_FALLBACK_VALUE
        from app.domain.curriculum_studio.curriculum_workspace import (
            CurriculumWorkspace,
        )

        updated = CurriculumWorkspace(
            workspace_id=workspace.workspace_id,
            subject_code=workspace.subject_code,
            subject_title=workspace.subject_title,
            version_label=workspace.version_label,
            version_id=workspace.version_id,
            status=workspace.status,
            workflow=workspace.workflow,
            facts=workspace.facts,
            section_ids=workspace.section_ids,
            topic_ids=workspace.topic_ids,
            objective_ids=workspace.objective_ids,
            prerequisite_edges=workspace.prerequisite_edges,
            metadata=tuple(sorted(meta.items())),
            estimated_workload_hours=workspace.estimated_workload_hours,
            notes=workspace.notes,
        )
        self._registry.put_workspace(updated)

    def _sync_workspace_facts(
        self,
        workspace_id: str,
        *,
        intelligence_certified: bool | None = None,
        calibration_applied: bool | None = None,
        legacy_publish_fallback: bool | None = None,
    ) -> None:
        if self._registry is None:
            return
        workspace = self._registry.get_workspace(workspace_id)
        if workspace is None:
            return
        facts = copy_publication_facts(
            workspace.facts,
            intelligence_certified=intelligence_certified,
            calibration_applied=calibration_applied,
            legacy_publish_fallback=legacy_publish_fallback,
        )
        self._registry.put_workspace(workspace.with_facts(facts))


def new_calibration_profile_id(workspace_id: str) -> str:
    """Stable-enough unique profile id for a calibration save."""
    return f"cal-{workspace_id}-{uuid4().hex[:10]}"
