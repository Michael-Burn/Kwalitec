"""BlueprintAssignmentService — explicit section → profile assignments."""

from __future__ import annotations

from app.application.curriculum_management._catalogue import CurriculumCatalogue
from app.application.curriculum_management._snapshots import version_snapshot
from app.application.curriculum_management.dto.version_snapshot import (
    VersionSnapshot,
)
from app.application.curriculum_management.exceptions import (
    BlueprintAssignmentError,
    VersionNotFound,
)
from app.application.curriculum_management.policies.publication_policy import (
    PublicationPolicy,
)
from app.application.curriculum_management.policies.version_policy import (
    VersionPolicy,
)
from app.domain.curriculum_management.blueprint_assignment import (
    BlueprintAssignment,
)
from app.domain.curriculum_management.publication_state import (
    PublicationState,
    PublicationTransitionEvent,
)
from app.domain.curriculum_management.subject_version import SubjectVersion


class BlueprintAssignmentService:
    """Associate curriculum sections with Instructional Blueprint Profiles.

    Assignments are explicit. No automatic recommendation.
    """

    def __init__(self, catalogue: CurriculumCatalogue) -> None:
        self._catalogue = catalogue

    def assign(
        self,
        version_id: str,
        section_ref: str,
        blueprint_profile_id: str,
        *,
        assignment_id: str | None = None,
        notes: str = "",
        metadata: list[str] | tuple[str, ...] | None = None,
        advance_state: bool = True,
    ) -> VersionSnapshot:
        """Record an explicit blueprint assignment.

        When ``advance_state`` is True and the version is VALIDATED,
        advances to BLUEPRINT_ASSIGNED after the first assignment.
        """
        version = self._require_version(version_id)
        PublicationPolicy.assert_not_archived(version)
        VersionPolicy.assert_mutable(version)
        if version.state not in {
            PublicationState.VALIDATED,
            PublicationState.BLUEPRINT_ASSIGNED,
            PublicationState.PREVIEW_READY,
            PublicationState.UPLOADED,
            PublicationState.DRAFT,
        }:
            raise BlueprintAssignmentError(
                f"Cannot assign blueprints in state {version.state.value}"
            )
        aid = assignment_id or self._catalogue.next_id("assignment")
        try:
            assignment = BlueprintAssignment.create(
                aid,
                version_id,
                section_ref,
                blueprint_profile_id,
                notes=notes,
                metadata=metadata,
            )
        except ValueError as exc:
            raise BlueprintAssignmentError(str(exc)) from exc

        if any(a.section_ref == assignment.section_ref for a in version.assignments):
            raise BlueprintAssignmentError(
                f"Section already assigned: {assignment.section_ref!r}"
            )

        version = version.with_assignment(assignment)
        if (
            advance_state
            and version.state is PublicationState.VALIDATED
            and version.assignments
        ):
            publication = version.publication
            assert publication is not None
            publication = publication.transition(
                PublicationTransitionEvent.MARK_BLUEPRINT_ASSIGNED,
                reason="blueprint_assigned",
            )
            version = version.with_publication(publication)
        self._catalogue.put_version(version)
        return version_snapshot(version)

    def list_assignments(
        self,
        version_id: str,
    ) -> tuple[BlueprintAssignment, ...]:
        """Return assignments for a version."""
        return self._require_version(version_id).assignments

    def _require_version(self, version_id: str) -> SubjectVersion:
        version = self._catalogue.get_version(version_id)
        if version is None:
            raise VersionNotFound(f"Version not found: {version_id!r}")
        return version
