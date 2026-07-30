"""Founder Calibration workflow (EI-002A).

Founder adjusts educational style dimensions; CalibrationRouter selects
the generation subset; GenerationOrchestrator.run_from regenerates and
re-certifies. Founder never edits curriculum nodes directly.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import uuid4

from app.application.curriculum_intelligence.generation_orchestrator import (
    GenerationOrchestrator,
    OrchestratorResult,
)
from app.application.curriculum_intelligence.ports.calibration_router_port import (
    CalibrationRouter,
    DefaultCalibrationRouter,
)
from app.application.curriculum_intelligence.ports.generation_store_port import (
    GenerationStorePort,
)
from app.application.curriculum_intelligence.workspace_generation_service import (
    WorkspaceGenerationService,
    build_default_orchestrator,
)
from app.application.curriculum_studio._registry import StudioRegistry
from app.domain.curriculum_intelligence.extracted_document import ExtractedDocument
from app.domain.curriculum_intelligence.generation import (
    CalibrationProfile,
    DifficultyBiasStyle,
    GranularityStyle,
    HierarchyStyle,
    TopicDensityStyle,
)
from app.domain.curriculum_intelligence.workspace_binding import (
    META_CALIBRATION_PROFILE_ID,
)


class CalibrationError(Exception):
    """Raised when calibration cannot proceed."""


@dataclass(frozen=True)
class CalibrationResult:
    """Outcome of a Founder calibration apply."""

    profile: CalibrationProfile
    generations_rerun: tuple[int, ...]
    orchestrator: OrchestratorResult
    intelligence_certified: bool


def _utc_now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


class FounderCalibrationService:
    """Apply Founder style calibration via CalibrationRouter + partial regen."""

    def __init__(
        self,
        store: GenerationStorePort,
        *,
        registry: StudioRegistry | None = None,
        orchestrator: GenerationOrchestrator | None = None,
        router: CalibrationRouter | None = None,
        workspace_service: WorkspaceGenerationService | None = None,
    ) -> None:
        self._store = store
        self._registry = registry
        self._orchestrator = orchestrator or build_default_orchestrator(store)
        self._router = router or DefaultCalibrationRouter()
        self._workspaces = workspace_service or WorkspaceGenerationService(
            store, registry=registry, orchestrator=self._orchestrator
        )

    def current_profile(self, workspace_id: str) -> CalibrationProfile | None:
        """Return the latest calibration profile bound to the workspace."""
        binding = self._workspaces.get_binding(workspace_id)
        if binding is None or not binding.calibration_profile_id:
            if self._registry is not None:
                workspace = self._registry.get_workspace(workspace_id)
                if workspace is not None:
                    meta = dict(workspace.metadata)
                    pid = meta.get(META_CALIBRATION_PROFILE_ID)
                    if pid:
                        return self._store.get_calibration_profile(pid)
            return None
        return self._store.get_calibration_profile(binding.calibration_profile_id)

    def apply(
        self,
        workspace_id: str,
        *,
        granularity: GranularityStyle | str,
        hierarchy: HierarchyStyle | str,
        topic_density: TopicDensityStyle | str,
        difficulty_bias: DifficultyBiasStyle | str,
        source_document_ids: tuple[int, ...] = (),
        source_documents: tuple[ExtractedDocument, ...] = (),
        subject_code: str = "CS1",
        version_label: str = "default",
        fixed_created_at_iso: str | None = None,
        profile_id: str | None = None,
    ) -> CalibrationResult:
        """Save calibration profile, partial-regen affected generations, re-certify."""
        binding = self._workspaces.ensure_binding(workspace_id)
        previous = self.current_profile(workspace_id)
        created_at = fixed_created_at_iso or _utc_now_iso()
        profile = CalibrationProfile(
            profile_id=profile_id or f"cal-{workspace_id}-{uuid4().hex[:10]}",
            workspace_id=workspace_id,
            granularity=_as_granularity(granularity),
            hierarchy=_as_hierarchy(hierarchy),
            topic_density=_as_density(topic_density),
            difficulty_bias=_as_difficulty(difficulty_bias),
            created_at_iso=created_at,
        )
        generations = self._router.select_generations(profile, previous=previous)
        if not generations:
            self._store.save_calibration_profile(profile)
            self._workspaces.sync_from_orchestrator(
                workspace_id,
                OrchestratorResult(
                    chain_id=binding.chain_id,
                    accepted_snapshots=(),
                    rejected_snapshots=(),
                    active_snapshot_id=binding.active_snapshot_id,
                    stopped_at_index=None,
                    rolled_back=False,
                ),
                profile=profile,
                calibration_applied=True,
            )
            return CalibrationResult(
                profile=profile,
                generations_rerun=(),
                orchestrator=OrchestratorResult(
                    chain_id=binding.chain_id,
                    accepted_snapshots=(),
                    rejected_snapshots=(),
                    active_snapshot_id=binding.active_snapshot_id,
                    stopped_at_index=None,
                    rolled_back=False,
                ),
                intelligence_certified=binding.is_certified,
            )

        start = generations[0]
        if self._store.get_active_snapshot(binding.chain_id) is None and start > 1:
            raise CalibrationError(
                "Calibration requires an existing Generation Chain. "
                "Run the EI pipeline before calibrating."
            )

        self._store.save_calibration_profile(profile)
        result = self._orchestrator.run_from(
            start,
            chain_id=binding.chain_id,
            workspace_id=workspace_id,
            source_document_ids=source_document_ids,
            through=7,
            profile=profile,
            source_documents=source_documents,
            subject_code=subject_code,
            version_label=version_label,
            fixed_created_at_iso=fixed_created_at_iso,
        )
        updated = self._workspaces.sync_from_orchestrator(
            workspace_id,
            result,
            profile=profile,
            calibration_applied=True,
        )
        return CalibrationResult(
            profile=profile,
            generations_rerun=generations,
            orchestrator=result,
            intelligence_certified=updated.is_certified,
        )


def _as_granularity(value: GranularityStyle | str) -> GranularityStyle:
    return value if isinstance(value, GranularityStyle) else GranularityStyle(value)


def _as_hierarchy(value: HierarchyStyle | str) -> HierarchyStyle:
    return value if isinstance(value, HierarchyStyle) else HierarchyStyle(value)


def _as_density(value: TopicDensityStyle | str) -> TopicDensityStyle:
    return value if isinstance(value, TopicDensityStyle) else TopicDensityStyle(value)


def _as_difficulty(value: DifficultyBiasStyle | str) -> DifficultyBiasStyle:
    return (
        value if isinstance(value, DifficultyBiasStyle) else DifficultyBiasStyle(value)
    )
