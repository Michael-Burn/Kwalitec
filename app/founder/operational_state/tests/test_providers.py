"""Unit tests for Founder Operational State providers (FOS-005 / FSI-001)."""

from __future__ import annotations

from app.founder.operational_state.providers import (
    CapabilityProvider,
    InternalAlphaProvider,
    KnowledgeProvider,
    StaticCapabilitySource,
    StaticInternalAlphaSource,
    StaticKnowledgeSource,
)
from app.founder.operational_state.tests.helpers import (
    make_alpha_dto,
    make_capability_dto,
    make_knowledge_dto,
)


class TestKnowledgeProvider:
    def test_returns_dto_from_source(self) -> None:
        dto = make_knowledge_dto(engineering_standards=9)
        provider = KnowledgeProvider(StaticKnowledgeSource(dto))
        assert provider.get().engineering_standards == 9
        assert provider.get().source_version == "knowledge-1.0"

    def test_static_default_source_is_empty(self) -> None:
        """Static KnowledgeProvider remains available for isolated unit tests."""
        dto = KnowledgeProvider().get()
        assert dto.indexed_artefacts == 0
        assert dto.source_version == "unwired"


class TestCapabilityProvider:
    def test_returns_dto_from_source(self) -> None:
        dto = make_capability_dto()
        provider = CapabilityProvider(StaticCapabilitySource(dto))
        result = provider.get()
        assert result.total_count == 2
        assert result.recent_capability_ids[0] == "FOS-003"

    def test_static_default_source_is_empty(self) -> None:
        """Static CapabilityProvider remains available for isolated unit tests."""
        dto = CapabilityProvider().get()
        assert dto.total_count == 0
        assert dto.current_release == ""


class TestInternalAlphaProvider:
    def test_returns_dto_from_source(self) -> None:
        provider = InternalAlphaProvider(StaticInternalAlphaSource(make_alpha_dto()))
        result = provider.get()
        assert result.current_week == "2026-W28"
        assert result.feedback_count == 7
        assert result.category_counts["Engineering"] == 3

    def test_default_source_is_empty(self) -> None:
        dto = InternalAlphaProvider().get()
        assert dto.current_week == ""
        assert dto.feedback_count == 0
