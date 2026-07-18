"""AssetService — attach curriculum asset references to a version package."""

from __future__ import annotations

from app.application.curriculum_management._catalogue import CurriculumCatalogue
from app.application.curriculum_management._snapshots import version_snapshot
from app.application.curriculum_management.dto.version_snapshot import (
    VersionSnapshot,
)
from app.application.curriculum_management.exceptions import (
    AssetError,
    AssetNotFound,
    VersionNotFound,
)
from app.application.curriculum_management.policies.publication_policy import (
    PublicationPolicy,
)
from app.application.curriculum_management.policies.version_policy import (
    VersionPolicy,
)
from app.domain.curriculum_management.curriculum_asset import (
    AssetKind,
    CurriculumAsset,
)
from app.domain.curriculum_management.curriculum_package import CurriculumPackage
from app.domain.curriculum_management.publication_state import (
    PublicationState,
    PublicationTransitionEvent,
)
from app.domain.curriculum_management.subject_version import SubjectVersion


class AssetService:
    """Manage curriculum asset references (never PDF bytes).

    Uploading the first asset advances DRAFT → UPLOADED when needed.
    """

    def __init__(self, catalogue: CurriculumCatalogue) -> None:
        self._catalogue = catalogue

    def add_asset(
        self,
        version_id: str,
        kind: AssetKind | str,
        reference: str,
        label: str,
        *,
        asset_id: str | None = None,
        media_type: str | None = None,
        checksum: str | None = None,
        metadata: list[str] | tuple[str, ...] | None = None,
    ) -> VersionSnapshot:
        """Attach an asset reference to the version package.

        Raises:
            VersionNotFound / AssetError / PolicyViolation.
        """
        version = self._require_version(version_id)
        PublicationPolicy.assert_not_archived(version)
        VersionPolicy.assert_mutable(version)
        aid = asset_id or self._catalogue.next_id("asset")
        try:
            asset = CurriculumAsset.create(
                aid,
                kind,
                reference,
                label,
                media_type=media_type,
                checksum=checksum,
                metadata=metadata,
            )
        except ValueError as exc:
            raise AssetError(str(exc)) from exc

        package = version.package
        if package is None:
            package = CurriculumPackage.create(
                self._catalogue.next_id("package"),
                version_id,
            )
        try:
            package = package.with_asset(asset)
        except ValueError as exc:
            raise AssetError(str(exc)) from exc

        version = version.with_package(package)
        if version.state is PublicationState.DRAFT:
            publication = version.publication
            assert publication is not None
            publication = publication.transition(
                PublicationTransitionEvent.MARK_UPLOADED,
                reason="asset_uploaded",
            )
            version = version.with_publication(publication)
        self._catalogue.put_version(version)
        return version_snapshot(version)

    def remove_asset(self, version_id: str, asset_id: str) -> VersionSnapshot:
        """Remove an asset reference from the version package."""
        version = self._require_version(version_id)
        PublicationPolicy.assert_not_archived(version)
        VersionPolicy.assert_mutable(version)
        package = version.package
        if package is None:
            raise AssetNotFound(f"No package on version {version_id!r}")
        try:
            package = package.without_asset(asset_id)
        except ValueError as exc:
            raise AssetNotFound(str(exc)) from exc
        version = version.with_package(package)
        self._catalogue.put_version(version)
        return version_snapshot(version)

    def list_asset_ids(self, version_id: str) -> tuple[str, ...]:
        """Return asset identities for a version."""
        version = self._require_version(version_id)
        if version.package is None:
            return ()
        return tuple(a.asset_id for a in version.package.assets)

    def _require_version(self, version_id: str) -> SubjectVersion:
        version = self._catalogue.get_version(version_id)
        if version is None:
            raise VersionNotFound(f"Version not found: {version_id!r}")
        return version
