"""Knowledge Engine snapshot DTOs for Founder Dashboard (FOS-004)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class KnowledgeSnapshot:
    """Immutable counts and health signals from the Knowledge Engine."""

    engineering_standards: int
    architecture_documents: int
    research_documents: int
    capability_documents: int
    indexed_artefacts: int
    tests_pass: bool = True
    validation_errors: int = 0
    recent_artefact_titles: tuple[str, ...] = ()


@dataclass(frozen=True)
class KnowledgeSection:
    """Knowledge summary panel for the Founder Dashboard."""

    engineering_standards: int
    architecture_documents: int
    research_documents: int
    capability_documents: int
    indexed_artefacts: int
    engineering_health: int
    architecture_health: int
