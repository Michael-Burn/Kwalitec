"""VersionService — compatibility alias for VersionHistoryService.

Prefer ``version_history_service.VersionHistoryService``.
"""

from __future__ import annotations

from app.application.curriculum_studio.version_history_service import (
    VersionHistoryService,
    VersionService,
)

__all__ = ["VersionHistoryService", "VersionService"]
