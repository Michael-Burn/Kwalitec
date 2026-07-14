"""Operational State live-provider integration tests (FSI-001).

Uses temporary fixtures — does not scan the real project repository.
"""

from __future__ import annotations

from pathlib import Path

from app.founder.capability_archive.tests.helpers import build_archive_fixture
from app.founder.knowledge_engine.tests.helpers import build_knowledge_fixture
from app.founder.operational_state.providers import (
    CapabilityArchiveProvider,
    KnowledgeQueryProvider,
    StaticInternalAlphaSource,
)
from app.founder.operational_state.providers.internal_alpha import (
    InternalAlphaProvider,
)
from app.founder.operational_state.services import FounderOperationalStateService
from app.founder.operational_state.tests.helpers import FIXED_NOW, make_alpha_dto


def _combined_fixture(tmp_path: Path) -> Path:
    root = tmp_path / "combined"
    build_knowledge_fixture(root)
    # Overlay archive entries onto the same fixture root.
    build_archive_fixture(root)
    return root


class TestOperationalStateLiveProviders:
    def test_live_providers_aggregate_fixture_repo(self, tmp_path: Path) -> None:
        repo = _combined_fixture(tmp_path)
        service = FounderOperationalStateService(
            knowledge=KnowledgeQueryProvider(repo_root=repo),
            capability=CapabilityArchiveProvider(repo_root=repo),
            internal_alpha=InternalAlphaProvider(
                StaticInternalAlphaSource(make_alpha_dto())
            ),
            clock=lambda: FIXED_NOW,
        )
        state = service.get_state()
        assert state.generated_at == FIXED_NOW
        assert state.source_versions.knowledge == "knowledge-engine-1.0"
        assert state.source_versions.capability_archive == "capability-archive-1.0"
        assert state.knowledge.indexed_artefacts >= 5
        assert state.knowledge.engineering_standards == 1
        assert state.capability.total_count == 2
        assert state.capability.completed_count == 1
        assert state.capability.active_count == 1
        assert state.capability.archive_inconsistencies == 0
        assert state.release.completed_capabilities == 1

    def test_provider_connectivity(self, tmp_path: Path) -> None:
        repo = _combined_fixture(tmp_path)
        knowledge = KnowledgeQueryProvider(repo_root=repo)
        capability = CapabilityArchiveProvider(repo_root=repo)
        k_dto = knowledge.get()
        c_dto = capability.get()
        assert k_dto.indexed_artefacts > 0
        assert c_dto.total_count > 0
        assert k_dto.source_version == "knowledge-engine-1.0"
        assert c_dto.source_version == "capability-archive-1.0"
