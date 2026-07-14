"""KnowledgeQueryProvider — live Knowledge Engine bridge (FSI-001).

Wraps ``KnowledgeQueryService`` for Operational State aggregation.
"""

from __future__ import annotations

from pathlib import Path

from app.founder.knowledge_engine import KnowledgeQueryService
from app.founder.operational_state.dto.knowledge import KnowledgeSubsystemDTO


class KnowledgeQueryProvider:
    """Retrieve live Knowledge Engine summaries for operational-state aggregation.

    Does not analyse documents. Does not mutate the repository.
    """

    def __init__(
        self,
        *,
        query_service: KnowledgeQueryService | None = None,
        repo_root: Path | None = None,
    ) -> None:
        self._service = query_service or KnowledgeQueryService(repo_root=repo_root)

    def get(self) -> KnowledgeSubsystemDTO:
        """Return the Knowledge Engine DTO mapped from the public query API."""
        summary = self._service.get_summary()
        return KnowledgeSubsystemDTO(
            source_version=summary.source_version,
            engineering_standards=summary.engineering_standards,
            architecture_documents=summary.architecture_documents,
            research_documents=summary.research_documents,
            capability_documents=summary.capability_documents,
            indexed_artefacts=summary.indexed_artefacts,
            tests_pass=summary.tests_pass,
            validation_errors=summary.validation_errors,
        )
