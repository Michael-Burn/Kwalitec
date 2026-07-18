"""CurriculumStudioService — public facade for Founder curriculum operations.

Coordinates Founder use-cases through specialised Studio services.
Never imports Curriculum Management, Ingestion, or Education Platform packages.
Collaborates only via optional injected ports.
Publication / version / validation authority remain on those ports.
"""

from __future__ import annotations

from app.application.curriculum_studio._registry import StudioRegistry
from app.application.curriculum_studio.dashboard_service import DashboardService
from app.application.curriculum_studio.diagnostics import DiagnosticReport, Diagnostics
from app.application.curriculum_studio.diff_service import DiffService, DiffSnapshot
from app.application.curriculum_studio.dto.dashboard_snapshot import DashboardSnapshot
from app.application.curriculum_studio.dto.subject_snapshot import SubjectSnapshot
from app.application.curriculum_studio.dto.workspace_snapshot import WorkspaceSnapshot
from app.application.curriculum_studio.ports.curriculum_ingestion_port import (
    CurriculumIngestionPort,
)
from app.application.curriculum_studio.ports.curriculum_management_port import (
    CurriculumManagementPort,
)
from app.application.curriculum_studio.ports.education_platform_port import (
    EducationPlatformPort,
)
from app.application.curriculum_studio.preview_service import PreviewService
from app.application.curriculum_studio.publication_checklist_service import (
    PublicationChecklistService,
)
from app.application.curriculum_studio.publication_service import PublicationService
from app.application.curriculum_studio.subject_service import SubjectService
from app.application.curriculum_studio.validation_service import ValidationService
from app.application.curriculum_studio.version_history_service import (
    VersionHistoryService,
)
from app.application.curriculum_studio.workflow_service import WorkflowService
from app.application.curriculum_studio.workspace_service import WorkspaceService
from app.domain.curriculum_studio.curriculum_diff import NormalisedCurriculum
from app.domain.curriculum_studio.publication_checklist import (
    WorkspacePublicationFacts,
)


class CurriculumStudioService:
    """Founder-facing Curriculum Studio application facade."""

    def __init__(
        self,
        registry: StudioRegistry | None = None,
        *,
        curriculum_management: CurriculumManagementPort | None = None,
        curriculum_ingestion: CurriculumIngestionPort | None = None,
        education_platform: EducationPlatformPort | None = None,
    ) -> None:
        self.registry = registry or StudioRegistry()
        self._ports = {
            "curriculum_management": curriculum_management,
            "curriculum_ingestion": curriculum_ingestion,
            "education_platform": education_platform,
        }
        self.subjects = SubjectService(
            self.registry, management=curriculum_management
        )
        self.workspaces = WorkspaceService(
            self.registry,
            management=curriculum_management,
            ingestion=curriculum_ingestion,
        )
        self.workflow = WorkflowService(self.registry)
        self.validation = ValidationService(
            self.registry,
            management=curriculum_management,
            ingestion=curriculum_ingestion,
        )
        self.preview = PreviewService(
            self.registry,
            management=curriculum_management,
            education_platform=education_platform,
        )
        self.checklist = PublicationChecklistService(
            self.registry, management=curriculum_management
        )
        self.publication = PublicationService(
            self.registry, management=curriculum_management
        )
        self.versions = VersionHistoryService(
            self.registry, management=curriculum_management
        )
        self.diff = DiffService(ingestion=curriculum_ingestion)
        self.dashboard = DashboardService(
            self.registry, management=curriculum_management
        )
        self.diagnostics = Diagnostics(
            registry=self.registry,
            ports=self._ports,
        )

    @classmethod
    def create(
        cls,
        *,
        curriculum_management: CurriculumManagementPort | None = None,
        curriculum_ingestion: CurriculumIngestionPort | None = None,
        education_platform: EducationPlatformPort | None = None,
    ) -> CurriculumStudioService:
        """Factory with optional port injection."""
        return cls(
            curriculum_management=curriculum_management,
            curriculum_ingestion=curriculum_ingestion,
            education_platform=education_platform,
        )

    # --- Founder use-case convenience ---------------------------------------

    def create_subject(
        self,
        subject_code: str,
        *,
        title: str = "",
        metadata: dict | None = None,
    ) -> SubjectSnapshot:
        """Create Subject."""
        return self.subjects.create_subject(
            subject_code, title=title, metadata=metadata
        )

    def create_workspace(
        self,
        workspace_id: str,
        subject_code: str,
        *,
        subject_title: str = "",
        version_label: str = "",
        version_id: str | None = None,
        section_ids: list[str] | tuple[str, ...] | None = None,
        topic_ids: list[str] | tuple[str, ...] | None = None,
        objective_ids: list[str] | tuple[str, ...] | None = None,
        prerequisite_edges: (
            list[tuple[str, str]] | tuple[tuple[str, str], ...] | None
        ) = None,
        estimated_workload_hours: float | None = None,
        facts: WorkspacePublicationFacts | None = None,
        notes: str = "",
    ) -> WorkspaceSnapshot:
        """Create / Open Workspace (Studio-owned Founder session)."""
        return self.workspaces.open_workspace(
            workspace_id,
            subject_code,
            subject_title=subject_title,
            version_label=version_label,
            version_id=version_id,
            section_ids=section_ids,
            topic_ids=topic_ids,
            objective_ids=objective_ids,
            prerequisite_edges=prerequisite_edges,
            estimated_workload_hours=estimated_workload_hours,
            facts=facts,
            notes=notes,
        )

    def open_workspace(self, *args, **kwargs) -> WorkspaceSnapshot:
        """Alias for create_workspace / Open Workspace."""
        return self.workspaces.open_workspace(*args, **kwargs)

    def get_workspace(self, workspace_id: str) -> WorkspaceSnapshot:
        """Return a workspace snapshot."""
        return self.workspaces.get_workspace(workspace_id)

    def list_workspaces(self) -> tuple[WorkspaceSnapshot, ...]:
        """List all registered workspace snapshots."""
        return self.workspaces.list_workspaces()

    def update_structure(self, *args, **kwargs) -> WorkspaceSnapshot:
        """Update structural fields on a workspace."""
        return self.workspaces.update_structure(*args, **kwargs)

    def upload_sources(self, *args, **kwargs) -> WorkspaceSnapshot:
        """Upload Curriculum Sources."""
        return self.workspaces.upload_sources(*args, **kwargs)

    def compare_curricula(
        self,
        left: NormalisedCurriculum,
        right: NormalisedCurriculum,
        *,
        diff_id: str = "diff",
    ) -> DiffSnapshot:
        """Compare two normalised curricula."""
        return self.diff.compare(left, right, diff_id=diff_id)

    def founder_dashboard(self, *, activity_limit: int = 20) -> DashboardSnapshot:
        """Return the Founder dashboard projection."""
        return self.dashboard.dashboard(activity_limit=activity_limit)

    def health(self) -> dict:
        """Return a compact health dictionary."""
        report = self.diagnostics.report()
        return {
            "studio_status": (
                "ready" if report.missing_ports == () else "degraded"
            ),
            "studio_version": report.studio_version,
            "workspace_count": report.workspace_count,
            "version_count": report.version_count,
            "registered_ports": list(report.registered_ports),
            "missing_ports": list(report.missing_ports),
        }

    def diagnostic_report(self) -> DiagnosticReport:
        """Return a full diagnostic report."""
        return self.diagnostics.report()

    def port_available(self, name: str) -> bool:
        """True when a named port is injected and available."""
        port = self._ports.get(name)
        if port is None:
            return False
        return bool(port.is_available())
