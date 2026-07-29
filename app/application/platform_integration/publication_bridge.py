"""Bridge Studio Management publish → Foundation student-facing Ready.

Studio publication authority remains Curriculum Management. Foundation
materialises PublishedCurriculumPackage so Subject Catalogue can show Ready.
"""

from __future__ import annotations

import json
import logging

from app.application.curriculum_studio._registry import StudioRegistry
from app.application.curriculum_studio.exceptions import PublicationError
from app.application.curriculum_studio.structure_preparation_service import (
    StructurePreparationService,
)
from app.application.curriculum_studio_foundation.exceptions import (
    PublicationError as FoundationPublicationError,
)
from app.application.curriculum_studio_foundation.exceptions import (
    SubjectNotFound,
)
from app.application.curriculum_studio_foundation.service import (
    CurriculumStudioFoundationService,
)
from app.domain.curriculum_studio_foundation.lifecycle import (
    FoundationPublicationState,
)
from app.extensions import db
from app.models.curriculum_studio_foundation import StudioFoundationVersion

logger = logging.getLogger(__name__)


class PublicationBridgeService:
    """Promote a Studio-published subject into Foundation Ready packages."""

    def __init__(
        self,
        registry: StudioRegistry,
        *,
        foundation: CurriculumStudioFoundationService | None = None,
        structure: StructurePreparationService | None = None,
    ) -> None:
        self._registry = registry
        self._foundation = foundation or CurriculumStudioFoundationService()
        self._structure = structure or StructurePreparationService(registry)

    def publish_to_catalogue(
        self,
        workspace_id: str,
        *,
        actor_id: str = "",
    ) -> dict:
        """Approve + publish Foundation version for student Subject Catalogue.

        Raises:
            PublicationError: When Foundation cannot materialise Ready state.
        """
        workspace = self._registry.get_workspace(workspace_id)
        if workspace is None:
            raise PublicationError(f"Workspace not found: {workspace_id!r}")

        version = self._resolve_foundation_version(workspace)
        self._ensure_structure(workspace_id, version)

        state = (version.publication_state or "").strip().lower()
        if state != FoundationPublicationState.APPROVED.value:
            if state not in {
                FoundationPublicationState.READY_FOR_REVIEW.value,
                FoundationPublicationState.APPROVED.value,
                FoundationPublicationState.PROCESSING.value,
                FoundationPublicationState.DRAFT.value,
            }:
                try:
                    self._foundation.validate_curriculum(
                        version.id, actor_id=actor_id, require_pass=False
                    )
                except Exception as exc:  # noqa: BLE001
                    logger.warning(
                        "Foundation validate before review failed: %s", exc
                    )
                version = self._require_version(version.id)

            try:
                self._foundation.founder_review(
                    version.id,
                    actor_id=actor_id,
                    approve=True,
                    notes="Studio publication bridge",
                )
            except Exception as exc:
                raise PublicationError(
                    f"Foundation approval failed for {workspace.subject_code}: "
                    f"{exc}"
                ) from exc
            version = self._require_version(version.id)

        try:
            package = self._foundation.publish_curriculum(
                version.id,
                actor_id=actor_id,
                activate=True,
            )
        except FoundationPublicationError as exc:
            raise PublicationError(str(exc)) from exc
        except Exception as exc:
            raise PublicationError(
                f"Foundation publish failed for {workspace.subject_code}: {exc}"
            ) from exc

        return {
            "subject_code": package.subject_code,
            "version_label": package.version_label,
            "package_id": package.package_id,
            "published_at": package.published_at,
            "is_active": package.is_active,
        }

    def _resolve_foundation_version(self, workspace):
        code = workspace.subject_code.strip().upper()
        label = (workspace.version_label or "").strip()
        try:
            versions = self._foundation.list_versions(code)
        except SubjectNotFound as exc:
            raise PublicationError(
                f"No Foundation subject for {code}. Re-upload documents, "
                "then publish again."
            ) from exc
        if not versions:
            raise PublicationError(
                f"No Foundation version for {code}. Upload Official CMP and "
                "Official Syllabus, then publish again."
            )
        if label:
            for snap in versions:
                if snap.version_label == label:
                    return self._require_version(snap.version_id)
        newest = sorted(versions, key=lambda v: v.version_label, reverse=True)[0]
        return self._require_version(newest.version_id)

    def _ensure_structure(
        self, workspace_id: str, version: StudioFoundationVersion
    ) -> None:
        structure = {}
        if version.parsed_structure_json:
            try:
                structure = json.loads(version.parsed_structure_json) or {}
            except json.JSONDecodeError:
                structure = {}
        if int(structure.get("section_count") or 0) > 0 or int(
            structure.get("topic_count") or 0
        ) > 0:
            return

        built = self._structure.structure_dict(workspace_id)
        if int(built.get("section_count") or 0) <= 0 and int(
            built.get("topic_count") or 0
        ) <= 0:
            raise PublicationError(
                "Cannot publish Ready without extracted curriculum structure. "
                "Complete extraction and review before publishing."
            )
        version.parsed_structure_json = json.dumps(
            built, default=str, sort_keys=True
        )
        if version.publication_state in {
            FoundationPublicationState.DRAFT.value,
            FoundationPublicationState.PROCESSING.value,
            FoundationPublicationState.FAILED.value,
            "",
        }:
            version.publication_state = (
                FoundationPublicationState.READY_FOR_REVIEW.value
            )
        db.session.add(version)
        db.session.commit()

    def _require_version(self, version_id: int) -> StudioFoundationVersion:
        version = StudioFoundationVersion.query.filter_by(
            id=version_id
        ).one_or_none()
        if version is None:
            raise PublicationError(f"Foundation version not found: {version_id}")
        return version
