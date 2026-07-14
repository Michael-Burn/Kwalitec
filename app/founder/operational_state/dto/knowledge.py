"""Knowledge Engine subsystem DTO for operational-state aggregation."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class KnowledgeSubsystemDTO:
    """Summary read-model from the Knowledge Engine (FOS-001).

    Counts and signals only — never raw document bodies.
    """

    source_version: str
    engineering_standards: int
    architecture_documents: int
    research_documents: int
    capability_documents: int
    indexed_artefacts: int
    tests_pass: bool = True
    validation_errors: int = 0
