"""CurriculumManagementPort — contract toward Curriculum Management.

Studio never imports Curriculum Management packages.
Adapters (future) implement this port.
Studio orchestrates Founder use-cases through these methods and
never becomes a second publication / version authority.
"""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class CurriculumManagementPort(Protocol):
    """Structural contract for Curriculum Management collaboration.

    Studio may request subject / version / publication / approval /
    preview / validation posture and drive Management mutations.
    It must never bypass Management publication policies.
    """

    @property
    def component_id(self) -> str:
        """Stable component identity (e.g. ``curriculum_management``)."""

    @property
    def component_version(self) -> str:
        """Version string for health / diagnostics."""

    def is_available(self) -> bool:
        """True when the Curriculum Management port can accept work."""

    # --- subjects -----------------------------------------------------------

    def create_subject(
        self,
        subject_code: str,
        *,
        title: str = "",
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Create an educational product subject; return opaque summary."""

    def get_subject_summary(self, subject_code: str) -> dict[str, Any] | None:
        """Return an opaque subject summary, or None when unknown."""

    def list_subjects(self) -> tuple[dict[str, Any], ...]:
        """Return opaque subject summaries."""

    # --- versions -----------------------------------------------------------

    def create_version(
        self,
        subject_code: str,
        version_label: str,
        *,
        version_id: str | None = None,
        parent_version_id: str | None = None,
        notes: str = "",
    ) -> dict[str, Any]:
        """Create a subject version; return opaque summary."""

    def get_version_summary(self, version_id: str) -> dict[str, Any] | None:
        """Return an opaque version summary, or None when unknown."""

    def list_versions(
        self, subject_code: str
    ) -> tuple[dict[str, Any], ...]:
        """Return opaque version summaries for a subject."""

    def archive_version(
        self,
        version_id: str,
        *,
        occurred_at: str = "",
    ) -> dict[str, Any]:
        """Archive a published version; return opaque summary."""

    def rollback_version(
        self,
        version_id: str,
        *,
        occurred_at: str = "",
    ) -> dict[str, Any]:
        """Roll back to a prior version when eligible; return opaque summary."""

    # --- assets / blueprints ------------------------------------------------

    def add_asset_ref(
        self,
        version_id: str,
        *,
        kind: str,
        reference: str,
        asset_id: str | None = None,
    ) -> dict[str, Any]:
        """Register a curriculum asset reference (never bytes)."""

    def list_assets(self, version_id: str) -> tuple[dict[str, Any], ...]:
        """List asset references for a version."""

    def assign_blueprint(
        self,
        version_id: str,
        *,
        section_id: str,
        blueprint_profile_id: str,
    ) -> dict[str, Any]:
        """Assign a blueprint profile to a section; return opaque summary."""

    # --- validation / preview / approval / publication ----------------------

    def validate_version(self, version_id: str) -> dict[str, Any]:
        """Run Management publication-gate validation; return opaque report."""

    def latest_validation(self, version_id: str) -> dict[str, Any] | None:
        """Return the latest Management validation report, or None."""

    def preview_version(self, version_id: str) -> dict[str, Any]:
        """Generate Founder publication-gate preview; return opaque payload."""

    def approve(
        self,
        version_id: str,
        *,
        actor_id: str | None = None,
        occurred_at: str = "",
        reason: str = "",
    ) -> dict[str, Any]:
        """Record Management approval; return opaque summary."""

    def reject(
        self,
        version_id: str,
        *,
        actor_id: str | None = None,
        occurred_at: str = "",
        reason: str = "",
    ) -> dict[str, Any]:
        """Record Management rejection; return opaque summary."""

    def publication_state(self, version_id: str) -> str | None:
        """Return the Management publication state token, or None."""

    def publish(
        self,
        version_id: str,
        *,
        actor_id: str | None = None,
        occurred_at: str = "",
    ) -> dict[str, Any]:
        """Publish via Management; return opaque publication summary."""

    def archive(
        self,
        version_id: str,
        *,
        actor_id: str | None = None,
        occurred_at: str = "",
    ) -> dict[str, Any]:
        """Archive a published release via Management."""
