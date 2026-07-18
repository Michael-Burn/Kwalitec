"""PublicationService — publication lifecycle transitions only."""

from __future__ import annotations

from app.application.curriculum_management._catalogue import CurriculumCatalogue
from app.application.curriculum_management._snapshots import publication_snapshot
from app.application.curriculum_management.dto.publication_snapshot import (
    PublicationSnapshot,
)
from app.application.curriculum_management.exceptions import (
    PublicationError,
    VersionNotFound,
)
from app.application.curriculum_management.policies.publication_policy import (
    PublicationPolicy,
)
from app.application.curriculum_management.policies.version_policy import (
    VersionPolicy,
)
from app.domain.curriculum_management.publication_state import (
    PublicationState,
    PublicationTransitionEvent,
)
from app.domain.curriculum_management.subject_version import SubjectVersion


class PublicationService:
    """Drive publication lifecycle for subject versions.

    Responsible for lifecycle only. No educational behaviour.
    """

    def __init__(self, catalogue: CurriculumCatalogue) -> None:
        self._catalogue = catalogue

    def get_publication(self, version_id: str) -> PublicationSnapshot:
        """Return the publication snapshot for a version."""
        version = self._require_version(version_id)
        assert version.publication is not None
        return publication_snapshot(version.publication)

    def publish(
        self,
        version_id: str,
        *,
        actor_id: str | None = None,
        occurred_at: str | None = None,
        activate: bool = True,
    ) -> PublicationSnapshot:
        """Publish an APPROVED version.

        When ``activate`` is True, sets the subject active_version_id.
        """
        version = self._require_version(version_id)
        PublicationPolicy.assert_can_publish(version)
        return self._transition(
            version,
            PublicationTransitionEvent.MARK_PUBLISHED,
            actor_id=actor_id,
            reason="published",
            occurred_at=occurred_at,
            activate=activate,
        )

    def archive(
        self,
        version_id: str,
        *,
        actor_id: str | None = None,
        occurred_at: str | None = None,
    ) -> PublicationSnapshot:
        """Archive a PUBLISHED version."""
        version = self._require_version(version_id)
        if version.state is not PublicationState.PUBLISHED:
            raise PublicationError(
                f"Archive requires PUBLISHED; got {version.state.value}"
            )
        return self._transition(
            version,
            PublicationTransitionEvent.MARK_ARCHIVED,
            actor_id=actor_id,
            reason="archived",
            occurred_at=occurred_at,
            activate=False,
        )

    def transition(
        self,
        version_id: str,
        event: PublicationTransitionEvent | str,
        *,
        actor_id: str | None = None,
        reason: str = "",
        occurred_at: str | None = None,
    ) -> PublicationSnapshot:
        """Apply an explicit lawful publication transition."""
        version = self._require_version(version_id)
        resolved = (
            event
            if isinstance(event, PublicationTransitionEvent)
            else PublicationTransitionEvent(str(event).strip().lower())
        )
        PublicationPolicy.assert_transition_allowed(version.state, resolved)
        return self._transition(
            version,
            resolved,
            actor_id=actor_id,
            reason=reason,
            occurred_at=occurred_at,
            activate=False,
        )

    def _transition(
        self,
        version: SubjectVersion,
        event: PublicationTransitionEvent,
        *,
        actor_id: str | None,
        reason: str,
        occurred_at: str | None,
        activate: bool,
    ) -> PublicationSnapshot:
        publication = version.publication
        if publication is None:
            raise PublicationError("Version has no publication carrier")
        try:
            publication = publication.transition(
                event,
                actor_id=actor_id,
                reason=reason,
                occurred_at=occurred_at,
            )
        except ValueError as exc:
            raise PublicationError(str(exc)) from exc
        version = version.with_publication(publication)
        self._catalogue.put_version(version)

        if activate and publication.state is PublicationState.PUBLISHED:
            subject = self._catalogue.get_subject(version.subject_id)
            if subject is not None:
                VersionPolicy.assert_can_activate(subject, version)
                subject = subject.with_active_version(version.version_id)
                self._catalogue.put_subject(subject)

        return publication_snapshot(publication)

    def _require_version(self, version_id: str) -> SubjectVersion:
        version = self._catalogue.get_version(version_id)
        if version is None:
            raise VersionNotFound(f"Version not found: {version_id!r}")
        return version
