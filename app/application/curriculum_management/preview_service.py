"""PreviewService — produce immutable previews (never publishes)."""

from __future__ import annotations

from app.application.curriculum_management._catalogue import CurriculumCatalogue
from app.application.curriculum_management.dto.preview_snapshot import (
    PreviewSnapshot,
)
from app.application.curriculum_management.exceptions import (
    PreviewError,
    VersionNotFound,
)
from app.application.curriculum_management.policies.approval_policy import (
    ApprovalPolicy,
)
from app.application.curriculum_management.policies.publication_policy import (
    PublicationPolicy,
)
from app.domain.curriculum_management.publication_state import (
    PublicationState,
    PublicationTransitionEvent,
)
from app.domain.curriculum_management.subject_version import SubjectVersion


class PreviewService:
    """Produce immutable previews of a subject version.

    Preview only. Never publishes. May advance BLUEPRINT_ASSIGNED → PREVIEW_READY.
    """

    def __init__(self, catalogue: CurriculumCatalogue) -> None:
        self._catalogue = catalogue

    def preview(
        self,
        version_id: str,
        *,
        advance_state: bool = True,
        preview_id: str | None = None,
    ) -> PreviewSnapshot:
        """Build an immutable preview snapshot.

        Raises:
            PreviewError: When the version is not ready for preview.
        """
        version = self._require_version(version_id)
        PublicationPolicy.assert_not_archived(version)
        if version.state in {
            PublicationState.DRAFT,
            PublicationState.UPLOADED,
        }:
            raise PreviewError(
                f"Preview requires at least VALIDATED; got {version.state.value}"
            )
        if version.package is None or version.package.asset_count == 0:
            raise PreviewError("Preview requires a non-empty curriculum package")

        if (
            advance_state
            and version.state is PublicationState.BLUEPRINT_ASSIGNED
        ):
            publication = version.publication
            assert publication is not None
            publication = publication.transition(
                PublicationTransitionEvent.MARK_PREVIEW_READY,
                reason="preview_ready",
            )
            version = version.with_publication(publication)
            self._catalogue.put_version(version)

        pid = preview_id or self._catalogue.next_preview_id()
        package = version.package
        notes = version.release_notes
        latest = version.latest_validation
        return PreviewSnapshot(
            preview_id=pid,
            version_id=version.version_id,
            subject_id=version.subject_id,
            version_label=version.version_label,
            display_name=version.display_name,
            publication_state=version.state.value,
            asset_count=0 if package is None else package.asset_count,
            assignment_count=len(version.assignments),
            section_refs=version.section_refs,
            assignment_sections=tuple(a.section_ref for a in version.assignments),
            asset_labels=tuple(
                a.label for a in (package.assets if package else ())
            ),
            release_note_texts=() if notes is None else notes.texts(),
            validation_passed=None if latest is None else latest.passed,
            ready_for_approval=ApprovalPolicy.can_advance_to_approved(version),
        )

    def _require_version(self, version_id: str) -> SubjectVersion:
        version = self._catalogue.get_version(version_id)
        if version is None:
            raise VersionNotFound(f"Version not found: {version_id!r}")
        return version
