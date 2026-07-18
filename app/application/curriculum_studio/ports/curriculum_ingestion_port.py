"""CurriculumIngestionPort — contract toward Curriculum Ingestion.

Studio never imports Curriculum Ingestion packages.
Adapters (future) implement this port.
Studio presents ingestion / validation results; it never parses PDFs.
"""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class CurriculumIngestionPort(Protocol):
    """Structural contract for Curriculum Ingestion collaboration.

    Studio may request ingestion jobs, normalised structures, and
    structural validation reports. It must never perform PDF parsing.
    """

    @property
    def component_id(self) -> str:
        """Stable component identity (e.g. ``curriculum_ingestion``)."""

    @property
    def component_version(self) -> str:
        """Version string for health / diagnostics."""

    def is_available(self) -> bool:
        """True when the Curriculum Ingestion port can accept work."""

    def start_ingestion(
        self,
        *,
        subject_code: str,
        sources: tuple[dict[str, Any], ...] | list[dict[str, Any]],
        job_id: str | None = None,
    ) -> dict[str, Any]:
        """Start an ingestion job from abstract source refs; return summary."""

    def get_ingestion_summary(self, job_id: str) -> dict[str, Any] | None:
        """Return an opaque ingestion job summary, or None when unknown."""

    def normalised_structure(
        self, job_id: str
    ) -> dict[str, Any] | None:
        """Return an opaque normalised curriculum structure, or None."""

    def get_validation_report(self, job_id: str) -> dict[str, Any] | None:
        """Return an opaque structural validation report, or None."""
