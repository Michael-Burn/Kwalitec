"""KnowledgeQueryService — public query API for the Knowledge Engine (FOS-001).

This service is the only public API exposed by the Knowledge Engine.
Consumers must not access the repository scanner or filesystem paths.
"""

from __future__ import annotations

from pathlib import Path

from app.founder.knowledge_engine.config import (
    COLLECTION_ADR,
    COLLECTION_ARCHITECTURE,
    COLLECTION_ENGINEERING_STANDARDS,
    COLLECTION_FOUNDER_CAPABILITY,
    COLLECTION_RESEARCH,
    KnowledgeEngineConfig,
    default_config,
    discover_repo_root,
)
from app.founder.knowledge_engine.dto.artefact import KnowledgeArtefactDTO
from app.founder.knowledge_engine.dto.summary import KnowledgeIndexSummaryDTO
from app.founder.knowledge_engine.dto.validation import (
    KnowledgeValidationIssue,
    KnowledgeValidationReport,
)
from app.founder.knowledge_engine.repository import KnowledgeRepositoryScanner
from app.founder.knowledge_engine.validators import KnowledgeIndexValidator


class KnowledgeQueryService:
    """Query indexed knowledge artefacts from a repository-backed index.

    Integration only — no AI, no persistence, no analysis beyond counting
    and deterministic classification.
    """

    def __init__(
        self,
        *,
        repo_root: Path | None = None,
        config: KnowledgeEngineConfig | None = None,
        validator: KnowledgeIndexValidator | None = None,
    ) -> None:
        self._root = (repo_root or discover_repo_root()).resolve()
        self._config = config or default_config()
        self._validator = validator or KnowledgeIndexValidator()
        self._scanner = KnowledgeRepositoryScanner(
            repo_root=self._root,
            config=self._config,
        )
        self._artefacts: tuple[KnowledgeArtefactDTO, ...] | None = None
        self._report: KnowledgeValidationReport | None = None
        self._missing_roots: tuple[str, ...] = ()

    def refresh(self) -> None:
        """Re-scan the repository and replace the in-memory index."""
        scan = self._scanner.scan()
        self._artefacts = scan.artefacts
        self._missing_roots = scan.missing_roots
        self._report = self._validator.validate(scan)

    def list_artefacts(
        self, *, collection: str | None = None
    ) -> tuple[KnowledgeArtefactDTO, ...]:
        """Return indexed artefacts, optionally filtered by collection.

        Args:
            collection: Logical collection name, or None for all.

        Returns:
            Immutable tuple of ``KnowledgeArtefactDTO``.
        """
        artefacts = self._ensure_index()
        if collection is None:
            return artefacts
        return tuple(a for a in artefacts if a.collection == collection)

    def get_summary(self) -> KnowledgeIndexSummaryDTO:
        """Return aggregated Knowledge Engine counts for consumers.

        Returns:
            Immutable ``KnowledgeIndexSummaryDTO``.
        """
        artefacts = self._ensure_index()
        report = self._report or KnowledgeValidationReport(issues=())
        engineering_standards = _count(artefacts, COLLECTION_ENGINEERING_STANDARDS)
        architecture_documents = _count(
            artefacts, COLLECTION_ARCHITECTURE
        ) + _count(artefacts, COLLECTION_ADR)
        research_documents = _count(artefacts, COLLECTION_RESEARCH)
        capability_documents = _count(artefacts, COLLECTION_FOUNDER_CAPABILITY)
        return KnowledgeIndexSummaryDTO(
            source_version=self._config.source_version,
            engineering_standards=engineering_standards,
            architecture_documents=architecture_documents,
            research_documents=research_documents,
            capability_documents=capability_documents,
            indexed_artefacts=len(artefacts),
            tests_pass=report.ok,
            validation_errors=report.error_count,
            missing_roots=self._missing_roots,
        )

    def list_validation_issues(self) -> tuple[KnowledgeValidationIssue, ...]:
        """Return validation issues from the last scan (missing roots, etc.)."""
        self._ensure_index()
        assert self._report is not None
        return self._report.issues

    def _ensure_index(self) -> tuple[KnowledgeArtefactDTO, ...]:
        if self._artefacts is None:
            self.refresh()
        assert self._artefacts is not None
        return self._artefacts


def _count(artefacts: tuple[KnowledgeArtefactDTO, ...], collection: str) -> int:
    return sum(1 for a in artefacts if a.collection == collection)
