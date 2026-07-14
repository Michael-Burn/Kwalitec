"""Knowledge Engine (FOS-001).

Repository-backed knowledge discovery. Public API:
``KnowledgeQueryService`` — the only surface other Founder components may use.

No Flask, no persistence, no AI.
"""

from __future__ import annotations

from app.founder.knowledge_engine.config import (
    KnowledgeEngineConfig,
    default_config,
    discover_repo_root,
)
from app.founder.knowledge_engine.dto import (
    KnowledgeArtefactDTO,
    KnowledgeIndexSummaryDTO,
    KnowledgeValidationIssue,
    KnowledgeValidationReport,
)
from app.founder.knowledge_engine.services import KnowledgeQueryService

__all__ = [
    "KnowledgeArtefactDTO",
    "KnowledgeEngineConfig",
    "KnowledgeIndexSummaryDTO",
    "KnowledgeQueryService",
    "KnowledgeValidationIssue",
    "KnowledgeValidationReport",
    "default_config",
    "discover_repo_root",
]
