"""Reconcile durable Studio workspace projections with Curriculum Management.

Curriculum Management is an in-memory bounded context. Studio workspace
projections are durable. After process restart, Management subject/version
objects may be absent while Studio still references them.

This service is the recovery path: restore Management subject + version
identities implied by durable workspace facts without inventing curriculum
content or bypassing workflow gates.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass

from app.application.curriculum_studio._ports import as_str, require_management
from app.application.curriculum_studio._registry import StudioRegistry
from app.application.curriculum_studio.exceptions import (
    SubjectAlreadyExists,
    SubjectNotFound,
    VersionError,
    WorkspaceNotFound,
)
from app.application.curriculum_studio.ports.curriculum_management_port import (
    CurriculumManagementPort,
)
from app.domain.curriculum_studio.curriculum_workspace import CurriculumWorkspace
from app.domain.curriculum_studio.publication_checklist import (
    WorkspacePublicationFacts,
)
from app.domain.curriculum_studio.version_history import (
    StudioVersionStatus,
    VersionRecord,
)

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class ReconciliationResult:
    """Outcome of one workspace ↔ Management reconciliation."""

    workspace_id: str
    subject_code: str
    version_id: str | None
    subject_restored: bool
    version_restored: bool
    mirror_restored: bool
    assets_restored: bool
    already_consistent: bool


class ManagementReconciliationService:
    """Restore Management subject/version from durable Studio projections."""

    def __init__(
        self,
        registry: StudioRegistry,
        *,
        management: CurriculumManagementPort | None = None,
    ) -> None:
        self._registry = registry
        self._management = management

    def reconcile_workspace(self, workspace_id: str) -> ReconciliationResult:
        """Ensure Management mirrors the durable workspace subject/version.

        Raises:
            WorkspaceNotFound: When the Studio workspace projection is missing.
            VersionError: When Management cannot recreate a required version.
        """
        workspace = self._registry.get_workspace(workspace_id)
        if workspace is None:
            raise WorkspaceNotFound(f"Workspace not found: {workspace_id!r}")

        mgmt = require_management(self._management, action="reconcile_management")
        code = workspace.subject_code.strip().upper()
        subject_restored = self._ensure_subject(mgmt, workspace)
        version_id, version_restored = self._ensure_version(mgmt, workspace)
        mirror_restored = self._ensure_version_mirror(workspace, version_id)
        if version_id and version_id != workspace.version_id:
            self._bind_version(workspace, version_id)
            workspace = self._registry.get_workspace(workspace_id) or workspace
        elif version_id and not workspace.facts.version_assigned:
            self._mark_version_assigned(workspace)

        assets_restored = False
        if version_id:
            assets_restored = self._ensure_package_assets(
                mgmt, workspace, version_id
            )

        already = not (
            subject_restored
            or version_restored
            or mirror_restored
            or assets_restored
        )
        if subject_restored or version_restored or assets_restored:
            logger.info(
                "Management reconciled workspace=%s subject=%s version=%s "
                "subject_restored=%s version_restored=%s assets_restored=%s",
                workspace_id,
                code,
                version_id,
                subject_restored,
                version_restored,
                assets_restored,
            )
        return ReconciliationResult(
            workspace_id=workspace_id,
            subject_code=code,
            version_id=version_id,
            subject_restored=subject_restored,
            version_restored=version_restored,
            mirror_restored=mirror_restored,
            assets_restored=assets_restored,
            already_consistent=already,
        )

    def reconcile_all(self) -> tuple[ReconciliationResult, ...]:
        """Reconcile every durable Studio workspace with Management."""
        results: list[ReconciliationResult] = []
        for workspace in self._registry.list_workspaces():
            try:
                results.append(self.reconcile_workspace(workspace.workspace_id))
            except Exception:  # noqa: BLE001 — boot must not die on one workspace
                logger.exception(
                    "Management reconciliation failed for %s",
                    workspace.workspace_id,
                )
        return tuple(results)

    def _ensure_subject(
        self,
        mgmt: CurriculumManagementPort,
        workspace: CurriculumWorkspace,
    ) -> bool:
        code = workspace.subject_code.strip().upper()
        if mgmt.get_subject_summary(code) is not None:
            return False
        title = (workspace.subject_title or code).strip() or code
        try:
            mgmt.create_subject(code, title=title)
            return True
        except Exception as exc:
            # Concurrent / duplicate create after restart race.
            if mgmt.get_subject_summary(code) is not None:
                return True
            raise VersionError(
                f"Cannot restore Management subject {code}: {exc}"
            ) from exc

    def _ensure_version(
        self,
        mgmt: CurriculumManagementPort,
        workspace: CurriculumWorkspace,
    ) -> tuple[str | None, bool]:
        """Return (version_id, restored)."""
        code = workspace.subject_code.strip().upper()
        label = (workspace.version_label or "").strip() or self._default_label()
        preferred_id = (workspace.version_id or "").strip() or None

        if preferred_id:
            existing = mgmt.get_version_summary(preferred_id)
            if existing is not None:
                return preferred_id, False

        # Prefer stable identity from durable projection when recreating.
        try:
            summary = mgmt.create_version(
                code,
                label,
                version_id=preferred_id,
                notes="management_reconciliation_after_restart",
            )
            vid = as_str(summary.get("version_id") or preferred_id)
            if not vid:
                raise VersionError("Management create_version returned no version_id")
            return vid, True
        except Exception as first_exc:
            # Label collision: bind the existing Management version for this label.
            try:
                for row in mgmt.list_versions(code):
                    if as_str(row.get("version_label")) == label:
                        vid = as_str(row.get("version_id"))
                        if vid:
                            return vid, preferred_id != vid
            except Exception:
                pass
            if preferred_id and mgmt.get_version_summary(preferred_id) is not None:
                return preferred_id, False
            raise VersionError(
                f"Cannot restore Management version for {code} ({label}): "
                f"{first_exc}"
            ) from first_exc

    def _ensure_version_mirror(
        self,
        workspace: CurriculumWorkspace,
        version_id: str | None,
    ) -> bool:
        if not version_id:
            return False
        if self._registry.get_version(version_id) is not None:
            return False
        label = (workspace.version_label or "").strip() or self._default_label()
        record = VersionRecord.create(
            version_id,
            workspace.workspace_id,
            workspace.subject_code.strip().upper(),
            label,
            status=StudioVersionStatus.DRAFT,
            notes="management_reconciliation_mirror",
        )
        self._registry.put_version(record)
        return True

    def _ensure_package_assets(
        self,
        mgmt: CurriculumManagementPort,
        workspace: CurriculumWorkspace,
        version_id: str,
    ) -> bool:
        """Re-attach CMP/syllabus asset refs from durable document metadata.

        Document uploads write durable Foundation rows and Management package
        assets. After Management restart the package is empty while documents
        remain — restore refs so ValidationPolicy does not emit empty_package.
        """
        from app.application.curriculum_studio.ports.document_metadata_port import (
            get_document_metadata_port,
        )

        try:
            from flask import has_app_context

            if not has_app_context():
                return False
        except Exception:
            return False

        try:
            metadata = get_document_metadata_port()
        except Exception:
            return False
        if metadata is None:
            return False

        summary = mgmt.get_version_summary(version_id) or {}
        existing_kinds = {
            str(k).strip().lower()
            for k in tuple(summary.get("asset_kinds") or ())
        }
        # Also inspect listed assets when asset_kinds is absent.
        try:
            for asset in mgmt.list_assets(version_id) or ():
                kind = str(asset.get("kind") or "").strip().lower()
                if kind:
                    existing_kinds.add(kind)
        except Exception:
            pass

        restored = False
        for kind in ("cmp", "syllabus"):
            if kind in existing_kinds:
                continue
            doc = metadata.find_active(workspace.workspace_id, kind)
            if doc is None or not (doc.reference or "").strip():
                continue
            try:
                mgmt.add_asset_ref(
                    version_id,
                    kind=kind,
                    reference=doc.reference.strip(),
                )
                restored = True
                existing_kinds.add(kind)
            except Exception as exc:
                logger.warning(
                    "Could not restore Management %s asset for %s: %s",
                    kind,
                    workspace.workspace_id,
                    exc,
                )
        return restored

    def _bind_version(
        self, workspace: CurriculumWorkspace, version_id: str
    ) -> None:
        label = (workspace.version_label or "").strip() or self._default_label()
        facts = WorkspacePublicationFacts.create(
            cmp_uploaded=workspace.facts.cmp_uploaded,
            official_syllabus_uploaded=workspace.facts.official_syllabus_uploaded,
            validation_passed=workspace.facts.validation_passed,
            blueprint_assigned=workspace.facts.blueprint_assigned,
            preview_built=workspace.facts.preview_built,
            preview_approved=workspace.facts.preview_approved,
            version_assigned=True,
            rollback_snapshot_created=workspace.facts.rollback_snapshot_created,
            intelligence_certified=workspace.facts.intelligence_certified,
            calibration_applied=workspace.facts.calibration_applied,
            legacy_publish_fallback=workspace.facts.legacy_publish_fallback,
        )
        updated = CurriculumWorkspace.create(
            workspace.workspace_id,
            workspace.subject_code,
            subject_title=workspace.subject_title,
            version_label=label,
            version_id=version_id,
            status=workspace.status,
            workflow=workspace.workflow,
            facts=facts,
            section_ids=workspace.section_ids,
            topic_ids=workspace.topic_ids,
            objective_ids=workspace.objective_ids,
            prerequisite_edges=workspace.prerequisite_edges,
            metadata=workspace.metadata,
            estimated_workload_hours=workspace.estimated_workload_hours,
            notes=workspace.notes,
        )
        self._registry.put_workspace(updated)

    def _mark_version_assigned(self, workspace: CurriculumWorkspace) -> None:
        facts = WorkspacePublicationFacts.create(
            cmp_uploaded=workspace.facts.cmp_uploaded,
            official_syllabus_uploaded=workspace.facts.official_syllabus_uploaded,
            validation_passed=workspace.facts.validation_passed,
            blueprint_assigned=workspace.facts.blueprint_assigned,
            preview_built=workspace.facts.preview_built,
            preview_approved=workspace.facts.preview_approved,
            version_assigned=True,
            rollback_snapshot_created=workspace.facts.rollback_snapshot_created,
            intelligence_certified=workspace.facts.intelligence_certified,
            calibration_applied=workspace.facts.calibration_applied,
            legacy_publish_fallback=workspace.facts.legacy_publish_fallback,
        )
        self._registry.put_workspace(workspace.with_facts(facts))

    @staticmethod
    def _default_label() -> str:
        from datetime import UTC, datetime

        return f"{datetime.now(UTC).year}.1"


# Re-export names used by upload recovery paths.
__all__ = [
    "ManagementReconciliationService",
    "ReconciliationResult",
    "SubjectAlreadyExists",
    "SubjectNotFound",
]
