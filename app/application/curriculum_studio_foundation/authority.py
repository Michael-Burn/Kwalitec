"""PublishedCurriculumAuthority — student-safe published curriculum access.

Invariant: students never consume draft / processing / review curricula.
Only PublishedCurriculumPackage rows are exposed.
"""

from __future__ import annotations

import json
import logging
from typing import Any

from app.application.curriculum_studio_foundation.dto import PublishedPackageSnapshot
from app.models.curriculum_studio_foundation import PublishedCurriculumPackage

logger = logging.getLogger(__name__)


class PublishedCurriculumAuthority:
    """Read-only authority for published curriculum packages.

    Draft StudioFoundationVersion rows are intentionally unreachable here.
    """

    AUTHORITY_ID = "published_curriculum"
    AUTHORITY_VERSION = "1.0.0"

    def get_active(self, subject_code: str) -> PublishedPackageSnapshot | None:
        """Return the active published package for a subject, or None."""
        code = (subject_code or "").strip().upper()
        if not code:
            return None
        row = (
            PublishedCurriculumPackage.query.filter_by(
                subject_code=code, is_active=True
            )
            .order_by(PublishedCurriculumPackage.published_at.desc())
            .first()
        )
        if row is None:
            return None
        snap = self._snapshot(row)
        if not self._runtime_accepts(snap.package):
            logger.warning(
                "Active package for %s rejected: runtime requires certified "
                "curriculum (or legacy migration authority)",
                code,
            )
            return None
        return snap

    def get_by_version_label(
        self, subject_code: str, version_label: str
    ) -> PublishedPackageSnapshot | None:
        """Return a published package by subject + label (must be published)."""
        code = (subject_code or "").strip().upper()
        label = (version_label or "").strip()
        row = PublishedCurriculumPackage.query.filter_by(
            subject_code=code, version_label=label
        ).first()
        if row is None:
            return None
        snap = self._snapshot(row)
        if not self._runtime_accepts(snap.package):
            return None
        return snap

    def list_published(
        self, subject_code: str | None = None
    ) -> tuple[PublishedPackageSnapshot, ...]:
        """List published packages only (never drafts)."""
        q = PublishedCurriculumPackage.query
        if subject_code:
            q = q.filter_by(subject_code=(subject_code or "").strip().upper())
        rows = q.order_by(
            PublishedCurriculumPackage.subject_code,
            PublishedCurriculumPackage.version_label,
        ).all()
        return tuple(
            s
            for r in rows
            for s in (self._snapshot(r),)
            if self._runtime_accepts(s.package)
        )

    def is_draft_reachable(self, version_id: int) -> bool:
        """Always False — drafts are not reachable through this authority."""
        _ = version_id
        return False

    @staticmethod
    def _runtime_accepts(package: dict[str, Any]) -> bool:
        """Student Runtime accepts certified packages; legacy during migration.

        Packages without a certification block (pre-EI-002A) remain readable.
        Packages explicitly marked ``legacy_cip_fallback`` are allowed.
        Packages marked with a non-certified authority other than legacy are
        rejected. Raw parser outputs never appear in PublishedCurriculumPackage.
        """
        cert = package.get("certification")
        if not isinstance(cert, dict) or not cert:
            return True  # pre-EI packages
        authority = str(cert.get("authority") or "").strip().lower()
        if authority in {
            "",
            "certified_snapshot",
            "legacy_cip_fallback",
            "legacy_or_unspecified",
        }:
            return True
        status = str(cert.get("status") or "").strip().lower()
        if status in {"certified", "certified_with_warnings"}:
            return True
        if authority.startswith("legacy"):
            return True
        return False

    def _snapshot(self, row: PublishedCurriculumPackage) -> PublishedPackageSnapshot:
        package: dict[str, Any] = {}
        try:
            package = json.loads(row.package_json) if row.package_json else {}
        except json.JSONDecodeError:
            logger.warning(
                "Corrupt published package payload for %s %s",
                row.subject_code,
                row.version_label,
            )
        return PublishedPackageSnapshot(
            package_id=row.id,
            subject_code=row.subject_code,
            version_id=row.version_id,
            version_label=row.version_label,
            is_active=row.is_active,
            published_by=row.published_by,
            published_at=row.published_at.isoformat() if row.published_at else "",
            package=package,
        )
