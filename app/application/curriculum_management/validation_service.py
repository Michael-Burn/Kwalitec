"""ValidationService — produce immutable readiness reports."""

from __future__ import annotations

from app.application.curriculum_management._catalogue import CurriculumCatalogue
from app.application.curriculum_management._snapshots import validation_snapshot
from app.application.curriculum_management.dto.validation_snapshot import (
    ValidationSnapshot,
)
from app.application.curriculum_management.exceptions import (
    ValidationFailed,
    VersionNotFound,
)
from app.application.curriculum_management.policies.publication_policy import (
    PublicationPolicy,
)
from app.application.curriculum_management.policies.validation_policy import (
    ValidationPolicy,
)
from app.domain.curriculum_management.publication_state import (
    PublicationState,
    PublicationTransitionEvent,
)
from app.domain.curriculum_management.subject_version import SubjectVersion
from app.domain.curriculum_management.validation_report import ValidationReport


class ValidationService:
    """Validate structural readiness of a subject version.

    Produces immutable ValidationReport instances. No PDF parsing.
    """

    def __init__(self, catalogue: CurriculumCatalogue) -> None:
        self._catalogue = catalogue

    def validate(
        self,
        version_id: str,
        *,
        advance_state: bool = True,
        report_id: str | None = None,
    ) -> ValidationSnapshot:
        """Run validation and append an immutable report.

        When ``advance_state`` is True and validation passes from UPLOADED,
        advances to VALIDATED. Blocking failures raise ValidationFailed
        after the report is stored.
        """
        version = self._require_version(version_id)
        PublicationPolicy.assert_not_archived(version)
        issues = ValidationPolicy.collect_issues(version)
        rid = report_id or self._catalogue.next_id("validation")
        report = ValidationReport.create(rid, version_id, issues=issues)
        version = version.with_validation_report(report)

        if advance_state and report.passed:
            publication = version.publication
            assert publication is not None
            if version.state is PublicationState.UPLOADED:
                publication = publication.transition(
                    PublicationTransitionEvent.MARK_VALIDATED,
                    reason="validation_passed",
                )
                version = version.with_publication(publication)
            # Assignments recorded before validation still advance the pipeline.
            if (
                version.state is PublicationState.VALIDATED
                and version.assignments
            ):
                publication = version.publication
                assert publication is not None
                publication = publication.transition(
                    PublicationTransitionEvent.MARK_BLUEPRINT_ASSIGNED,
                    reason="assignments_present",
                )
                version = version.with_publication(publication)

        self._catalogue.put_version(version)
        snapshot = validation_snapshot(report)
        if report.blocks_publication:
            raise ValidationFailed(
                f"Validation blocked publication for {version_id}: "
                f"{report.summary}"
            )
        return snapshot

    def latest(self, version_id: str) -> ValidationSnapshot | None:
        """Return the latest validation snapshot, or None."""
        version = self._require_version(version_id)
        report = version.latest_validation
        if report is None:
            return None
        return validation_snapshot(report)

    def _require_version(self, version_id: str) -> SubjectVersion:
        version = self._catalogue.get_version(version_id)
        if version is None:
            raise VersionNotFound(f"Version not found: {version_id!r}")
        return version
