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
        return self._snapshot(row)

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
        return self._snapshot(row)

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
        return tuple(self._snapshot(r) for r in rows)

    def is_draft_reachable(self, version_id: int) -> bool:
        """Always False — drafts are not reachable through this authority."""
        _ = version_id
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
