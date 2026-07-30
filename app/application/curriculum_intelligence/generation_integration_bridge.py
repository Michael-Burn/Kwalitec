"""Generation pipeline integration bridge (EI-002A).

After CIP reaches a terminal stage, invoke the Curriculum Intelligence
Engine and bind the workspace to the Generation Chain.
"""

from __future__ import annotations

import logging
from typing import Any

from app.application.curriculum_intelligence.in_memory_generation_store import (
    InMemoryGenerationStore,
)
from app.application.curriculum_intelligence.ports.generation_store_port import (
    GenerationStorePort,
)
from app.application.curriculum_intelligence.workspace_generation_service import (
    WorkspaceGenerationService,
)
from app.application.curriculum_studio._registry import StudioRegistry
from app.domain.curriculum_intelligence.extracted_document import ExtractedDocument
from app.domain.curriculum_intelligence.pipeline_stage import PipelineStage

logger = logging.getLogger(__name__)

# Stages after which the EI engine may run (CIP progress milestones).
_EI_TRIGGER_STAGES = frozenset(
    {
        PipelineStage.NORMALIZED,
        PipelineStage.GRAPH_BUILT,
        PipelineStage.READY_FOR_EMBEDDINGS,
    }
)


class GenerationIntegrationBridge:
    """Invoke GenerationOrchestrator after CIP milestones."""

    def __init__(
        self,
        store: GenerationStorePort | None = None,
        *,
        registry: StudioRegistry | None = None,
        workspace_service: WorkspaceGenerationService | None = None,
        enabled: bool = True,
    ) -> None:
        self._store = store
        self._registry = registry
        self._workspace_service = workspace_service
        self._enabled = enabled

    def _resolve_service(self) -> WorkspaceGenerationService:
        if self._workspace_service is not None:
            return self._workspace_service
        store = self._store
        if store is None:
            try:
                from app.infrastructure.adapters.curriculum_intelligence.generation_store import (  # noqa: E501
                    SqlAlchemyGenerationStore,
                )

                store = SqlAlchemyGenerationStore()
            except Exception:  # noqa: BLE001 — unit paths without DB
                store = InMemoryGenerationStore()
            self._store = store
        self._workspace_service = WorkspaceGenerationService(
            store, registry=self._registry
        )
        return self._workspace_service

    def maybe_run_after_cip(
        self,
        *,
        workspace_id: str,
        stage: PipelineStage | str,
        document_id: int | None = None,
        subject_code: str = "CS1",
        version_label: str = "default",
        source_documents: tuple[ExtractedDocument, ...] = (),
        force: bool = False,
    ) -> dict[str, Any] | None:
        """Run EI pipeline when CIP reaches a trigger stage.

        Returns a small status dict, or None when skipped.
        """
        if not self._enabled and not force:
            return None
        resolved = (
            stage if isinstance(stage, PipelineStage) else PipelineStage(str(stage))
        )
        if resolved not in _EI_TRIGGER_STAGES and not force:
            return None
        # Prefer terminal CIP stage for full engine runs to avoid duplicate work.
        if resolved is PipelineStage.NORMALIZED and not force:
            return {
                "skipped": True,
                "reason": "awaiting_graph_built",
                "workspace_id": workspace_id,
            }
        service = self._resolve_service()
        source_ids = (document_id,) if document_id is not None else ()
        try:
            result = service.run_initial_pipeline(
                workspace_id,
                source_document_ids=source_ids,
                source_documents=source_documents,
                subject_code=subject_code,
                version_label=version_label,
            )
            return {
                "skipped": False,
                "workspace_id": workspace_id,
                "chain_id": result.binding.chain_id,
                "intelligence_certified": result.intelligence_certified,
                "active_snapshot_id": result.binding.active_snapshot_id,
                "certified_snapshot_id": result.binding.certified_snapshot_id,
                "certification_status": (
                    result.binding.certification_status.value
                    if result.binding.certification_status
                    else None
                ),
            }
        except Exception:  # noqa: BLE001 — CIP must remain operational
            logger.exception(
                "EI generation bridge failed for workspace %s", workspace_id
            )
            return {
                "skipped": False,
                "error": True,
                "workspace_id": workspace_id,
            }
