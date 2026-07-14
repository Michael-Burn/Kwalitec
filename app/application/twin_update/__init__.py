"""Twin Update write path — Coordinator, Composer, and shared contracts.

Owns Sequencing Strategies → Composer → Repository for Evidence-driven Twin
succession. Never interprets Evidence or reasons educationally.
"""

from __future__ import annotations

from app.application.twin_update.composer import (
    DomainOutputCollection,
    TwinComposer,
    TwinCompositionError,
)
from app.application.twin_update.coordinator import TwinUpdateCoordinator
from app.application.twin_update.evidence import (
    CONTRACT_VERSION_1_0,
    EVIDENCE_PACKAGE_VERSION_1_0,
    EducationalEvidencePackage,
    ObservedEvent,
)
from app.application.twin_update.knowledge_strategy import KnowledgeUpdateStrategy
from app.application.twin_update.outputs import (
    KNOWLEDGE_OWNED_DOMAIN,
    KNOWLEDGE_STRATEGY_IDENTITY,
    DomainStrategyOutput,
    KnowledgeStrategyOutput,
)
from app.application.twin_update.protocols import (
    TwinComposerProtocol,
    TwinSuccessorRepositoryProtocol,
    TwinUpdateCoordinatorProtocol,
    TwinUpdateStrategyProtocol,
)
from app.application.twin_update.reasoning import ReasoningTrace
from app.application.twin_update.result import (
    TwinUpdateFailure,
    TwinUpdateFailureReason,
    TwinUpdateResult,
    TwinUpdateSuccess,
)

__all__ = [
    "CONTRACT_VERSION_1_0",
    "EVIDENCE_PACKAGE_VERSION_1_0",
    "DomainOutputCollection",
    "DomainStrategyOutput",
    "EducationalEvidencePackage",
    "KNOWLEDGE_OWNED_DOMAIN",
    "KNOWLEDGE_STRATEGY_IDENTITY",
    "KnowledgeStrategyOutput",
    "KnowledgeUpdateStrategy",
    "ObservedEvent",
    "ReasoningTrace",
    "TwinComposer",
    "TwinComposerProtocol",
    "TwinCompositionError",
    "TwinSuccessorRepositoryProtocol",
    "TwinUpdateCoordinator",
    "TwinUpdateCoordinatorProtocol",
    "TwinUpdateFailure",
    "TwinUpdateFailureReason",
    "TwinUpdateResult",
    "TwinUpdateStrategyProtocol",
    "TwinUpdateSuccess",
]
