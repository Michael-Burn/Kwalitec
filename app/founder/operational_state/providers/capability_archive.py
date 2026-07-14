"""CapabilityArchiveProvider — live Capability Archive bridge (FSI-001).

Wraps ``CapabilityArchiveQueryService`` for Operational State aggregation.
"""

from __future__ import annotations

from pathlib import Path

from app.founder.capability_archive import CapabilityArchiveQueryService
from app.founder.operational_state.dto.capability import CapabilitySubsystemDTO


class CapabilityArchiveProvider:
    """Retrieve live Capability Archive summaries for operational-state aggregation.

    Does not mutate archives. Does not evaluate capabilities.
    """

    def __init__(
        self,
        *,
        query_service: CapabilityArchiveQueryService | None = None,
        repo_root: Path | None = None,
    ) -> None:
        self._service = query_service or CapabilityArchiveQueryService(
            repo_root=repo_root
        )

    def get(self) -> CapabilitySubsystemDTO:
        """Return the Capability Archive DTO mapped from the public query API."""
        summary = self._service.get_summary()
        return CapabilitySubsystemDTO(
            source_version=summary.source_version,
            total_count=summary.total_count,
            completed_count=summary.completed_count,
            active_count=summary.active_count,
            archive_inconsistencies=summary.archive_inconsistencies,
            current_release=summary.current_release,
            recent_capability_ids=summary.recent_capability_ids,
        )
