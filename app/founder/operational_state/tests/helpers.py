"""Shared builders for Founder Operational State tests (FOS-005).

Pure helpers only — no filesystem scanning, no Flask app dependency.
"""

from __future__ import annotations

from datetime import UTC, datetime
from types import MappingProxyType

from app.founder.operational_state.builders import OperationalStateBuilder
from app.founder.operational_state.dto.capability import CapabilitySubsystemDTO
from app.founder.operational_state.dto.internal_alpha import (
    InternalAlphaSubsystemDTO,
)
from app.founder.operational_state.dto.knowledge import KnowledgeSubsystemDTO
from app.founder.operational_state.providers import (
    CapabilityProvider,
    InternalAlphaProvider,
    KnowledgeProvider,
    StaticCapabilitySource,
    StaticInternalAlphaSource,
    StaticKnowledgeSource,
)
from app.founder.operational_state.services import FounderOperationalStateService

FIXED_NOW = datetime(2026, 7, 14, 12, 0, 0, tzinfo=UTC)


def make_knowledge_dto(**overrides) -> KnowledgeSubsystemDTO:
    base = dict(
        source_version="knowledge-1.0",
        engineering_standards=5,
        architecture_documents=4,
        research_documents=3,
        capability_documents=2,
        indexed_artefacts=10,
        tests_pass=True,
        validation_errors=0,
    )
    base.update(overrides)
    return KnowledgeSubsystemDTO(**base)


def make_capability_dto(**overrides) -> CapabilitySubsystemDTO:
    base = dict(
        source_version="capability-1.0",
        total_count=2,
        completed_count=1,
        active_count=1,
        archive_inconsistencies=0,
        current_release="1.0.0",
        recent_capability_ids=("FOS-003", "FOS-004"),
    )
    base.update(overrides)
    return CapabilitySubsystemDTO(**base)


def make_alpha_dto(**overrides) -> InternalAlphaSubsystemDTO:
    base = dict(
        source_version="alpha-1.0",
        current_week="2026-W28",
        feedback_count=7,
        duplicate_count=2,
        category_counts=MappingProxyType({"Engineering": 3, "UX": 4}),
        recent_week_labels=("2026-W28", "2026-W27"),
    )
    base.update(overrides)
    return InternalAlphaSubsystemDTO(**base)


def make_builder(**kwargs) -> OperationalStateBuilder:
    return OperationalStateBuilder(clock=lambda: FIXED_NOW, **kwargs)


def make_service(
    *,
    knowledge: KnowledgeSubsystemDTO | None = None,
    capability: CapabilitySubsystemDTO | None = None,
    alpha: InternalAlphaSubsystemDTO | None = None,
) -> FounderOperationalStateService:
    return FounderOperationalStateService(
        knowledge=KnowledgeProvider(StaticKnowledgeSource(knowledge)),
        capability=CapabilityProvider(StaticCapabilitySource(capability)),
        internal_alpha=InternalAlphaProvider(StaticInternalAlphaSource(alpha)),
        clock=lambda: FIXED_NOW,
    )
