"""Knowledge Provider — wraps Knowledge Engine public reads (FOS-005)."""

from __future__ import annotations

from app.founder.operational_state.dto.knowledge import KnowledgeSubsystemDTO

DEFAULT_KNOWLEDGE_SOURCE_VERSION = "unwired"


class StaticKnowledgeSource:
    """Injectable Knowledge Engine source for tests and defaults."""

    def __init__(self, dto: KnowledgeSubsystemDTO | None = None) -> None:
        self._dto = dto or KnowledgeSubsystemDTO(
            source_version=DEFAULT_KNOWLEDGE_SOURCE_VERSION,
            engineering_standards=0,
            architecture_documents=0,
            research_documents=0,
            capability_documents=0,
            indexed_artefacts=0,
        )

    def load(self) -> KnowledgeSubsystemDTO:
        return self._dto


class KnowledgeProvider:
    """Retrieve Knowledge Engine summary for operational-state aggregation.

    Does not analyse documents. Does not index. Aggregation input only.
    """

    def __init__(self, source: StaticKnowledgeSource | None = None) -> None:
        self._source = source or StaticKnowledgeSource()

    def get(self) -> KnowledgeSubsystemDTO:
        """Return the Knowledge Engine DTO from the wrapped source."""
        return self._source.load()
